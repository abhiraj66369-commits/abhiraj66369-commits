# Feature parity with the reference profile

The reference is a mature profile README with animated header, project tables, certification badges, competitive-programming cards and a generated metrics set. This repository reproduces the **functional equivalent** of each feature using its own design, data and code. No text, identity, statistics, images or claims were copied.

`scripts/validate_profile.py` re-checks this table on every push. Framework `PASS*` means implemented and statically valid, provable after the first Actions run.

| # | Reference feature | Equivalent here | How it is built |
|---|---|---|---|
| 1 | Animated typing hero | Self-hosted animated SVG banner | `assets/hero.svg`, CSS keyframes, reduced-motion safe |
| 2 | Professional intro | Intro blockquote grounded in real repos | `README.md` |
| 3-4 | Featured projects and descriptions | Generated table | `data/profile.json`, `scripts/update_readme.py` |
| 5 | Technology badges | Grouped icon rows plus text names | `skillicons.dev`, only evidenced skills |
| 6 | Live demo links | Demo column | links come from each repo's About field |
| 7 | Developer / community tools | Developer Tools table | `dev_tools` in data |
| 8 | Open-source PR table | Real-PR table or "Open Source Journey" | `open_source` in data |
| 9-11 | Portfolio, resume, contact | Badge row, shown only when a link exists | `links` in data |
| 12 | Tech stack | Eight-group table | `skills` in data |
| 13 | GitHub stats and top languages | Self-rendered cards | Metrics workflow, committed SVGs |
| 14 | Contribution streak | Streak card | Metrics workflow (`plugin_streak`) |
| 15-16, 23 | DSA and coding-platform stats | Profile-link table, no scraped numbers | `coding_profiles` in data |
| 17 | Certifications | Verified-only table with placeholder | `certifications`, `certificates/` |
| 18, 22 | Achievements | Achievements card | Metrics workflow |
| 19 | Detailed metrics (collapsible) | `<details>` block | `README.md` |
| 20 | Isometric calendar | Isometric card | Metrics workflow |
| 21 | Coding habits | Habits card | Metrics workflow |
| 24 | Starred topics | Topics card | Metrics workflow |
| 25 | Contribution snake | Snake on `output` branch | Snake workflow |
| 26 | Animated footer | Self-hosted animated SVG | `assets/footer.svg` |

## Reference features intentionally replaced

| Reference feature | Why not copied | Replacement |
|---|---|---|
| Hosted typing and banner generators | Third-party servers; can be slow or rate-limited | Self-hosted SVG |
| Hosted stats and streak cards | Public instances are often rate-limited | Metrics workflow output committed to the repo |
| Profile view counter | Third-party tracking with little value | None |
| LeetCode card, typing-speed card, Holopin, credential badges | Need accounts and credentials that are not yours yet | `coding_profiles` and `certifications` frameworks |
| Star-badge refresh workflow | Repository-health table with plain text covers it | Profile update workflow |
| Image optimiser and Renovate config | Few binary assets; Dependabot is built in | `.github/dependabot.yml` |

## Additions beyond the reference

- AI and engineering focus table with Built / Planned status, so nothing is overclaimed.
- Architecture diagrams (Mermaid) with dashed nodes for planned work.
- Repository-health table: stars, forks, open issues and PRs, CI result, latest release, last push.
- Single data file plus a generator, so updating the profile never means editing generated Markdown.
- Offline validator with PASS / FAIL output, run in CI.
- Accessibility: alt text on every image, one H1, no skipped heading levels, reduced-motion support.
- Secret scanning, Dependabot, least-privilege workflow permissions.
