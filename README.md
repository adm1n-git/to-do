# Recall — Spaced Repetition Study Tracker

Recall is a Streamlit-based study companion that helps you retain what you learn — not just for the next test, but for the long run.

Instead of cramming and forgetting, Recall nudges you to revisit topics at expanding intervals based on how memory naturally fades over time. Add what you're studying, and Recall tracks when it's time to review — from the next day out to a full year later — so what you learn actually sticks.

## Project structure

```
to-do/
├── scripts/
│   ├── index.py      # Home page
│   ├── update.py     # Update / review workflow
│   └── tasks.py      # Task management page
├── support/           # Supporting utilities/assets
├── ui.py              # App entry point (Streamlit navigation & config)
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
└── .gitignore
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/adm1n-git/to-do.git
   cd to-do
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the app locally with:

```bash
streamlit run ui.py
```

Then open the local URL Streamlit prints in your terminal (typically `http://localhost:8501`).

## How it works

1. **Add a topic** you're studying.
2. Recall schedules your first review for the next day.
3. Each time you successfully recall the material, the interval expands, reinforcing long-term retention while minimizing unnecessary review time.
4. If you forget a topic, it resets to an earlier interval so you get more frequent practice until it sticks.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/adm1n-git/to-do/issues) or open a pull request.

## License

No license specified yet — consider adding one (e.g. MIT) if you plan to share or accept contributions.
