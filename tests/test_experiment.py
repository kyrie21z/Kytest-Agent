"""Frozen experiment inputs remain verifiable and cannot be silently replaced."""
import json

import pytest

from eval.experiment import freeze_sources, sha256_file, verify_sources


@pytest.fixture
def experiment(tmp_path):
    root = tmp_path / "repo"
    (root / "src").mkdir(parents=True)
    source = root / "src/agent.py"
    source.write_text("# 固定输入\n")
    spec = {"schema": "fixture", "jobs": [(1, "A0", "case/0")],
            "files_sha256": {"src/agent.py": sha256_file(source)}}
    return root, tmp_path / "run", spec


def test_freeze_and_resume_preserve_inputs_and_completed_results(experiment):
    root, output, spec = experiment
    freeze_sources(root, output, spec)
    assert (output / "source/src/agent.py").read_bytes() == (root / "src/agent.py").read_bytes()
    assert verify_sources(output, live_root=root) == json.loads(json.dumps(spec))
    manifest = (output / "manifest.json").read_bytes()
    (output / "completed.json").write_text('{"score": 1}')
    freeze_sources(root, output, spec)
    assert (output / "manifest.json").read_bytes() == manifest
    assert (output / "completed.json").read_text() == '{"score": 1}'
    assert not list(output.glob("*.tmp"))


@pytest.mark.parametrize("changed", ["frozen", "live", "spec"])
def test_changed_inputs_refuse_resume_without_replacing_evidence(experiment, changed):
    root, output, spec = experiment
    freeze_sources(root, output, spec)
    manifest = (output / "manifest.json").read_bytes()
    if changed == "frozen":
        (output / "source/src/agent.py").write_text("tampered")
    elif changed == "live":
        (root / "src/agent.py").write_text("new code")
    else:
        spec = dict(spec, jobs=[(1, "A4", "case/0")])
    with pytest.raises(ValueError, match={"frozen": "Frozen source mismatch",
                                       "live": "Live source changed", "spec": "inputs changed"}[changed]):
        freeze_sources(root, output, spec)
    assert (output / "manifest.json").read_bytes() == manifest


def test_new_freeze_requires_empty_output(experiment):
    root, output, spec = experiment
    output.mkdir()
    (output / "completed.json").write_text("keep")
    with pytest.raises(ValueError, match="must be empty"):
        freeze_sources(root, output, spec)
    assert (output / "completed.json").read_text() == "keep"
    assert not (output / "manifest.json").exists()


def test_changed_source_cannot_publish_a_complete_manifest(experiment):
    root, output, spec = experiment
    (root / "src/agent.py").write_text("changed after specification")
    with pytest.raises(ValueError, match="Source changed during freeze"):
        freeze_sources(root, output, spec)
    assert not (output / "manifest.json").exists()


@pytest.mark.parametrize("name", ["../outside.py", "/outside.py", "C:\\outside.py"])
def test_sources_cannot_escape_the_repository(experiment, name):
    root, output, spec = experiment
    spec["files_sha256"] = {name: "0" * 64}
    with pytest.raises(ValueError, match="Invalid source path"):
        freeze_sources(root, output, spec)
    assert not list(output.iterdir())


def test_symlinked_inputs_cannot_enter_a_frozen_experiment(experiment):
    root, output, spec = experiment
    link = root / "alias.py"
    try:
        link.symlink_to(root / "src/agent.py")
    except OSError:
        pytest.skip("symlinks unavailable")
    spec["files_sha256"] = {"alias.py": sha256_file(link)}
    with pytest.raises(ValueError, match="Symlink source path"):
        freeze_sources(root, output, spec)
    assert not list(output.iterdir())
