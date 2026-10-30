# EquityLens - important conversation context

Updated 2026-10-30 (Asia/Calcutta).

This is a curated handover of important project discussion, not a verbatim chat export. Unrelated coursework and personal/browser screenshots are intentionally excluded.

## User and working preferences

- Final-year computer science engineering student building a resume-worthy AI Stock Research Assistant.
- Wants to learn while building, with simple explanations and guided implementation.
- Understand, implement, verify, then record a useful commit. Do not replace learning with unexplained large code drops.
- User asked to keep the detailed weekly plan and important project context in the project folder.

## Repository and workspace

- Existing repository: https://github.com/abhinandanmalik4-stack/equitylens
- Owner: abhinandanmalik4-stack; default branch: main; visibility: PRIVATE.
- Reuse this repository; never create a replacement or make it public without explicit instruction.
- Local checkout: E:\gpt\equitylens. It was cloned on October 26 and had a clean main branch tracking origin/main before this documentation change.
- E:\gpt contains unrelated coursework and other artifacts. Work inside the dedicated checkout; never stage the parent directory.
- The original E:\gpt\EquityLens-Project.md is an older standalone copy. The checkout's project brief is the active version.

## Important user instructions and decisions

1. Initial project handover: preserve the private repository, verify current local/remote state, and wait before implementation.
2. User asked for a useful GitHub description rather than only calling it a final-year project; README and About were expanded.
3. User requested daily commits and cares about contribution streaks. Only real work counts; do not create empty/filler commits, fabricate activity or backdate history.
4. User chose Indian stocks first and US support in the future. Keep exchange/currency/provider metadata extensible.
5. User asked whether the project can be made without handwritten HTML, CSS and JavaScript and accepted a Python-first approach.
6. Current stack direction: Streamlit UI, Plotly charts, pandas/NumPy data processing, SQLite persistence, scikit-learn forecasting and Python retrieval/LLM integration.
7. Earlier React/Lightweight Charts and separate FastAPI suggestions are superseded for the first version. FastAPI is optional later if a separate API is useful.
8. User accepted week-wise planning. Eight weeks at approximately 1-2 hours/day is a planning assumption, not a completion guarantee or fixed start date.

## Intended experience

- Left: company search, stock selection and watchlist.
- Centre: latest available price, daily change, volume and interactive historical chart/ranges.
- Below: historical comparisons and evaluated forecasts with uncertainty.
- Right: research chat about company history, business development, results, risks and outlook, supported by cited reliable sources.
- Native Streamlit layouts are the first approach; exact highly custom frontend behavior may be limited.

## Data and research integrity

- Prices must come from data functions/provider responses with source and as-of information.
- Sample data must be visibly labelled synthetic; never silently substitute it for unavailable market data.
- Forecasts come from reproducible evaluated models. Compare with a simple baseline using chronological splits and no future leakage.
- Explain forecast errors and interval limitations; never invent accuracy, certainty or investment results.
- Company answers cite actual reliable documents. Missing evidence should produce an explicit limitation rather than a fabricated answer.
- Initial data scope: proposed 10-20 stocks on one Indian exchange, daily history, not a promise of live quotes.
- Reliable provider access, display rights and possible paid live-data requirements remain to be evaluated.

## Daily automation - observed configuration

- Automation ID: daily-equitylens-development.
- Created and observed ACTIVE on October 26; daily at 10:00 AM in the intended IST schedule.
- Returns to this chat, aiming for up to 10 useful commits including any existing commits for that day.
- The saved prompt was updated on October 27 to explicitly use the user's Python/Streamlit direction, consult the roadmap/context, and avoid duplicate work after the daily target is already pushed. The 10:00 AM schedule and ACTIVE state were preserved.
- The schedule is not a guarantee of execution or successful pushes; local tasks need the computer/app available and appropriate access.
- Report genuine shortfalls and blockers. No filler, artificial splitting, backdating or forced history changes.
- scripts/Add-DailyUpdate.ps1 only appends a manual progress entry. It is not itself a scheduler and does not commit or push.
- Private-contribution display was enabled in the user's GitHub screenshots. Do not alter repository visibility to affect the graph. A commit is not proof that a profile graph has updated.

## Known completed work versus planned work

Completed: initial project brief, private GitHub repository, expanded README/About, dated progress entries, manual log script, local clone, documentation/roadmap, isolated Python environment, exchange-aware demo catalogue, validated synthetic daily data, price calculations, local SQLite watchlist, Plotly charts/comparison and native Streamlit dashboard. The first implementation has 19 passing local automated tests and a Windows/Linux GitHub Actions workflow.

Not yet implemented: real data provider, trained/evaluated forecasts, document retrieval, chatbot, user authentication or deployment. Browser layout/gestures have not been visually verified; local tests are headless. CI configuration is not proof that remote jobs passed. Do not describe planned features as completed.

## Immediate next task

October 30 learning update: docs/FOUNDATION_PRACTICE.md now provides a short exercise and checked answers using only the existing invented six-row CSV, including previous-close/window returns, observation intervals, drawdown, an empty window and a rejected high. Calculations and the offline inspection report were executed against current code. This prepares the student review; it does not claim the student completed it. The latest full automated suite result remains 44 passes from October 29; application behavior was not changed today.

October 29 maintenance update: CSV import rejects incorrect argument types with controlled validation errors before reading observations. Added regression checks for the 10,000-row limit and inconsistent/unknown demo markers. All 44 local tests pass, as does the dependency check. One coherent commit records the fix, checks and documentation; no quota commits were added. The student walkthrough and provider selection below remain pending.

October 28 maintenance update: finite arithmetic and instrument/history-metadata boundary handling were hardened. The full local suite now has 41 passing tests, with pip compatibility checks passing. This focused maintenance run contains three commits including the progress documentation; the ten-commit aspiration was not padded with filler. The next major milestone remains student walkthrough and exchange/data-source selection; do not leap ahead to unrequested paid integration or pretend that walkthrough happened.

October 27 update: bounded CSV import/export, source identity, calendar windows, historical horizons/drawdown, offline inspection and watchlist-navigation repairs are implemented. The current suite has 36 passing local tests. Uploads are unverified; direct provider integration is still pending. Use CSV_IMPORT_GUIDE.md and DATA_PROVIDER_REVIEW.md for the next review. Earlier 19-test descriptions below/above refer to the October 26 milestone, not the current total.

Walk through docs/RUN_AND_LEARN.md with the student and explain the implemented foundation. Next implementation milestone is provider selection/integration for historical Indian prices, after verifying costs and usage rights. The student has not yet demonstrated learning these features merely because the assistant wrote them.

## Keep this context useful

After a material decision, update DECISIONS.md and the project brief. After actual work, append DAILY_PROGRESS.md. Revise the roadmap if scope or effort changes. Do not store passwords, API keys, financial account data or unrelated personal information here.
