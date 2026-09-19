# Security Policy

## Sensitive Data

The following may contain sensitive information and must be handled carefully:

- `Config/config.json` (Discord webhook URL and Epic session data)
- Browser/session data used for Epic login
- Discord webhook URLs
- API keys (including optional `RAWG_API_KEY`)
- Logs, terminal output, screenshots, and screen recordings

## Never Commit or Share

Do **not** commit, upload, or publicly share:

- `Config/config.json`
- Session exports, cookies, or browser profile data
- Webhook URLs or API keys
- Unredacted logs/screenshots that reveal credentials, tokens, or account/session identifiers

## If Data Is Exposed

If a webhook, API key, or session value is exposed:

1. Revoke or rotate the exposed webhook/key immediately.
2. Recreate local config/session data (`Config/config.json`) with fresh values.
3. Remove exposed data from repository history and force-rotate affected secrets.
4. Review automation logs/screenshots and delete unsafe copies.

## Account Protection

CAPTCHA and account-verification protections must not be bypassed.

If verification is required during a run, complete it manually and retry later.

## Reporting a Vulnerability

Please report security issues privately through GitHub's private vulnerability reporting for this repository:

1. Open the repository on GitHub.
2. Go to the **Security** tab.
3. Use **Report a vulnerability** (GitHub Security Advisory draft) to contact the maintainer privately.

Avoid filing sensitive vulnerability details in public issues.
