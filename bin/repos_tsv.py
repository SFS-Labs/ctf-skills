"""repos_tsv — die eine Lesestelle fuer repos.tsv.

Format: slug \t owner/repo \t Klasse \t Layer \t Rolle [\t key=value; key=value]

Ein Alias ist eine Quelle, die keinen eigenen Skill bekommt, weil ihr Baum mit
einem schon vorhandenen Skill identisch ist. Damit das eine pruefbare Aussage
bleibt und keine datierte Behauptung, muss jede Alias-Zeile ihren Beweis
mitfuehren:

    alias_of=<slug>; tree_sha256=<64 hex>; files=<n>

`tree_sha256` ist der Digest des Ziel-Baums (Pfad + Datei-Digest, ohne den
Fabrik-Marker `.fetched`). `bin/alias-check` rechnet ihn lokal und gegen den
Remote nach, `bin/gen_skills` und `bin/doctor` verweigern die Arbeit, sobald der
aktuelle Baum nicht mehr zum gepinnten Digest passt.
"""
import hashlib
import os

ALIAS_KEYS = ("alias_of", "tree_sha256", "files")
SKIP = (".fetched",)
HEX = set("0123456789abcdef")


class RepoTableError(Exception):
    """repos.tsv ist nicht eindeutig lesbar oder ein Alias-Beweis fehlt."""


def tree_digest(root):
    """(sha256_hex, dateien) ueber alle Dateien unter root, ohne `.fetched`.

    Deterministisch: Verzeichnisse und Dateien werden sortiert, der Pfad geht
    mit in den Hash. Zwei Baeume sind genau dann identisch, wenn Digest und
    Dateizahl gleich sind.
    """
    if not os.path.isdir(root):
        raise RepoTableError("kein Baum: %s" % root)
    acc = hashlib.sha256()
    files = 0
    for base, dirs, names in os.walk(root):
        dirs.sort()
        for name in sorted(names):
            path = os.path.join(base, name)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            if rel in SKIP:
                continue
            files += 1
            with open(path, "rb") as fh:
                digest = hashlib.sha256(fh.read()).hexdigest()
            acc.update(rel.encode("utf-8") + b"\0" + digest.encode("ascii") + b"\n")
    if not files:
        raise RepoTableError("leerer Baum: %s" % root)
    return acc.hexdigest(), files


def _extra(text, lineno):
    out = {}
    for chunk in text.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            raise RepoTableError("Zeile %d: '%s' ist kein key=value" % (lineno, chunk))
        key, value = (x.strip() for x in chunk.split("=", 1))
        if key not in ALIAS_KEYS:
            raise RepoTableError("Zeile %d: unbekannter Schluessel '%s' (erlaubt: %s)"
                                 % (lineno, key, ", ".join(ALIAS_KEYS)))
        if key in out:
            raise RepoTableError("Zeile %d: '%s' doppelt" % (lineno, key))
        out[key] = value
    return out


def load(path):
    """Liest repos.tsv und prueft die Form. Rueckgabe: (skills, aliases).

    skills:  dicts mit slug/repo/cls/layer/role
    aliases: dieselben Felder plus target/tree_sha256/files
    """
    rows, aliases = [], []
    for lineno, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 5 or len(parts) > 6:
            raise RepoTableError("Zeile %d: %d Spalten, erwartet 5 oder 6"
                                 % (lineno, len(parts)))
        slug, repo, cls, layer, role = (p.strip() for p in parts[:5])
        if not slug or "/" not in repo:
            raise RepoTableError("Zeile %d: slug/repo fehlt oder repo ist nicht owner/name"
                                 % lineno)
        extra = _extra(parts[5] if len(parts) == 6 else "", lineno)
        rec = {"slug": slug, "repo": repo, "cls": cls, "layer": layer, "role": role}
        if "alias_of" in extra:
            missing = [k for k in ("tree_sha256", "files") if k not in extra]
            if missing:
                raise RepoTableError(
                    "Zeile %d: Alias %s ohne Beweis (%s fehlt). Erst "
                    "`bin/alias-check --update` laufen lassen." % (lineno, slug, ", ".join(missing)))
            digest = extra["tree_sha256"].lower()
            if len(digest) != 64 or set(digest) - HEX:
                raise RepoTableError("Zeile %d: tree_sha256 ist kein sha256-Hex" % lineno)
            try:
                files = int(extra["files"])
            except ValueError:
                raise RepoTableError("Zeile %d: files ist keine Zahl" % lineno)
            if files < 1:
                raise RepoTableError("Zeile %d: files muss > 0 sein" % lineno)
            rec.update(target=extra["alias_of"], tree_sha256=digest, files=files)
            aliases.append(rec)
        else:
            if extra:
                raise RepoTableError("Zeile %d: %s hat Alias-Felder ohne alias_of" % (lineno, slug))
            rows.append(rec)

    slugs = [r["slug"] for r in rows] + [a["slug"] for a in aliases]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        raise RepoTableError("Slug doppelt: %s" % ", ".join(sorted(dupes)))
    source_slugs = {r["slug"] for r in rows}
    source_repos = {r["repo"] for r in rows}
    alias_repos = set()
    for a in aliases:
        if a["target"] == a["slug"]:
            raise RepoTableError("Alias %s zeigt auf sich selbst" % a["slug"])
        if a["target"] not in source_slugs:
            raise RepoTableError("Alias %s zeigt auf keinen eigenstaendigen Skill: %s"
                                 % (a["slug"], a["target"]))
        if a["repo"] in source_repos:
            raise RepoTableError("Alias-Repo %s steht auch als eigener Skill in repos.tsv"
                                 % a["repo"])
        if a["repo"] in alias_repos:
            raise RepoTableError("Alias-Repo %s doppelt" % a["repo"])
        alias_repos.add(a["repo"])
    return rows, aliases
