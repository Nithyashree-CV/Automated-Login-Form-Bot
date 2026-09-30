# Automated Login & Form Bot

Automates logging into a test website with both valid and invalid credentials, verifying the success/failure messages.

Target site: https://the-internet.herokuapp.com/login (a public demo site).

## Setup

Requires Python 3 and Google Chrome. Selenium 4.6+ downloads the matching driver automatically.

```bash
pip install -r requirements.txt
```

## Run

```bash
python login_bot.py
```

The bot runs three checks and exits non-zero if any fail:

1. Valid credentials -> "You logged into a secure area!"
2. Invalid username -> "Your username is invalid!"
3. Invalid password -> "Your password is invalid!"

Set `headless=False` in `LoginBot()` to watch the browser.
