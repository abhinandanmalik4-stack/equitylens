"""Run from the checkout: python -m streamlit run app.py."""

import os
from pathlib import Path
import sqlite3

import streamlit as st

from equitylens.analytics import RANGES, calendar_window, range_history, summarize
from equitylens.catalog import get_instrument, search_instruments
from equitylens.charts import comparison_figure, price_figure
from equitylens.providers import DemoProvider
from equitylens.csv_data import import_history
from equitylens.exports import dataset_id, export_history
from equitylens.performance import historical_returns, max_drawdown_pct
from equitylens.watchlist import Watchlist

st.set_page_config(page_title="EquityLens | Stock research", page_icon=":material/query_stats:", layout="wide")
ROOT = Path(__file__).resolve().parent
st.session_state.setdefault("instrument", "NSE:RELIANCE")
st.session_state.setdefault("search_query", "")
st.session_state.setdefault("csv_histories", {})


@st.cache_data(max_entries=20, show_spinner=False)
def load_history(key: str):
    return DemoProvider().history(get_instrument(key))


def choose_saved(key: str):
    st.session_state.search_query = ""
    st.session_state.instrument = key


with st.sidebar:
    st.title("EquityLens")
    st.caption("A clearer view of the company behind the stock.")
    st.divider()
    st.subheader("Explore Indian stocks")
    query = st.text_input("Search company, symbol or sector", key="search_query", placeholder="Try Infosys or banking")
    matches = search_instruments(query)
    selected = None
    if not matches:
        st.info("No matching companies. Try another name, symbol or sector.")
    else:
        options = [i.key for i in matches]
        if st.session_state.instrument not in options:
            st.session_state.instrument = options[0]
        selected = st.selectbox(
            "Company", options, key="instrument",
            format_func=lambda key: f"{get_instrument(key).name} ({get_instrument(key).symbol})",
        )
        instrument = get_instrument(selected)
        st.caption(f"{instrument.exchange} demo universe · {instrument.currency} · {instrument.sector}")
    store = None
    saved = []
    try:
        store = Watchlist(os.environ.get("EQUITYLENS_DB_PATH", str(ROOT / "data" / "watchlist.db")))
        saved = store.items()
    except (OSError, sqlite3.Error):
        store = None
        st.warning("Watchlist storage is unavailable. Charts still work; check folder permissions.")
    label = "Remove from watchlist" if selected in saved else "Save to watchlist"
    if st.button(label, key="watchlist_action", disabled=store is None or selected is None, width="stretch"):
        try:
            if selected in saved:
                store.remove(selected)
            else:
                store.add(selected)
            st.rerun()
        except (OSError, sqlite3.Error, ValueError):
            st.warning("Could not update the watchlist. Try again after checking storage access.")
    st.divider()
    st.subheader("Your watchlist")
    if not saved:
        st.caption("Save a company to find it here next time.")
    for key in saved:
        try:
            item = get_instrument(key)
        except ValueError:
            st.caption(f"Unavailable catalogue entry: {key}")
            if st.button("Remove unavailable entry", key=f"remove_stale:{key}", disabled=store is None):
                try:
                    store.remove(key)
                    st.rerun()
                except (OSError, sqlite3.Error):
                    st.warning("Could not remove that entry. Check storage access.")
            continue
        st.button(item.name, key=f"open:{key}", on_click=choose_saved, args=(key,), width="stretch")
    st.caption("Stored on this computer. This is a single-user demo, not a portfolio account.")

if selected is None:
    st.stop()

with st.sidebar:
    st.divider()
    mode = st.segmented_control("Data source", ["Demo", "CSV upload"], default="Demo", required=True, key="data_mode")
    if mode == "CSV upload":
        st.caption("Import one company's daily history. Files stay in session memory; source claims are not independently verified.")
        with st.form(f"import:{selected}"):
            uploaded = st.file_uploader("Daily OHLCV CSV (up to 2 MiB)", type="csv", max_upload_size=2, key=f"upload:{selected}")
            source = st.text_input("Data source or original download URL", max_chars=200, key=f"source:{selected}")
            adjustment = st.selectbox("Price adjustment policy", ["Unknown", "Unadjusted", "Adjusted OHLC consistently"], key=f"adjustment:{selected}")
            declared_demo = st.checkbox("This file contains demonstration data", value=True, key=f"demo:{selected}")
            submitted = st.form_submit_button("Validate and load CSV", key="load_csv")
        if submitted:
            # Invalid replacement files must not leave an old chart labelled as the new data.
            st.session_state.csv_histories.pop(selected, None)
            try:
                if uploaded is None:
                    raise ValueError("Choose a CSV before loading.")
                st.session_state.csv_histories[selected] = import_history(
                    uploaded.getvalue(), instrument, source, adjustment, is_demo=declared_demo,
                )
            except (ValueError, TypeError) as exc:
                st.error(f"CSV rejected: {exc}")
        if st.button("Clear imported data", key="clear_csv"):
            st.session_state.csv_histories.pop(selected, None)
        st.caption("Required: date,open,high,low,close,volume. Dates: YYYY-MM-DD. Keep rows in increasing date order.")

st.caption("RESEARCH WORKSPACE / INDIA")
st.title(instrument.name)

try:
    if mode == "CSV upload":
        history = st.session_state.csv_histories.get(selected)
        if history is None:
            st.info("Load a valid CSV for this company to see its history. Demo data is not substituted in upload mode.")
            st.stop()
        if history.is_demo:
            st.warning("This uploaded dataset is marked as demonstration data, not verified market observations.")
        else:
            st.warning("User-supplied historical data: source and accuracy are unverified. These are not live quotes.")
    else:
        history = load_history(selected)
        st.warning(
            "All prices and volumes on this page are invented demonstration data, not market quotes. "
            "The fixture ends 23 October 2026 and does not refresh with today's market.",
            icon=":material/science:",
        )
except (ValueError, TypeError):
    st.error("Price history failed validation. No substitute prices have been generated.")
    st.stop()

