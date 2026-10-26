# EquityLens
## AI Stock Research Assistant

### Project goal
Build a stock research website as a final-year computer science project while learning full-stack development, data engineering, machine learning, and AI application development.

### Planned experience
- Left panel: search companies and stocks, select a stock, and manage a watchlist.
- Centre panel: latest available stock price, interactive chart, daily change, volume, and historical views.
- Below the chart: previous closing prices, historical performance, and evaluated forecasts with uncertainty.
- Right panel: an AI chatbot discussing company history, financial results, risks, and forecast findings, with sources.

### Initial scope
Indian stocks first, with US stocks as future scope. Proposed first version: one Indian exchange, 10–20 stocks, historical daily data, company question answering, and one forecast model compared against a simple baseline. The exact exchange, provider and stock list remain pending.

### Proposed components
- Interface: Python and Streamlit, without requiring handwritten HTML, CSS or JavaScript.
- Charts: Plotly.
- Application logic: separate Python modules; a FastAPI service is optional later.
- Data processing and storage: pandas, NumPy and SQLite.
- Data: a stock data provider selected for exchange coverage and usage rights.
- Machine learning: chronological evaluation, baseline comparison, error metrics, and uncertainty reporting.
- Chatbot: retrieval-augmented generation using reliable company documents and backend tools for prices.
- Automation: scheduled data refreshes and model performance tracking.

### Resume goals
Deliver a working demo, clear architecture, reproducible model evaluation, source-backed chatbot responses, and useful documentation.

### Current status
Updated 2026-10-26: repository cloned into E:\gpt\equitylens. Python-first direction and an eight-week learning/build roadmap are documented. Application implementation has not started.

### Project knowledge
- Start with [START_HERE.md](START_HERE.md).
- Follow [the detailed weekly roadmap](docs/WEEKLY_ROADMAP.md).
- Preserve [important conversation context](docs/PROJECT_CONTEXT.md) and [decisions](docs/DECISIONS.md).

