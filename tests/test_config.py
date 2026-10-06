"""配置层测试。

重点是 `.env` 的查找顺序：`-C/--workspace` 必须同时隔离配置与文件访问，
否则多项目、多评测实例之间会静默串用模型与凭据。
"""
from __future__ import annotations

from pathlib import Path

from code_agent.config import Settings, parse_env_file

ENV_BODY = """\
# 注释行
LLM_BASE_URL=https://example.invalid/v1
LLM_MODEL=test-model
LLM_API_KEY="sk-quoted"
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024
"""


def test_parse_env_file_handles_comments_quotes_and_blanks(tmp_path: Path):
    target = tmp_path / ".env"
    target.write_text(ENV_BODY + "\n\nBADLINE\n", encoding="utf-8")
    parsed = parse_env_file(target)
    assert parsed["LLM_MODEL"] == "test-model"
    assert parsed["LLM_API_KEY"] == "sk-quoted"  # 引号被剥掉
    assert parsed["LLM_TEMPERATURE"] == "0.7"
    assert "BADLINE" not in parsed


def test_parse_env_file_returns_empty_for_missing_file(tmp_path: Path):
    assert parse_env_file(tmp_path / "nope.env") == {}


def test_output_limit_and_total_budget_are_separate_fields():
    """两个语义必须分开，否则"不限预算(0)"会被当成"输出上限 0"从而请求 400。"""
    settings = Settings()
    assert settings.llm_max_tokens == 2048
    assert settings.max_total_tokens == 0


def test_output_limit_is_clamped_to_at_least_one():
    assert Settings(llm_max_tokens=0).llm_max_tokens == 1
    assert Settings(llm_max_tokens=-5).llm_max_tokens == 1


def test_total_budget_zero_means_unlimited():
    assert Settings(max_total_tokens=0).max_total_tokens == 0
    assert Settings(max_total_tokens=-3).max_total_tokens == 0


def test_explicit_env_file_wins(tmp_path: Path):
    custom = tmp_path / "custom.env"
    custom.write_text(ENV_BODY, encoding="utf-8")
    settings = Settings.from_env(workspace=tmp_path, env_file=custom)
    assert settings.model == "test-model"
    assert settings.llm_max_tokens == 1024
    assert settings.temperature == 0.7


def test_workspace_env_is_preferred_over_cwd(tmp_path: Path, monkeypatch):
    """工作区里的 .env 优先于当前目录的 .env。"""
    workspace = tmp_path / "project"
    workspace.mkdir()
    (workspace / ".env").write_text("LLM_MODEL=from-workspace\n", encoding="utf-8")

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / ".env").write_text("LLM_MODEL=from-cwd\n", encoding="utf-8")
    monkeypatch.chdir(elsewhere)

    settings = Settings.from_env(workspace=workspace)
    assert settings.model == "from-workspace"


def test_workspace_without_env_falls_back_to_cwd(tmp_path: Path, monkeypatch):
    workspace = tmp_path / "bare"
    workspace.mkdir()

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / ".env").write_text("LLM_MODEL=from-cwd\n", encoding="utf-8")
    monkeypatch.chdir(elsewhere)

    assert Settings.from_env(workspace=workspace).model == "from-cwd"


def test_workspace_with_no_env_anywhere_is_offline(tmp_path: Path, monkeypatch):
    """`-C <空目录>` 必须得到"未配置"状态，而不是读到别处的凭据。

    这是评测隔离的基础：每个实例的工作区是临时目录，不应该继承本仓库的 .env。
    """
    workspace = tmp_path / "bare"
    workspace.mkdir()
    empty_cwd = tmp_path / "empty"
    empty_cwd.mkdir()
    monkeypatch.chdir(empty_cwd)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.delenv("LLM_BASE_URL", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    settings = Settings.from_env(workspace=workspace)
    assert settings.model == ""
    assert settings.is_llm_configured is False


def test_masked_api_key_never_reveals_the_secret():
    settings = Settings(api_key="sk-abcdefghijklmnop")
    masked = settings.masked_api_key
    assert "abcdefghijklmnop" not in masked
    assert masked.startswith("sk-a") and masked.endswith("mnop")
    assert Settings(api_key="").masked_api_key == "(未设置)"
