"""Plotly figures built only from validated observations."""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from equitylens.analytics import normalized_comparison
from equitylens.providers import validate_history


def price_figure(frame: pd.DataFrame, currency: str, chart_type: str = "Line", *, data_label: str = "Demo") -> go.Figure:
    frame = validate_history(frame)
    if chart_type not in ("Line", "Candlestick"):
        raise ValueError("Unknown chart type.")
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_heights=[0.78, 0.22])
    if chart_type == "Candlestick":
        trace = go.Candlestick(
            x=frame.date, open=frame.open, high=frame.high, low=frame.low, close=frame.close,
            name=f"{data_label} price ({currency})", increasing_line_color="#24735C", decreasing_line_color="#B24B4B",
        )
    else:
        trace = go.Scatter(
            x=frame.date, y=frame.close, name=f"{data_label} close ({currency})", mode="lines",
            line={"color": "#24735C", "width": 2.5}, fill="tozeroy", fillcolor="rgba(36,115,92,0.08)",
            hovertemplate="%{x|%d %b %Y}<br>" + currency + " %{y:,.2f}<extra>" + data_label + " close</extra>",
        )
    fig.add_trace(trace, row=1, col=1)
    fig.add_trace(go.Bar(x=frame.date, y=frame.volume, name=f"{data_label} volume", marker_color="#9BB9AB"), row=2, col=1)
    fig.update_layout(
        height=440, margin={"l": 15, "r": 15, "t": 15, "b": 10},
        showlegend=False, hovermode="x unified", xaxis_rangeslider_visible=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_yaxes(title_text=currency, row=1, col=1, rangemode="normal")
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_xaxes(title_text="Observation date", row=2, col=1)
    return fig


def comparison_figure(a: pd.DataFrame, b: pd.DataFrame, labels: tuple[str, str]) -> go.Figure:
    common = normalized_comparison(a, b)
    fig = go.Figure()
    for column, label, color in zip(("close_a", "close_b"), labels, ("#24735C", "#536DA3")):
        fig.add_trace(go.Scatter(x=common.date, y=common[column], name=label, mode="lines", line_color=color))
    fig.update_layout(
        height=300, margin={"l": 10, "r": 10, "t": 15, "b": 10},
        yaxis_title="First common observation = 100", xaxis_title="Observation date",
        hovermode="x unified", legend_orientation="h", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig
