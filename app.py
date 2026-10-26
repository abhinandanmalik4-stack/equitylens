"""Run from the checkout: python -m streamlit run app.py."""

import os
from pathlib import Path
import sqlite3

import streamlit as st

from equitylens.analytics import RANGES, range_history, summarize
from equitylens.catalog import get_instrument, search_instruments
from equitylens.charts import comparison_figure, price_figure
from equitylens.providers import DemoProvider
from equitylens.watchlist import Watchlist

st.set_page_config(page_title="EquityLens | Stock research", page_icon=":material/query_stats:", layout="wide")
ROOT = Path(__file__).resolve().parent
st.session_state.setdefault("instrument", "NSE:RELIANCE")
st.session_state.setdefault("search_query", "")


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
    if not matches:
        st.info("No matching companies. Try another name, symbol or sector.")
        st.stop()
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
        st.warning("Watchlist storage is unavailable. Charts still work; check folder permissions.")
    label = "Remove from watchlist" if selected in saved else "Save to watchlist"
    if st.button(label, key="watchlist_action", disabled=store is None, width="stretch"):
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
            continue
        st.button(item.name, key=f"open:{key}", on_click=choose_saved, args=(key,), width="stretch")
    st.caption("Stored on this computer. This is a single-user demo, not a portfolio account.")

st.caption("RESEARCH WORKSPACE / INDIA")
st.title(instrument.name)
st.warning(
    "All prices and volumes on this page are invented demonstration data, not market quotes. "
    "The fixture ends 23 October 2026 and does not refresh with today's market.",
    icon=":material/science:",
)

try:
    history = load_history(selected)
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
    visible = range_history(history.frame, period)
    metrics = summarize(history.frame, visible)
    metric_columns = st.columns(4)
    metric_columns[0].metric("Demo close (INR)", f"{metrics.latest:,.2f}", border=True)
    metric_columns[1].metric("Change vs previous", f"{metrics.change:+,.2f}" if metrics.change is not None else "Unavailable", border=True)
    metric_columns[2].metric("Change (%)", f"{metrics.change_pct:+.2f}%" if metrics.change_pct is not None else "Unavailable", border=True)
    metric_columns[3].metric("Demo volume", f"{metrics.volume:,}", border=True)
    st.plotly_chart(price_figure(visible, instrument.currency, chart_type), width="stretch", key="price_chart", alt=f"Synthetic {instrument.name} prices and volume for the selected observation range.")
    st.caption(
        f"Source: {history.source} · Last observation: {history.as_of} · "
        f"{len(visible)} observations · Range shortcuts approximate months using 21 observations/month."
    )
    st.caption("Demo dates are weekdays, not an exchange holiday calendar. No dividends or corporate actions are modelled.")
    st.subheader("Historical comparison")
    st.markdown(f"Selected-range price change: **{metrics.range_return_pct:+.2f}%** (synthetic data).")
    peer = st.selectbox(
        "Compare with", ["None"] + [i.key for i in search_instruments() if i.key != selected],
        format_func=lambda key: "Choose a second company" if key == "None" else get_instrument(key).name,
        key=f"peer:{selected}",
    )
    if peer != "None":
        other = range_history(load_history(peer).frame, period)
        st.plotly_chart(
            comparison_figure(visible, other, (instrument.symbol, get_instrument(peer).symbol)),
            width="stretch", key="comparison_chart", alt="Synthetic stock-price comparison rebased to 100 on matching dates.",
        )
        st.caption("Both series start at 100 on the first shared date. Price returns only; not a forecast.")
    if st.toggle("Show underlying observations", key="show_data"):
        st.dataframe(visible, hide_index=True, alt="Synthetic dated OHLCV observations for the selected company.")
    export = visible.assign(instrument=selected, currency=instrument.currency, source=history.source, is_demo=True)
    st.download_button("Download labelled demo CSV", export.to_csv(index=False).encode("utf-8"), file_name=f"DEMO_{instrument.symbol}_{period}.csv", mime="text/csv", key="download_demo")

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
st.caption("EquityLens · A learning project in stock research · Demo mode · US-market support is future scope.")
