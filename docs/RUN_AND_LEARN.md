# Run EquityLens and understand the first milestone

## What works

A Python/Streamlit local demo with ten Indian company identities, search, line/candlestick price charts, volume, historical-range metrics, aligned comparisons, a persistent single-user watchlist, and explicitly labelled synthetic CSV exports.

Built-in prices/volumes are invented fixtures ending 2026-10-23. The app also supports local CSV imports with unverified provenance, calendar windows and historical statistics; see CSV_IMPORT_GUIDE.md. No direct market provider, trained forecast or AI chatbot is configured. No API key is needed. Do not interpret sample paths as company performance.

## First-time setup

Python 3.13 is the locally tested version. Open a terminal in the project folder:

```powershell
cd E:\gpt\equitylens
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt -e .
```

`pyproject.toml` declares supported dependency ranges; `requirements-lock.txt` captures the exact tested dependency versions. The editable install makes the `src/equitylens` package importable. The environment is isolated and ignored by Git; no activation or PowerShell execution-policy change is required.

The environment is already installed on the current machine. On a new machine, install Python first, then follow the steps above. If `python` selects a different installation, use that machine's Python 3.13 launcher/path.

## Start the app

```powershell
.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Open the Local URL printed by Streamlit, usually http://127.0.0.1:8501. Stop the server with Ctrl+C. Run from the project root so the checked-in theme config is loaded. This is a local preview, not an internet deployment.

## Five-minute walkthrough

1. Read the demo notice. Find the source and last observation date below the chart.
2. Search for Infosys or banking; select a company and inspect the changed chart and metrics.
3. Switch Line/Candlestick and 1M/3M/6M/1Y/All. These shortcuts count observations, not exact calendar months.
4. Save a company to the watchlist. Restart the app and confirm it is still saved. Remove it and check it disappears.
5. Select another company for comparison. Both paths begin at 100 on matching dates.
6. Show the underlying observations and download a demo CSV; its columns include source, currency and `is_demo=True`.
7. Notice that research and forecasting panels explicitly describe future milestones instead of fabricating answers.

## Run checks

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\python.exe -m pip check
```

The current suite has 36 tests (October 27), checking OHLCV, CSV limits/provenance, export roundtrips, calculations, calendar windows, historical statistics, file inspection, SQLite and app interactions. Streamlit may log a harmless missing-ScriptRunContext warning from the headless testing harness.

GitHub Actions is configured for Python 3.13 on Windows and Linux. Local Windows test success is not evidence that the remote jobs passed: inspect the Actions tab after pushing. Headless app tests do not verify actual browser layout, pan/zoom gestures, hover rendering or mobile appearance; those still need visual review.

## Where your watchlist lives

Default: `data/watchlist.db` inside the checkout, excluded from Git. To choose a different location:

```powershell
$env:EQUITYLENS_DB_PATH = 'E:\gpt\equitylens\data\my-watchlist.db'
.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

This is one local watchlist, shared by anyone using that database. Do not deploy it as an authenticated multi-user service. Tests create isolated temporary databases and do not touch your saved watchlist.

## Understand the code in this order

| File | What to understand | Exercise |
| --- | --- | --- |
| src/equitylens/catalog.py | Dataclasses, identity, filtering and exchange/currency fields | Explain why symbol alone is not a global identity. |
| src/equitylens/providers.py | A provider interface, metadata, validation and deterministic fixtures | Trace one invalid high/low value and explain its rejection. |
| src/equitylens/analytics.py | DataFrame slicing, percentage changes and common dates | Calculate a change from 110 to 99 by hand and compare with the test. |
| src/equitylens/watchlist.py | SQLite, unique keys, parameterized statements and connection cleanup | Explain how duplicate saves and restarts are handled. |
| src/equitylens/charts.py | Plotly figures built from passed data | Trace one close value from the DataFrame into the line trace. |
| app.py | Widgets, session state, caching and composition | Follow a company selection through provider, metrics and chart. |
| tests/ | Expected outcomes and edge cases | Explain why tests include missing dates, bad volume and storage failure. |

Do the walkthrough together before adding more features. Code implemented by the assistant is not evidence that the student has learned it yet.

## Next milestone

Compare Indian historical-data providers for coverage, cost, adjustment policy, limits and display rights. Select one before integrating real prices. Keep US support behind the same exchange-aware provider contract. See WEEKLY_ROADMAP.md for the remaining stages.
