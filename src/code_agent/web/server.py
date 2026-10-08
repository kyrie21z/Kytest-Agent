"""Loopback-only stdlib HTTP adapter; Agent policies stay in the existing CLI factory."""
import argparse
import hashlib
from dataclasses import replace
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import tempfile
import threading
import time
from types import SimpleNamespace
from urllib.parse import parse_qs, urlsplit
import uuid

from ..cli import build_agent
from ..config import Settings
from ..errors import ToolError
from ..session import redact_text
from ..tools.base import resolve_workspace_path
from ..tools.shell_tools import RunCommandTool
from .demo import DemoLLM, SOURCE, TASK
from .examples import ROTATION_SOURCE, ROTATION_TASK
from .quality import evaluate_quality
from ..pytest_result import parse_pytest_result

FILES = {"solution.py", "test_solution.py", "testgen_report.json", "fault_feedback.json", "quality_report.json"}


class RequestError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


class Run:
    def __init__(self, settings, source, task, mode, variant):
        self.id = uuid.uuid4().hex
        self.directory = tempfile.TemporaryDirectory(prefix="code-agent-ui-")
        self.workspace = Path(self.directory.name)
        self.settings = replace(settings, workspace=self.workspace, session_dir=None)
        self.source, self.task, self.mode, self.variant = source, task, mode, variant
        (self.workspace/"solution.py").write_bytes(source.encode("utf-8"))
        self.lock = threading.Lock()
        self.cancelled = threading.Event()
        self.events = []
        self.done = False
        self.agent = None
        self.result = None
        self.started = time.monotonic()
        self.finished = None
        self.thread = None
        self.comparison_id = None
        self.report = None
        self.phase = "queued"
        self.generation_finished = None
        self.started_wall = None
        self.finished_wall = None

    def clean(self, value):
        return json.loads(redact_text(json.dumps(value, ensure_ascii=False), [self.settings.api_key]))

    def emit(self, value):
        with self.lock:
            self.events.append(self.clean({**value,"elapsed_sec":round(time.monotonic()-self.started,3)}))

    def cancel(self):
        self.cancelled.set()
        if self.agent is not None:
            self.agent.abort()

    def file(self, name):
        if name not in FILES:
            raise RequestError("文件不在可下载清单中", 404)
        try:
            path = resolve_workspace_path(self.workspace, name, must_exist=True)
            if not path.is_file() or path.stat().st_size > 200_000:
                raise ValueError("文件不可用或过大")
            return redact_text(path.read_text(encoding="utf-8"), [self.settings.api_key])
        except (OSError, ValueError, UnicodeError, ToolError) as exc:
            raise RequestError("文件尚未生成或不可读取", 404) from exc

    def snapshot(self, after=0):
        with self.lock:
            return {"id":self.id, "events":self.events[after:], "next":len(self.events),
                    "done":self.done, "result":self.result, "mode":self.mode,
                    "variant":self.variant, "source":self.clean(self.source),
                    "task":self.clean(self.task), "comparison_id":self.comparison_id,
                    "phase":self.phase, "report":self.report,
                    "generation_sec":None if self.generation_finished is None else round(self.generation_finished-self.started,3),
                    "timing":{"started_unix":self.started_wall,"finished_unix":self.finished_wall},
                    "source_sha256":hashlib.sha256(self.source.encode()).hexdigest(),
                    "budget":{"turns":self.settings.max_steps,"tokens":self.settings.max_total_tokens,
                              "request_seconds":self.settings.request_timeout,
                              "command_seconds":self.settings.max_exec_timeout},
                    "elapsed_sec":0 if self.phase=="queued" else round((self.finished or time.monotonic())-self.started,1)}

    def refresh_report(self):
        if self.variant != "A4":
            return
        try:
            report = json.loads(self.file("testgen_report.json"))
        except (RequestError, ValueError):
            return
        with self.lock:
            self.report = report

    def handle_event(self, event):
        data = event.to_dict()
        self.emit(data)
        if data["type"]=="tool_call_end" and data["name"]=="submit_tests":
            self.refresh_report()

    def source_intact(self):
        source = self.workspace/"solution.py"
        try:
            return not source.is_symlink() and source.read_bytes()==self.source.encode("utf-8")
        except OSError:
            return False

    def restore_source(self):
        source = self.workspace/"solution.py"
        if source.is_symlink():
            source.unlink()
        source.write_bytes(self.source.encode("utf-8"))

    def execute(self):
        with self.lock:
            self.started = time.monotonic()
            self.started_wall = time.time()
            self.phase = "running"
        try:
            args = SimpleNamespace(mock=False, tools=None, test_generation=self.variant=="A4",
                                   fault_feedback=False)
            agent, _, _ = build_agent(args, self.settings, self.handle_event,
                                      session_enabled=False)
            self.agent = agent
            if self.mode == "demo":
                agent.llm = DemoLLM(variant=self.variant)
            policy_position = 1  # The first user message is the submitted task.
            def before_turn(current, state):
                nonlocal policy_position
                for message in state.messages[policy_position:]:
                    text = message.get("content", "")
                    if self.variant=="A4" and message.get("role")=="user" and isinstance(text,str) and text.startswith("[System]"):
                        self.emit({"type":"policy_feedback","message":text})
                policy_position = len(state.messages)
                if self.cancelled.is_set() or time.monotonic()-self.started > 300:
                    current.abort()
            agent.before_turn = before_turn
            agent.state.add_user(self.task)
            result = agent.run().to_dict()
            with self.lock:
                self.generation_finished = time.monotonic()
                self.phase = "validating"
            self.refresh_report()
            # Final verification is visible and separate from the model's own tool calls.
            unchanged = self.source_intact()
            validation = {"passed":False,"content":"运行已停止，未进行最终复验。","source_unchanged":unchanged}
            if not unchanged:
                self.restore_source()
                validation["content"] = "目标源码被改写，已恢复原件；本次测试不作为有效产出。"
            elif result["status"] not in {"aborted", "llm_error"} and not self.cancelled.is_set():
                self.emit({"type":"validation_start"})
                try:
                    self.file("test_solution.py")  # Rejects symlinks outside the workspace.
                except RequestError:
                    validation["content"] = "未生成可读取的 test_solution.py；最终复验未通过。"
                else:
                    checked = RunCommandTool(self.settings).run(
                        command="python -m pytest test_solution.py -q", timeout=15)
                    observed = parse_pytest_result(checked.process)
                    validation.update(passed=observed.all_pass, content=checked.content,counts=observed.counts)
                    if not self.source_intact():
                        self.restore_source()
                        validation.update(passed=False,source_unchanged=False,
                            content="最终测试改写了目标源码，已恢复原件；本次产出无效。")
            if self.cancelled.is_set():
                result["status"]="aborted"
                validation["passed"]=False
            self.emit({"type":"validation_end", **validation})
            with self.lock:
                self.phase = "evaluating"
            self.emit({"type":"evaluation_start"})
            quality = evaluate_quality(self.settings,self.source,self.file,validation,self.cancelled,self.emit)
            if not self.source_intact():
                self.restore_source()
                validation.update(passed=False,source_unchanged=False,
                                  content="质量评测后源码检查未通过，已恢复；本次产出无效。")
            if self.cancelled.is_set():
                result["status"]="aborted"
            result["validation"] = validation
            result["quality"] = quality
            quality_path = self.workspace/"quality_report.json"
            if quality_path.is_symlink():
                quality_path.unlink()
            quality_path.write_text(json.dumps(self.clean(quality),ensure_ascii=False,indent=2))
            self.emit({"type":"evaluation_end", "quality":quality})
            with self.lock:
                self.result = self.clean(result)
        except Exception as exc:
            self.emit({"type":"error", "where":"web", "message":str(exc)})
            with self.lock:
                self.result = self.clean({"status":"error", "error":str(exc),
                                          "validation":{"passed":False}})
        finally:
            with self.lock:
                self.finished = time.monotonic()
                self.finished_wall = time.time()
                self.done = True
                self.phase = "done"


