"""Build the coursework profile from an explicit whitelist; retain research originals."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = "https://github.com/kyrie21z/Kytest-Agent/blob/e34bb5c8770f85815612e5669a50a02a0c5f5532/"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def source_state(selected):
    # A standalone extraction must not inherit the identity of a parent repository.
    if (ROOT / ".git").exists():
        revision = subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT).decode().strip()
        dirty = bool(subprocess.check_output(["git","status","--porcelain"],cwd=ROOT))
        return revision,dirty
    manifest = ROOT / "SUBMISSION_MANIFEST.json"
    if manifest.exists():
        old = json.loads(manifest.read_text())
        previous = old["files"]
        changed = set(selected)!=set(previous) or any(
            name not in previous or digest(path.read_bytes())!=previous[name]["sha256"]
            for name,path in selected.items())
        return old["source_commit"],bool(old["source_worktree_dirty"] or changed)
    return "unversioned",True

def selected_files(spec):
    chosen = {name:ROOT/name for name in spec["files"]}
    chosen.update({"tests/"+name:ROOT/"tests"/name for name in spec["tests"]})
    for directory,pattern in spec["roots"].items():
        for path in (ROOT/directory).glob(pattern):
            if path.is_file() and not any(part in {"__pycache__",".pytest_cache"} for part in path.parts):
                chosen[str(path.relative_to(ROOT))] = path
    for target,source in spec["overrides"].items():
        candidate = ROOT/source
        chosen[target] = candidate if candidate.exists() else ROOT/target
    forbidden = {".env","id_rsa","id_ed25519"}
    for target,source in chosen.items():
        if Path(target).is_absolute() or ".." in Path(target).parts or Path(target).name in forbidden:
            raise ValueError("Invalid submission target: "+target)
        if not source.is_file() or source.is_symlink() or ROOT not in source.resolve().parents:
            raise ValueError("Missing or external submission input: "+str(source))
    return chosen

def archive_links(text,relative_path,chosen):
    def replace(match):
        label,target = match.groups()
        if target.startswith(("http://","https://","#")):
            return match.group(0)
        path,separator,anchor = target.partition("#")
        resolved = (ROOT/relative_path).parent.joinpath(path).resolve()
        if ROOT not in resolved.parents:
            return match.group(0)
        name = str(resolved.relative_to(ROOT))
        if name in chosen:
            return match.group(0)
        return f"[{label}]({ARCHIVE}{name}{separator}{anchor})"
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)",replace,text)

def build(output,zip_path):
    spec = json.loads((ROOT/"submission/spec.json").read_text())
    selected = selected_files(spec)
    if output.exists() or zip_path.exists():
        raise ValueError("Use a new output directory and ZIP; completed artifacts are not overwritten")
    revision,dirty = source_state(selected)
    output.mkdir(parents=True,exist_ok=False)
    manifest = {"schema":spec["schema"],"source_commit":revision,"source_worktree_dirty":dirty,
        "profile":"coursework: runnable code, unchanged core regression subset, concise docs and derived evidence",
        "archive":"https://github.com/kyrie21z/Kytest-Agent/tree/e34bb5c8770f85815612e5669a50a02a0c5f5532",
        "fixture_reason":spec["fixture_reason"],"files":{}}
    for name,source in sorted(selected.items()):
        original = source.read_bytes()
        data = original
        transformation = None
        if name in spec["archive_link_docs"]:
            data = archive_links(original.decode(),name,selected).encode()
            if data!=original:
                transformation = "Excluded research links redirected to their pinned archive; no behavior change"
        destination = output/name
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(data)
        manifest["files"][name] = {"bytes":len(data),"sha256":digest(data),
            "source_path":str(source.relative_to(ROOT)),"source_sha256":digest(original),
            "transformation":transformation}
    manifest["content_files"] = len(selected)
    (output/"SUBMISSION_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    zip_path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(zip_path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        archive.comment = revision.encode()
        for path in sorted(output.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo("code-agent/"+str(path.relative_to(output)),date_time=(2026,10,7,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info,path.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(zip_path) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP integrity failure")
        expected = {"code-agent/"+name for name in selected}|{"code-agent/SUBMISSION_MANIFEST.json"}
        if len(archive.namelist())!=len(expected) or set(archive.namelist())!=expected:
            raise ValueError("ZIP member matrix differs")
        for name,entry in manifest["files"].items():
            if digest(archive.read("code-agent/"+name))!=entry["sha256"]:
                raise ValueError("ZIP content changed: "+name)
    print(json.dumps({"output":str(output),"zip":str(zip_path),"files":len(selected)+1,
        "bytes":zip_path.stat().st_size,"sha256":digest(zip_path.read_bytes()),
        "source_commit":revision,"source_worktree_dirty":dirty},ensure_ascii=False,indent=2))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True,type=Path)
    parser.add_argument("--zip",type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    zip_path = args.zip.resolve() if args.zip else output.with_suffix(".zip")
    build(output,zip_path)

if __name__ == "__main__":
    main()
