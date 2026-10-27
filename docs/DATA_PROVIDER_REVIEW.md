# Indian historical-data provider review

Checked 2026-10-27. No provider account, API key, purchase or licensing agreement has been created. This is a documented shortlist, not a claim of verified exchange-wide coverage.

## Current usable route

The app can now inspect a local, single-company historical CSV. The user is responsible for obtaining a file they are allowed to use and declaring its source, instrument, currency and adjustment policy. The app checks structure and consistency, not market accuracy or legal entitlement. Uploads are always labelled unverified; sample files stay marked demo.

This allows development to continue without silently scraping a site, promising live quotes, or selecting a paid provider on the user's behalf.

## Options checked against official documentation

| Route | What the official source establishes | Still to verify before use |
| --- | --- | --- |
| NSE reports/archive downloads | The official reports page includes security-wise price/volume archives and report downloads; older bhavcopy formats have changed. [NSE reports](https://www.nseindia.com/all-reports) | Exact chosen report schema, series, symbol mapping, available dates, adjustments, access conditions and app display/reuse rights. The generic EquityLens CSV importer is not a raw UDiFF/bhavcopy converter. |
| NSE real-time products or authorized vendors | NSE describes paid real-time feeds, snapshot/delayed products and authorized-vendor routes. This is separate from daily-history development. [NSE data products](https://www.nseindia.com/static/market-data/real-time-data-subscription) | Cost and agreements, allowed display medium, technical delivery and whether real-time access is needed at all. No subscription is selected. |
| Alpha Vantage | Its documentation provides global-equity time-series and symbol-search APIs; the daily-adjusted endpoint is marked premium. [API documentation](https://www.alphavantage.co/documentation/) | Exact intended Indian exchange/symbol coverage through an authorized account, current limits/pricing, historical depth, output availability and display rights. Do not assume a global-equity endpoint proves NSE coverage. |

These are different access routes, not interchangeable providers or confirmed recommendations. No price or free-access promise is recorded because those depend on current plans and entitlements.

## Acceptance record for whichever source is selected

Before integrating an adapter, record:

1. Exchange and exact stock symbols, including historical symbol changes and series.
2. Data source URL/product, access method and permissible use/display scope.
3. Currency, timezone, session calendar, delay and retrieval time.
4. Historical date coverage, granularity, request limits and error responses.
5. Whether OHLC and volume are adjusted consistently for splits/dividends; never mix adjusted close with unexplained raw OHLC.
6. A small inspected example, schema mapping and checks against the original source.
7. Missing/duplicate-session policy and caching/refresh strategy.
8. Behavior on failure: preserve accurate source/as-of labels and do not replace real data with synthetic observations.

## Next decision

Review the demo and CSV workflow with the student. Then choose the initial Indian exchange and a permissible historical-data source. Live data and US support remain later work; evaluated forecasts and company document research are separate milestones.
