#!/usr/bin/env python3
"""SFS GitHub Copilot delegation layer - Freebuff leads, Copilot executes bounded subtasks.

Policy (default, no spend):
    * Reads are free and always allowed (identity, repo, suggested actors, agent-task list).
    * Paid delegation is gated by ``.copilot/policy.json`` (both ``paid_delegation_allowed``
      and ``credits_exhausted == false``) AND ``--allow-paid`` on the command line.
    * ``--execute`` is refused unless the gate is open. ``--dry-run`` is the default.
    * No auto-merge, no deployment, no publication, no force-push, no secret handling.

Lifecycle:
    PREFLIGHT -> DETECT -> DELEGATE -> WATCH -> REVIEW -> PROFICIENCY
    States: PLANNED, BLOCKED_PAID_GATE, BLOCKED_ROUTE, DELEGATED, QUEUED,
    IN_PROGRESS, WAITING_FOR_USER, PR_OPENED, CI_PENDING, CI_FAILED, CI_PASSED,
    COMPLETED, FAILED, TIMED_OUT, CANCELLED, QUOTA_BLOCKED, WATCH_ERROR,
    WATCH_LIMIT_REACHED, REVIEWED, CHANGES_REQUIRED, COMPLETED_UNVERIFIED.

The mock server (``demo``/``selftest``) exercises the whole lifecycle over real HTTP
against simulated GitHub responses. Simulated records are never counted as Copilot
proficiency evidence.

Exit codes: 0 success/verified, 1 failed or blocked, 2 usage/configuration error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

API_URL = "https://api.github.com"
API_VERSION = "2026-03-10"
GRAPHQL_FEATURES = "issues_copilot_assignment_api_support, coding_agent_model_selection"
BOT_LOGIN = "copilot-swe-agent"
BOT_FULL = "copilot-swe-agent[bot]"
DEFAULT_REPO = "SFS-Labs/ctf-skill-factory"
STANDARD_REPO = "SFS-Labs/sfs-ai-development-gateway"
STANDARD_PATHS = (
    "docs/COPILOT_PROFICIENCY_OPERATING_STANDARD.md",
    "COPILOT_PROFICIENCY_OPERATING_STANDARD.md",
    "docs/copilot-proficiency-operating-standard.md",
    ".github/copilot-instructions.md",
    "README.md",
)

DOMAINS = (
    {
        "id": "ai-collaboration",
        "name": "AI Collaboration",
        "evidence": "Observed Copilot agent activity (started event / completed session) "
                    "and a Copilot-authored pull request.",
    },
    {
        "id": "prompting",
        "name": "Prompting",
        "evidence": "A bounded delegation brief with objective, scope, acceptance criteria "
                    "and tests, plus a review proving the delivered change stayed in scope.",
    },
    {
        "id": "code-generation-validation",
        "name": "Code Generation & Validation",
        "evidence": "Copilot-generated diff, CI evidence for the exact head SHA, and an "
                    "independent review with positive and negative checks.",
    },
    {
        "id": "agent-configuration",
        "name": "Agent Configuration",
        "evidence": "A custom agent, repository instructions or skill demonstrably used by "
                    "the Copilot session. The GitHub API does not expose this by default.",
    },
    {
        "id": "tool-context-integration",
        "name": "Tool & Context Integration",
        "evidence": "An MCP server, CLI or other tool actually invoked inside Copilot. "
                    "GitHub's issue/agent-task APIs do not report tool invocations.",
    },
)

TERMINAL_STATES = {
    "COMPLETED", "FAILED", "TIMED_OUT", "CANCELLED", "QUOTA_BLOCKED",
    "WATCH_ERROR", "WATCH_LIMIT_REACHED", "REVIEWED", "CHANGES_REQUIRED",
    "COMPLETED_UNVERIFIED", "BLOCKED_PAID_GATE", "BLOCKED_ROUTE", "DUPLICATE",
}
SUCCESS_STATES = {"COMPLETED", "REVIEWED"}
DEFAULT_POLICY = {
    "version": 1,
    "paid_delegation_allowed": False,
    "credits_exhausted": True,
    "auto_merge": False,
    "max_tasks_per_run": 1,
    "allow_issue_creation": True,
    "updated_at": None,
    "notes": "Copilot agent credits are exhausted. Paid delegation stays closed until "
             "the user restores quota and explicitly opens the gate.",
}

FORBIDDEN_PATH_PREFIXES = (
    ".git/", ".github/workflows/", ".github/actions/", "vendor/", "venvs/",
    "tools/", "backups/", ".copilot/", "dist/", "node_modules/",
)
FORBIDDEN_SCOPE_PATTERNS = (
    (r"\b(secret|credential|api[ _-]?key|private key|password)\b", "secret handling"),
    (r"\b(deploy|publish|release to production|production deploy)\b", "deployment/publication"),
    (r"\b(auto[ -]?merge|merge (?:the )?pr|force[ -]?push)\b", "merge/destructive git"),
    (r"\b(live transaction|mainnet|real funds|send (?:eth|funds|tokens))\b", "live transaction"),
    (r"\b(tailscale|rustdesk|netdata|ssh config|desktop settings)\b", "infrastructure/desktop"),
    (r"\b(rm -rf|drop (?:the )?database|reset --hard)\b", "destructive operation"),
    (r"\b(enable issues|change repository settings|add collaborator)\b", "repo administration"),
)
SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
)
DELIVERABLE_RE = re.compile(
    r"\b(add|implement|fix|refactor|extract|rename|update|document|test|remove|replace|"
    r"introduce|harden|migrate|simplify)\b", re.I)
BOUNDED_RE = re.compile(
    r"(?:\b[\w./-]+\.(?:py|js|jsx|ts|tsx|md|ya?ml|json|sh|sol|toml|cfg|ini)\b)|"
    r"\b(?:file|function|class|module|test|method|handler|endpoint)\b", re.I)
ACCEPTANCE_RE = re.compile(r"\b(test|tests|acceptance|verify|assert|ci|lint|regression)\b", re.I)
BROAD_RE = re.compile(
    r"\b(redesign|rearchitect|entire codebase|whole codebase|all repositories|"
    r"migrate everything|rewrite everything)\b", re.I)
CREDIT_RE = re.compile(r"(insufficient|out of|exhausted|no)[^.\n]{0,40}(ai )?credits?", re.I)
PATH_RE = re.compile(r"\b[\w.-]+(?:/[\w.-]+)*\.(?:py|js|jsx|ts|tsx|md|ya?ml|json|sh|sol|toml|cfg|ini)\b")


class CopilotError(RuntimeError):
    """Configuration or contract error (exit code 2)."""


class APIError(CopilotError):
    def __init__(self, status, message, *, url=None, body=None):
        super().__init__(f"GitHub API {status}: {message}")
        self.status = status
        self.url = url
        self.body = body


# --------------------------------------------------------------------------
# Small utilities
# --------------------------------------------------------------------------
def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def sha256_bytes(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def repo_root():
    return Path(__file__).resolve().parent.parent


def ensure_state(state_dir):
    path = Path(state_dir or repo_root() / ".copilot")
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except OSError:
        pass
    return path


def write_json(path, obj, mode=0o600):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp-{os.getpid()}")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=False) + "\n",
                   encoding="utf-8")
    try:
        tmp.chmod(mode)
    except OSError:
        pass
    os.replace(tmp, path)
    return path


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def tail(text, limit=4000):
    text = text or ""
    return text[-limit:]


def _redact(text):
    text = str(text)
    for pattern in (r"gh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}",
                    r"Bearer\s+[A-Za-z0-9._-]+"):
        text = re.sub(pattern, "[REDACTED]", text)
    return text


def load_token():
    for name in ("GH_TOKEN", "GITHUB_TOKEN"):
        value = os.environ.get(name, "").strip()
        if value:
            return value, name
    path = Path.home() / ".config" / "gh-token"
    try:
        value = path.read_text(encoding="utf-8").strip().splitlines()[0].strip()
    except (OSError, IndexError):
        return None, "none"
    return (value or None), str(path)


def split_repo(value):
    if not value or "/" not in value:
        raise CopilotError("repository must be OWNER/REPO")
    owner, name = value.split("/", 1)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", owner) or not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise CopilotError("invalid repository name")
    return owner, name


def norm_path(value):
    value = str(value).strip().replace("\\", "/")
    if not value or value.startswith("/") or ".." in Path(value).parts:
        raise CopilotError(f"invalid path: {value!r}")
    return value.lstrip("./")


# --------------------------------------------------------------------------
# GitHub client
# --------------------------------------------------------------------------
class APIResponse:
    def __init__(self, status, headers, body, method, url):
        self.status = status
        self.headers = {k.lower(): v for k, v in (headers or {}).items()}
        self.body = body or b""
        self.method = method
        self.url = url

    def json(self):
        if not self.body:
            return None
        try:
            return json.loads(self.body.decode("utf-8"))
        except ValueError as exc:
            raise CopilotError(f"invalid JSON from GitHub: {exc}") from exc

    def text(self):
        return self.body.decode("utf-8", errors="replace")


class GitHubClient:
    def __init__(self, token=None, api_url=None, timeout=20, retries=2):
        if token is None:
            token, self.token_source = load_token()
        else:
            self.token_source = "injected"
        self.token = token
        self.api_url = (api_url or os.environ.get("COPILOT_GITHUB_API_URL") or API_URL).rstrip("/")
        self.timeout = timeout
        self.retries = max(0, int(retries))

    def request(self, method, path, *, json_body=None, accept="application/vnd.github+json",
                extra_headers=None, raw=False):
        url = path if path.startswith("http") else self.api_url + "/" + path.lstrip("/")
        headers = {
            "Accept": accept,
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "sfs-copilot-delegate/1.0",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if json_body is not None:
            headers["Content-Type"] = "application/json"
            data = canonical(json_body).encode("utf-8")
        else:
            data = None
        headers.update(extra_headers or {})

        last_error = None
        for attempt in range(self.retries + 1):
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    body = resp.read(8 * 1024 * 1024)
                    return APIResponse(resp.status, dict(resp.headers), body, method, url)
            except urllib.error.HTTPError as exc:
                body = exc.read(1024 * 1024)
                status = exc.code
                retryable = status in (429, 502, 503, 504) or (
                    status == 403 and exc.headers.get("x-ratelimit-remaining") == "0")
                if retryable and attempt < self.retries:
                    delay = _retry_delay(exc.headers, attempt)
                    last_error = APIError(status, "transient rate limit", url=url, body=body)
                    time.sleep(delay)
                    continue
                message = _error_message(body, status)
                raise APIError(status, message, url=url, body=body) from exc
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                if attempt < self.retries:
                    last_error = APIError(0, str(exc), url=url)
                    time.sleep(min(0.5 * (2 ** attempt), 4.0))
                    continue
                raise APIError(0, str(exc), url=url) from exc
        raise last_error or APIError(0, "request failed", url=url)

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, body=None, **kwargs):
        return self.request("POST", path, json_body=body, **kwargs)

    def graphql(self, query, variables=None):
        payload = {"query": query}
        if variables is not None:
            payload["variables"] = variables
        resp = self.request("POST", "/graphql", json_body=payload,
                            extra_headers={"GraphQL-Features": GRAPHQL_FEATURES})
        data = resp.json() or {}
        errors = data.get("errors") or []
        if errors:
            message = "; ".join(str(e.get("message", e)) for e in errors)[:500]
            raise APIError(0, f"GraphQL: {message}", url=resp.url)
        return data.get("data") or {}

    def paged(self, path, key, max_pages=3):
        sep = "&" if "?" in path else "?"
        out = []
        for page in range(1, max_pages + 1):
            resp = self.get(f"{path}{sep}per_page=100&page={page}")
            data = resp.json()
            batch = (data.get(key) if isinstance(data, dict) else data) or []
            out.extend(batch)
            if len(batch) < 100:
                break
        return out


def _retry_delay(headers, attempt):
    try:
        value = float(headers.get("retry-after", ""))
    except (TypeError, ValueError):
        value = 0.5 * (2 ** attempt)
    return max(0.0, min(value, 5.0))


def _error_message(body, status):
    try:
        data = json.loads(body.decode("utf-8", errors="replace"))
        if isinstance(data, dict):
            return str(data.get("message") or data.get("error") or status)[:500]
    except ValueError:
        pass
    return status


# --------------------------------------------------------------------------
# Policy and standard
# --------------------------------------------------------------------------
def policy_path(state_dir):
    return Path(state_dir) / "policy.json"


def load_policy(state_dir):
    data = read_json(policy_path(state_dir), {}) or {}
    policy = dict(DEFAULT_POLICY)
    if isinstance(data, dict):
        policy.update({k: v for k, v in data.items() if k in DEFAULT_POLICY})
    return policy


def save_policy(state_dir, policy):
    policy = dict(policy)
    policy["updated_at"] = utcnow()
    write_json(policy_path(state_dir), policy)
    return policy


def local_standard_path(root=None):
    return Path(root or repo_root()) / "docs" / "COPILOT_PROFICIENCY_OPERATING_STANDARD.md"


def load_local_standard(root=None):
    base = Path(root or repo_root()) / "docs"
    candidates = [
        base / "COPILOT_PROFICIENCY_OPERATING_STANDARD.md",
        base / "COPILOT-PROFICIENCY-STANDARD.md",
    ]
    path = None
    text = ""
    for candidate in candidates:
        try:
            text = candidate.read_text(encoding="utf-8")
            path = candidate
            break
        except OSError:
            continue
    canonical = path is not None and path.name == "COPILOT_PROFICIENCY_OPERATING_STANDARD.md"
    origin = {}
    if canonical:
        meta = read_json(path.with_name(path.stem + ".provenance.json"), {}) or {}
        origin = {k: meta.get(k) for k in (
            "source_repo", "path", "ref", "blob_sha", "retrieved_at",
            "retrieved_via", "pat_api_status", "bytes") if meta.get(k) is not None}
    return {
        "source": "local-vendored" if canonical else "local-fallback",
        "repo": STANDARD_REPO,
        "path": str(path) if path else None,
        "sha256": sha256_bytes(text) if text else None,
        "bytes": len(text.encode("utf-8")),
        "domains": [dict(d) for d in DOMAINS],
        "origin": origin,
        "note": ("Verbatim abgerufener zentraler Standard; Provenance im Begleit-JSON."
                 if canonical else
                 "Lokale Arbeitsfassung; der zentrale Standard war nicht abrufbar."),
    }


def resolve_standard(client, state_dir, root=None, refresh=False, max_age=86400):
    cache_path = Path(state_dir) / "standard.json"
    cached = read_json(cache_path)
    local = load_local_standard(root)
    if cached and not refresh:
        # A local fallback cache must follow edits to the local standard file.
        same_source = (cached.get("source") == "remote"
                       or cached.get("sha256") == local["sha256"])
        try:
            age = time.time() - float(cached.get("fetched_epoch", 0))
        except (TypeError, ValueError):
            age = max_age + 1
        if same_source and age < max_age:
            return cached
    result = {
        "version": 1,
        "fetched_at": utcnow(),
        "fetched_epoch": time.time(),
        "repo": STANDARD_REPO,
        "source": local["source"],
        "remote": {"status": None, "attempts": []},
        "document": None,
        "local": local,
        "domains": [dict(d) for d in DOMAINS],
    }
    if client is not None:
        try:
            meta = client.get(f"/repos/{STANDARD_REPO}")
            result["remote"]["status"] = meta.status
            result["remote"]["default_branch"] = (meta.json() or {}).get("default_branch")
        except APIError as exc:
            result["remote"]["status"] = exc.status
            result["remote"]["error"] = str(exc)[:300]
        if result["remote"]["status"] == 200:
            for path in STANDARD_PATHS:
                try:
                    resp = client.get(f"/repos/{STANDARD_REPO}/contents/{path}",
                                      accept="application/vnd.github.raw")
                    text = resp.text()
                    result["remote"]["attempts"].append({"path": path, "status": resp.status})
                    result["source"] = "remote"
                    result["path"] = path
                    result["sha256"] = sha256_bytes(text)
                    result["document"] = text[:200000]
                    break
                except APIError as exc:
                    result["remote"]["attempts"].append({"path": path, "status": exc.status})
        else:
            result["remote"]["attempts"].append(
                {"path": None, "status": result["remote"]["status"]})
    if result["source"] != "remote":
        result["source"] = local["source"]
        result["sha256"] = local["sha256"]
        result["path"] = local["path"]
        result["origin"] = local.get("origin") or {}
    write_json(cache_path, result)
    return result


# --------------------------------------------------------------------------
# Brief detection and validation
# --------------------------------------------------------------------------
def _infer_paths(task):
    found = []
    for match in PATH_RE.findall(task):
        if "://" not in match and match not in found:
            found.append(match)
    return found[:20]


def _title(task):
    line = re.split(r"[\n.!?]", task.strip(), maxsplit=1)[0].strip()
    line = re.sub(r"^(please\s+|bitte\s+)", "", line, flags=re.I)
    line = line[:1].upper() + line[1:] if line else "Copilot-Teilaufgabe"
    return line[:72]


def _default_test_commands(paths):
    if any(p.endswith((".js", ".jsx", ".ts", ".tsx")) for p in paths):
        return ["npm test --silent"]
    return ["python3 -m unittest discover -s tests"]


def detect_brief(task, repo=DEFAULT_REPO, base_ref="main", paths=None, test_commands=None):
    task = (task or "").strip()
    if not task:
        raise CopilotError("task text is required")
    split_repo(repo)
    explicit_paths = [norm_path(p) for p in (paths or [])]
    inferred = explicit_paths or [p for p in _infer_paths(task) if p not in FORBIDDEN_PATH_PREFIXES]
    reasons = []
    score = 0
    if DELIVERABLE_RE.search(task):
        score += 1
        reasons.append("enthaelt ein abgegrenztes Lieferobjekt (Verb)")
    else:
        reasons.append("kein abgegrenztes Lieferobjekt erkannt")
    if len(explicit_paths) > 0 or inferred:
        score += 1
        reasons.append("Dateipfad oder Modul genannt")
    elif BOUNDED_RE.search(task):
        score += 1
        reasons.append("begrenzte Einheit (Datei/Funktion/Test) genannt")
    else:
        reasons.append("keine begrenzte Einheit genannt")
    if ACCEPTANCE_RE.search(task):
        score += 1
        reasons.append("Abnahmekriterium/Test genannt")
    else:
        reasons.append("kein Abnahmekriterium genannt")
    if len(task) <= 800:
        score += 1
        reasons.append("Aufgabentext kompakt")
    else:
        reasons.append("Aufgabentext zu gross fuer eine Delegation")
    if BROAD_RE.search(task):
        score -= 2
        reasons.append("breite/architekturweite Formulierung")
    forbidden = []
    for pattern, label in FORBIDDEN_SCOPE_PATTERNS:
        if re.search(pattern, task, re.I):
            forbidden.append(label)
    if forbidden:
        reasons.append("verbotener Scope: " + ", ".join(sorted(set(forbidden))))
    eligible = score >= 3 and not forbidden
    if not eligible and not forbidden and score < 3:
        reasons.append("Score zu niedrig; Freebuff arbeitet selbst weiter")

    acceptance = [
        "Bestehende Tests bleiben gruen; neue oder geaenderte Tests decken die Aenderung ab.",
        "Der Diff bleibt innerhalb der erlaubten Pfade und ist minimal.",
        "Keine Secrets, keine Deployments, keine Live-Transaktionen, kein Auto-Merge.",
    ]
    if test_commands:
        commands = [str(c).strip() for c in test_commands if str(c).strip()]
    else:
        commands = _default_test_commands(inferred)
    brief = {
        "brief_version": 1,
        "id": f"brief-{stamp()}-{os.urandom(3).hex()}",
        "created_at": utcnow(),
        "title": _title(task),
        "objective": task,
        "repo": repo,
        "base_ref": base_ref or "main",
        "allowed_paths": inferred,
        "forbidden_paths": list(FORBIDDEN_PATH_PREFIXES),
        "acceptance": acceptance,
        "test_commands": commands,
        "constraints": [
            "Kein Merge, kein Auto-Merge, kein Deployment oder Publish.",
            "Keine Secrets, Tokens, Zugangsdaten oder Live-Transaktionen.",
            "Keine Aenderungen an Workflows, Repo-Einstellungen oder Infrastruktur.",
            "Bei Blockade exakt berichten; keinen Erfolg erfinden.",
        ],
        "domains": [d["id"] for d in DOMAINS],
        "eligibility": {
            "eligible": eligible,
            "score": score,
            "reasons": reasons,
            "forbidden_scope": sorted(set(forbidden)),
        },
    }
    return brief


def build_prompt(brief):
    paths = "\n".join(f"- `{p}`" for p in brief.get("allowed_paths") or []) or "- (kein Allowlist-Pfad; minimaler Diff)"
    tests = "\n".join(f"- `{c}`" for c in brief.get("test_commands") or []) or "- keine Vorgabe"
    acceptance = "\n".join(f"- {a}" for a in brief.get("acceptance") or [])
    constraints = "\n".join(f"- {c}" for c in brief.get("constraints") or [])
    prompt = f"""# Delegierte Teilaufgabe: {brief['title']}

