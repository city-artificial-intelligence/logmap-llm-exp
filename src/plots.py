"""Reusable plotting helpers for the analysis / estimation notebooks.

Every function takes a prepared DataFrame plus a ``plot_kwargs`` (``pk``) dict and reads its
styling/layout from it with sensible defaults, e.g. ``width = pk.get("width", 900)``. This keeps
the notebooks thin: they prepare data and call these helpers with config + ``plot_kwargs``.

Plotly helpers return the ``Figure`` (and show it when ``pk.get("show", True)``); the matplotlib
helper returns the ``Axes``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

if TYPE_CHECKING:
    import pandas as pd


def _maybe_show(fig: go.Figure, pk: dict[str, Any]) -> go.Figure:
    if pk.get("show", True):
        fig.show()
    return fig


def grouped_bar(
    data: pd.DataFrame,
    x: str,
    y: str | list[str],
    color: str | None = None,
    title: str = "",
    labels: dict[str, str] | None = None,
    plot_kwargs: dict[str, Any] | None = None,
) -> go.Figure:
    """Bar chart. ``plot_kwargs``: width, height, tickangle, showlegend, barmode, color_discrete_map."""
    pk = plot_kwargs or {}
    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        labels=labels or {},
        barmode=pk.get("barmode", "relative"),
        color_discrete_map=pk.get("color_discrete_map"),
    )
    fig.update_layout(
        width=pk.get("width", 1200),
        height=pk.get("height", 500),
        xaxis_tickangle=pk.get("tickangle", -90),
        showlegend=pk.get("showlegend", True),
    )
    return _maybe_show(fig, pk)


def stacked_bar(
    data: pd.DataFrame,
    x: str,
    y_cols: list[str],
    title: str = "",
    labels: dict[str, str] | None = None,
    plot_kwargs: dict[str, Any] | None = None,
) -> go.Figure:
    """Stacked bar over several value columns. ``plot_kwargs``: width, height, tickangle, color_discrete_map."""
    pk = plot_kwargs or {}
    fig = px.bar(
        data,
        x=x,
        y=y_cols,
        title=title,
        labels=labels or {},
        barmode="stack",
        color_discrete_map=pk.get("color_discrete_map"),
    )
    fig.update_layout(
        width=pk.get("width", 1200),
        height=pk.get("height", 600),
        xaxis_tickangle=pk.get("tickangle", -45),
    )
    return _maybe_show(fig, pk)


def scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    symbol: str | None = None,
    size: str | None = None,
    hover_data: list[str] | None = None,
    title: str = "",
    labels: dict[str, str] | None = None,
    plot_kwargs: dict[str, Any] | None = None,
) -> go.Figure:
    """Scatter plot. ``plot_kwargs``: width, height."""
    pk = plot_kwargs or {}
    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        symbol=symbol,
        size=size,
        hover_data=hover_data,
        title=title,
        labels=labels or {},
    )
    fig.update_layout(width=pk.get("width", 900), height=pk.get("height", 500))
    return _maybe_show(fig, pk)


def cost_heatmap(
    cost_data: pd.DataFrame,
    tasks: list[str],
    source_data: pd.DataFrame | None = None,
    title: str = "Cost per (model, experiment)",
    plot_kwargs: dict[str, Any] | None = None,
) -> go.Figure:
    """Render a plotly heatmap of per-task cost with optional real/scaled ``(R/S)`` annotations.

    ``cost_data`` is indexed by row label with one column per task; ``source_data`` (same shape)
    holds ``real``/``scaled`` markers. ``plot_kwargs``: width, height, colorscale.
    """
    pk = plot_kwargs or {}
    rows = cost_data.index.tolist()
    annot, hover = [], []
    for i in range(cost_data.shape[0]):
        annot_row, hover_row = [], []
        for j, col in enumerate(tasks):
            val = float(cost_data.iloc[i, j])
            marker = ""
            if source_data is not None:
                src = str(source_data.iloc[i][col]) if col in source_data.columns else ""
                marker = f" ({src[0].upper()})" if src else ""
            annot_row.append(f"{val:.4f}{marker}")
            hover_row.append(f"<b>{rows[i]}</b><br>Task: {col}<br>Cost: ${val:.4f}{marker}")
        annot.append(annot_row)
        hover.append(hover_row)

    fig = go.Figure(
        go.Heatmap(
            z=cost_data[tasks].to_numpy(),
            x=tasks,
            y=rows,
            text=annot,
            customdata=hover,
            texttemplate="%{text}",
            coloraxis="coloraxis",
            hovertemplate="%{customdata}<extra></extra>",
        )
    )
    fig.update_layout(
        title=title,
        width=pk.get("width", 1350),
        height=pk.get("height", max(500, len(cost_data) * 30)),
        xaxis_title=pk.get("xaxis_title", "Task"),
        yaxis_title=pk.get("yaxis_title", "Model | Experiment"),
        xaxis={"tickangle": pk.get("tickangle", -90)},
        coloraxis={
            "colorscale": pk.get("colorscale", "YlOrRd"),
            "colorbar": {"title": pk.get("colorbar_title", "Task Cost (USD)"), "x": 1.02, "len": 0.5, "y": 0.75},
        },
    )
    return _maybe_show(fig, pk)


def cost_heatmap_mpl(
    heatmap_data: pd.DataFrame,
    title: str = "Estimated cost per task (USD)",
    plot_kwargs: dict[str, Any] | None = None,
) -> plt.Axes:
    """Matplotlib/seaborn cost heatmap. ``plot_kwargs``: figsize, cmap, fmt, linewidths."""
    pk = plot_kwargs or {}
    figsize = pk.get("figsize", (14, max(8, len(heatmap_data) * 0.35)))
    _, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        heatmap_data,
        annot=pk.get("annot", True),
        fmt=pk.get("fmt", ".3f"),
        cmap=pk.get("cmap", "YlOrRd"),
        ax=ax,
        linewidths=pk.get("linewidths", 0.5),
        cbar_kws={"label": pk.get("colorbar_title", "Cost (USD)")},
    )
    ax.set_title(title)
    plt.tight_layout()
    if pk.get("show", True):
        plt.show()
    return ax
