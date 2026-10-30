# Foundation practice: explain your first working dashboard

Prepared 2026-10-30. Allow 20-30 minutes. This is a practice worksheet, not a record that you have completed it.

Use only [the included invented CSV](../examples/DEMO_NSE_RELIANCE.csv). Every value below is synthetic and says nothing about Reliance's actual performance. No real-data account or API key is needed.

## 1. Read the six observations (five minutes)

Before opening the dashboard, identify the company key, currency, source and demo marker in the CSV. Read the closes in chronological order:

| Date | Invented close (INR) | Invented volume |
| --- | ---: | ---: |
| 2026-01-02 | 110 | 1,000 |
| 2026-01-05 | 108 | 900 |
| 2026-01-06 | 102 | 1,200 |
| 2026-01-07 | 107 | 1,100 |
| 2026-01-08 | 105 | 850 |
| 2026-01-09 | 118 | 1,400 |

Write your own answers before reading the key:

1. What are the last close, previous close and absolute change?
2. Calculate previous-observation change: `(last - previous) / previous * 100`.
3. Calculate the full-window change: `(last - first) / first * 100`. Why is it different from answer 2?
4. Are six observations enough for a five-interval return? Are they enough for 21 intervals?
5. Find the worst close-based drawdown: for each close, compute `(close / highest close seen so far - 1) * 100`, then take the minimum. Do not use intraday lows.

## 2. Confirm the data path (ten minutes)

Follow [Run and learn](RUN_AND_LEARN.md) to start the local app. Select Reliance Industries, choose CSV upload and load the included file with source `EquityLens invented example`, adjustment `Synthetic unadjusted`, and the demo checkbox selected.

- Inspect the DEMO notice, source and last observation date. A file loading successfully does not verify its prices or licence.
- Display the observations and compare the top metrics with your answers.
- Enable historical return periods. Explain why longer horizons are blank instead of zero.
- Select calendar dates January 6-9, 2026. Recalculate the window return and worst drawdown. Top metrics still refer to the latest observation of the complete accepted dataset; window statistics refer to your selected rows.
- Select January 3-4, 2026. The example has no rows in that window: expect an empty-window message, not generated prices. This only describes the fixture, not an exchange calendar.
- Download the labelled CSV and check that instrument, currency, source, adjustment and `is_demo=True` remain attached.

Without the browser, run this from the project folder to inspect the same file:

```powershell
.venv\Scripts\python.exe -m equitylens.inspect_data examples/DEMO_NSE_RELIANCE.csv --instrument NSE:RELIANCE --source "EquityLens invented example" --adjustment "Synthetic unadjusted" --demo
```

Expect six observations from January 2 to January 9, `is_demo: true`, and a largest calendar gap of three days. The JSON's `valid_structure` means the file passes format checks; it does not certify market accuracy.

## 3. Explain a rejected file (five minutes)

Leave the checked-in example unchanged. For an optional experiment, make a local practice copy in the ignored data folder:

```powershell
New-Item -ItemType Directory -Force data | Out-Null
Copy-Item examples/DEMO_NSE_RELIANCE.csv data/practice.csv
```

Change just the January 6 high from 111 to 101 in the practice copy, leaving open 108 unchanged. Try importing the copy. Predict the error first: a high of 101 cannot be below an open of 108. The app should reject the replacement and clear the previously accepted chart instead of retaining misleading old prices. Restore your copy or reimport the original when finished.

## Answer key

| Question | Expected answer for this invented file |
| --- | --- |
| Identity and provenance | `NSE:RELIANCE`, `INR`, `EquityLens invented example`, `is_demo=True`; these are declarations on a synthetic fixture. |
| Latest/previous/absolute change | 118, 105 and +13 INR; latest volume 1,400. |
| Previous-observation change | `(118 - 105) / 105 * 100 = +12.38%`. |
| Entire-window change | `(118 - 110) / 110 * 100 = +7.27%`; it starts at a different close. |
| Horizon availability | Six observations span five intervals. The 21/63/126-interval results are unavailable, not zero. |
| Entire-window worst close drawdown | The running peak remains 110 through January 8; the January 6 close of 102 gives `(102 / 110 - 1) * 100 = -7.27%`. |
| January 6-9 return | `(118 - 102) / 102 * 100 = +15.69%`. |
| January 6-9 worst close drawdown | The peak rises to 107, then close falls to 105: `(105 / 107 - 1) * 100 = -1.87%`. The earlier peak of 110 is outside this window. |
| January 3-4 | Zero observations; do not infer a return or fabricate rows. |

Values are rounded here to two decimal places. Price changes exclude dividends and costs; drawdown is descriptive past movement, not a forecast or a guaranteed future-risk bound.

## Explain it back before the next milestone

In your own words, explain: CSV -> validation -> accepted DataFrame plus source metadata -> date window -> calculations -> chart/export. Why do invalid inputs stop at validation? Why must demo and unverified labels remain visible?

Also explain where the SQLite watchlist is saved and why selecting another company must not reuse the first company's uploaded history. Review the relevant modules with the [code-reading table](RUN_AND_LEARN.md#understand-the-code-in-this-order).

Write down what is still unclear. The next decision is the first Indian exchange and a permitted historical source; use [the provider review](DATA_PROVIDER_REVIEW.md). Completing this worksheet is not provider selection or model evaluation.