class Application:
    def __init__(self, settings):
        self.settings = settings
        self.lock = threading.Lock()
        self.runs = {}
        self.comparisons = {}

    def validate(self, data):
        source, task = data.get("source"), data.get("task")
        mode, variant = data.get("mode"), data.get("variant", "A0")
        if not isinstance(source,str) or not source.strip() or len(source)>32_000:
            raise RequestError("请提供不超过32000字符的Python源码")
        if not isinstance(task,str) or not task.strip() or len(task)>4_000:
            raise RequestError("请提供不超过4000字符的任务")
        if mode not in {"demo","real"} or variant not in {"A0","A4"}:
            raise RequestError("请选择有效的模型模式和Agent策略")
        if mode=="demo" and (source.strip()!=SOURCE.strip() or task.strip()!=TASK):
            raise RequestError("离线模式仅演示固定示例和任务；编辑源码或任务请选择真实模型")
        if mode=="real" and not self.settings.is_llm_configured:
            raise RequestError("真实模型未配置。请在项目.env填写LLM_API_KEY、LLM_BASE_URL、LLM_MODEL并重启UI")
        return source, task, mode, variant

    def admit(self, count):
        if any(not run.done for run in self.runs.values()):
            raise RequestError("已有任务在运行，请等待完成或先停止", 409)
        while len(self.runs)+count>8:
            oldest = next(iter(self.runs))
            self.runs.pop(oldest).directory.cleanup()
        self.comparisons = {key:ids for key,ids in self.comparisons.items()
                            if all(run_id in self.runs for run_id in ids)}

    def start(self, data):
        source,task,mode,variant = self.validate(data)
        with self.lock:
            self.admit(1)
            run = Run(self.settings, source, task, mode, variant)
            self.runs[run.id] = run
            run.thread=threading.Thread(target=run.execute, daemon=True)
            run.thread.start()
            return run

    def compare(self, data):
        source,task,mode,_ = self.validate(data)
        with self.lock:
            self.admit(2)
            comparison_id = uuid.uuid4().hex
            pair = [Run(self.settings,source,task,mode,variant) for variant in ("A0","A4")]
            for run in pair:
                run.comparison_id = comparison_id
                self.runs[run.id] = run
            self.comparisons[comparison_id] = [run.id for run in pair]
            gate = threading.Event()
            def execute_one(run):
                gate.wait()
                run.execute()
            for run in pair:
                run.thread = threading.Thread(target=execute_one,args=(run,),daemon=True)
                run.thread.start()
            gate.set()
            return comparison_id

    def comparison(self, comparison_id, after_a0=0, after_a4=0):
        with self.lock:
            ids = self.comparisons.get(comparison_id)
            if ids is None:
                raise RequestError("对比记录不存在或已清理",404)
            snapshots = [self.runs[run_id].snapshot(after) for run_id,after in zip(ids,(after_a0,after_a4))]
        return {"id":comparison_id,"execution":"parallel","runs":snapshots,"done":all(run["done"] for run in snapshots)}

    def stop_comparison(self, comparison_id):
        snapshot = self.comparison(comparison_id)
        for run in snapshot["runs"]:
            self.get(run["id"]).cancel()

    def get(self, run_id):
        with self.lock:
            run = self.runs.get(run_id)
        if run is None:
            raise RequestError("运行记录不存在或已清理", 404)
        return run

    def close(self):
        for run in self.runs.values():
            run.cancel()
        for run in self.runs.values():
            if run.thread is not None:
                run.thread.join()
            run.directory.cleanup()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, status, data, content_type="application/json; charset=utf-8", download=None):
        body = data if isinstance(data,bytes) else json.dumps(data,ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'")
        if download:
            self.send_header("Content-Disposition", f'attachment; filename="{download}"')
        self.end_headers()
        self.wfile.write(body)

    def dispatch(self, method):
        try:
            host = self.headers.get("Host", "")
            port = self.server.server_address[1]
            if host not in {f"127.0.0.1:{port}",f"localhost:{port}"}:
                raise RequestError("仅接受本地访问", 403)
            origin = self.headers.get("Origin")
            if origin is not None and origin!=f"http://{host}":
                raise RequestError("拒绝跨站请求", 403)
            url = urlsplit(self.path)
            app = self.server.app
            if method=="GET" and url.path in {"/","/index.html"}:
                return self.send(200,Path(__file__).with_name("index.html").read_bytes(),"text/html; charset=utf-8")
            if method=="GET" and url.path=="/api/config":
                with app.lock:
                    latest=next(reversed(app.runs),None)
                    comparison_id=app.runs[latest].comparison_id if latest else None
                return self.send(200,{"source":SOURCE,"task":TASK,"real_configured":app.settings.is_llm_configured,
                    "examples":[{"id":"rotation","name":"区间旋转 · MBPP/304（差异案例）","source":ROTATION_SOURCE,"task":ROTATION_TASK,
                                 "note":"从已有真实实验筛选：A0三次有两次参考测试失败，A4三次全部通过。新运行结果可能不同。"},
                                {"id":"classify","name":"区间分类（机制入门）","source":SOURCE,"task":TASK,
                                 "note":"短小示例用于观察工具与候选验证；两组通常都能覆盖完整行为。"}],
                    "model":redact_text(app.settings.model,[app.settings.api_key]),"execution_mode":app.settings.execution_mode,
                    "latest_run":latest,"latest_comparison":comparison_id})
            if method=="GET" and url.path=="/api/examples/rotation-record":
                path=Path(__file__).resolve().parents[3]/"submission/evidence/ui-rotation.json"
                try:
                    receipt=json.loads(path.read_text())
                    comparison=receipt["comparison"]
                except (OSError,ValueError,KeyError) as exc:
                    raise RequestError("已保存案例不可用",404) from exc
                origin={"kind":"saved_real","label":"MBPP/304 · 已保存真实并行运行",
                        "model":receipt["model"],"scope":receipt["scope"],
                        "note":"从既有实验筛选，再以当前界面重新运行。此视图读取保存记录，不调用模型；新运行可能不同。"}
                comparison["origin"]=origin
                for run in comparison["runs"]:
                    run["origin"]=origin
                return self.send(200,json.loads(redact_text(json.dumps(comparison,ensure_ascii=False),[app.settings.api_key])))
            parts = url.path.strip("/").split("/")
            if method=="GET" and len(parts)==3 and parts[:2]==["api","comparisons"]:
                query = parse_qs(url.query)
                after_a0,after_a4 = (int(query.get(key,["0"])[0]) for key in ("after_a0","after_a4"))
                if min(after_a0,after_a4)<0:
                    raise RequestError("无效的事件位置")
                return self.send(200,app.comparison(parts[2],after_a0,after_a4))
            if method=="GET" and len(parts)==3 and parts[:2]==["api","runs"]:
                after = int(parse_qs(url.query).get("after",["0"])[0])
                if after<0:
                    raise RequestError("无效的事件位置")
                return self.send(200, app.get(parts[2]).snapshot(after))
            if method=="GET" and len(parts)==5 and parts[:2]==["api","runs"] and parts[3]=="files":
                name=parts[4]
                return self.send(200,app.get(parts[2]).file(name).encode(),"text/plain; charset=utf-8",download=name)
            if method=="POST":
                if self.headers.get_content_type()!="application/json":
                    raise RequestError("请求必须为JSON",415)
                size=int(self.headers.get("Content-Length","0"))
                if size<=0 or size>100_000:
                    raise RequestError("请求为空或超过100KB",413)
                data=json.loads(self.rfile.read(size))
                if not isinstance(data,dict):
                    raise RequestError("请求必须为JSON对象")
                if url.path=="/api/runs":
                    return self.send(202,{"id":app.start(data).id})
                if url.path=="/api/comparisons":
                    return self.send(202,{"id":app.compare(data)})
                if len(parts)==4 and parts[:2]==["api","comparisons"] and parts[3]=="stop":
                    app.stop_comparison(parts[2])
                    return self.send(202,{"stopping":True})
                if len(parts)==4 and parts[:2]==["api","runs"] and parts[3]=="stop":
                    app.get(parts[2]).cancel()
                    return self.send(202,{"stopping":True})
            raise RequestError("页面或接口不存在",404)
        except RequestError as exc:
            self.send(exc.status,{"error":str(exc)})
        except (ValueError,UnicodeError) as exc:
            self.send(400,{"error":"请求格式错误"})
        except (BrokenPipeError,ConnectionResetError):
            pass

    def do_GET(self):
        self.dispatch("GET")

    def do_POST(self):
        self.dispatch("POST")


def create_server(settings, port=8765):
    server = ThreadingHTTPServer(("127.0.0.1",port),Handler)
    server.app = Application(settings)
    return server


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port",type=int,default=8765)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[3]
    settings=Settings.from_env(env_file=root/".env",workspace=root)
    settings=replace(settings,max_steps=12,max_total_tokens=30000,llm_max_tokens=4096,
                     max_retries=1,exec_timeout=15,max_exec_timeout=15)
    server=create_server(settings,args.port)
    print(f"Code Agent UI: http://127.0.0.1:{server.server_address[1]}  (Ctrl-C to stop)",flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.app.close()
        server.server_close()
