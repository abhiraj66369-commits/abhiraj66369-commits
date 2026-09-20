# Security policy

This repository contains no application code and no secrets. It is a static profile plus automation.

## Reporting a problem

If you notice a leaked credential, a malicious dependency or a vulnerable workflow here, please open a
[private security advisory](https://github.com/abhiraj66369-commits/abhiraj66369-commits/security/advisories/new)
rather than a public issue.

## Practices used here

- Workflows declare least-privilege `permissions` and never print secrets.
- The only secret used is `METRICS_TOKEN`, stored as a GitHub Actions secret and never committed.
- Bot commits use `GITHUB_TOKEN`, which cannot trigger further workflows, so there are no loops.
- Third-party actions are limited to well-known maintainers and kept current by Dependabot.
- `.env` files are ignored by Git; example files must never hold real values.
- Gitleaks runs on every push and pull request.
