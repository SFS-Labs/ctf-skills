#!/usr/bin/env python3
"""Install the canonical V8 skill into a specific *new-session* Freebuff project.

Dry-run by default. Never overwrite an existing skill or claim runtime activation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

RELATIVE_SKILL = Path(".agents/skills/ctf-skill-index-v8/SKILL.md")


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True,
                        help="Actual Freebuff project directory, not the CTF tool repository")
    parser.add_argument("--skills-root", type=Path, default=Path.home() / "ctf-skills")
    parser.add_argument("--apply", action="store_true",
                        help="Explicitly write the missing skill file; no overwrite")
    args = parser.parse_args()
    project = args.project.expanduser().resolve(strict=False)
    source = (args.skills_root.expanduser() / RELATIVE_SKILL).resolve(strict=False)
    dest = project / RELATIVE_SKILL
    if not project.is_dir():
        parser.error(f"project does not exist: {project}")
    if not source.is_file():
        parser.error(f"canonical V8 source missing: {source}")
    source_bytes = source.read_bytes()
    if not source_bytes.startswith(b"---\nname: ctf-skill-index-v8\n"):
        parser.error("canonical V8 skill frontmatter name does not match directory")
    if b"bin/skill-orchestrator.py" not in source_bytes:
        parser.error("V8 source does not reference the orchestrator")
    for part in (project / ".agents", project / ".agents/skills", dest.parent):
        if part.is_symlink():
            parser.error(f"refusing symlinked destination parent: {part}")
    status = "DRY_RUN"
    if dest.exists() or dest.is_symlink():
        if dest.is_symlink() or not dest.is_file():
            parser.error(f"destination is not a regular file: {dest}")
        if dest.read_bytes() != source_bytes:
            parser.error(f"destination conflict; no overwrite: {dest}")
        status = "ALREADY_IDENTICAL_RUNTIME_UNVERIFIED"
    elif args.apply:
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            with dest.open("xb") as stream:
                stream.write(source_bytes)
        except FileExistsError:
            parser.error("concurrent destination modification; no overwrite")
        if dest.read_bytes() != source_bytes:
            parser.error("post-write integrity check failed")
        status = "INSTALLED_RUNTIME_UNVERIFIED"
    print(json.dumps({
        "status": status, "project": str(project), "source": str(source),
        "target": str(dest), "sha256": digest(source_bytes),
        "native_skill_invocation_observed": False,
        "note": "Start a NEW Freebuff project session; verify a native skill tool call separately.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
