"""Post-run measurements, isolated from generation and never fed back to either agent."""
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import re
import tempfile
import time

from ..tools.shell_tools import RunCommandTool
from .demo import SOURCE
from .examples import ROTATION_SOURCE, ROTATION_FAULTS

FAULTS = (
    ('lower_inclusive', '下边界错误排除', SOURCE.replace('value < low', 'value <= low'), (2, 2, 8), 0),
    ('upper_inclusive', '上边界错误排除', SOURCE.replace('value > high', 'value >= high'), (8, 2, 8), 0),
    ('below_zero', '下方错误返回0', SOURCE.replace('return -1', 'return 0'), (1, 2, 8), -1),
    ('above_zero', '上方错误返回0', SOURCE.replace('return 1', 'return 0'), (9, 2, 8), 1),
    ('inside_one', '区间内部错误返回1', SOURCE.rsplit('return 0', 1)[0]+'return 1\n', (5, 2, 8), 0),
)


def pytest_counts(content):
    counts = {'passed':0, 'failed':0, 'errors':0, 'skipped':0}
    summaries = [line for line in content.splitlines()
                 if re.search(r'\b\d+ (?:passed|failed|errors?|skipped)\b.*\bin \d+(?:\.\d+)?s', line)]
    if summaries:
        for number, name in re.findall(r'(\d+) (passed|failed|errors?|skipped)\b', summaries[-1]):
            counts['errors' if name in ('error', 'errors') else name] = int(number)
    return counts


