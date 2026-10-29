# Historical CSV import and inspection

Updated 2026-10-27. This feature reads files the user is allowed to use. It does not fetch or independently verify prices, establish licensing, or select a market provider.

## Try the invented example

1. Launch the app using RUN_AND_LEARN.md and select Reliance Industries.
2. Select **CSV upload** in the sidebar, then choose `examples/DEMO_NSE_RELIANCE.csv`.
3. Enter `EquityLens invented example` as the source, select an adjustment declaration and leave the demo checkbox selected.
4. Click **Validate and load CSV**. Inspect the source, demo notice, last date and dataset identifier.
5. Toggle **Choose calendar dates** or **Show historical return periods**. One-row windows have no range return; empty windows display no chart.
6. Download the labelled CSV. Source, identity, currency, demo flag and adjustment remain attached. An embedded True demo marker cannot be erased by unchecking the form box.
7. Select another company. Upload mode needs an accepted file for that company and never reuses another company's prices or substitutes demo prices.

An invalid replacement clears the old chart. **Clear imported data** also removes accepted history from the current session. Switching back to Demo restores built-in fixtures.

## File contract

- UTF-8 or UTF-8 with BOM; comma-separated; at most 2 MiB and 10,000 observations.
- Required columns: `date,open,high,low,close,volume`.
- Optional columns: `instrument,currency,source,is_demo,adjustment`.
- Headers are trimmed/case-normalized; duplicate and unknown columns are rejected.
- Dates: YYYY-MM-DD, unique, increasing and no later than today's India date. No exchange holiday calendar is inferred.
- Prices: positive, finite, consistent high/low. Volume: finite nonnegative whole numbers. Booleans are not prices or volumes.
- Instrument/currency metadata, when supplied, must match the selection. Source, adjustment and demo metadata must be constant across rows.
- `is_demo` accepts consistent True/False markers. A True file marker always keeps the history marked demo.
- Bare OHLCV relies on the user's company/currency declaration; it cannot prove the file belongs to the selected company.
- Source and adjustment entries are declarations, not verified facts. Non-demo uploads still explicitly say **unverified**.

Raw NSE UDiFF/bhavcopy or vendor-specific files require explicit mapping first. There is no vendor-specific converter, corporate-action adjustment, intraday import or live refresh.

## Interpretation

Top metrics use the latest row of the full dataset. Chart, range return and worst close-based drawdown use the selected window. Historical horizons count observation intervals, not calendar days: five intervals require six observations. Missing horizons remain blank. Drawdown is a past close-based statistic, not a future-risk guarantee or total return.

Uploaded files are never compared with synthetic peers. Exports verify rows belong to the labelled history and escape formula-like metadata for spreadsheet opening. Dataset SHA-256 proves identity of data and declarations, not source ownership or market accuracy.

October 28 update: finite prices can still produce a percentage too large for numeric representation. The dashboard marks that return unavailable; it does not fabricate a zero or display infinity as performance.

## Inspect a file without the interface

For Python callers, `import_history` expects file bytes, an `Instrument`, nonempty source/adjustment strings of at most 200 characters, and an explicit boolean `is_demo`. Invalid argument types raise `ValueError` before parsing; strings such as `"False"` are not boolean flags. This prevents accidental truthiness from changing a file's demo declaration. The CSV column itself still accepts the documented True/False text markers.

```powershell
.venv\Scripts\python.exe -m equitylens.inspect_data examples/DEMO_NSE_RELIANCE.csv --instrument NSE:RELIANCE --source "EquityLens invented example" --adjustment "Synthetic unadjusted" --demo
```

The JSON report gives row count, date coverage, zero-volume count, largest calendar gap and dataset identity. A valid structure is not verified market data. Calendar gaps can include holidays/weekends and are not diagnosed as missing trading sessions. Invalid files return exit code 2.

## Storage and verification limits

Uploads/accepted history stay in session memory, not Git or the watchlist database; a fresh session may require reimport. This feature sends no files to a stock API or LLM. The watchlist remains local and single-user.

Tests mock only the browser file-picker boundary and exercise the actual form/parser/state/metrics path. Browser file selection, appearance and chart gestures remain separate manual checks.
