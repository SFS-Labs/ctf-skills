#!/usr/bin/env python3
"""Two-source answer-masked benchmark handoff and conservative metadata grading.

Uses Python stdlib only; does not launch agents, deploy contracts or execute PoCs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))
CASE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$")
GITHUB_RE = re.compile(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?")
HTTP_TIMEOUT = 20


class GatewayError(Exception):
    pass


def validate_id(case_id: str) -> str:
    if not CASE_RE.fullmatch(case_id):
        raise GatewayError("Invalid case ID: simple identifier required, no paths")
    return case_id


def raw_url(source: str, path: str) -> str:
    conf = SOURCES[source]
    return f"https://raw.githubusercontent.com/{conf['repository']}/{conf['ref']}/{path}"


def fetch_text(source: str, path: str) -> str:
    request = urllib.request.Request(
        raw_url(source, path),
        headers={"User-Agent": "SFS-Security-Benchmark-Gateway/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
            data = response.read(2_000_001)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise GatewayError(f"Upstream file unavailable: {path} ({exc})") from exc
    if len(data) > 2_000_000:
        raise GatewayError("Upstream input too large")
    return data.decode("utf-8")


def fetch_github_json(url: str) -> dict | list:
    """Fetch metadata from GitHub's public API without credentials."""
    if not url.startswith("https://api.github.com/repos/"):
        raise GatewayError("Unexpected GitHub API endpoint")
    request = urllib.request.Request(
        url, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "SFS-Security-Benchmark-Gateway/1.1",
        }
    )
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
            raw = response.read(2_000_001)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise GatewayError(f"Cannot fetch public repository metadata ({exc})") from exc
    if len(raw) > 2_000_000:
        raise GatewayError("GitHub metadata exceeded size limit")
    return json.loads(raw)


