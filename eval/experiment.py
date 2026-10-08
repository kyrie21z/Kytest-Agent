"""Freeze experiment inputs and refuse resumes with changed code or evidence."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _source_path(root: Path, name: str) -> Path:
    if root.is_symlink():
        raise ValueError("Symlink source path: " + name)
    relative = PurePosixPath(name.replace("\\", "/"))
    if relative.is_absolute() or ".." in relative.parts or not relative.parts or ":" in name:
        raise ValueError("Invalid source path: " + name)
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError("Symlink source path: " + name)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Invalid source path: " + name)
    return path


def verify_sources(output: Path, *, live_root: Path | None = None) -> dict:
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["files_sha256"].items():
        frozen = _source_path(output / "source", name)
        if not frozen.is_file() or sha256_file(frozen) != expected:
            raise ValueError("Frozen source mismatch: " + name)
        if live_root is not None:
            live = _source_path(live_root, name)
            if not live.is_file() or sha256_file(live) != expected:
                raise ValueError("Live source changed: " + name)
    return manifest


def freeze_sources(root: Path, output: Path, spec: dict) -> None:
    output.mkdir(parents=True, exist_ok=True)
    manifest = output / "manifest.json"
    if manifest.exists():
        if json.loads(json.dumps(spec)) != verify_sources(output, live_root=root):
            raise ValueError("Experiment inputs changed; use a new output directory")
        return
    if any(output.iterdir()):
        raise ValueError("New experiment output must be empty")
    # Resolve the complete input set before copying any file.
    sources = [(name, expected, _source_path(root, name),
                _source_path(output / "source", name))
               for name, expected in spec["files_sha256"].items()]
    for name, expected, source, destination in sources:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        if sha256_file(destination) != expected:
            raise ValueError("Source changed during freeze: " + name)
    # A manifest marks a complete freeze; failed copies never publish one.
    write_json(manifest, spec)