## Ziel
{brief['objective']}

## Repository und Basis
- Repository: `{brief['repo']}`
- Basis-Branch: `{brief['base_ref']}`
- Erlaubte Pfade:
{paths}

## Abnahmekriterien
{acceptance}

## Tests
{tests}

## Harte Grenzen
{constraints}

## Arbeitsweise
- Lies zuerst die betroffenen Dateien und vorhandenen Tests.
- Aendere nur, was fuer das Ziel und die Abnahmekriterien noetig ist.
- Fuehre die genannten Tests aus und berichte echte Ergebnisse.
- Wenn du blockiert bist, kommentiere den exakten Blocker; erfinde keinen Erfolg.
- Oeffne einen Draft-PR gegen `{brief['base_ref']}` und markiere ihn erst nach
  bestandenen Tests als bereit zum Review.
"""
    return prompt[:12000]


def validate_brief(brief):
    errors = []
    if not isinstance(brief, dict):
        return ["brief must be an object"]
    for key in ("title", "objective", "repo", "base_ref"):
        if not isinstance(brief.get(key), str) or not brief[key].strip():
            errors.append(f"missing {key}")
    if len(str(brief.get("title", ""))) > 100:
        errors.append("title too long")
    if len(str(brief.get("objective", ""))) > 4000:
        errors.append("objective too long")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", str(brief.get("repo", ""))):
        errors.append("invalid repo")
    try:
        split_repo(str(brief.get("repo", "")))
    except CopilotError as exc:
        errors.append(str(exc))
    if not re.fullmatch(r"[A-Za-z0-9._/-]{1,120}", str(brief.get("base_ref", ""))):
        errors.append("invalid base_ref")
    for key in ("allowed_paths", "forbidden_paths", "acceptance", "test_commands",
                "constraints", "domains"):
        if key in brief and not isinstance(brief[key], list):
            errors.append(f"{key} must be a list")
    for path in brief.get("allowed_paths") or []:
        try:
            norm_path(path)
        except CopilotError as exc:
            errors.append(str(exc))
    blob = canonical(brief)
    for pattern in SECRET_PATTERNS:
        if pattern.search(blob):
            errors.append("brief contains a secret-like value")
            break
    return errors


def brief_sha(brief):
    # id/created_at are per-call metadata; the delegation contract is the rest.
    stable = {k: v for k, v in brief.items() if k not in ("id", "created_at")}
    return sha256_bytes(canonical(stable))


def build_issue_body(brief):
    return (
        build_prompt(brief)
        + "\n\n---\n"
        + "Delegiert durch den Freebuff-Orchestrator (`bin/copilot-delegate`). "
          "Der Agent darf nicht mergen, deployen oder veroeffentlichen. "
          "Review und Merge bleiben beim Menschen.\n"
    )


# --------------------------------------------------------------------------
# Preflight
# --------------------------------------------------------------------------
QUERY_ACTORS = """
query($owner:String!, $name:String!) {
  repository(owner:$owner, name:$name) {
    suggestedActors(capabilities:[CAN_BE_ASSIGNED], first:50) {
      nodes { login __typename ... on Bot { id } ... on User { id } }
    }
  }
}
"""

MUTATION_ASSIGN = """
mutation($assignableId:ID!, $actorIds:[ID!]!) {
  replaceActorsForAssignable(input:{assignableId:$assignableId, actorIds:$actorIds}) {
    assignable { ... on Issue { id number url } }
  }
}
"""


def _attempt(client, method, path, **kwargs):
    try:
        resp = client.request(method, path, **kwargs)
        return {"http": resp.status, "ok": 200 <= resp.status < 300, "data": resp.json()}
    except APIError as exc:
        return {"http": exc.status, "ok": False, "error": _redact(str(exc))[:300]}


def preflight(client, repo=DEFAULT_REPO, state_dir=None, root=None, standard=None,
              refresh_standard=False, simulated=False, write=True):
    owner, name = split_repo(repo)
    state = ensure_state(state_dir or (Path(root or repo_root()) / ".copilot"))
    checks = []

    auth = _attempt(client, "GET", "/user")
    login = (auth.get("data") or {}).get("login")
    checks.append({"name": "auth", "ok": auth["ok"], "http": auth["http"],
                   "detail": f"login={login}" if login else auth.get("error", "")})

    rate = _attempt(client, "GET", "/rate_limit")
    checks.append({"name": "rate_limit", "ok": rate["ok"], "http": rate["http"],
                   "detail": "read-only"})

    repo_resp = _attempt(client, "GET", f"/repos/{repo}")
    repo_info = repo_resp.get("data") or {}
    permissions = repo_info.get("permissions") or {}
    checks.append({"name": "repository", "ok": repo_resp["ok"], "http": repo_resp["http"],
                   "detail": f"private={repo_info.get('private')} "
                             f"issues={repo_info.get('has_issues')}"})

    actors = {}
    try:
        data = client.graphql(QUERY_ACTORS, {"owner": owner, "name": name})
        nodes = (((data.get("repository") or {}).get("suggestedActors") or {}).get("nodes") or [])
        actors = next((n for n in nodes if str(n.get("login", "")).startswith(BOT_LOGIN)), {})
        checks.append({"name": "copilot_actor", "ok": bool(actors), "http": 200,
                       "detail": actors.get("login") or "not offered"})
    except APIError as exc:
        checks.append({"name": "copilot_actor", "ok": False, "http": exc.status,
                       "detail": _redact(str(exc))[:300]})

    issues = _attempt(client, "GET", f"/repos/{repo}/issues?state=all&per_page=1")
    checks.append({"name": "issues_api", "ok": issues["ok"], "http": issues["http"],
                   "detail": "read" if issues["ok"] else issues.get("error", "")})

    agents_user = _attempt(client, "GET", "/agents/tasks?per_page=1")
    checks.append({"name": "agent_tasks_user", "ok": agents_user["ok"],
                   "http": agents_user["http"], "detail": "read" if agents_user["ok"] else "denied"})

    agents_repo = _attempt(client, "GET", f"/agents/repos/{repo}/tasks?per_page=1")
    checks.append({"name": "agent_tasks_repo", "ok": agents_repo["ok"],
                   "http": agents_repo["http"],
                   "detail": "read" if agents_repo["ok"] else agents_repo.get("error", "")})

    if standard is None:
        standard = resolve_standard(client, state, root=root, refresh=refresh_standard)

    policy = load_policy(state)
    issue_reasons = []
    if not repo_info.get("has_issues"):
        issue_reasons.append("repository has issues disabled")
    if not issues["ok"]:
        issue_reasons.append(f"issues API status {issues['http']}")
    if not actors:
        issue_reasons.append("copilot-swe-agent is not assignable")
    agent_reasons = []
    if not agents_repo["ok"]:
        agent_reasons.append(f"agent tasks repo status {agents_repo['http']}")
    if not agents_user["ok"]:
        agent_reasons.append(f"agent tasks user status {agents_user['http']}")

    paid_open = bool(policy.get("paid_delegation_allowed")) and not bool(
        policy.get("credits_exhausted"))
    routes = {
        "issue": {
            "available": not issue_reasons,
            "reasons": issue_reasons,
            "endpoints": [
                f"POST /repos/{repo}/issues",
                "GraphQL replaceActorsForAssignable",
            ],
        },
        "agent-task": {
            "available": not agent_reasons,
            "reasons": agent_reasons,
            "endpoints": [f"POST /agents/repos/{repo}/tasks"],
        },
    }
    blockers = []
    if standard.get("remote", {}).get("status") not in (None, 200):
        if standard.get("source") == "local-vendored":
            blockers.append(
                f"PAT cannot read {STANDARD_REPO} "
                f"({standard.get('remote', {}).get('status')}); vendored standard "
                f"sha={str(standard.get('sha256'))[:12]} in use")
        else:
            blockers.append(
                f"standard source {STANDARD_REPO} returned "
                f"{standard.get('remote', {}).get('status')}; local fallback in use")
    if not routes["issue"]["available"]:
        blockers.append("issue route: " + "; ".join(issue_reasons))
    if not routes["agent-task"]["available"]:
        blockers.append("agent-task route: " + "; ".join(agent_reasons))
    if policy.get("credits_exhausted"):
        blockers.append("copilot credits marked exhausted in policy")
    if not policy.get("paid_delegation_allowed"):
        blockers.append("paid delegation gate closed in policy")

    result = {
        "version": 1,
        "checked_at": utcnow(),
        "simulated": bool(simulated),
        "repo": repo,
        "login": login,
        "token_source": client.token_source,
        "checks": checks,
        "repository": {
            "default_branch": repo_info.get("default_branch"),
            "private": repo_info.get("private"),
            "has_issues": repo_info.get("has_issues"),
            "permissions": permissions,
        },
        "copilot": {
            "bot_login": actors.get("login"),
            "bot_id": actors.get("id"),
            "offered": bool(actors),
            "agent_tasks_user_read": agents_user["ok"],
            "agent_tasks_repo_read": agents_repo["ok"],
        },
        "routes": routes,
        "policy": policy,
        "paid_gate": {
            "open": paid_open,
            "paid_delegation_allowed": bool(policy.get("paid_delegation_allowed")),
            "credits_exhausted": bool(policy.get("credits_exhausted")),
            "requires_flag": "--allow-paid",
        },
        "standard": {
            "source": standard.get("source"),
            "remote_status": standard.get("remote", {}).get("status"),
            "sha256": standard.get("sha256"),
            "path": standard.get("path"),
            "origin": standard.get("origin") or {},
            "domains": [d["id"] for d in standard.get("domains") or DOMAINS],
        },
        "ready_for_free_checks": auth["ok"] and repo_resp["ok"],
        "ready_to_delegate": paid_open and any(r["available"] for r in routes.values()),
        "blockers": blockers,
    }
    if write:
        path = state / "receipts" / f"preflight-{stamp()}.json"
        write_json(path, result)
        result["receipt"] = str(path)
    return result


# --------------------------------------------------------------------------
# Delegation
# --------------------------------------------------------------------------
def delegation_dir(state_dir):
    return Path(state_dir) / "delegations"


def review_dir(state_dir):
    return Path(state_dir) / "reviews"


def load_delegation(state_dir, ident):
    if not re.fullmatch(r"d-[A-Za-z0-9-]+", str(ident)):
        raise CopilotError("invalid delegation id")
    data = read_json(delegation_dir(state_dir) / f"{ident}.json")
    if not isinstance(data, dict):
        raise CopilotError(f"delegation not found: {ident}")
    return data


def save_delegation(state_dir, record):
    record["updated_at"] = utcnow()
    write_json(delegation_dir(state_dir) / f"{record['id']}.json", record)
    return record


def append_history(record, state, detail=""):
    record["state"] = state
    record.setdefault("history", []).append({
        "at": utcnow(),
        "state": state,
        "detail": _redact(detail)[:500],
    })
    record["history"] = record["history"][-120:]


def _terminal(record):
    return record.get("state") in TERMINAL_STATES


def _find_duplicate(state_dir, repo, brief_hash, simulated):
    for path in sorted(delegation_dir(state_dir).glob("d-*.json")):
        rec = read_json(path)
        if not isinstance(rec, dict):
            continue
        if rec.get("repo") != repo or rec.get("brief_sha256") != brief_hash:
            continue
        if bool(rec.get("simulated")) != bool(simulated):
            continue
        if not _terminal(rec):
            return rec
    return None


def _planned_requests(brief, route):
    prompt = build_prompt(brief)
    repo = brief["repo"]
    if route == "agent-task":
        return [{
            "method": "POST",
            "path": f"/agents/repos/{repo}/tasks",
            "body": {"prompt": prompt[:400] + "...", "base_ref": brief["base_ref"],
                     "create_pull_request": True},
        }]
    return [
        {
            "method": "POST",
            "path": f"/repos/{repo}/issues",
            "body": {"title": brief["title"], "body": build_issue_body(brief)[:400] + "..."},
        },
        {
            "method": "POST",
            "path": "/graphql",
            "body": {"query": "replaceActorsForAssignable(...)",
                     "variables": {"actorIds": ["<copilot bot id>"]}},
        },
    ]


def create_delegation(client, brief, state_dir, route="auto", execute=False,
                      allow_paid=False, simulated=False, root=None):
    state = ensure_state(state_dir or (Path(root or repo_root()) / ".copilot"))
    errors = validate_brief(brief)
    if errors:
        raise CopilotError("invalid brief: " + "; ".join(errors))
    repo = brief["repo"]
    bhash = brief_sha(brief)
    requested_route = route
    if route == "auto" and (not execute or simulated):
        route = "issue"

    if not execute:
        return {
            "status": "DRY_RUN",
            "simulated": bool(simulated),
            "repo": repo,
            "route": route,
            "brief_sha256": bhash,
            "brief": brief,
            "planned_requests": _planned_requests(brief, route),
            "note": "No write request was sent. Add --execute and open the paid gate.",
        }

    duplicate = _find_duplicate(state, repo, bhash, simulated)
    if duplicate:
        duplicate["duplicate_of"] = duplicate["id"]
        return duplicate

    policy = load_policy(state)
    gate_open = bool(policy.get("paid_delegation_allowed")) and not bool(
        policy.get("credits_exhausted"))
    if not simulated and (not gate_open or not allow_paid):
        record = {
            "id": f"d-{stamp()}-{bhash[:8]}",
            "created_at": utcnow(),
            "updated_at": utcnow(),
            "simulated": False,
            "repo": repo,
            "route": route,
            "brief": brief,
            "brief_sha256": bhash,
            "state": "BLOCKED_PAID_GATE",
            "history": [],
            "policy": policy,
            "remote": {},
        }
        reasons = []
        if not policy.get("paid_delegation_allowed"):
            reasons.append("policy paid_delegation_allowed=false")
        if policy.get("credits_exhausted"):
            reasons.append("policy credits_exhausted=true")
        if not allow_paid:
            reasons.append("--allow-paid missing")
        append_history(record, "BLOCKED_PAID_GATE", "; ".join(reasons))
        save_delegation(state, record)
        record["blocked_reasons"] = reasons
        return record

    if not simulated:
        pf = preflight(client, repo, state_dir=state, root=root, simulated=False)
        if requested_route == "auto":
            if pf["routes"]["issue"]["available"]:
                route = "issue"
            elif pf["routes"]["agent-task"]["available"]:
                route = "agent-task"
            else:
                route = "issue"
        chosen = pf["routes"].get(route) or {}
        if not chosen.get("available"):
            record = {
                "id": f"d-{stamp()}-{bhash[:8]}",
                "created_at": utcnow(),
                "updated_at": utcnow(),
                "simulated": False,
                "repo": repo,
                "route": route,
                "brief": brief,
                "brief_sha256": bhash,
                "state": "BLOCKED_ROUTE",
                "history": [],
                "policy": policy,
                "remote": {},
                "preflight": pf.get("receipt"),
            }
            append_history(record, "BLOCKED_ROUTE", "; ".join(chosen.get("reasons") or []))
            save_delegation(state, record)
            record["blocked_reasons"] = chosen.get("reasons") or []
            return record
        bot_id = (pf.get("copilot") or {}).get("bot_id")
    else:
        bot_id = "BOT_SIMULATED"
        pf = {"simulated": True}

    record = {
        "id": f"d-{stamp()}-{bhash[:8]}",
        "created_at": utcnow(),
        "updated_at": utcnow(),
        "simulated": bool(simulated),
        "repo": repo,
        "route": route,
        "brief": brief,
        "brief_sha256": bhash,
        "state": "PLANNED",
        "history": [],
        "policy": policy,
        "remote": {"bot_id": bot_id},
        "preflight": pf.get("receipt") if isinstance(pf, dict) else None,
        "observed_activity": False,
        "branches": [],
        "pull_request": None,
        "ci": None,
    }
    append_history(record, "PLANNED", f"route={route} brief={bhash[:12]}")
    save_delegation(state, record)

    try:
        if route == "agent-task":
            _delegate_agent_task(client, record, state)
        elif route == "issue":
            _delegate_issue(client, record, state, bot_id)
        else:
            raise CopilotError(f"unknown route: {route}")
    except APIError as exc:
        append_history(record, "FAILED", f"delegation request failed: {exc}")
        record["error"] = _redact(str(exc))[:500]
        save_delegation(state, record)
        return record
    return record


def _delegate_issue(client, record, state, bot_id):
    brief = record["brief"]
    repo = record["repo"]
    issue = client.post(f"/repos/{repo}/issues",
                        {"title": brief["title"], "body": build_issue_body(brief)}).json() or {}
    number = issue.get("number")
    node_id = issue.get("node_id")
    record["remote"].update({
        "issue_number": number,
        "issue_node_id": node_id,
        "issue_url": issue.get("html_url"),
    })
    if not number or not node_id:
        append_history(record, "FAILED", "issue response missing number/node_id")
        save_delegation(state, record)
        return
    append_history(record, "ISSUE_CREATED", f"issue #{number}")
    if not bot_id:
        append_history(record, "FAILED", "copilot bot id unavailable")
        save_delegation(state, record)
        return
    try:
        data = client.graphql(MUTATION_ASSIGN, {
            "assignableId": node_id,
            "actorIds": [bot_id],
        })
        assigned = ((data.get("replaceActorsForAssignable") or {}).get("assignable") or {})
        record["remote"]["assigned"] = bool(assigned)
        append_history(record, "DELEGATED", f"issue #{number} assigned to copilot")
    except APIError as exc:
        record["remote"]["assigned"] = False
        append_history(record, "FAILED", f"assignment failed: {exc}")
    save_delegation(state, record)


def _delegate_agent_task(client, record, state):
    brief = record["brief"]
    repo = record["repo"]
    body = {
        "prompt": build_prompt(brief),
        "base_ref": brief["base_ref"],
        "create_pull_request": True,
    }
    task = client.post(f"/agents/repos/{repo}/tasks", body).json() or {}
    record["remote"].update({
        "task_id": task.get("id"),
        "task_url": task.get("html_url"),
        "task_state": task.get("state"),
    })
    if not task.get("id"):
        append_history(record, "FAILED", "agent task response missing id")
    else:
        append_history(record, "DELEGATED", f"agent task {task.get('id')} state={task.get('state')}")
    save_delegation(state, record)


# --------------------------------------------------------------------------
# Watch
# --------------------------------------------------------------------------
def _bot_login(login):
    return str(login or "").lower() in (BOT_LOGIN, BOT_FULL, "app/copilot-swe-agent")


def _timeline(client, repo, number):
    resp = client.get(f"/repos/{repo}/issues/{number}/timeline?per_page=100")
    return resp.json() or []


def _comments(client, repo, number):
    try:
        return client.get(f"/repos/{repo}/issues/{number}/comments?per_page=100").json() or []
    except APIError:
        return []


def _extract_issue_pr(events):
    for event in events:
        if event.get("event") in ("cross-referenced", "connected"):
            source = event.get("source") or {}
            issue = source.get("issue") or {}
            if issue.get("pull_request"):
                return issue.get("number"), issue.get("html_url")
    return None, None


def fetch_ci(client, repo, sha):
    result = {"sha": sha, "conclusion": "none", "checks": [], "status_state": None}
    try:
        data = client.get(f"/repos/{repo}/commits/{sha}/check-runs?per_page=100").json() or {}
        runs = data.get("check_runs") or []
        result["total"] = data.get("total_count", len(runs))
        for run in runs[:100]:
            result["checks"].append({
                "name": run.get("name"),
                "status": run.get("status"),
                "conclusion": run.get("conclusion"),
                "details_url": run.get("details_url") or run.get("html_url"),
            })
        if runs:
            conclusions = [r.get("conclusion") for r in runs]
            if any(c in ("failure", "timed_out", "cancelled", "action_required",
                         "stale") for c in conclusions):
                result["conclusion"] = "failure"
            elif any(c is None for c in conclusions) or any(
                    r.get("status") != "completed" for r in runs):
                result["conclusion"] = "pending"
            else:
                result["conclusion"] = "success"
    except APIError as exc:
        result["error"] = _redact(str(exc))[:300]
    try:
        status = client.get(f"/repos/{repo}/commits/{sha}/status").json() or {}
        result["status_state"] = status.get("state")
        if result["conclusion"] != "failure" and status.get("state") == "failure":
            result["conclusion"] = "failure"
        if result["conclusion"] == "none" and status.get("state") == "success":
            result["conclusion"] = "success"
    except APIError:
        pass
    result["evidence_sha256"] = sha256_bytes(canonical(result))
    return result


def _apply_pr(client, record, number):
    repo = record["repo"]
    pr = client.get(f"/repos/{repo}/pulls/{number}").json() or {}
    head = pr.get("head") or {}
    base = pr.get("base") or {}
    user = (pr.get("user") or {}).get("login")
    branches = record.setdefault("branches", [])
    if head.get("ref") and head["ref"] not in branches:
        branches.append(head["ref"])
    record["pull_request"] = {
        "number": pr.get("number", number),
        "html_url": pr.get("html_url"),
        "title": pr.get("title"),
        "state": pr.get("state"),
        "draft": pr.get("draft"),
        "merged": pr.get("merged"),
        "mergeable_state": pr.get("mergeable_state"),
        "head_ref": head.get("ref"),
        "head_sha": head.get("sha"),
        "base_ref": base.get("ref"),
        "author": user,
        "changed_files": pr.get("changed_files"),
        "additions": pr.get("additions"),
        "deletions": pr.get("deletions"),
    }
    sha = head.get("sha")
    if not sha:
        append_history(record, "FAILED", "pull request has no head SHA")
        return
    ci = fetch_ci(client, repo, sha)
    record["ci"] = ci
    if ci["conclusion"] == "failure":
        append_history(record, "CI_FAILED", f"PR #{number} sha={sha[:12]}")
    elif ci["conclusion"] == "pending":
        append_history(record, "CI_PENDING", f"PR #{number} sha={sha[:12]}")
    elif pr.get("draft"):
        append_history(record, "PR_OPENED", f"draft PR #{number}")
    elif ci["conclusion"] == "success":
        append_history(record, "COMPLETED", f"PR #{number} checks passed sha={sha[:12]}")
    else:
        append_history(record, "COMPLETED_UNVERIFIED",
                       f"PR #{number} ready but no CI evidence")


def _poll_issue(client, record):
    repo = record["repo"]
    number = (record.get("remote") or {}).get("issue_number")
    if not number:
        append_history(record, "FAILED", "no issue number recorded")
        return
    issue = client.get(f"/repos/{repo}/issues/{number}").json() or {}
    events = _timeline(client, repo, number)
    activity = any(e.get("event") == "copilot_work_started" for e in events)
    assigned = any(_bot_login((e.get("assignee") or {}).get("login"))
                   for e in events if e.get("event") == "assigned")
    pr_number, pr_url = _extract_issue_pr(events)
    comments = _comments(client, repo, number) if not pr_number else []
    bodies = [c.get("body") or "" for c in comments
              if _bot_login((c.get("user") or {}).get("login"))]
    bodies += [e.get("body") or "" for e in events if e.get("event") == "issue_comment"]
    quota = next((b for b in bodies if CREDIT_RE.search(b)), None)
    record["observed_activity"] = bool(activity or pr_number)
    record["remote"]["assigned"] = bool(record["remote"].get("assigned") or assigned)
    record["remote"]["issue_state"] = issue.get("state")
    record["remote"]["pr_number"] = pr_number
    if pr_url:
        record["remote"]["pr_url"] = pr_url
    if quota:
        append_history(record, "QUOTA_BLOCKED", quota[:300])
        return
    if pr_number:
        _apply_pr(client, record, pr_number)
        return
    if issue.get("state") == "closed":
        append_history(record, "FAILED", "issue closed without a pull request")
        return
    if activity or assigned:
        append_history(record, "IN_PROGRESS",
                       "copilot started" if activity else "assigned, no work event yet")
    else:
        append_history(record, "DELEGATED", "waiting for Copilot activity")


def _task_number(client, record, task):
    repo = record["repo"]
    for artifact in task.get("artifacts") or []:
        if artifact.get("type") != "pull":
            continue
        data = artifact.get("data") or {}
        if data.get("number"):
            return data["number"]
        url = data.get("html_url") or ""
        match = re.search(r"/pull/(\d+)", url)
        if match:
            return int(match.group(1))
        if data.get("id"):
            try:
                pulls = client.get(f"/repos/{repo}/pulls?state=all&per_page=100").json() or []
                for pr in pulls:
                    if pr.get("id") == data["id"]:
                        return pr.get("number")
            except APIError:
                pass
    sessions = task.get("sessions") or []
    for session in sessions:
        head_ref = session.get("head_ref")
        if head_ref:
            try:
                pulls = client.get(
                    f"/repos/{repo}/pulls?state=all&head={urllib.parse.quote(repo.split('/')[0])}:"
                    f"{urllib.parse.quote(head_ref)}").json() or []
                if pulls:
                    return pulls[0].get("number")
            except APIError:
                pass
    return None


def _poll_agent_task(client, record):
    task_id = (record.get("remote") or {}).get("task_id")
    if not task_id:
        append_history(record, "FAILED", "no agent task id recorded")
        return
    task = client.get(f"/agents/tasks/{task_id}").json() or {}
    state = task.get("state")
    record["remote"]["task_state"] = state
    for artifact in task.get("artifacts") or []:
        if artifact.get("type") == "branch":
            data = artifact.get("data") or {}
            ref = data.get("head_ref") or data.get("name")
            branches = record.setdefault("branches", [])
            if ref and ref not in branches:
                branches.append(ref)
    sessions = task.get("sessions") or []
    errors = [s.get("error", {}).get("message") for s in sessions
              if isinstance(s.get("error"), dict) and s["error"].get("message")]
    error = task.get("error", {}).get("message") if isinstance(task.get("error"), dict) else None
    error = error or (errors[-1] if errors else None)
    usage = [s.get("usage") for s in sessions if s.get("usage")]
    if usage:
        record["remote"]["usage"] = usage[-1]
    if error:
        record["remote"]["error"] = _redact(str(error))[:500]
    record["observed_activity"] = state in ("in_progress", "completed", "waiting_for_user")
    if state in ("queued",):
        append_history(record, "QUEUED", f"task {task_id}")
    elif state in ("in_progress",):
        append_history(record, "IN_PROGRESS", f"task {task_id}")
    elif state in ("waiting_for_user", "idle"):
        append_history(record, "WAITING_FOR_USER", f"task {task_id}")
    elif state in ("timed_out",):
        append_history(record, "TIMED_OUT", f"task {task_id}")
    elif state in ("cancelled",):
        append_history(record, "CANCELLED", f"task {task_id}")
    elif state == "failed":
        if error and CREDIT_RE.search(error):
            append_history(record, "QUOTA_BLOCKED", error[:300])
        else:
            append_history(record, "FAILED", str(error or "task failed")[:300])
    elif state == "completed":
        number = _task_number(client, record, task)
        if number:
            _apply_pr(client, record, number)
        else:
            append_history(record, "COMPLETED_UNVERIFIED",
                           "task completed without a pull request artifact")
    else:
        append_history(record, "IN_PROGRESS", f"unknown task state {state}")
    _ = usage


def poll_delegation(client, record):
    if _terminal(record):
        return record
    if record.get("route") == "agent-task":
        _poll_agent_task(client, record)
    else:
        _poll_issue(client, record)
    return record


def watch(client, record, state_dir, follow=True, interval=10.0, max_polls=30):
    state = ensure_state(state_dir)
    polls = max(1, int(max_polls)) if follow else 1
    for index in range(polls):
        try:
            poll_delegation(client, record)
        except APIError as exc:
            record["last_error"] = _redact(str(exc))[:500]
            append_history(record, "WATCH_ERROR", str(exc))
        save_delegation(state, record)
        if _terminal(record):
            break
        if index + 1 < polls:
            if interval > 0:
                time.sleep(min(float(interval), 60.0))
    if not _terminal(record) and follow:
        append_history(record, "WATCH_LIMIT_REACHED",
                       f"no terminal state after {polls} polls")
        save_delegation(state, record)
    return record


# --------------------------------------------------------------------------
# Independent review
# --------------------------------------------------------------------------
def _secret_hits(files):
    hits = []
    for row in files:
        patch = row.get("patch") or ""
        for line in patch.splitlines():
            if not line.startswith("+") or line.startswith("+++"):
                continue
            text = line[1:]
            if re.search(r"(?i)(example|dummy|redacted|placeholder|<[^>]+>|\*\*\*)", text):
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    hits.append({"path": row.get("filename"), "pattern": pattern.pattern[:40]})
                    break
    return hits


def _git_binary():
    found = shutil.which("git")
    if found:
        return found
    bundled = Path("/opt/Freebuff/resources/git/bin/git")
    return str(bundled) if bundled.is_file() else None


def resolve_test_profile(profile, custom_path=None):
    if profile in (None, "none"):
        return None
    if profile == "python-unittest":
        return {"argv": [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                "timeout": 300}
    if profile == "python-pytest":
        return {"argv": [sys.executable, "-m", "pytest", "-q"], "timeout": 300}
    if profile == "node-test":
        return {"argv": ["npm", "test", "--silent"], "timeout": 300}
    if profile == "custom":
        data = read_json(custom_path)
        if not isinstance(data, dict) or not isinstance(data.get("argv"), list):
            raise CopilotError("custom test profile needs {'argv': [...]}")
        argv = [str(x) for x in data["argv"]]
        if not argv or not all(argv):
            raise CopilotError("custom test profile argv is empty")
        return {"argv": argv, "timeout": int(data.get("timeout", 300))}
    raise CopilotError(f"unknown test profile: {profile}")


def run_local_tests(repo_path, diff_text, profile):
    repo_path = Path(repo_path).resolve()
    if not (repo_path / ".git").exists():
        return {"status": "SKIP", "detail": "not a git repository"}
    git = _git_binary()
    if not git:
        return {"status": "SKIP", "detail": "git not available"}
    tmp = Path(tempfile.mkdtemp(prefix="copilot-review-"))
    worktree = tmp / "wt"
    try:
        subprocess.run([git, "-C", str(repo_path), "worktree", "add", "--detach",
                        str(worktree), "HEAD"], check=True, capture_output=True, timeout=60)
        check = subprocess.run([git, "-C", str(worktree), "apply", "--check", "-"],
                               input=diff_text.encode("utf-8"), capture_output=True, timeout=60)
        if check.returncode != 0:
            return {"status": "FAIL", "detail": "diff does not apply: "
                    + tail(check.stderr.decode("utf-8", "replace"), 1000)}
        subprocess.run([git, "-C", str(worktree), "apply", "-"],
                       input=diff_text.encode("utf-8"), check=True, capture_output=True,
                       timeout=60)
        proc = subprocess.run(profile["argv"], cwd=worktree, capture_output=True,
                              timeout=profile.get("timeout", 300), start_new_session=True)
        out = tail((proc.stdout or b"").decode("utf-8", "replace")
                   + (proc.stderr or b"").decode("utf-8", "replace"), 4000)
        return {
            "status": "PASS" if proc.returncode == 0 else "FAIL",
            "exit_code": proc.returncode,
            "argv": profile["argv"],
            "output_tail": out,
            "log_sha256": sha256_bytes(out),
        }
    except subprocess.TimeoutExpired:
        return {"status": "FAIL", "detail": "test timeout", "argv": profile["argv"]}
    except subprocess.CalledProcessError as exc:
        return {"status": "FAIL", "detail": tail(str(exc), 1000),
                "argv": profile.get("argv")}
    finally:
        subprocess.run([git, "-C", str(repo_path), "worktree", "remove", "--force",
                        str(worktree)], capture_output=True, timeout=60)
        shutil.rmtree(tmp, ignore_errors=True)


def build_evidence_note(record, result):
    """Compact note in the format of the SFS operating standard (not auto-posted)."""
    verified = (not record.get("simulated")
                and str(result.get("verdict", "")).startswith("VERIFIED"))
    if verified:
        evidence = (f"observed Copilot activity; PR {result.get('html_url')}; "
                    f"head {str(result.get('head_sha'))[:12]}")
        areas = "ai-collaboration, prompting, code-generation-validation"
        practice = "deterministic independent review with CI/secret/scope checks"
    else:
        evidence = ("not verified (simulated mock; excluded from proficiency)"
                    if record.get("simulated") else "not verified by review")
        areas = "none"
        practice = "none"
    tests = f"CI={result.get('ci', {}).get('conclusion')}"
    if result.get("local_tests"):
        tests += f"; local={result['local_tests'].get('status')}"
    return "\n".join([
        f"Copilot evidence: {evidence}",
        f"Skill areas: {areas}",
        f"Advanced/Expert practice: {practice}",
        f"Proof: {result.get('receipt')}; Tests: {tests}",
        "Uncovered: agent-configuration, tool-context-integration "
        "(GitHub API exposes no tool/config invocation evidence)",
        f"Decision: {result.get('verdict')}",
    ])


def review_delegation(client, record, state_dir, local_repo=None, test_profile=None,
                      custom_profile=None):
    state = ensure_state(state_dir)
    repo = record["repo"]
    pr = record.get("pull_request") or {}
    number = pr.get("number")
    if not number:
        result = {
            "delegation_id": record["id"],
            "verdict": "REVIEW_BLOCKED",
            "simulated": bool(record.get("simulated")),
            "checks": [{"name": "pull_request", "status": "FAIL",
                        "detail": "no pull request recorded"}],
            "next_actions": ["Warte auf PR oder delegiere erneut."],
        }
        return result

    fresh = client.get(f"/repos/{repo}/pulls/{number}").json() or {}
    head = fresh.get("head") or {}
    head_sha = head.get("sha") or pr.get("head_sha")
    files = client.paged(f"/repos/{repo}/pulls/{number}/files", "files", max_pages=3)
    diff_resp = client.get(f"/repos/{repo}/pulls/{number}",
                           accept="application/vnd.github.v3.diff")
    diff_text = diff_resp.text()
    ci = fetch_ci(client, repo, head_sha) if head_sha else {"conclusion": "none"}
    brief = record.get("brief") or {}
    checks = []

    recorded_sha = pr.get("head_sha")
    same_sha = bool(head_sha) and bool(recorded_sha) and head_sha == recorded_sha
    checks.append({"name": "head_sha", "status": "PASS" if same_sha else "FAIL",
                   "detail": f"{str(head_sha)[:12]} vs {str(pr.get('head_sha'))[:12]}"})

    author = (fresh.get("user") or {}).get("login")
    checks.append({"name": "copilot_authorship",
                   "status": "PASS" if _bot_login(author) else "FAIL",
                   "detail": f"author={author}"})

    base_ref = (fresh.get("base") or {}).get("ref")
    checks.append({"name": "base_ref",
                   "status": "PASS" if base_ref == brief.get("base_ref") else "FAIL",
                   "detail": f"{base_ref} vs {brief.get('base_ref')}"})

    filenames = [f.get("filename") for f in files if f.get("filename")]
    allowed = brief.get("allowed_paths") or []
    forbidden = tuple(brief.get("forbidden_paths") or FORBIDDEN_PATH_PREFIXES)
    outside = [f for f in filenames if allowed and not any(
        f == a or f.startswith(a.rstrip("/") + "/") for a in allowed)]
    forbidden_hits = [f for f in filenames if any(
        f == p.rstrip("/") or f.startswith(p) for p in forbidden)]
    scope_ok = not outside and not forbidden_hits
    checks.append({"name": "scope", "status": "PASS" if scope_ok else "FAIL",
                   "detail": f"files={len(filenames)} outside={outside[:5]} "
                             f"forbidden={forbidden_hits[:5]}"})

    too_big = len(filenames) > 60 or (fresh.get("additions", 0) or 0) > 5000
    checks.append({"name": "diff_size", "status": "FAIL" if too_big else "PASS",
                   "detail": f"files={len(filenames)} additions={fresh.get('additions')}"})

    secrets = _secret_hits(files)
    checks.append({"name": "secret_scan", "status": "FAIL" if secrets else "PASS",
                   "detail": f"hits={len(secrets)}" if secrets else "no added secrets"})

    ci_status = {"success": "PASS", "failure": "FAIL"}.get(ci.get("conclusion"), "WARN")
    checks.append({"name": "ci", "status": ci_status,
                   "detail": f"conclusion={ci.get('conclusion')} checks={len(ci.get('checks') or [])}"})

    local = None
    profile = resolve_test_profile(test_profile, custom_profile)
    if profile and local_repo:
        local = run_local_tests(local_repo, diff_text, profile)
        checks.append({"name": "local_tests",
                       "status": "PASS" if local["status"] == "PASS" else local["status"],
                       "detail": local.get("detail") or f"exit={local.get('exit_code')}"})
    elif local_repo:
        checks.append({"name": "local_tests", "status": "SKIP",
                       "detail": "no test profile selected"})

    fails = [c for c in checks if c["status"] == "FAIL"]
    ci_ok = ci.get("conclusion") == "success"
    local_ok = bool(local and local.get("status") == "PASS")
    if fails:
        verdict = "CHANGES_REQUIRED"
    elif ci_ok:
        verdict = "VERIFIED"
    elif local_ok:
        verdict = "VERIFIED_LOCAL"
    else:
        verdict = "UNVERIFIED"

    next_actions = []
    if verdict == "CHANGES_REQUIRED":
        names = {c["name"] for c in fails}
        if "ci" in names:
            next_actions.append("CI-Fehler lokal reproduzieren und beheben; Copilot mit "
                                "dem exakten Fehler erneut beauftragen.")
        if "scope" in names:
            next_actions.append("Diff auf die erlaubten Pfade zurueckfuehren; keine "
                                "Workflow-/Infrastruktur-Dateien uebernehmen.")
        if "secret_scan" in names:
            next_actions.append("Fundstelle entfernen und Token rotieren; PR nicht mergen.")
        if "copilot_authorship" in names:
            next_actions.append("PR stammt nicht nachweislich von Copilot; nicht als "
                                "Copilot-Leistung zaehlen.")
        if not next_actions:
            next_actions.append("Befunde beheben und Review wiederholen.")
    else:
        next_actions.append("Mensch entscheidet ueber Merge; kein Auto-Merge.")

    result = {
        "delegation_id": record["id"],
        "simulated": bool(record.get("simulated")),
        "repo": repo,
        "pull_request": number,
        "html_url": fresh.get("html_url"),
        "head_sha": head_sha,
        "diff_sha256": sha256_bytes(diff_text),
        "files": filenames,
        "checks": checks,
        "ci": ci,
        "local_tests": local,
        "verdict": verdict,
        "next_actions": next_actions,
        "reviewed_at": utcnow(),
    }
    receipt = review_dir(state) / f"{record['id']}-{str(head_sha)[:12]}.json"
    write_json(receipt, result)
    result["receipt"] = str(receipt)
    result["evidence_note"] = build_evidence_note(record, result)
    record["review"] = {
        "verdict": verdict,
        "head_sha": head_sha,
        "receipt": str(receipt),
        "receipt_sha256": sha256_bytes(Path(receipt).read_bytes()),
    }
    append_history(record, "REVIEWED" if verdict.startswith("VERIFIED") else "CHANGES_REQUIRED",
                   f"verdict={verdict} head={str(head_sha)[:12]}")
    save_delegation(state, record)
    return result


# --------------------------------------------------------------------------
# Proficiency (evidence only, simulations excluded)
# --------------------------------------------------------------------------
def collect_proficiency(state_dir):
    state = ensure_state(state_dir)
    records = []
    simulated = 0
    for path in sorted(delegation_dir(state).glob("d-*.json")):
        rec = read_json(path)
        if not isinstance(rec, dict):
            continue
        if rec.get("simulated"):
            simulated += 1
            continue
        records.append(rec)

    evidence = {d["id"]: [] for d in DOMAINS}
    verified = []
    for rec in records:
        if rec.get("state") not in SUCCESS_STATES:
            continue
        review = rec.get("review") or {}
        receipt_path = review.get("receipt")
        receipt = read_json(receipt_path) if receipt_path else None
        if not isinstance(receipt, dict):
            continue
        if receipt.get("verdict") not in ("VERIFIED", "VERIFIED_LOCAL"):
            continue
        if receipt.get("head_sha") != review.get("head_sha"):
            continue
        if sha256_bytes(Path(receipt_path).read_bytes()) != review.get("receipt_sha256"):
            continue
        verified.append(rec)
        pr = rec.get("pull_request") or {}
        common = {
            "delegation_id": rec["id"],
            "repo": rec.get("repo"),
            "pull_request": pr.get("html_url"),
            "head_sha": pr.get("head_sha"),
            "review_receipt": review.get("receipt"),
            "review_receipt_sha256": review.get("receipt_sha256"),
        }
        if rec.get("observed_activity") and pr:
            evidence["ai-collaboration"].append({**common, "kind": "observed_agent_pr"})
        if rec.get("brief_sha256") and any(
                c.get("name") == "scope" and c.get("status") == "PASS"
                for c in receipt.get("checks") or []):
            evidence["prompting"].append({**common, "kind": "bounded_brief_scope_pass",
                                          "brief_sha256": rec["brief_sha256"]})
        if receipt.get("ci", {}).get("conclusion") == "success" and pr:
            evidence["code-generation-validation"].append(
                {**common, "kind": "diff_ci_review", "diff_sha256": receipt.get("diff_sha256")})
        config = rec.get("agent_configuration") or {}
        if config.get("observed") and config.get("kind"):
            evidence["agent-configuration"].append({**common, "kind": config["kind"],
                                                    "config_sha256": config.get("sha256")})
        tools = rec.get("tool_context") or {}
        if tools.get("observed") and tools.get("tools"):
            evidence["tool-context-integration"].append(
                {**common, "kind": "tool_invocation", "tools": tools["tools"]})

    domains = {}
    proven = 0
    for domain in DOMAINS:
        rows = evidence[domain["id"]]
        if rows:
            proven += 1
            status = "PROVEN"
            gap = None
        else:
            status = "UNPROVEN"
            gap = {
                "ai-collaboration": "Keine echte, beobachtete Copilot-Delegation mit PR.",
                "prompting": "Kein realer Brief mit bestandenem Scope-Review.",
                "code-generation-validation": "Kein realer Diff mit CI-Nachweis und Review.",
                "agent-configuration": "Kein Nachweis, dass eine Custom-Agent-/Instruktions-"
                                       "Konfiguration tatsaechlich genutzt wurde.",
                "tool-context-integration": "GitHub-API liefert keinen Nachweis ueber "
                                            "tatsaechlich aufgerufene Tools/MCP.",
            }[domain["id"]]
        domains[domain["id"]] = {
            "name": domain["name"],
            "status": status,
            "evidence_count": len(rows),
            "evidence": rows[:20],
            "gap": gap,
        }
    return {
        "generated_at": utcnow(),
        "scope": "only real, observed, independently reviewed Copilot activity",
        "simulated_excluded": simulated,
        "verified_delegations": [r["id"] for r in verified],
        "domains": domains,
        "proven_domains": proven,
        "total_domains": len(DOMAINS),
        "note": "Keine Aussage ueber ein GitHub-Proficiency-Level. GitHub ist die "
                "Autoritaet; diese Erfassung belegt nur eigene, nachpruefbare Evidenz.",
    }


def proficiency_markdown(report):
    lines = [
        "# Copilot Proficiency - belegte Aktivitaet",
        "",
        f"Stand: {report['generated_at']}  ",
        f"Belegte Delegationen: {len(report['verified_delegations'])}  ",
        f"Simulationen ausgeschlossen: {report['simulated_excluded']}",
        "",
        "| Kompetenzbereich | Status | Belege | Luecke |",
        "|---|---|---|---|",
    ]
    for row in report["domains"].values():
        lines.append(f"| {row['name']} | {row['status']} | {row['evidence_count']} | "
                     f"{row['gap'] or '-'} |")
    lines += ["", report["note"], ""]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Offline mock GitHub (simulated responses, no real API, no spend)
# --------------------------------------------------------------------------
DIFF_HAPPY = """diff --git a/src/fix.py b/src/fix.py
index 1111111..2222222 100644
--- a/src/fix.py
+++ b/src/fix.py
@@ -1,3 +1,3 @@
 def add(a, b):
