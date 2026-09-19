# Contributing to Gamico Claim

Thanks for helping improve Gamico Claim.

## Prerequisites

- Python 3.10+
- A local clone of this repository
- Installed dependencies from `requirements.txt`
- Linux contributors: `xvfb-run` (Xvfb package)
- Windows contributors: PowerShell and an interactive desktop session for browser-driven runs

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
patchright install chromium
```

3. (Linux only) install Xvfb:

```bash
sudo apt install xvfb
```

## Safe Local Workflow

`Config/config.json` stores Discord webhook and Epic session data. Treat it as sensitive at all times.

- Never commit, upload, or share `Config/config.json`.
- Use your own local credentials only.
- Before sharing logs/screenshots, redact webhook URLs, session values, tokens, and cookies.

### First-time setup flow

Run:

- Linux: `.venv/bin/python main.py`
- Windows: `.\.venv\Scripts\python.exe main.py`

Then complete Discord and Epic login setup in the GUI. This creates local session/config data.

### Claim workflow

Run:

- Linux: `./run.sh`
- Windows: `.\run_windows.bat`

Do not automate CAPTCHA bypass or account-verification bypass. Complete any required checks manually.

## Coding and Style Guidance

- Keep changes focused and minimal.
- Follow existing Python style in the repository (clear naming, small functions, readable control flow).
- Prefer standard library and existing dependencies over introducing new packages.
- Update documentation when behavior or setup guidance changes.

## Testing Guidance

This repository currently has no dedicated automated test suite.

When contributing code changes:

- Validate the specific changed path locally (for example, config loading/saving, launcher behavior, notification formatting).
- Avoid real Epic claims during validation where possible.
- If adding tests, prefer mocked/stubbed network responses and fixtures over live account actions.

## Issues and Pull Requests

### Issues

Please include:

- Clear reproduction steps
- Expected vs actual behavior
- OS and Python version
- Sanitized logs (no secrets)

### Pull Requests

- Keep PRs small and scoped to one problem.
- Reference related issues when applicable.
- Include validation steps performed.
- Update docs/templates when required by the change.
- Confirm no secrets are included in changed files.

## Useful Contribution Areas

- Documentation clarity and onboarding
- Testing and mock coverage
- Windows reliability/support improvements
- Linux scheduling and cron guidance
- Error handling and recovery messages
- Discord notification formatting and resilience