def evaluate_quality(settings, source, read_file, validation, cancelled, emit):
    started = time.monotonic()
    if source.strip()==SOURCE.strip():
        profile,entry_point,pool='classify-five-v1','classify',FAULTS
    elif source.strip()==ROTATION_SOURCE.strip():
        profile,entry_point,pool='mbpp-304-ror-lcr-bcr-v2','find_Element',ROTATION_FAULTS
    else:
        profile,entry_point,pool=None,None,()
    total=len(pool) if pool else None
    report = {'schema':'ui-quality-v1', 'status':'blocked', 'coverage':{'status':'not_measured'},
              'fault_detection':{'status':'not_measured', 'profile':profile, 'total':total,
                                 'confirmed_killed':0, 'survived':0, 'uncertain':total, 'percent':None, 'results':[]},
              'limits':{'command_seconds':15, 'fault_seconds':5},
              'scope':'This run only. Coverage is execution reach; fixed sample faults measure detection, not general superiority.'}
    def finish(status):
        report['status'] = status
        report['evaluation_sec'] = round(time.monotonic()-started,3)
        return report
    if not validation.get('passed') or validation.get('source_unchanged') is not True:
        report['reason'] = '最终测试须实际通过且目标源码保持原样，才进行质量评测。'
        return finish('blocked')
    if cancelled.is_set():
        return finish('cancelled')
    try:
        tests = read_file('test_solution.py')
        report['test_sha256'] = hashlib.sha256(tests.encode()).hexdigest()
        with tempfile.TemporaryDirectory(prefix='code-agent-ui-quality-') as name:
            workspace = Path(name)
            source_path,tests_path = workspace/'solution.py',workspace/'test_solution.py'
            source_path.write_bytes(source.encode());tests_path.write_bytes(tests.encode())
            tool = RunCommandTool(replace(settings,workspace=workspace))
            def intact(expected_source):
                return (not source_path.is_symlink() and not tests_path.is_symlink()
                        and source_path.read_bytes()==expected_source.encode()
                        and tests_path.read_bytes()==tests.encode())
            emit({'type':'evaluation_progress','stage':'coverage','message':'独立副本：执行语句与分支覆盖率测量。'})
            checked = tool.run(command='python -m coverage run --branch --source=solution -m pytest test_solution.py -q',timeout=15)
            counts = pytest_counts(checked.content)
            if not intact(source):
                report['reason'] = '评测期间输入文件被改写，质量结果无效。'
                return finish('invalid')
            reference_valid = checked.ok and counts['passed']>0 and not counts['failed'] and not counts['errors']
            if cancelled.is_set():
                return finish('cancelled')
            if reference_valid:
                exported = tool.run(command='python -m coverage json -o quality_coverage.json',timeout=15)
                path = workspace/'quality_coverage.json'
                if exported.ok and path.is_file() and not path.is_symlink() and path.stat().st_size<=200_000:
                    payload = json.loads(path.read_text())
                    target = next(value for key,value in payload['files'].items() if Path(key).name=='solution.py')
                    summary = target['summary']
                    lines,covered = summary['num_statements'],summary['covered_lines']
                    branches,covered_branches = summary.get('num_branches',0),summary.get('covered_branches',0)
                    report['coverage'] = {'status':'measured','statements':lines,'covered_statements':covered,
                        'line_percent':round(100*covered/lines,1) if lines else None,
                        'branches':branches,'covered_branches':covered_branches,
                        'branch_percent':round(100*covered_branches/branches,1) if branches else None,
                        'missing_lines':target.get('missing_lines',[]),'missing_branches':target.get('missing_branches',[])}
            if report['coverage']['status']!='measured':
                report['coverage'] = {'status':'unavailable','diagnostic':checked.content,
                                      'reason':'覆盖率依赖、执行或报告不可用；未将缺失值当成0。'}
            faults = report['fault_detection']
            if not pool:
                faults.update(status='not_applicable',total=None,uncertain=None,
                              reason='仅内置区间分类与旋转数组样例配置固定故障集；当前源码未配置。')
                return finish('measured' if reference_valid else 'unavailable')
            if not reference_valid:
                faults['reason']='覆盖率运行中的参考复验未通过，故障检出未计分。'
                return finish('unavailable')
            faults.update(status='measuring', results=[{'id':key,'label':label,'status':'NOT_RUN'} for key,label,*_ in pool])
            for index,(key,label,mutant,witness,expected) in enumerate(pool):
                if cancelled.is_set():
                    faults['status']='cancelled'
                    return finish('cancelled')
                # These modules are our fixed, constant fixture, never user/model code.
                namespace={};exec(compile(mutant,'<fixed-ui-fault>','exec'),namespace)
                observed=namespace[entry_point](*witness)
                assert observed!=expected, 'Fixed fault witness must expose a real semantic difference'
                source_path.write_bytes(mutant.encode())
                emit({'type':'evaluation_progress','stage':'fault','index':index+1,'total':total,'message':label})
                outcome=tool.run(command='python -m pytest test_solution.py -q',timeout=5)
                counts=pytest_counts(outcome.content)
                unchanged=intact(mutant)
                assertion_exit = bool(re.match(r'^\$[^\n]*\n\[退出码 1｜',outcome.content))
                status=('SURVIVED' if outcome.ok and counts['passed']>0 and unchanged else
                        'KILLED' if assertion_exit and counts['failed']>0 and not counts['errors'] and unchanged else 'UNCERTAIN')
                faults['results'][index]={'id':key,'label':label,'status':status,'witness':list(witness),
                    'expected':expected,'faulty_result':observed,'source_sha256':hashlib.sha256(mutant.encode()).hexdigest(),
                    'diagnostic':outcome.content}
                faults['confirmed_killed']=sum(item['status']=='KILLED' for item in faults['results'])
                faults['survived']=sum(item['status']=='SURVIVED' for item in faults['results'])
                faults['uncertain']=total-faults['confirmed_killed']-faults['survived']
                source_path.write_bytes(source.encode());tests_path.write_bytes(tests.encode())
            faults['status']='measured' if not faults['uncertain'] else 'partial'
            faults['percent']=round(100*faults['confirmed_killed']/total,1) if not faults['uncertain'] else None
            faults['confirmed_lower_percent']=round(100*faults['confirmed_killed']/total,1)
            return finish('measured')
    except Exception as exc:
        report['reason'] = '质量评测未完成：'+str(exc)
        return finish('unavailable')
