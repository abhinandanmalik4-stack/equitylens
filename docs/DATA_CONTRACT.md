# Daily data contract and demo provenance

## What a provider returns

`PriceProvider.history(instrument)` returns `PriceHistory`: instrument identity, a DataFrame, source, demo flag, last observation date and adjustment policy. This boundary lets a later real provider replace the synthetic provider without changing the chart/calculation code.

Instrument identity includes exchange, symbol, currency and country. The demo catalogue uses proposed NSE identifiers; it does not verify current listings or future provider coverage. A future US instrument has its own exchange/currency identity.

| Column | Meaning | Required checks |
| --- | --- | --- |
| date | Daily session label, timezone-naive midnight | Valid, unique, strictly increasing |
| open | Opening price in instrument currency | Positive, finite |
| high | Session maximum | At least open, close and low |
| low | Session minimum | At most open, close and high |
| close | Closing price | Positive, finite |
| volume | Shares/units traded | Finite, nonnegative whole number |

The validator rejects bad data. It does not silently sort, fill missing prices, infer a quote, or remove duplicate sessions. An actual provider adapter must explicitly decide and document those policies. The last data date must equal the metadata's as-of date.

## Synthetic fixture v1

- All prices and volumes are invented; they are not observations of the named companies.
- The fixture contains 252 weekday observations ending 2026-10-23. It is fixed, not updated daily.
- A symbol/exchange-derived seed produces repeatable paths. Different instruments get different data.
- Weekdays are not an exchange holiday calendar. Corporate actions, dividends, adjusted prices and true intraday data are not modelled.
- INR is a display unit for the Indian demo, not evidence of a real quote.
- Range shortcuts use observation counts: 1M = 21, 3M = 63, 6M = 126, 1Y = 252. They are approximations, not calendar windows.

## Calculations

October 28 boundary handling: positive finite input values can still produce an unrepresentable percentage. Such returns are unavailable, never displayed as infinity or replaced with zero. Normalized comparisons divide before scaling to avoid premature overflow; genuinely nonfinite normalized paths are rejected. Instrument metadata requires nonempty trimmed text without control characters, uppercase currency/country codes and no colon within the exchange/symbol components. Malformed provider records raise controlled validation errors.

- Previous close is the previous observation in the full series, not the beginning of the selected range.
- Change = latest close - previous close.
- Change percent = 100 * change / previous close.
- Range return = 100 * (last visible close / first visible close - 1).
- With one observation, previous-close change and range return are unavailable, not invented as zero.
- Comparison joins on common observation dates and rebases each series to 100 on the first common date. It is a price comparison, not total return or a forecast.

## Real-provider acceptance checklist (future milestone)

The October 27 local CSV workflow already accepts canonical OHLCV with bounded size, identity checks and explicit unverified declarations. Exports preserve source, currency, identity, adjustment and demo state. Calendar windows are inclusive; historical horizons count observation intervals. See [CSV_IMPORT_GUIDE.md](CSV_IMPORT_GUIDE.md) for the complete contract and limits.

Verify exchange coverage, provider symbol mapping, current listings, license/display rights, request limits, source timestamps, refresh policy, session timezone/calendar, adjusted-price rules, errors and missing values before replacing demo mode. Never silently fall back from real data to synthetic data. No provider or paid plan is selected yet.
