# EquityLens - decision register

Recorded 2026-10-26. Status describes agreement, not implementation.

| Topic | Status | Decision / reason |
| --- | --- | --- |
| Repository | Confirmed | Reuse abhinandanmalik4-stack/equitylens; keep PRIVATE. |
| Workspace | Confirmed | E:\gpt\equitylens, isolated from coursework. |
| Market | Confirmed | Indian stocks first; US stocks later. |
| Indian exchange | Pending | NSE is a candidate; confirm provider coverage and user choice. |
| Interface | Accepted direction | Streamlit, so the first version can be built in Python without writing HTML/CSS/JS. |
| Charts | Accepted direction | Plotly for interactive price/candlestick/volume charts. |
| Data processing | Accepted direction | pandas and NumPy; source/provenance kept with data. |
| Persistence | Planned | SQLite for local first-version storage; review hosting persistence before deployment. |
| Separate API | Deferred | No separate FastAPI service needed initially; keep business logic separate from UI for future extraction. |
| Scope | Proposed | 10-20 stocks, daily history, company Q&A, one evaluated model and a baseline. |
| Forecast model | Pending | Choose after defining target/horizon and establishing a baseline; no accuracy promise. |
| Company AI | Planned | Retrieval from reliable documents, cited evidence and LLM access selected later. |
| Data provider | Pending | Check cost, Indian coverage, limits, historical adjustment and display rights first. |
| Hosting / LLM budget | Pending | No provider, purchase or deployment has been agreed. |
| Learning schedule | Accepted direction | Eight milestone weeks; 1-2 hours/day is an adjustable assumption; no fixed start date. |
| Commit practice | Confirmed constraint | Aim for useful daily commits; never manufacture ten changes to meet a number. |

Earlier React/Lightweight Charts suggestions are archived in conversation context; they are not the current first-version plan.
