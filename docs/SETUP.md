# Setup guide

Everything below happens in the repository `abhiraj66369-commits/abhiraj66369-commits` (the special repository whose README shows on your profile).

## 1. Install the files (safely)

The README currently shown on your profile is GitHub's default template. Back the repository up before overwriting it, and check for any other files in it first.

```bash
git clone https://github.com/abhiraj66369-commits/abhiraj66369-commits
cd abhiraj66369-commits
git switch -c backup/original-readme && git push -u origin backup/original-readme
git switch main
# copy the contents of this package over the clone (keep the .github folder!)
git add -A
git commit -m "feat: redesign profile"
git push
```

Only `README.md` is replaced by this package; any other file already in the repository is left alone unless it has the same path.

## 2. Repository secrets

| Secret | Needed by | How to create |
|---|---|---|
| `METRICS_TOKEN` | Metrics workflow only | GitHub, Settings, Developer settings, Personal access tokens (classic), scope `read:user`. Add `repo` only if you want private activity counted. Then repository Settings, Secrets and variables, Actions, New repository secret. |

Snake, Profile update and Quality use the built-in `GITHUB_TOKEN`. No other secrets exist.

## 3. Repository settings

1. Settings, Actions, General: allow all actions and reusable workflows, and under *Workflow permissions* choose **Read and write permissions**.
2. Settings, Code security: enable *Dependabot alerts*, *Dependabot security updates* and *Secret scanning* (free for public repositories).
3. Profile: on your profile page, pin your four flagship repositories.
4. Keep the repository **public**, otherwise the README does not appear on your profile.

## 4. Enable each automation (first run)

Go to the Actions tab and run these once with *Run workflow*, in this order:

1. **Profile update**: fills the repository-health table with live numbers.
2. **Snake**: creates the `output` branch that the README image reads.
3. **Metrics**: renders the seven cards into `metrics/` (requires `METRICS_TOKEN`).
4. **Quality**: should go green; link and Markdown checks are advisory.

After that they run on their own: snake and metrics daily, profile update weekly and whenever `data/profile.json` changes.

## 5. Updating the profile later

- Edit `data/profile.json`, commit, and the Profile update workflow refreshes the README. Never edit text between `<!-- BEGIN:... -->` and `<!-- END:... -->` by hand; it will be overwritten.
- Static prose (intro, headings, architecture diagrams) lives in `README.md` outside those markers.
- To preview locally: `python scripts/update_readme.py --offline`, then `python scripts/validate_profile.py`.

## 6. Content that needs your input

The build never invents these. Add them to `data/profile.json` when they are real.

| Field | What to add |
|---|---|
| `links.portfolio`, `links.resume`, `links.linkedin`, `links.email` | Real URLs. Use an email address you are happy to publish. |
| `projects` StudyOS and KANHAIYA | Repository name, one-line description, tech list; then remove `"hidden": true`. |
| `projects[].status` | The statuses are working assumptions; change them to the truth. |
| `skills` with `"confirmed": false` (Python, C++, Prisma, Docker, RAG / vector search) | Set `confirmed` to `true` and fill `evidence` with the repository that proves it. |
| `certifications` | Only real certificates, with a verification URL. |
| `coding_profiles` | LeetCode, CodeChef and similar profile URLs. Numbers are never scraped or typed. |
| `open_source` | Merged pull requests only: repository, PR number, URL, description. |
| `learning` | What you are studying right now. |
| `metrics.timezone` and `TZ_NAME` in `metrics.yml` | Set to your timezone; it is assumed to be Asia/Kolkata. |

## 7. Third-party services

| Service | Used for | Runtime dependency for visitors? |
|---|---|---|
| GitHub Actions, GitHub REST API | All automation and repository stats | No (results are committed) |
| `lowlighter/metrics` | Stats, streak, calendar, habits, achievements, topics, languages | No (renders into your repo) |
| `Platane/snk` | Contribution snake | No (renders to your `output` branch) |
| shields.io | Static link badges | Yes |
| skillicons.dev | Tech stack icon rows | Yes; names are also printed as text |
| Mermaid (built into GitHub) | Architecture diagrams | No |
| Gitleaks, lychee, markdownlint, actionlint | Quality checks in CI | No |

Deliberately not used: the public github-readme-stats, streak-stats and capsule-render servers (frequent rate limits), profile-view counters (third-party tracking), and any LeetCode or typing-speed cards (no verified accounts).

## 8. Security considerations

- The only credential is `METRICS_TOKEN`; keep its scope minimal and rotate it if it ever appears in a log or file.
- Workflows request only the permissions they use; bot commits carry `[skip ci]` and use `GITHUB_TOKEN`, which cannot start other workflows.
- Never put real values in files named `.env*`; `.gitignore` blocks them. Commit `.env.example` with placeholders only.
- Do not add government ID numbers, phone numbers or home addresses to certificates or the README.

## 9. Troubleshooting

- **Snake image is broken:** the `output` branch appears only after the Snake workflow has run once.
- **Metrics cards still say "Placeholder":** `METRICS_TOKEN` is missing or the Metrics run failed. Open the run log.
- **Metrics run fails at "Commit rendered cards":** the render folder was not where the step expects. On each `lowlighter/metrics` step change `output_action: none` to `output_action: commit` and remove the final commit step.
- **Quality shows a Markdown lint warning:** advisory only; run `npx markdownlint-cli2 README.md` locally to see it.

## 10. Verification checklist

- [ ] `python scripts/validate_profile.py` reports no FAIL.
- [ ] All four workflows have a green run in the Actions tab.
- [ ] The `output` branch exists and the snake renders on your profile.
- [ ] `metrics/*.svg` no longer contain the word "Placeholder".
- [ ] The repository-health table shows real numbers (or dashes), with a recent snapshot date.
- [ ] Profile page in a private window: dark mode and light mode both look right.
- [ ] Every link in the README opens the intended page.
- [ ] Section 6 items are either filled with real data or intentionally left empty.