def snapshot_head(repo_url: str) -> str:
    """Pin a public upstream HEAD when ReEVMBench omits base_commit."""
    match = re.fullmatch(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", repo_url)
    if not match:
        raise GatewayError("Unexpected source repository URL")
    owner, name = match.groups()
    data = fetch_github_json(
        f"https://api.github.com/repos/{owner}/{name}/commits?per_page=1"
    )
    sha = data[0].get("sha", "") if isinstance(data, list) and data else ""
    if not re.fullmatch(r"[a-fA-F0-9]{40}", sha):
        raise GatewayError("Cannot establish immutable source revision")
    return sha


def catalog(source: str) -> dict:
    if source == "cyberchainbench":
        conf = SOURCES[source]
        repo = conf["repository"]
        ref = conf["ref"]
        rows = fetch_github_json(
            f"https://api.github.com/repos/{repo}/contents/data/benchmark/cases?ref={ref}"
        )
        if not isinstance(rows, list):
            raise GatewayError("CyberChainBench catalog unavailable")
        ids = sorted(
            row["name"][:-5] for row in rows
            if isinstance(row, dict)
            and re.fullmatch(r"bench-[0-9]+\.json", row.get("name", ""))
        )
    else:
        ids = sorted(
            line.strip() for line in fetch_text(source, "splits/detect-tasks.txt").splitlines()
            if line.strip() and not line.strip().startswith("#")
        )
    if not ids or len(ids) != len(set(ids)) or any(
        not CASE_RE.fullmatch(case_id) for case_id in ids
    ):
        raise GatewayError("Invalid or empty benchmark catalog")
    return {
        "schema": "sfs-benchmark-catalog-v1",
        "benchmark": source,
        "revision": SOURCES[source]["ref"],
        "case_count": len(ids),
        "case_ids": ids,
        "note": "Catalog for evaluator selection only. Do not pass case IDs to blind auditor.",
    }


def yaml_scalar(contents: str, key: str) -> str | None:
    match = re.search(
        rf"(?m)^{re.escape(key)}:\s*['\"]?([^\n#'\"]+)", contents
    )
    return match.group(1).strip() if match else None


def case_alias(source: str, case_id: str) -> str:
    return "audit-" + hashlib.sha256(
        f"{source}:{case_id}".encode()
    ).hexdigest()[:12]


def load_reference(source: str, case_id: str) -> dict:
    validate_id(case_id)
    if source == "cyberchainbench":
        document = json.loads(fetch_text(
            source, f"data/benchmark/cases/{case_id}.json"
        ))
        if document.get("id") != case_id:
            raise GatewayError("Case ID mismatch")
        for field in ("chain", "vulnerable_address", "block_number", "type", "function"):
            if field not in document:
                raise GatewayError(f"Case missing required field: {field}")
        if not re.fullmatch(r"0x[a-fA-F0-9]{40}", str(document["vulnerable_address"])):
            raise GatewayError("Invalid contract address")
        return document

    if source == "reevmbench":
        config = fetch_text(source, f"audits/{case_id}/config.yaml")
        dockerfile = fetch_text(source, f"audits/{case_id}/Dockerfile")
        repository = GITHUB_RE.search(dockerfile)
        commit = yaml_scalar(config, "base_commit")
        if yaml_scalar(config, "id") != case_id:
            raise GatewayError("Case ID mismatch")
        if not repository:
            raise GatewayError("Audit Dockerfile does not name a public source repository")
        repo_url = repository.group(0).removesuffix(".git")
        revision_method = "benchmark_base_commit"
        if not commit:
            commit = snapshot_head(repo_url)
            revision_method = "upstream_head_at_preparation"
        if not re.fullmatch(r"[a-fA-F0-9]{40}", commit):
            raise GatewayError("Cannot pin the audit target source")
        references = []
        for block in re.split(r"(?m)^[ \\t]+- id:[ \\t]*", config)[1:]:
            match_id = re.match(r"""["']?([A-Za-z0-9_-]+)""", block)
            match_title = re.search(r"(?m)^[ \\t]+title:[ \\t]*(.+)$", block)
            if match_id:
                title = match_title.group(1).strip() if match_title else ""
                references.append({
                    "id": match_id.group(1),
                    "title": title.strip("\\\"'"),
                })
        return {
            "id": case_id,
            "repo_url": repo_url,
            "base_commit": commit,
            "revision_method": revision_method,
            "run_cmd_dir": yaml_scalar(config, "run_cmd_dir"),
            "vulnerability_ids": [entry["id"] for entry in references],
            "reference_findings": references,
        }
    raise GatewayError("Unsupported source")


def prepare(source: str, case_id: str, phase: str) -> dict:
    document = load_reference(source, case_id)
    brief = {
        "schema": "sfs-benchmark-brief-v1",
        "task": "independent-security-audit" if phase == "detect" else "historical-reproduction",
        "alias": case_alias(source, case_id),
        "instructions": (
            "Use ctf-skill-index V7 and all available security tools. Independently "
            "derive findings from the authorized historical target. Freeze the "
            "report and evidence before evaluator access. Do not inspect upstream "
            "benchmark ground truth, patches or incident reports."
        ),
        "submission_schema": {
            "findings": [{
                "type": "string or null",
                "function": "string or null",
                "finding_id": "string or null",
                "evidence_path": "string or null",
            }],
            "notes": "string",
        },
        "provenance": {
            "benchmark": source,
            "ref": SOURCES[source]["ref"],
        },
    }
    if source == "cyberchainbench":
        brief["target"] = {
            "chain": document["chain"],
            "contract_address": document["vulnerable_address"],
        }
        if phase == "reproduce":
            brief["target"]["historical_block"] = document["block_number"]
    else:
        brief["target"] = {
            "source_repository": document["repo_url"],
            "source_commit": document["base_commit"],
            "revision_method": document["revision_method"],
            "working_subdirectory": document.get("run_cmd_dir"),
        }
    # No case IDs, incident names, known attack txs, fix text, vuln labels or functions.
    return brief


def grade(source: str, case_id: str, submission: dict) -> dict:
    document = load_reference(source, case_id)
    findings = submission.get("findings", [])
    if not isinstance(findings, list) or len(findings) > 100 or not all(
        isinstance(f, dict) for f in findings
    ):
        raise GatewayError("Submission requires findings: array of <=100 objects")
    grade_result = {
        "schema": "sfs-benchmark-grade-v1",
        "frozen_submission_sha256": hashlib.sha256(
            json.dumps(submission, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest(),
        "alias": case_alias(source, case_id),
        "benchmark": source,
        "reported_findings": len(findings),
        "independent_reproduction": "NOT_VERIFIED",
        "warning": "Metadata matching alone does not establish exploitability or soundness.",
    }
    if source == "cyberchainbench":
        expected_type = str(document["type"]).casefold().strip()
        expected_function = str(document["function"]).casefold().strip()
        matches = [
            i for i, finding in enumerate(findings)
            if str(finding.get("type") or "").casefold().strip() == expected_type
            and str(finding.get("function") or "").casefold().strip() == expected_function
        ]
        grade_result["label_match"] = bool(matches)
        grade_result["matching_finding_indices"] = matches
        grade_result["status"] = (
            "LABEL_MATCH_UNVERIFIED" if matches else "NO_EXACT_LABEL_MATCH"
        )
    else:
        gold_ids = set(document["vulnerability_ids"])
        matches = [
            i for i, finding in enumerate(findings)
            if finding.get("finding_id") in gold_ids
        ]
        grade_result["finding_id_match"] = bool(matches)
        grade_result["matching_finding_indices"] = matches
        grade_result["reference_findings"] = document["reference_findings"]
        grade_result["status"] = "MANUAL_REVIEW_REQUIRED"
        grade_result["warning"] = (
            "ReEVMBench finding IDs are withheld from the blind auditor. "
            "Use the reference findings above only after freezing the report; "
            "review technical evidence independently. No official score claimed."
        )
    return grade_result


def confined_submission_path(argument: str) -> Path:
    root = (HERE / "submissions").resolve()
    target = (root / argument).resolve()
    if not target.is_relative_to(root) or target.suffix != ".json" or not target.is_file():
        raise GatewayError("Submission must be an existing JSON under benchmarks/submissions/")
    if target.stat().st_size > 1_000_000:
        raise GatewayError("Submission too large")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["catalog", "prepare", "grade", "smoke"])
    parser.add_argument("--source", choices=sorted(SOURCES), required=True)
    parser.add_argument("--case-id", default="")
    parser.add_argument("--phase", choices=["detect", "reproduce"], default="detect")
    parser.add_argument("--submission", help="JSON filename inside benchmarks/submissions/")
    parser.add_argument("--submission-json-env", action="store_true",
                        help="Read JSON from SUBMISSION_JSON environment variable")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args(argv)

    try:
        if args.command == "catalog":
            result = catalog(args.source)
        elif args.command == "smoke":
            result = {
                "schema": "sfs-benchmark-smoke-v1",
                "cases": [
                    prepare("cyberchainbench", "bench-01", "detect"),
                    prepare("reevmbench", "2024-06-thorchain", "detect"),
                ],
                "note": "Two live upstream case adapters exercised; no agent or exploit executed.",
            }
        elif args.command == "prepare":
            result = prepare(args.source, args.case_id, args.phase)
        else:
            if args.submission_json_env:
                raw = os.environ.get("SUBMISSION_JSON", "")
                if not raw or len(raw) > 50000:
                    raise GatewayError("SUBMISSION_JSON missing or too large")
                submission = json.loads(raw)
            elif args.submission:
                submission = json.loads(
                    confined_submission_path(args.submission).read_text(encoding="utf-8")
                )
            else:
                raise GatewayError("Provide --submission or --submission-json-env")
            if not isinstance(submission, dict):
                raise GatewayError("Submission must be a JSON object")
            result = grade(args.source, args.case_id, submission)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"{args.command}: {args.source} / {args.case_id} -> {output}")
        return 0
    except (GatewayError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"Gateway error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
