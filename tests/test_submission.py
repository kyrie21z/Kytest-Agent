"""Submission layout and copy integrity, without model calls or research data."""
import hashlib
import json
from pathlib import Path
import zipfile

import pytest

from scripts import build_submission as builder


@pytest.fixture
def submission_source(tmp_path, monkeypatch):
    source = tmp_path/"source"
    (source/"submission").mkdir(parents=True)
    (source/"docs").mkdir()
    contents = {
        "README.md": b"# Project\nRead the design.\n",
        "Design.md": b"# Design\nArchitecture and validation.\n",
        "main.py": b"print('agent')\n",
        "docs/demo.mp4": b"video-fixture\x00\xff",
    }
    for name, data in contents.items():
        (source/name).write_bytes(data)
    (source/".env").write_text("LLM_API_KEY=not-for-submission\n")
    spec = {"schema":"fixture", "files":list(contents), "tests":[], "roots":{},
            "overrides":{}, "archive_link_docs":[], "fixture_reason":"isolated fixture",
            "root_copies":{"README.md":"README.md", "Design.md":"Design.md",
                           "demo.mp4":"docs/demo.mp4"}}
    (source/"submission/spec.json").write_text(json.dumps(spec))
    monkeypatch.setattr(builder, "ROOT", source)
    return source, spec, contents


def test_submission_has_code_and_identical_root_documents_and_video(submission_source, tmp_path):
    source, spec, contents = submission_source
    output, archive_path = tmp_path/"delivery", tmp_path/"delivery.zip"
    builder.build(output, archive_path)
    assert {item.name for item in output.iterdir()} == {"code-agent", "README.md", "Design.md", "demo.mp4"}
    with zipfile.ZipFile(archive_path) as archive:
        expected = {"code-agent/"+name for name in contents}
        expected |= {"code-agent/SUBMISSION_MANIFEST.json", "README.md", "Design.md", "demo.mp4"}
        assert set(archive.namelist()) == expected
        assert archive.testzip() is None
        assert not any(Path(name).name == ".env" for name in archive.namelist())
        manifest = json.loads(archive.read("code-agent/SUBMISSION_MANIFEST.json"))
        for name, data in contents.items():
            assert archive.read("code-agent/"+name) == data
            assert manifest["files"][name]["sha256"] == hashlib.sha256(data).hexdigest()
        for name, inner in spec["root_copies"].items():
            assert archive.read(name) == archive.read("code-agent/"+inner)
            assert (output/name).read_bytes() == (output/"code-agent"/inner).read_bytes()
            assert manifest["root_copies"][name]["code_path"] == inner


@pytest.mark.parametrize("existing", ["directory", "zip"])
def test_submission_keeps_completed_artifacts(submission_source, tmp_path, existing):
    output, archive_path = tmp_path/"delivery", tmp_path/"delivery.zip"
    if existing == "directory":
        output.mkdir()
        (output/"sentinel.txt").write_text("keep")
    else:
        archive_path.write_bytes(b"existing archive")
    with pytest.raises(ValueError, match="not overwritten"):
        builder.build(output, archive_path)
    if existing == "directory":
        assert (output/"sentinel.txt").read_text() == "keep"
        assert not archive_path.exists()
    else:
        assert archive_path.read_bytes() == b"existing archive"
        assert not output.exists()


@pytest.mark.parametrize("name, inner", [("../README.md", "README.md"), ("README.md", "../outside.md")])
def test_submission_rejects_root_copy_outside_its_layout(submission_source, tmp_path, name, inner):
    source, spec, _ = submission_source
    spec["root_copies"] = {name:inner}
    (source/"submission/spec.json").write_text(json.dumps(spec))
    output, archive_path = tmp_path/"delivery", tmp_path/"delivery.zip"
    with pytest.raises(ValueError, match="Invalid root copy"):
        builder.build(output, archive_path)
    assert not output.exists() and not archive_path.exists()
