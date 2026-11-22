#!/usr/bin/env python3
"""Read-only ZIP/TAR inventory for a local blind-evaluation input bundle.

Never extracts entries or reads their contents; names are data, not instructions.
Does not establish evaluator isolation or challenge correctness.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tarfile
from datetime import datetime, timezone
import zipfile

TARGET = PurePosixPath("case-b/task.json")


def is_unsafe(name):
    path = PurePosixPath(name.replace("\\", "/"))
    return path.is_absolute() or ".." in path.parts or "\x00" in name or not path.parts


def inspect_bundle(path):
    records = []
    if zipfile.is_zipfile(path):
        kind = "zip"
        with zipfile.ZipFile(path) as archive:
            for item in archive.infolist():
                if item.is_dir():
                    continue
                symlink = ((item.external_attr >> 16) & 0o170000) == 0o120000
                records.append((item.filename, symlink))
    elif tarfile.is_tarfile(path):
        kind = "tar"
        with tarfile.open(path, "r:*") as archive:
            for item in archive:
                if item.isdir():
                    continue
                records.append((item.name, item.issym() or item.islnk()))
    else:
        raise ValueError("archive is not a supported ZIP or TAR")
    names = [name for name, _ in records]
    unsafe = sum(is_unsafe(name) or symlink for name, symlink in records)
    duplicates = len(names) - len(set(names))
    suffix = [name for name in names if tuple(PurePosixPath(name).parts[-2:]) == TARGET.parts]
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(block)
    return {"archive_type": kind, "sha256": checksum.hexdigest(),
            "file_entries": len(records), "unsafe_or_link_entries": unsafe,
            "duplicate_paths": duplicates,
            "case_b_task_json_entries": len(suffix),
            "case_b_task_json_in_archive": bool(suffix)}


def inventory_workspace(path):
    if path is None:
        return None
    if not path.is_dir():
        raise ValueError(f"extracted directory not found: {path}")
    files = 0
    task_found = 0
    symlinks = 0
    for directory, dirs, names in os.walk(path, followlinks=False):
        base = Path(directory)
        symlinks += sum((base / name).is_symlink() for name in dirs)
        dirs[:] = [name for name in dirs if not (base / name).is_symlink()]
        for name in names:
            target = base / name
            if target.is_symlink():
                symlinks += 1
                continue
            if not target.is_file():
                continue
            files += 1
            if tuple(target.relative_to(path).parts[-2:]) == TARGET.parts:
                task_found += 1
    return {"file_entries": files, "symlink_entries": symlinks,
            "case_b_task_json_entries": task_found}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--extracted-dir", type=Path)
    parser.add_argument("--expected-entries", type=int)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if not args.archive.is_file():
        parser.error("archive missing")
    try:
        bundle = inspect_bundle(args.archive)
        extracted = inventory_workspace(args.extracted_dir)
    except (OSError, ValueError, tarfile.TarError, zipfile.BadZipFile) as exc:
        parser.error(str(exc))
    result = {
        "schema_version": 1, "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "bundle": bundle, "extracted": extracted,
        "expected_file_entries": args.expected_entries,
        "expected_count_matches": (None if args.expected_entries is None
                                   else bundle["file_entries"] == args.expected_entries),
        "evaluation": "STRUCTURAL_ONLY",
        "blind_isolation_verified": False, "official_evaluation_verified": False,
        "notes": [
            "A partial extraction may be deliberate; entry counts alone do not establish missing task content.",
            "Presence of case-b/task.json does not establish its required role or safe visibility.",
            "This inspection does not read contents, freeze artifacts, or evaluate vulnerabilities.",
        ],
    }
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    print(output, end="")
    if args.out:
        dest = args.out.expanduser()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(output, encoding="utf-8")
    return 0 if bundle["unsafe_or_link_entries"] == 0 and bundle["duplicate_paths"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
