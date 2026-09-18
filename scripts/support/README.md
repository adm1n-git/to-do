# Support

A small collection of user-defined Python classes and functions used to simplify scripts across projects. It bundles helpers for sending mail through the Microsoft Graph API, working with a SQLite database, and converting between `datetime` objects and strings.

## Contents

```
support/
├── __init__.py
├── requirements.txt
├── microsoft_graph_api/
│   └── microsoft_graph_api.py   # OAuth2 + send mail via Microsoft Graph
├── sqlite_database/
│   └── sqlite_database.py       # Thin wrapper around sqlite3
└── others/
    └── dt.py                    # datetime <-> string helpers
```

The package `__init__.py` re-exports the main entry points, so you can import directly from `support`:

```python
from support import send_message, sqlite_database, dt2str, str2dt
```

## Installation

Clone the repo as a subfolder/submodule of your project (it's imported as the `support` package), then install its dependency:

```bash
git clone https://github.com/adm1n-git/support.git
pip install -r support/requirements.txt
```

**Dependency:** [`msal`](https://pypi.org/project/msal/) (Microsoft Authentication Library), used by the Microsoft Graph module.

## Modules

### `microsoft_graph_api`

Authenticates against Azure AD (via `msal`) and sends email through the Microsoft Graph API, with optional file attachments.

**Setup:** set the following environment variables before use:

| Variable | Description |
|---|---|
| `APPLICATION_ID` | Azure AD application (client) ID |
| `CLIENT_SECRET` | Azure AD application client secret |

On first run, the script opens a browser window for the OAuth2 authorization-code flow and prompts for the authorization code on the command line. The resulting refresh token is cached in `auth/refresh_token.txt` (created automatically) so subsequent runs can silently refresh the access token.

**Usage:**

```python
from support import send_message

send_message(
    to_recipients=["someone@example.com"],
    subject_text="Hello",
    body_text="<p>This is an HTML email body.</p>",
    attachments=["/path/to/file.pdf"],  # optional
)
```

Requires the Graph scopes `User.Read`, `Mail.ReadWrite`, and `Mail.Send`, which are requested automatically.

### `sqlite_database`

A minimal wrapper around Python's built-in `sqlite3` module that returns query results as a list of dictionaries.

**Usage:**

```python
from support import sqlite_database

db = sqlite_database("path/to/database.db")

# SELECT queries return a list of dicts
rows = db.exec_query("SELECT * FROM users WHERE id = :id", {"id": 1})

# Non-SELECT queries (INSERT/UPDATE/DELETE/CREATE) return None
db.exec_query(
    "INSERT INTO users (name) VALUES (:name)",
    {"name": "Ada"},
)

db.close()
```

### `others.dt`

Small helpers for converting between `datetime` objects and their string representation (`%Y-%m-%d %H:%M:%S`).

```python
from support import dt2str, str2dt
from datetime import datetime

dt2str(datetime.now())          # -> "2026-09-18 14:30:00"
str2dt("2026-09-18 14:30:00")   # -> datetime(2026, 9, 18, 14, 30, 0)
```

## Notes

- The Microsoft Graph module writes a plaintext refresh token to `auth/refresh_token.txt`; treat this file as a secret and keep it out of version control (add it to `.gitignore`).
- `sqlite_database` detects `SELECT` queries by checking whether the trimmed query string starts with `SELECT`; other statement types will not return fetched rows.

## License

Copyright (c) 2026 Ayyappan Mani. All rights reserved.

This code is proprietary and confidential. No part of it may be copied, modified, distributed, or used without prior written permission from the copyright holder.