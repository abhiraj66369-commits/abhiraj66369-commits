#!/usr/bin/env python3
"""Render the data-driven sections of README.md from data/profile.json.

Design rules
------------
* Standard library only, so it runs anywhere with Python 3.9+.
* Never invents data. Empty / null fields are omitted or shown as a clear
  placeholder ("Add verified certifications here").
* Repository stats come from the GitHub REST API when reachable and fall back
  to data/snapshot.json otherwise, so the script also works offline.

Usage
-----
    python scripts/update_readme.py             # fetch stats, rewrite README
    python scripts/update_readme.py --offline   # use data/snapshot.json only
    python scripts/update_readme.py --check     # exit 1 if README is stale

Set GITHUB_TOKEN (optional) to avoid anonymous API rate limits.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUP_ORDER = ["Languages", "Frontend", "Backend", "Database", "AI / LLM", "DevOps", "Cloud / Deployment", "Tools"]
DASH = "—"


# --------------------------------------------------------------------------- helpers
def esc(text: str) -> str:
    """Escape characters that would break a Markdown table cell."""
    return str(text).replace("|", "\\|").replace("\n", " ")


def shield(label: str, message: str, color: str, logo: str | None = None) -> str:
    def enc(s: str) -> str:
        return urllib.parse.quote(s.replace("-", "--").replace("_", "__"), safe="")

    url = f"https://img.shields.io/badge/{enc(label)}-{enc(message)}-{color}?style=for-the-badge"
    if logo:
        url += f"&logo={logo}&logoColor=white"
    return url


def repo_url(owner: str, repo: str) -> str:
    return f"https://github.com/{owner}/{repo}"


def cell(value) -> str:
    return DASH if value in (None, "") else esc(value)


# --------------------------------------------------------------------------- GitHub API
def api_get(path: str, token: str | None):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-readme-updater",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.load(resp)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None


def fetch_repo(owner: str, repo: str, token: str | None):
    info = api_get(f"/repos/{owner}/{repo}", token)
    if not info:
        return None
    runs = api_get(f"/repos/{owner}/{repo}/actions/runs?per_page=1", token)
    ci = None
    if runs and runs.get("workflow_runs"):
        run = runs["workflow_runs"][0]
        ci = run.get("conclusion") or run.get("status")
    rel = api_get(f"/repos/{owner}/{repo}/releases/latest", token)
    return {
        "stars": info.get("stargazers_count"),
        "forks": info.get("forks_count"),
        "open_issues": info.get("open_issues_count"),  # GitHub counts open PRs here too
        "pushed_at": info.get("pushed_at"),
        "language": info.get("language"),
        "ci": ci,
        "release": (rel or {}).get("tag_name"),
    }


def refresh_snapshot(data: dict, snapshot: dict, offline: bool):
    if offline:
        return snapshot, 0
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    updated = 0
    repos = snapshot.setdefault("repos", {})
    for project in data["projects"]:
        repo = project.get("repo")
        if not repo or project.get("hidden"):
            continue
        fresh = fetch_repo(data["owner"], repo, token)
        if fresh:
            repos[repo] = fresh
            updated += 1
    if updated:
        snapshot["as_of"] = dt.datetime.now(dt.timezone.utc).date().isoformat()
    return snapshot, updated


# --------------------------------------------------------------------------- renderers
def render_social(d):
    links = d["links"]
    items = [("GitHub", "Profile", "181717", "github", links.get("github"))]
    items += [
        ("Portfolio", "Visit", "6366F1", "googlechrome", links.get("portfolio")),
        ("Resume", "Download", "0EA5E9", "readthedocs", links.get("resume")),
        ("LinkedIn", "Connect", "0A66C2", "linkedin", links.get("linkedin")),
        ("Email", "Contact", "D14836", "gmail", f"mailto:{links['email']}" if links.get("email") else None),
    ]
    parts = [f'[![{l} — {m}]({shield(l, m, c, logo)})]({url})' for l, m, c, logo, url in items if url]
    return "\n".join(parts)


def visible_projects(d):
    return [p for p in d["projects"] if not p.get("hidden") and p.get("repo")]


def render_projects(d):
    rows = ["| Project | What it does | Tech | Status | Demo |", "|---|---|---|---|---|"]
    for p in visible_projects(d):
        name = f"[{p['emoji']} {esc(p['name'])}]({repo_url(d['owner'], p['repo'])})"
        tech = " • ".join(esc(t) for t in p["tech"]) or DASH
        demo = f"[Live ↗]({p['demo']})" if p.get("demo") else DASH
        rows.append(f"| {name} | {esc(p['description'])} | {tech} | {esc(p['status'])} | {demo} |")
    more = d.get("more_repos", [])
    if more:
        links = " · ".join(f"[{m['repo']}]({repo_url(d['owner'], m['repo'])}) ({esc(m['note'].lower())})" for m in more)
        rows += ["", f"More repositories: {links}"]
    return "\n".join(rows)


def render_health(d, snap):
    rows = [
        "| Repository | ★ Stars | Forks | Open issues + PRs | CI | Latest release | Last push | Main language |",
        "|---|---|---|---|---|---|---|---|",
    ]
    total = 0
    for p in visible_projects(d):
        s = snap.get("repos", {}).get(p["repo"], {})
        pushed = (s.get("pushed_at") or "")[:10] or None
        total += s.get("stars") or 0
        rows.append(
            f"| [{esc(p['repo'])}]({repo_url(d['owner'], p['repo'])}) | {cell(s.get('stars'))} | {cell(s.get('forks'))} "
            f"| {cell(s.get('open_issues'))} | {cell(s.get('ci'))} | {cell(s.get('release'))} | {cell(pushed)} | {cell(s.get('language'))} |"
        )
    rows += ["", f"<sub>Real numbers only; {DASH} means not available. Stars across these repositories: {total}. Snapshot date: {snap.get('as_of', DASH)}.</sub>"]
    return "\n".join(rows)


def render_stack(d):
    groups: dict[str, list[dict]] = {}
    for s in d["skills"]:
        if s.get("confirmed", True) is False or not s.get("evidence"):
            continue  # unverified skills stay out of the README until evidence exists
        groups.setdefault(s["group"], []).append(s)
    rows = ["| Area | Technologies |", "|---|---|"]
    for g in GROUP_ORDER + [g for g in groups if g not in GROUP_ORDER]:
        items = groups.get(g)
        if not items:
            continue
        icons = [s["icon"] for s in items if s.get("icon")]
        names = " · ".join(esc(s["name"]) for s in items)
        img = ""
        if icons:
            alt = f"{g} technology icons"
            img = f"![{alt}](https://skillicons.dev/icons?i={','.join(icons)}&theme=dark&perline=10)<br/>"
        rows.append(f"| **{g}** | {img}{names} |")
    return "\n".join(rows)


def render_practices(d):
    rows = ["| Practice | Where it shows up |", "|---|---|"]
    rows += [f"| {esc(x['practice'])} | {esc(x['where'])} |" for x in d["engineering_practices"]]
    return "\n".join(rows)


def render_devtools(d):
    rows = ["| Tool | What it is |", "|---|---|"]
    rows += [f"| [{esc(t['repo'])}]({repo_url(d['owner'], t['repo'])}) | {esc(t['description'])} |" for t in d["dev_tools"]]
    return "\n".join(rows)


def render_focus(d):
    return "\n".join(f"- 🔭 {f}" for f in d["focus"])


def render_learning(d):
    if not d["learning"]:
        return "*Add what you are actively learning here (data/profile.json → learning).*"
    return "\n".join(f"- 🌱 {esc(x)}" for x in d["learning"])


def render_roadmap(d):
    return "\n".join(f"- [ ] {esc(r['item'])} *({r['status']})*" for r in d["roadmap"])


def render_certs(d):
    certs = d["certifications"]
    if not certs:
        return "*Add verified certifications here.*"
    rows = ["| Certification | Issuer | Year | Credential |", "|---|---|---|---|"]
    for c in certs:
        link = f"[Verify ↗]({c['url']})" if c.get("url") else DASH
        rows.append(f"| {esc(c['name'])} | {esc(c['issuer'])} | {cell(c.get('year'))} | {link} |")
    return "\n".join(rows)


def render_coding(d):
    profiles = d["coding_profiles"]
    if not profiles:
        return "*Add your LeetCode / CodeChef / HackerRank / Codeforces profile links here. Statistics are only shown when they can be fetched reliably.*"
    rows = ["| Platform | Handle | Profile |", "|---|---|---|"]
    rows += [f"| {esc(p['platform'])} | {esc(p['handle'])} | [Open ↗]({p['url']}) |" for p in profiles]
    return "\n".join(rows)


def render_oss(d):
    prs = d["open_source"]
    if not prs:
        return (
            "**Open Source Journey.** Merged upstream contributions will be listed here, with real PR links only. "
            "Until then, my public repositories above are the work to look at."
        )
    rows = ["| Repository | PR | Description |", "|---|---|---|"]
    for pr in prs:
        rows.append(f"| [{esc(pr['repo'])}](https://github.com/{pr['repo']}) | [#{pr['number']}]({pr['url']}) | {esc(pr['description'])} |")
    return "\n".join(rows)



RENDERERS = {
    "SOCIAL": lambda d, s: render_social(d),
    "FOCUS": lambda d, s: render_focus(d),
    "PROJECTS": lambda d, s: render_projects(d),
    "HEALTH": render_health,
    "PRACTICES": lambda d, s: render_practices(d),
    "DEVTOOLS": lambda d, s: render_devtools(d),
    "OSS": lambda d, s: render_oss(d),
    "STACK": lambda d, s: render_stack(d),
    "CERTS": lambda d, s: render_certs(d),
    "CODING": lambda d, s: render_coding(d),
    "LEARNING": lambda d, s: render_learning(d),
    "ROADMAP": lambda d, s: render_roadmap(d),
    "CONTACT": lambda d, s: render_social(d),
}


def apply_markers(text: str, data: dict, snap: dict) -> str:
    for name, fn in RENDERERS.items():
        pattern = re.compile(rf"(<!-- BEGIN:{name} -->)(.*?)(<!-- END:{name} -->)", re.DOTALL)
        if not pattern.search(text):
            raise SystemExit(f"README.md is missing the marker pair BEGIN:{name} / END:{name}")
        body = fn(data, snap)
        text = pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text, count=1)
    return text


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--offline", action="store_true", help="do not call the GitHub API")
    ap.add_argument("--check", action="store_true", help="exit 1 if README.md would change")
    ap.add_argument("--readme", default=str(ROOT / "README.md"))
    ap.add_argument("--data", default=str(ROOT / "data" / "profile.json"))
    ap.add_argument("--snapshot", default=str(ROOT / "data" / "snapshot.json"))
    args = ap.parse_args()

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    snap_path = Path(args.snapshot)
    snap = json.loads(snap_path.read_text(encoding="utf-8")) if snap_path.exists() else {"repos": {}}

    snap, updated = refresh_snapshot(data, snap, args.offline or args.check)
    readme_path = Path(args.readme)
    old = readme_path.read_text(encoding="utf-8")
    new = apply_markers(old, data, snap)

    if args.check:
        if new != old:
            print("README.md is out of date. Run: python scripts/update_readme.py", file=sys.stderr)
            return 1
        print("README.md is up to date.")
        return 0

    if updated:
        snap_path.write_text(json.dumps(snap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if new != old:
        readme_path.write_text(new, encoding="utf-8")
        print(f"README.md updated ({updated} repositories refreshed from the API).")
    else:
        print(f"README.md already current ({updated} repositories refreshed from the API).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
