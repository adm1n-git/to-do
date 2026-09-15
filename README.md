# Study & Writing Tools

A web app that bundles a small collection of study and writing utilities:

- **Recall** — a spaced-repetition study tracker. Add topics you're learning, and Recall schedules review reminders at increasing intervals (1, 3, 7, 14, 30, 90, 180, and 365 days) based on the natural pattern of memory decay, so you can mark topics as remembered or forgotten and keep the schedule up to date.
- **Fix Text** — a grammar-correction and rephrasing assistant. Paste any text to get it cleaned up for spelling, grammar, and punctuation, plus an alternate rephrased version for tone and clarity, powered by an LLM through LangChain.

The app is gated behind Microsoft account login (via the built-in `st.login`/OpenID Connect auth) before any of the tools are accessible.

## Project Structure

```
to-do/
├── app.py                              # Entry point: handles login and page navigation
├── requirements.txt                    # Python dependencies
├── data/                               # SQLite database lives here (gitignored)
└── scripts/
    ├── index.py                        # Home page
    ├── recall/
    │   ├── update.py                   # Add a new topic to track
    │   └── tasks.py                    # Review topics due for recall
    ├── fix-text/
    │   └── fix-text.py                 # Grammar-fix / rephrase tool
    └── support/
        ├── microsoft_graph_api/        # Helper for sending mail via MS Graph API
        └── sqlite_database/            # Lightweight SQLite wrapper class
```

## Requirements

- Python 3.9+
- A Microsoft (Azure AD) app registration, used for Streamlit's login flow
- An API key from OpenAI and/or Anthropic (whichever model provider you set in `MODEL`)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/adm1n-git/to-do.git
   cd to-do
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The app needs two configuration files that are **not** committed to the repository (they're listed in `.gitignore`): a `.env` file at the project root, and a `.streamlit/secrets.toml` file used by Streamlit's authentication feature. Create both before running the app.

### 1. Register a Microsoft Azure AD application

The app's login flow authenticates users against a Microsoft identity provider, so you first need an app registration in the [Azure Portal](https://portal.azure.com/):

1. Go to **Azure Active Directory → App registrations → New registration**.
2. Choose a name (e.g. `to-do-app`), and under **Supported account types** select **Personal Microsoft accounts only** (the app uses the `consumers` tenant endpoint).
3. Under **Redirect URI**, add a **Web** platform redirect URI pointing at your app, e.g. `http://localhost:8501/oauth2callback` for local development.
4. After creation, note the **Application (client) ID** — this is your `client_id`.
5. Go to **Certificates & secrets → New client secret**, create one, and copy its **value** immediately (it won't be shown again) — this is your `client_secret`.

### 2. Create the `.env` file

Create a file named `.env` in the project root:

```dotenv
PROJECT_DIR=
DB_DIR=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
MODEL=
```

| Variable            | Description                                                                                                                                                     |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `PROJECT_DIR`       | Absolute path to the repository's root directory. It's added to `sys.path` so the `scripts/recall/*.py` pages can `import support`. Example: `/home/user/to-do`. |
| `DB_DIR`            | Path to the SQLite database file used to store Recall topics, e.g. `/home/user/to-do/data/to_do.db`. The `data/` directory already exists (kept via `.gitkeep`); the `.db` file itself is created automatically on first run. |
| `OPENAI_API_KEY`    | Your OpenAI API key. Required only if `MODEL` points to an OpenAI model.                                                                                        |
| `ANTHROPIC_API_KEY` | Your Anthropic API key. Required only if `MODEL` points to an Anthropic (Claude) model.                                                                         |
| `MODEL`             | The chat model identifier passed to LangChain's `init_chat_model`, used by the Fix Text tool. Examples: `openai:gpt-4o-mini` or `anthropic:claude-sonnet-4-5`. |

Example:

```dotenv
PROJECT_DIR=/home/user/to-do
DB_DIR=/home/user/to-do/data/to_do.db
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MODEL=openai:gpt-4o-mini
```

### 3. Create the `.streamlit/secrets.toml` file

Create a `.streamlit` directory in the project root (if it doesn't already exist) and add a `secrets.toml` file inside it:

```bash
mkdir -p .streamlit
```

`.streamlit/secrets.toml`:

```toml
[auth]
redirect_uri = ""
cookie_secret = ""
client_id = ""
client_secret = ""
server_metadata_url = "https://login.microsoftonline.com/consumers/v2.0/.well-known/openid-configuration"
```

| Key                    | Description                                                                                                                                  |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `redirect_uri`          | Must match, exactly, one of the redirect URIs configured on the Azure app registration. Example for local dev: `http://localhost:8501/oauth2callback`. |
| `cookie_secret`         | A random secret string used by Streamlit to encrypt the auth session cookie. Generate one, for example: `python -c "import secrets; print(secrets.token_hex(32))"`. |
| `client_id`             | The **Application (client) ID** from your Azure app registration.                                                                             |
| `client_secret`         | The **client secret value** generated for your Azure app registration.                                                                        |
| `server_metadata_url`   | OpenID Connect discovery URL. Leave as-is — it points at Microsoft's `consumers` (personal accounts) tenant metadata endpoint.               |

Example:

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "a1b2c3d4e5f6...replace-with-a-real-random-string"
client_id = "00000000-0000-0000-0000-000000000000"
client_secret = "your-azure-client-secret-value"
server_metadata_url = "https://login.microsoftonline.com/consumers/v2.0/.well-known/openid-configuration"
```

> ⚠️ Both `.env` and `.streamlit/secrets.toml` contain sensitive credentials. Never commit them — they're already excluded via `.gitignore`.

## Running the App

Once `.env` and `.streamlit/secrets.toml` are configured, start the app from the project root:

```bash
streamlit run app.py
```

The app will open in your browser (default: `http://localhost:8501`). You'll be prompted to log in with a Microsoft account; once authenticated, you'll have access to the Home, Recall, and Fix Text pages.

## Notes

- The `scripts/support/microsoft_graph_api` module (used for sending email via Microsoft Graph) additionally expects `APPLICATION_ID` and `CLIENT_SECRET` environment variables if you use its `send_message` function directly — set these in `.env` as well if needed.
- The SQLite database and its `to_do` table are created automatically the first time a Recall page runs, using the path from `DB_DIR`.
