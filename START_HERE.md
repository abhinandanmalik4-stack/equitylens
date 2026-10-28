# Start here - EquityLens

Your Python-first AI Stock Research Assistant. Indian stocks first, future US support.

## Open the plan

- [Visual eight-week roadmap](docs/assets/equitylens-eight-week-roadmap.png)
- [Detailed roadmap: daily tasks, learning goals and completion checks](docs/WEEKLY_ROADMAP.md)
- [Important project conversation and handover context](docs/PROJECT_CONTEXT.md)
- [Confirmed decisions and pending choices](docs/DECISIONS.md)
- [Current project brief](EquityLens-Project.md)
- [Actual progress log](DAILY_PROGRESS.md)

## Current position

Repository cloned into E:\gpt\equitylens. The Streamlit dashboard and bounded CSV import/export now have 41 passing local tests (October 28), including numeric-limit and metadata-contract regressions. Built-in prices are synthetic; user-supplied files remain unverified. Direct provider integration, forecasting and AI research are future milestones.

Start with [Run and learn](docs/RUN_AND_LEARN.md), then try [CSV import](docs/CSV_IMPORT_GUIDE.md) and review [Architecture](docs/ARCHITECTURE.md). Next: select a permitted historical-data source using [the provider review](docs/DATA_PROVIDER_REVIEW.md).

## Learning order

Python and Git -> Streamlit -> pandas and APIs -> Plotly and SQLite -> chronological ML evaluation -> retrieval and cited AI answers -> testing and deployment.

No handwritten HTML, CSS or JavaScript is needed for the first version. A separate FastAPI service is optional later.

## Working rules

1. Read the context and decisions before changing project direction.
2. Work in this checkout; leave parent-folder coursework alone.
3. Explain each feature and verify it before recording completion.
4. Keep market data, research sources and model results traceable.
5. Keep the existing GitHub repository private and credentials outside Git.
6. Save important new decisions here through linked documentation; update the log only for real work.

The roadmap is a plan, not evidence that every feature is built. The initial development batch commits the plan and working foundation together with tests and updated progress. Check Git history for the exact pushed changes.
