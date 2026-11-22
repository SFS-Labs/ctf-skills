#!/usr/bin/env python3
"""Read-only toolchain inventory for a local Freebuff/EVM analysis session.

Does not load challenge inputs, install software, or claim runtime skill activation.
"""
import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone

KEYS = ("git", "docker", "docker_compose", "forge", "anvil", "slither", "mythril", "manticore", "ida", "oz_foundry_upgrades", "v8_skill", "freebuff_trace")


def cmd_result(cmd, args=("--version",), timeout=5):
    resolved = shutil.which(cmd)
    if not resolved:
        return {"status": "MISSING", "path": None}
    try:
        proc = subprocess.run([resolved, *args], capture_output=True, text=True,
                              timeout=timeout, check=False, stdin=subprocess.DEVNULL)
        excerpt = (proc.stdout or proc.stderr).strip().splitlines()
        return {"status": "PASS" if proc.returncode == 0 else "FAILED",
                "path": resolved, "exit_code": proc.returncode,
                "detail": excerpt[0][:240] if excerpt else ""}
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "path": resolved}
    except OSError as exc:
        return {"status": "FAILED", "path": resolved, "detail": type(exc).__name__}


def inspection(project, skills_root, bundled_git):
    out = {}
    out["git"] = cmd_result("git")
    if out["git"]["status"] == "MISSING" and bundled_git.is_file():
        out["git"] = {"status": "BUNDLED_OUTSIDE_PATH", "path": str(bundled_git),
                      "detail": "Repair via scripts/security-toolchain-repair.sh git"}
    out["docker"] = cmd_result("docker", ("info", "--format", "{{.ServerVersion}}"))
    out["docker_compose"] = cmd_result("docker", ("compose", "version"))
    for tool in ("forge", "anvil", "slither", "mythril", "manticore"):
        out[tool] = cmd_result(tool)
    ida_binary = shutil.which("ida") or shutil.which("ida64") or shutil.which("idat64")
    out["ida"] = ({"status": "INSTALLATION_FOUND_LICENSE_UNVERIFIED", "path": ida_binary}
                  if ida_binary else {"status": "MISSING_LICENSE_REQUIRED", "path": None})
    locations = [project / "lib/openzeppelin-foundry-upgrades",
                 project / "node_modules/@openzeppelin/foundry-upgrades"]
    installed = [p for p in locations if p.is_dir()]
    out["oz_foundry_upgrades"] = (
        {"status": "INSTALLED_NOT_VALIDATED", "path": str(installed[0]),
         "detail": "Requires real Foundry project compile and upgrade safety validation"}
        if installed else {"status": "MISSING_PROJECT_DEPENDENCY", "path": None})
    skill = skills_root / ".agents/skills/ctf-skill-index-v8/SKILL.md"
    if skill.is_file():
        try:
            first_lines = skill.read_text(encoding="utf-8").splitlines()[:5]
            valid = "name: ctf-skill-index-v8" in first_lines
        except OSError:
            valid = False
        out["v8_skill"] = {"status": "PRESENT_RUNTIME_UNVERIFIED" if valid else "INVALID_FRONTMATTER",
                           "path": str(skill)}
    else:
        out["v8_skill"] = {"status": "MISSING", "path": str(skill)}
    out["freebuff_trace"] = {"status": "UNVERIFIED", "path": None,
                              "detail": "CLI environment check cannot prove a Freebuff skill tool call"}
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--skills-root", type=Path, default=Path.home() / "ctf-skills")
    parser.add_argument("--bundled-git", type=Path,
                        default=Path("/opt/Freebuff/resources/git/bin/git"))
    parser.add_argument("--out", type=Path, help="Explicit local JSON output path")
    parser.add_argument("--require", default="", help="Comma-separated keys that must be PASS")
    args = parser.parse_args()
    required = [s.strip() for s in args.require.split(",") if s.strip()]
    unknown = set(required) - set(KEYS)
    if unknown:
        parser.error(f"unknown required keys: {', '.join(sorted(unknown))}")
    tools = inspection(args.project.resolve(), args.skills_root.expanduser().resolve(),
                       args.bundled_git.expanduser())
    doc = {"schema_version": 1,
           "generated_utc": datetime.now(timezone.utc).isoformat(),
           "system": {"os": platform.system(), "arch": platform.machine()},
           "context": {"project": str(args.project.resolve()),
                       "skills_root": str(args.skills_root.expanduser().resolve())},
           "checks": tools, "required": required,
           "required_pass": all(tools[k]["status"] == "PASS" for k in required),
           "notice": "Environment diagnostics only; no skill invocation, blind isolation, or exploit proven."}
    output = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    print(output, end="")
    if args.out:
        dest = args.out.expanduser()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(output, encoding="utf-8")
    return 0 if doc["required_pass"] else 2


if __name__ == "__main__":
    sys.exit(main())