main, research = st.columns([3, 1], gap="large")
with main:
    st.subheader("Price explorer")
    controls = st.columns([2, 1], vertical_alignment="bottom")
    with controls[0]:
        period = st.segmented_control("History range", list(RANGES), default="3M", key="period", required=True)
    with controls[1]:
        chart_type = st.segmented_control("Chart", ["Line", "Candlestick"], default="Line", key="chart_type", required=True)
    fingerprint = dataset_id(history)
    custom = st.toggle("Choose calendar dates", key="custom_dates")
    if custom:
        bounds = st.date_input("Observation date window", value=(history.frame.date.iloc[0].date(), history.as_of),
                               min_value=history.frame.date.iloc[0].date(), max_value=history.as_of, key=f"dates:{fingerprint[:16]}")
        if not isinstance(bounds, tuple) or len(bounds) != 2:
            st.info("Choose both a start date and an end date.")
            st.stop()
        try:
            visible = calendar_window(history.frame, *bounds)
        except ValueError as exc:
            st.error(str(exc))
            st.stop()
        if visible.empty:
            st.info("No observations in this date window. No prices have been filled or invented.")
            st.stop()
    else:
        visible = range_history(history.frame, period)
    metrics = summarize(history.frame, visible)
    label = "Demo" if mode == "Demo" else ("Uploaded demo" if history.is_demo else "Uploaded (unverified)")
    metric_columns = st.columns(4)
    metric_columns[0].metric(f"{label} latest close ({instrument.currency})", f"{metrics.latest:,.2f}", border=True)
    metric_columns[1].metric("Change vs previous", f"{metrics.change:+,.2f}" if metrics.change is not None else "Unavailable", border=True)
    metric_columns[2].metric("Change (%)", f"{metrics.change_pct:+.2f}%" if metrics.change_pct is not None else "Unavailable", border=True)
    metric_columns[3].metric(f"{label} latest volume", f"{metrics.volume:,}", border=True)
    st.caption("Top metrics use the last available observation in the full dataset. The chart and range statistics use your selected window.")
    st.plotly_chart(price_figure(visible, instrument.currency, chart_type, data_label=label), width="stretch", key="price_chart", alt=f"{label} {instrument.name} prices and volume for the selected observation range.")
    st.caption(
        f"Source: {history.source} · Last observation: {history.as_of} · "
        f"{len(visible)} observations · Range shortcuts approximate months using 21 observations/month."
    )
    st.caption(f"Adjustment policy: {history.adjustment} · Dataset ID: {fingerprint[:16]}")
    if mode == "Demo":
        st.caption("Demo dates are weekdays, not an exchange holiday calendar. No dividends or corporate actions are modelled.")
    st.subheader("Historical comparison")
    if metrics.range_return_pct is None:
        if len(visible) < 2:
            st.caption("Range price change is unavailable with only one observation.")
        else:
            st.caption("Range price change is unavailable because the result exceeds finite numeric limits.")
    else:
        st.markdown(f"Selected-range price change: **{metrics.range_return_pct:+.2f}%** ({label.lower()} data).")
    drawdown = max_drawdown_pct(visible)
    if drawdown is not None:
        st.caption(f"Worst close-based drawdown within the selected window: {drawdown:.2f}%. Not a forecast or total return.")
    if st.toggle("Show historical return periods", key="show_returns"):
        st.dataframe(historical_returns(visible), hide_index=True, alt="Historical price changes with explicit start/end dates; unavailable horizons are blank.")
        st.caption("Intervals count observations, not calendar days. Longer horizons stay blank when history is insufficient.")
    if mode == "Demo":
        peer = st.selectbox(
            "Compare with", ["None"] + [i.key for i in search_instruments() if i.key != selected],
            format_func=lambda key: "Choose a second company" if key == "None" else get_instrument(key).name,
            key=f"peer:{selected}",
        )
        if peer != "None":
            other = calendar_window(load_history(peer).frame, visible.date.iloc[0], visible.date.iloc[-1])
            if len(visible) < 2 or len(other) < 2:
                st.info("Comparison needs at least two matching observation dates.")
            else:
                st.plotly_chart(
                    comparison_figure(visible, other, (instrument.symbol, get_instrument(peer).symbol)),
                    width="stretch", key="comparison_chart", alt="Synthetic stock-price comparison rebased to 100 on matching dates.",
                )
                st.caption("Both series start at 100 on the first shared date. Price returns only; not a forecast.")
    else:
        st.caption("Cross-company comparison is disabled in upload mode so your history cannot be mixed with synthetic peers.")
    if st.toggle("Show underlying observations", key="show_data"):
        st.dataframe(visible, hide_index=True, alt=f"{label} dated OHLCV observations for the selected company.")
    prefix = "DEMO" if history.is_demo else "UNVERIFIED"
    window_label = "custom" if custom else period
    st.download_button("Download labelled CSV", export_history(history, visible), file_name=f"{prefix}_{instrument.symbol}_{window_label}.csv", mime="text/csv", key="download_demo")

with research:
    with st.container(border=True):
        st.subheader("Company research", icon=":material/menu_book:")
        st.info("Cited research chat is planned for weeks 6-7. No AI answers are generated in this version.")
        st.markdown("Future answers will cover company history, financial results and risks, grounded in reliable documents.")
    with st.container(border=True):
        st.subheader("Forecast lab", icon=":material/monitoring:")
        st.caption("Planned for weeks 4-5")
        st.markdown("Establish a simple baseline first. Add one model only after chronological evaluation, then report errors and assessed uncertainty.")
        st.caption("No trained model, accuracy score or forecast is available yet.")
    with st.container(border=True):
        st.subheader("Build with understanding")
        st.markdown("**Milestone 1:** dashboard foundation\n\nNext: select a licensed historical-data provider for Indian stocks.")
        st.caption("Python · Streamlit · Plotly · SQLite")

st.divider()
st.caption(f"EquityLens · A learning project in stock research · {mode} mode · US-market support is future scope.")