-    return a - b
+    return a + b
"""


class MockGitHub:
    """Stateful fake GitHub API for the full offline delegation lifecycle."""

    def __init__(self, scenario="happy", pr_login=BOT_FULL, has_issues=True):
        self.scenario = scenario
        self.pr_login = pr_login
        self.has_issues = has_issues
        self.calls = []
        self.write_calls = []
        self.issue = None
        self.assigned = False
        self.polls = 0
        self.task = None
        self.task_polls = 0
        self.rate_limited = False
        self._lock = threading.Lock()
        self._httpd = ThreadingHTTPServer(("127.0.0.1", 0), _MockHandler)
        self._httpd.daemon_threads = True
        self._httpd.mock = self
        self._thread = None

    @property
    def url(self):
        return f"http://127.0.0.1:{self._httpd.server_address[1]}"

    def start(self):
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()
        return self

    def stop(self):
        self._httpd.shutdown()
        self._httpd.server_close()
        if self._thread:
            self._thread.join(timeout=5)

    def _json(self, status, obj, headers=None):
        return status, {"Content-Type": "application/json"}, json.dumps(obj).encode("utf-8")

    def handle(self, method, path, headers, body):
        with self._lock:
            self.calls.append((method, path))
            if method in ("POST", "PUT", "PATCH", "DELETE"):
                self.write_calls.append((method, path))
            parsed = urllib.parse.urlparse(path)
            route = parsed.path
            query = urllib.parse.parse_qs(parsed.query)
            try:
                payload = json.loads(body.decode("utf-8")) if body else {}
            except ValueError:
                payload = {}

            if route == "/user":
                return self._json(200, {"login": "SFS-Labs", "id": 128276266})
            if route == "/rate_limit":
                return self._json(200, {"resources": {"core": {"remaining": 4999}}})
            if route.startswith("/repos/SFS-Labs/sfs-ai-development-gateway"):
                return self._json(404, {"message": "Not Found"})
            if route == "/repos/demo/repo":
                return self._json(200, {
                    "full_name": "demo/repo", "private": True, "default_branch": "main",
                    "has_issues": self.has_issues,
                    "permissions": {"admin": True, "push": True},
                })
            if route == "/graphql":
                query_text = str(payload.get("query") or "")
                if "suggestedActors" in query_text:
                    return self._json(200, {"data": {"repository": {"suggestedActors": {
                        "nodes": [{"login": BOT_LOGIN, "__typename": "Bot",
                                   "id": "BOT_kgDOC9w8XQ"}]}}}})
                if "replaceActorsForAssignable" in query_text:
                    if self.scenario == "assign-failure":
                        return self._json(200, {"errors": [{"message": "assignment denied"}]})
                    self.assigned = True
                    return self._json(200, {"data": {"replaceActorsForAssignable": {
                        "assignable": {"id": "I_issue71", "number": 71,
                                       "url": "https://api.github.com/repos/demo/repo/issues/71"}}}})
                return self._json(200, {"data": {}})
            if route == "/repos/demo/repo/issues":
                if method == "GET":
                    if not self.has_issues:
                        return self._json(403, {"message": "issues disabled"})
                    return self._json(200, [self.issue] if self.issue else [])
                if method == "POST":
                    self.issue = {
                        "number": 71, "node_id": "I_issue71", "state": "open",
                        "title": payload.get("title"), "body": payload.get("body"),
                        "html_url": "https://github.com/demo/repo/issues/71",
                        "assignees": [],
                    }
                    return self._json(201, self.issue)
            if route == "/repos/demo/repo/issues/71":
                issue = dict(self.issue or {"number": 71, "node_id": "I_issue71"})
                issue["assignees"] = ([{"login": BOT_LOGIN}] if self.assigned else [])
                return self._json(200, issue)
            if route == "/repos/demo/repo/issues/71/timeline":
                self.polls += 1
                events = []
                if self.assigned:
                    events.append({"event": "assigned",
                                   "assignee": {"login": BOT_LOGIN}})
                if self.assigned and self.polls >= 1:
                    events.append({"event": "copilot_work_started"})
                if self.scenario == "quota" and self.assigned:
                    events.append({"event": "issue_comment", "body":
                                   "Copilot could not start: insufficient AI credits."})
                if self.scenario not in ("quota", "timeout") and self.assigned and self.polls >= 2:
                    events.append({"event": "cross-referenced", "source": {"issue": {
                        "number": 12, "html_url": "https://github.com/demo/repo/pull/12",
                        "pull_request": {"url": "https://api.github.com/repos/demo/repo/pulls/12"},
                    }}})
                return self._json(200, events)
            if route == "/repos/demo/repo/issues/71/comments":
                rows = []
                if self.scenario == "quota" and self.assigned:
                    rows.append({"user": {"login": BOT_FULL}, "body":
                                 "Copilot could not start: insufficient AI credits."})
                return self._json(200, rows)
            if route == "/repos/demo/repo/pulls/12":
                if "diff" in headers.get("Accept", ""):
                    return 200, {"Content-Type": "text/plain"}, DIFF_HAPPY.encode("utf-8")
                return self._json(200, {
                    "number": 12, "html_url": "https://github.com/demo/repo/pull/12",
                    "title": "Fix add()", "state": "open", "draft": False, "merged": False,
                    "mergeable_state": "clean", "changed_files": 1, "additions": 1,
                    "deletions": 1, "user": {"login": self.pr_login},
                    "head": {"ref": "copilot/fix-add", "sha": "abc123def456"},
                    "base": {"ref": "main"},
                })
            if route == "/repos/demo/repo/pulls/12/files":
                files = [{"filename": "src/fix.py", "status": "modified", "additions": 1,
                          "deletions": 1,
                          "patch": "@@ -1,3 +1,3 @@\n def add(a, b):\n-    return a - b\n+    return a + b\n"}]
                if self.scenario == "scope-violation":
                    files.append({"filename": ".github/workflows/release.yml",
                                  "status": "modified", "additions": 1, "deletions": 0,
                                  "patch": "@@ -0,0 +1 @@\n+on: push\n"})
                if self.scenario == "secret":
                    files.append({"filename": "src/fix.py", "status": "modified",
                                  "additions": 1, "deletions": 0,
                                  "patch": "@@ -3,0 +4,1 @@\n+API_KEY = \"ghp_"
                                           + "a" * 36 + "\"\n"})
                return self._json(200, files)
            if route == "/repos/demo/repo/commits/abc123def456/check-runs":
                conclusion = "failure" if self.scenario == "ci-failure" else "success"
                return self._json(200, {"total_count": 2, "check_runs": [
                    {"name": "tests", "status": "completed", "conclusion": conclusion,
                     "html_url": "https://github.com/demo/repo/actions/runs/1"},
                    {"name": "lint", "status": "completed", "conclusion": "success",
                     "html_url": "https://github.com/demo/repo/actions/runs/2"},
                ]})
            if route == "/repos/demo/repo/commits/abc123def456/status":
                state = "failure" if self.scenario == "ci-failure" else "success"
                return self._json(200, {"state": state, "statuses": []})
            if route == "/agents/tasks":
                return self._json(200, {"tasks": [self.task] if self.task else []})
            if route == "/agents/repos/demo/repo/tasks":
                if method == "GET":
                    return self._json(200, {"tasks": [self.task] if self.task else []})
                if method == "POST":
                    self.task = {
                        "id": "task-1", "state": "queued", "name": payload.get("prompt", "")[:60],
                        "html_url": "https://github.com/demo/repo/agents/task-1",
                        "artifacts": [], "sessions": [],
                    }
                    return self._json(201, self.task)
            if route == "/agents/tasks/task-1":
                if self.scenario == "rate-limit" and not self.rate_limited:
                    self.rate_limited = True
                    return 429, {"Retry-After": "0", "Content-Type": "application/json"}, \
                        json.dumps({"message": "rate limited"}).encode("utf-8")
                self.task_polls += 1
                if self.scenario == "quota":
                    self.task = {"id": "task-1", "state": "failed",
                                 "error": {"message": "insufficient AI credits"},
                                 "sessions": [], "artifacts": []}
                elif self.scenario == "timeout" or self.task_polls < 2:
                    self.task = {"id": "task-1", "state": "in_progress",
                                 "sessions": [{"state": "in_progress"}], "artifacts": []}
                else:
                    self.task = {
                        "id": "task-1", "state": "completed",
                        "sessions": [{"state": "completed",
                                      "usage": {"type": "ai_credits", "amount": 1}}],
                        "artifacts": [{"provider": "github", "type": "pull",
                                       "data": {"id": 1201, "number": 12,
                                                "html_url": "https://github.com/demo/repo/pull/12"}}],
                    }
                return self._json(200, self.task)
            if route == "/repos/demo/repo/pulls" and method == "GET":
                return self._json(200, [])
            return self._json(404, {"message": f"mock route not found: {route}"})


class _MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")

    def do_PUT(self):
        self._handle("PUT")

    def do_DELETE(self):
        self._handle("DELETE")

    def _handle(self, method):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        try:
            status, headers, data = self.server.mock.handle(
                method, self.path, dict(self.headers), body)
        except Exception as exc:  # noqa: BLE001 - mock must answer, not crash
            status, headers, data = 500, {"Content-Type": "application/json"}, \
                json.dumps({"message": f"mock error: {exc}"}).encode("utf-8")
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


# --------------------------------------------------------------------------
# Demo / selftest
# --------------------------------------------------------------------------
def run_demo(scenario="happy", state_dir=None, route="issue"):
    mock = MockGitHub(scenario).start()
    state = ensure_state(state_dir or Path(tempfile.mkdtemp(prefix="copilot-demo-")))
    try:
        client = GitHubClient(token="simulated", api_url=mock.url, retries=2)
        standard = load_local_standard()
        pre = preflight(client, "demo/repo", state_dir=state, standard=standard,
                        simulated=True, write=True)
        brief = detect_brief(
            "Add a bounded fix in src/fix.py so the existing tests pass and add a "
            "regression test for the sign error.", "demo/repo", "main", ["src/fix.py"])
        if not brief["eligibility"]["eligible"]:
            return {"ok": False, "scenario": scenario, "error": "brief not eligible",
                    "brief": brief}
        record = create_delegation(client, brief, state, route=route, execute=True,
                                   allow_paid=True, simulated=True)
        record = watch(client, record, state, follow=True, interval=0,
                       max_polls=2 if scenario in ("quota", "timeout") else 4)
        review = None
        if record.get("pull_request"):
            review = review_delegation(client, record, state)
        prof = collect_proficiency(state)
        expected = {
            "happy": ("REVIEWED", "VERIFIED"),
            "agent-task": ("REVIEWED", "VERIFIED"),
            "rate-limit": ("REVIEWED", "VERIFIED"),
            "ci-failure": ("CHANGES_REQUIRED", "CHANGES_REQUIRED"),
            "scope-violation": ("CHANGES_REQUIRED", "CHANGES_REQUIRED"),
            "secret": ("CHANGES_REQUIRED", "CHANGES_REQUIRED"),
            "quota": ("QUOTA_BLOCKED", None),
            "timeout": ("WATCH_LIMIT_REACHED", None),
        }.get(scenario, ("REVIEWED", "VERIFIED"))
        state_ok = record.get("state") == expected[0]
        review_ok = expected[1] is None or (review and review.get("verdict") == expected[1])
        return {
            "ok": bool(state_ok and review_ok),
            "scenario": scenario,
            "route": route,
            "simulated": True,
            "paid_spend": 0,
            "preflight_ready": pre["ready_to_delegate"],
            "state": record.get("state"),
            "expected_state": expected[0],
            "review_verdict": review.get("verdict") if review else None,
            "expected_review": expected[1],
            "proven_domains": prof["proven_domains"],
            "simulated_excluded": prof["simulated_excluded"],
            "write_calls": [f"{m} {p}" for m, p in mock.write_calls],
            "api_calls": len(mock.calls),
        }
    finally:
        mock.stop()


def run_selftest():
    scenarios = [
        ("happy", "issue"), ("agent-task", "agent-task"), ("rate-limit", "agent-task"),
        ("ci-failure", "issue"), ("scope-violation", "issue"), ("secret", "issue"),
        ("quota", "issue"), ("timeout", "agent-task"),
    ]
    rows = []
    for scenario, route in scenarios:
        with tempfile.TemporaryDirectory(prefix="copilot-selftest-") as tmp:
            rows.append(run_demo(scenario, tmp, route=route))
    return {
        "ok": all(r["ok"] for r in rows),
        "scenarios": rows,
        "real_api_calls": 0,
        "paid_spend": 0,
        "note": "Alle Szenarien laufen gegen den lokalen Mock-Server; keine echte "
                "Copilot-Delegation und keine Kosten.",
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _print(obj, as_json=True):
    if as_json:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    else:
        print(obj)


def _common(parser, repo=False):
    parser.add_argument("--state-dir", type=Path, default=None)
    parser.add_argument("--api-url", default=None)
    parser.add_argument("--json", action="store_true", default=False)
    if repo:
        parser.add_argument("--repo", default=DEFAULT_REPO)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Freebuff-led GitHub Copilot delegation (read-only preflight, gated writes).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    st = sub.add_parser("standard", help="Resolve the SFS proficiency standard (remote, local fallback)")
    st.add_argument("--refresh", action="store_true")
    _common(st)

    pf = sub.add_parser("preflight", help="Read-only auth, repo, Copilot and route check")
    _common(pf, repo=True)

    det = sub.add_parser("detect", help="Detect a bounded Copilot subtask and build a brief")
    det.add_argument("--task", required=True)
    det.add_argument("--base", default="main")
    det.add_argument("--path", action="append", default=[])
    det.add_argument("--test-command", action="append", default=[])
    det.add_argument("--out", type=Path)
    _common(det, repo=True)

    dele = sub.add_parser("delegate", help="Create an issue assignment or agent task (dry-run default)")
    dele.add_argument("--brief", type=Path, required=True)
    dele.add_argument("--route", choices=["auto", "issue", "agent-task"], default="auto")
    dele.add_argument("--execute", action="store_true")
    dele.add_argument("--allow-paid", action="store_true")
    dele.add_argument("--simulate", action="store_true",
                      help="use a local mock server instead of GitHub")
    _common(dele, repo=True)

    wat = sub.add_parser("watch", help="Poll task/issue, branch, PR and CI status")
    wat.add_argument("--id", required=True)
    wat.add_argument("--follow", action="store_true")
    wat.add_argument("--interval", type=float, default=10.0)
    wat.add_argument("--max-polls", type=int, default=30)
    _common(wat)

    rev = sub.add_parser("review", help="Independently review the delivered diff and CI")
    rev.add_argument("--id", required=True)
    rev.add_argument("--local-repo", type=Path)
    rev.add_argument("--test-profile", default="none",
                     choices=["none", "python-unittest", "python-pytest", "node-test", "custom"])
    rev.add_argument("--custom-profile", type=Path)
    _common(rev)

    prof = sub.add_parser("proficiency", help="Evidence-only view across the five domains")
    prof.add_argument("--markdown", action="store_true")
    prof.add_argument("--write", type=Path)
    prof.add_argument("--state-dir", type=Path, default=None)
    prof.add_argument("--json", action="store_true", default=False)

    pol = sub.add_parser("policy", help="Inspect or change the local paid-delegation gate")
    pol.add_argument("--show", action="store_true")
    pol.add_argument("--allow-paid", action="store_true")
    pol.add_argument("--forbid-paid", action="store_true")
    pol.add_argument("--credits-restored", action="store_true")
    pol.add_argument("--credits-exhausted", action="store_true")
    pol.add_argument("--state-dir", type=Path, default=None)
    pol.add_argument("--json", action="store_true", default=False)

    dem = sub.add_parser("demo", help="Full offline lifecycle against simulated API responses")
    dem.add_argument("--scenario", default="happy",
                     choices=["happy", "agent-task", "rate-limit", "ci-failure",
                              "scope-violation", "secret", "quota", "timeout"])
    dem.add_argument("--route", choices=["issue", "agent-task"], default="issue")
    dem.add_argument("--state-dir", type=Path, default=None)
    dem.add_argument("--json", action="store_true", default=False)

    stf = sub.add_parser("selftest", help="Run all offline scenarios")
    stf.add_argument("--json", action="store_true", default=False)

    args = parser.parse_args(argv)
    root = repo_root()
    state = ensure_state(getattr(args, "state_dir", None) or root / ".copilot")

    try:
        if args.cmd == "policy":
            policy = load_policy(state)
            if args.allow_paid:
                policy["paid_delegation_allowed"] = True
            if args.forbid_paid:
                policy["paid_delegation_allowed"] = False
            if args.credits_restored:
                policy["credits_exhausted"] = False
            if args.credits_exhausted:
                policy["credits_exhausted"] = True
            if any([args.allow_paid, args.forbid_paid, args.credits_restored,
                    args.credits_exhausted]):
                policy = save_policy(state, policy)
            _print(policy, True)
            return 0

        if args.cmd == "demo":
            result = run_demo(args.scenario, args.state_dir, route=args.route)
            _print(result, True)
            return 0 if result.get("ok") else 1

        if args.cmd == "selftest":
            result = run_selftest()
            _print(result, True)
            return 0 if result.get("ok") else 1

        if args.cmd == "proficiency":
            report = collect_proficiency(state)
            if args.write:
                args.write.parent.mkdir(parents=True, exist_ok=True)
                args.write.write_text(proficiency_markdown(report), encoding="utf-8")
                report["written"] = str(args.write)
            if args.markdown:
                print(proficiency_markdown(report))
            else:
                _print(report, True)
            return 0

        if args.cmd == "standard":
            client = GitHubClient(api_url=args.api_url)
            result = resolve_standard(client, state, root=root, refresh=args.refresh)
            _print({k: v for k, v in result.items() if k != "document"}, True)
            return 0

        if args.cmd == "preflight":
            client = GitHubClient(api_url=args.api_url)
            result = preflight(client, args.repo, state_dir=state, root=root)
            _print(result, True)
            return 0 if result["ready_for_free_checks"] else 1

        if args.cmd == "detect":
            brief = detect_brief(args.task, args.repo, args.base, args.path,
                                 args.test_command)
            if args.out:
                write_json(args.out, brief, mode=0o644)
            _print(brief, True)
            return 0 if brief["eligibility"]["eligible"] else 1

        if args.cmd == "delegate":
            brief = read_json(args.brief)
            if not isinstance(brief, dict):
                raise CopilotError(f"brief not found or invalid: {args.brief}")
            if args.repo and args.repo != DEFAULT_REPO:
                brief["repo"] = args.repo
            mock = None
            if args.simulate:
                # --simulate must never reach GitHub, even if --api-url is set.
                mock = MockGitHub("happy").start()
                client = GitHubClient(token="simulated", api_url=mock.url, retries=1)
            else:
                client = GitHubClient(api_url=args.api_url)
            try:
                result = create_delegation(client, brief, state, route=args.route,
                                           execute=args.execute, allow_paid=args.allow_paid,
                                           simulated=args.simulate, root=root)
            finally:
                if mock:
                    mock.stop()
            _print(result, True)
            if result.get("state") in ("BLOCKED_PAID_GATE", "BLOCKED_ROUTE", "FAILED"):
                return 1
            return 0

        if args.cmd == "watch":
            record = load_delegation(state, args.id)
            client = GitHubClient(api_url=args.api_url)
            result = watch(client, record, state, follow=args.follow,
                           interval=args.interval, max_polls=args.max_polls)
            _print(result, True)
            return 0 if result.get("state") in SUCCESS_STATES else 1

        if args.cmd == "review":
            record = load_delegation(state, args.id)
            client = GitHubClient(api_url=args.api_url)
            result = review_delegation(client, record, state, args.local_repo,
                                       args.test_profile, args.custom_profile)
            _print(result, True)
            return 0 if result.get("verdict", "").startswith("VERIFIED") else 1

        raise CopilotError(f"unknown command: {args.cmd}")
    except CopilotError as exc:
        payload = {"status": "ERROR", "error": _redact(str(exc))}
        if getattr(args, "json", False):
            _print(payload, True)
        else:
            print(f"copilot-delegate: {payload['error']}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
