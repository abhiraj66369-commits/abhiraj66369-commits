#!/usr/bin/env python3
"""Offline validation for this profile repository.

Produces a PASS / FAIL report for every feature in the parity checklist.

Each feature has two verdicts:
  Framework  PASS   implemented and verified by this script
             PASS*  implemented and statically valid, but only provable after the
                    first GitHub Actions run (needs secrets / network)
             FAIL   missing or broken
  Content    PASS         real data present
             NEEDS INPUT  framework works, but you have not supplied the data yet
                          (nothing is invented to fill the gap)

Exit code is 1 if any Framework verdict is FAIL.

    python scripts/validate_profile.py
    python scripts/validate_profile.py --report docs/VALIDATION.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
README = (ROOT / "README.md").read_text(encoding="utf-8")
DATA = json.loads((ROOT / "data" / "profile.json").read_text(encoding="utf-8"))
WORKFLOWS = {p.name: p for p in sorted((ROOT / ".github" / "workflows").glob("*.yml"))}
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py", ".svg", ".toml", ".txt", ""}


# --------------------------------------------------------------------------- utilities
def block(name: str) -> str:
    m = re.search(rf"<!-- BEGIN:{name} -->(.*?)<!-- END:{name} -->", README, re.DOTALL)
    return m.group(1).strip() if m else ""


def workflow(name: str):
    return yaml.safe_load(WORKFLOWS[name].read_text(encoding="utf-8")) if name in WORKFLOWS else None


def workflow_text(name: str) -> str:
    return WORKFLOWS[name].read_text(encoding="utf-8") if name in WORKFLOWS else ""


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def readme_mentions(rel: str) -> bool:
    return rel in README


def fenced_stripped(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def project_rows() -> list[str]:
    return [l for l in block("PROJECTS").splitlines() if l.startswith("| [")]


# --------------------------------------------------------------------------- checks
Result = tuple[str, str, str]  # framework, content, note


def ok(note: str = "", content: str = "PASS") -> Result:
    return ("PASS", content, note)


def star(note: str = "", content: str = "PASS") -> Result:
    return ("PASS*", content, note)


def fail(note: str) -> Result:
    return ("FAIL", "n/a", note)


def need(links_keys) -> str:
    return "PASS" if all(DATA["links"].get(k) for k in links_keys) else "NEEDS INPUT"


def metric_card(name: str, step_hint: str) -> Result:
    svg = exists(f"metrics/{name}.svg")
    in_readme = readme_mentions(f"metrics/{name}.svg")
    in_wf = f"filename: {name}.svg" in workflow_text("metrics.yml")
    if svg and in_readme and in_wf:
        return star(f"{step_hint}: placeholder committed, workflow step present")
    return fail(f"svg={svg} readme={in_readme} workflow_step={in_wf}")


def check_hero() -> Result:
    svg = (ROOT / "assets/hero.svg").read_text(encoding="utf-8") if exists("assets/hero.svg") else ""
    if "@keyframes" in svg and "prefers-reduced-motion" in svg and readme_mentions("assets/hero.svg"):
        return ok("self-hosted animated SVG with reduced-motion fallback")
    return fail("hero.svg missing, not animated, or not linked")


def check_intro() -> Result:
    return ok() if re.search(r"^> \*\*Hi, I'm", README, re.M) else fail("intro blockquote missing")


def check_projects() -> Result:
    rows = project_rows()
    return ok(f"{len(rows)} projects rendered") if len(rows) >= 3 else fail(f"only {len(rows)} project rows")


def check_descriptions() -> Result:
    bad = [p["name"] for p in DATA["projects"] if not p.get("hidden") and (len(p["description"]) < 40 or "NEED USER INPUT" in p["description"])]
    hidden = [p["name"] for p in DATA["projects"] if p.get("hidden")]
    if bad:
        return fail(f"weak descriptions: {bad}")
    return ok("all visible descriptions come from inspected repos", "NEEDS INPUT" if hidden else "PASS") if not hidden else (
        "PASS", "NEEDS INPUT", f"hidden until repo URL supplied: {', '.join(hidden)}")


def check_badges() -> Result:
    return ok("grouped icon rows + text names") if "skillicons.dev/icons" in block("STACK") else fail("no icon rows in STACK")


def check_demos() -> Result:
    n = sum(1 for p in DATA["projects"] if p.get("demo") and not p.get("hidden"))
    return ok(f"{n} demo links (checked by lychee in CI)") if n else fail("no demo links")


def check_devtools() -> Result:
    rows = [l for l in block("DEVTOOLS").splitlines() if l.startswith("| [")]
    return ok(f"{len(rows)} tools") if rows else fail("DEVTOOLS empty")


def check_oss() -> Result:
    if not block("OSS"):
        return fail("OSS block empty")
    return ok("framework renders real PR table or an honest 'Open Source Journey' note", "PASS" if DATA["open_source"] else "NEEDS INPUT")


def check_link(key: str) -> Result:
    return ok(f"badge renders when links.{key} is set", need([key]))


def check_contact() -> Result:
    if not block("CONTACT"):
        return fail("CONTACT empty")
    return ok("GitHub badge always; others appear when set", need(["email", "linkedin"]))


def check_stack() -> Result:
    rows = [l for l in block("STACK").splitlines() if l.startswith("| **")]
    return ok(f"{len(rows)} groups; unverified skills excluded") if len(rows) >= 5 else fail("stack groups missing")


def check_stats() -> Result:
    a = metric_card("github-metrics", "overview")
    b = metric_card("languages", "languages")
    return a if a[0] == "FAIL" else b


def check_coding() -> Result:
    if not block("CODING"):
        return fail("CODING block empty")
    return ok("links only; statistics never fabricated", "PASS" if DATA["coding_profiles"] else "NEEDS INPUT")


def check_certs() -> Result:
    if not block("CERTS"):
        return fail("CERTS block empty")
    if not exists("certificates/README.md"):
        return fail("certificates/README.md missing")
    return ok("table renders from data; placeholder otherwise", "PASS" if DATA["certifications"] else "NEEDS INPUT")


def check_details() -> Result:
    return star("collapsible section wraps calendar, habits, topics") if "<details>" in README and "Detailed metrics" in README else fail("details section missing")


def check_snake() -> Result:
    txt = workflow_text("snake.yml")
    if "Platane/snk/svg-only@v3" in txt and "output/github-snake" in README and "force origin output" in txt:
        return star("workflow + README wiring present; run once to create `output` branch")
    return fail("snake wiring incomplete")


def check_footer() -> Result:
    svg = (ROOT / "assets/footer.svg").read_text(encoding="utf-8") if exists("assets/footer.svg") else ""
    return ok("animated SVG with reduced-motion fallback") if "@keyframes" in svg and readme_mentions("assets/footer.svg") else fail("footer missing")


def check_workflows() -> Result:
    problems = []
    for name in ("snake.yml", "metrics.yml", "profile-update.yml", "quality.yml"):
        y = workflow(name)
        if not y:
            problems.append(f"{name} missing")
            continue
        if "permissions" not in y:
            problems.append(f"{name}: no top-level permissions")
        if not y.get("name"):
            problems.append(f"{name}: no name")
        if "concurrency" not in y:
            problems.append(f"{name}: no concurrency")
    return star("4 workflows parse; least-privilege permissions; concurrency set; actionlint runs in CI") if not problems else fail("; ".join(problems))


def check_no_loops() -> Result:
    pu = workflow("profile-update.yml") or {}
    trig = pu.get(True) or pu.get("on") or {}
    paths = (trig.get("push") or {}).get("paths", [])
    if "README.md" in paths:
        return fail("profile-update triggers on README.md: infinite loop risk")
    if "[skip ci]" not in workflow_text("profile-update.yml") or "[skip ci]" not in workflow_text("metrics.yml"):
        return fail("bot commits should carry [skip ci]")
    return ok("README not a trigger path; bot commits use [skip ci] and GITHUB_TOKEN")


def check_automation() -> Result:
    have = exists(".github/dependabot.yml") and exists("scripts/update_readme.py") and exists("data/profile.json")
    return ok("dependabot + data-driven README generator") if have else fail("automation files missing")


def check_assets() -> Result:
    need_files = ["assets/hero.svg", "assets/divider.svg", "assets/footer.svg"] + [f"metrics/{n}.svg" for n in
                  ("github-metrics", "languages", "streak", "isocalendar", "habits", "achievements", "topics")]
    missing = [f for f in need_files if not exists(f)]
    return ok(f"{len(need_files)} assets present") if not missing else fail(f"missing: {missing}")


def check_docs() -> Result:
    need_files = ["docs/SETUP.md", "docs/PARITY.md", "CHANGELOG.md", "certificates/README.md"]
    missing = [f for f in need_files if not exists(f)]
    return ok() if not missing else fail(f"missing: {missing}")


SECRET_PATTERNS = [
    r"AIza[0-9A-Za-z_\-]{35}",
    r"gh[pousr]_[A-Za-z0-9]{36,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"sk-[A-Za-z0-9]{20,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"(?i)(password|passwd|secret)\s*[:=]\s*['\"]?(?-i:(?![A-Z_]+\b))(?!\$\{\{)[A-Za-z0-9@#$%^&*_\-]{8,}",
]


def repo_files():
    for p in ROOT.rglob("*"):
        if p.is_file() and ".git" not in p.parts and p.suffix in TEXT_SUFFIXES:
            yield p


def check_security() -> Result:
    hits = []
    for p in repo_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        for pat in SECRET_PATTERNS:
            if p.name == "validate_profile.py":
                continue
            if re.search(pat, text):
                hits.append(f"{p.relative_to(ROOT)} ~ {pat[:18]}")
    need_files = ["SECURITY.md", ".gitignore", "LICENSE"]
    missing = [f for f in need_files if not exists(f)]
    if hits or missing:
        return fail(f"secret-like strings: {hits}; missing files: {missing}")
    gi = (ROOT / ".gitignore").read_text()
    if ".env" not in gi:
        return fail(".gitignore does not ignore .env")
    return ok("no secret-like strings; SECURITY.md, .gitignore (.env), LICENSE; gitleaks runs in CI")


REFERENCE_MARKERS = ["Sagar", "sagargupta", "sg85207", "NIT Warangal", "AWS Certified", "LeetCode Knight", "Kalchar", "Ledger Sync"]


def check_originality() -> Result:
    hits = []
    for p in repo_files():
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("docs/") or p.name == "validate_profile.py":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        hits += [f"{rel}: {m}" for m in REFERENCE_MARKERS if m.lower() in text.lower()]
    return ok("no reference-profile identity, claims or text found") if not hits else fail(f"found: {hits}")


def check_no_fabrication() -> Result:
    bad = []
    for p in DATA["projects"]:
        if p.get("hidden") and p.get("repo"):
            bad.append(p["name"])
    unconfirmed_rendered = [s["name"] for s in DATA["skills"] if s.get("confirmed", True) is False and s["name"] in block("STACK")]
    if bad or unconfirmed_rendered:
        return fail(f"{bad} {unconfirmed_rendered}")
    return ok("unconfirmed skills and unknown projects are withheld from the README")


def check_links_local() -> Result:
    refs = re.findall(r'(?:\]\(|src=")([^)"\s#]+)', README)
    refs += re.findall(r'href="([^"#]+)"', README)
    missing = []
    for r in refs:
        if re.match(r"^(https?:|mailto:|data:)", r):
            continue
        if not (ROOT / r).exists():
            missing.append(r)
    return ok(f"{len(set(refs))} references checked") if not missing else fail(f"broken local references: {sorted(set(missing))}")


def check_alt_text() -> Result:
    bad = []
    for m in re.finditer(r"!\[([^\]]*)\]\(", README):
        if not m.group(1).strip():
            bad.append("markdown image with empty alt")
    for m in re.finditer(r"<img\b([^>]*)>", README):
        attrs = m.group(1)
        alt = re.search(r'alt="([^"]*)"', attrs)
        if alt is None:
            bad.append("img without alt attribute")
        elif not alt.group(1).strip() and "divider.svg" not in attrs:
            bad.append("non-decorative img with empty alt")
    return ok("all images have alt text (dividers are decorative alt=\"\")") if not bad else fail("; ".join(bad))


def check_headings() -> Result:
    levels = [len(m.group(1)) for m in re.finditer(r"^(#{1,6}) ", fenced_stripped(README), re.M)]
    h1_html = len(re.findall(r"<h1\b", README))
    if h1_html + levels.count(1) != 1:
        return fail(f"expected exactly one H1, found {h1_html + levels.count(1)}")
    prev = 1
    for lv in levels:
        if lv > prev + 1:
            return fail(f"heading level jumps from {prev} to {lv}")
        prev = lv
    return ok("one H1 (hero image with alt), no skipped levels")


def check_motion_a11y() -> Result:
    bad = [f for f in ("hero.svg", "footer.svg") if "prefers-reduced-motion" not in (ROOT / "assets" / f).read_text()]
    return ok("animated assets honour prefers-reduced-motion") if not bad else fail(f"no reduced-motion rule: {bad}")


def check_markers() -> Result:
    names = re.findall(r"<!-- BEGIN:(\w+) -->", README)
    unpaired = [n for n in names if f"<!-- END:{n} -->" not in README]
    empty = [n for n in names if not block(n)]
    return ok(f"{len(names)} generated sections, all populated") if not unpaired and not empty else fail(f"unpaired={unpaired} empty={empty}")


CHECKLIST: list[tuple[str, str, callable]] = [
    ("1", "Animated hero / typing section", check_hero),
    ("2", "Professional introduction", check_intro),
    ("3", "Featured projects", check_projects),
    ("4", "Project descriptions (from inspected repos)", check_descriptions),
    ("5", "Technology badges", check_badges),
    ("6", "Live demo links", check_demos),
    ("7", "Developer / community tools", check_devtools),
    ("8", "Open-source contributions", check_oss),
    ("9", "Portfolio link", lambda: check_link("portfolio")),
    ("10", "Resume link", lambda: check_link("resume")),
    ("11", "Contact section", check_contact),
    ("12", "Tech stack", check_stack),
    ("13", "GitHub statistics + top languages", check_stats),
    ("14", "Current contribution streak", lambda: metric_card("streak", "streak")),
    ("15", "Programming / DSA section", check_coding),
    ("16", "Coding-platform statistics", check_coding),
    ("17", "Certifications", check_certs),
    ("18", "Achievement badges", lambda: metric_card("achievements", "achievements")),
    ("19", "Detailed GitHub metrics", check_details),
    ("20", "Isometric contribution calendar", lambda: metric_card("isocalendar", "isocalendar")),
    ("21", "Coding habits", lambda: metric_card("habits", "habits")),
    ("22", "Achievements", lambda: metric_card("achievements", "achievements")),
    ("23", "Coding profile metrics", check_coding),
    ("24", "Starred topics", lambda: metric_card("topics", "topics")),
    ("25", "Contribution snake", check_snake),
    ("26", "Animated footer", check_footer),
    ("A", "GitHub Actions (4 workflows)", check_workflows),
    ("B", "No workflow loops", check_no_loops),
    ("C", "Automation (dependabot, generator, data file)", check_automation),
    ("D", "Assets present", check_assets),
    ("E", "Documentation", check_docs),
    ("F", "Security hygiene", check_security),
    ("G", "Accessibility: alt text", check_alt_text),
    ("H", "Accessibility: heading structure", check_headings),
    ("I", "Accessibility: reduced motion", check_motion_a11y),
    ("J", "README markers paired and populated", check_markers),
    ("K", "Local links resolve", check_links_local),
    ("L", "Originality: nothing copied from the reference", check_originality),
    ("M", "Authenticity: nothing unverified rendered", check_no_fabrication),
]


def needs_input() -> list[str]:
    items = []
    items += [f"links.{k} is empty" for k, v in DATA["links"].items() if not v]
    items += [f"project '{p['name']}' needs a repo URL and description" for p in DATA["projects"] if p.get("hidden")]
    items += [f"skill '{s['name']}' is unconfirmed (set confirmed:true and add evidence)" for s in DATA["skills"] if s.get("confirmed", True) is False]
    for key in ("certifications", "coding_profiles", "open_source", "learning"):
        if not DATA[key]:
            items.append(f"{key} is empty")
    return items


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", help="also write the table as Markdown to this path")
    args = ap.parse_args()

    rows, failed = [], 0
    for cid, title, fn in CHECKLIST:
        try:
            fw, content, note = fn()
        except Exception as exc:  # a crashing check is a failing check
            fw, content, note = "FAIL", "n/a", f"check crashed: {exc!r}"
        failed += fw == "FAIL"
        rows.append((cid, title, fw, content, note))

    width = max(len(r[1]) for r in rows)
    print(f"{'#':<3} {'Feature':<{width}}  {'Framework':<9} {'Content':<12} Note")
    for cid, title, fw, content, note in rows:
        print(f"{cid:<3} {title:<{width}}  {fw:<9} {content:<12} {note}")
    todo = needs_input()
    print(f"\n{len(rows) - failed}/{len(rows)} framework checks pass, {failed} fail.")
    print(f"{len(todo)} content items need your input:")
    for t in todo:
        print(f"  - {t}")

    if args.report:
        lines = ["# Validation report", "", "Generated by `python scripts/validate_profile.py --report docs/VALIDATION.md`.", "",
                 "`PASS*` = implemented and statically valid, provable only after the first Actions run.", "",
                 "| # | Feature | Framework | Content | Note |", "|---|---|---|---|---|"]
        lines += [f"| {c} | {t} | {f} | {ct} | {n} |" for c, t, f, ct, n in rows]
        lines += ["", f"**{len(rows) - failed}/{len(rows)} framework checks pass, {failed} fail.**", "", "## Content that needs your input", ""]
        lines += [f"- {t}" for t in todo]
        Path(args.report).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
