"""Data visualization helpers and chart renderers for Power BI style analytics."""

import plotly.express as px
import numpy as np
import pandas as pd

def polish_plot(fig, title_text: str):
    """Applies clean styling and clear typography to Plotly figures."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title_text}</b>",
            font=dict(size=16, color="#0f172a")
        ),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8fafc",
        font=dict(family="sans-serif", size=12, color="#1e293b"),
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            tickfont=dict(size=11, color="#0f172a"),
            title=dict(font=dict(size=13, color="#0f172a")),
            showgrid=True,
            gridcolor="#e2e8f0"
        ),
        yaxis=dict(
            tickfont=dict(size=11, color="#0f172a"),
            title=dict(font=dict(size=13, color="#0f172a")),
            showgrid=True,
            gridcolor="#e2e8f0"
        )
    )
    return fig

def render_bar_chart(df: pd.DataFrame, category_col: str, metric_col: str, agg_func: str):
    """Renders a clean vertical bar chart with exact value labels on top."""
    # Group and aggregate data
    if agg_func == "Total (Sum)":
        agg_df = df.groupby(category_col, as_index=False)[metric_col].sum()
    elif agg_func == "Average (Mean)":
        agg_df = df.groupby(category_col, as_index=False)[metric_col].mean().round(2)
    else:
        agg_df = df.groupby(category_col, as_index=False)[metric_col].count()
        agg_df.rename(columns={metric_col: "Record Count"}, inplace=True)
        metric_col = "Record Count"

    # Treat x-axis as string to prevent fractional numbers/years
    agg_df[category_col] = agg_df[category_col].astype(str)
    agg_df = agg_df.sort_values(by=metric_col, ascending=False)

    fig = px.bar(
        agg_df,
        x=category_col,
        y=metric_col,
        text=metric_col,
        color_discrete_sequence=["#2563eb"]
    )
    fig.update_traces(
        textposition="outside",
        texttemplate="%{text:,.2f}" if agg_func == "Average (Mean)" else "%{text:,.0f}",
        marker=dict(line=dict(width=1, color="#1e293b"))
    )
    fig.update_layout(
        xaxis=dict(type="category", title=dict(text=str(category_col))),
        yaxis=dict(title=dict(text=f"{agg_func} of {metric_col}"))
    )
    return polish_plot(fig, f"{agg_func} of {metric_col} by {category_col}")

def render_donut_chart(df: pd.DataFrame, category_col: str, metric_col: str, agg_func: str):
    """Renders an intuitive donut/pie breakdown chart showing percentage share."""
    if agg_func == "Total (Sum)":
        agg_df = df.groupby(category_col, as_index=False)[metric_col].sum()
    elif agg_func == "Average (Mean)":
        agg_df = df.groupby(category_col, as_index=False)[metric_col].mean().round(2)
    else:
        agg_df = df.groupby(category_col, as_index=False)[metric_col].count()
        agg_df.rename(columns={metric_col: "Record Count"}, inplace=True)
        metric_col = "Record Count"

    agg_df[category_col] = agg_df[category_col].astype(str)

    fig = px.pie(
        agg_df,
        names=category_col,
        values=metric_col,
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return polish_plot(fig, f"Share Breakdown: {metric_col} by {category_col}")

def render_line_trend(df: pd.DataFrame, time_or_cat_col: str, metric_col: str, agg_func: str):
    """Renders a trend line over categories or years."""
    if agg_func == "Total (Sum)":
        agg_df = df.groupby(time_or_cat_col, as_index=False)[metric_col].sum()
    elif agg_func == "Average (Mean)":
        agg_df = df.groupby(time_or_cat_col, as_index=False)[metric_col].mean().round(2)
    else:
        agg_df = df.groupby(time_or_cat_col, as_index=False)[metric_col].count()
        agg_df.rename(columns={metric_col: "Record Count"}, inplace=True)
        metric_col = "Record Count"

    agg_df[time_or_cat_col] = agg_df[time_or_cat_col].astype(str)
    agg_df = agg_df.sort_values(by=time_or_cat_col)

    fig = px.line(
        agg_df,
        x=time_or_cat_col,
        y=metric_col,
        markers=True,
        color_discrete_sequence=["#0d9488"]
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(
        xaxis=dict(type="category", title=dict(text=str(time_or_cat_col))),
        yaxis=dict(title=dict(text=f"{agg_func} of {metric_col}"))
    )
    return polish_plot(fig, f"Trend: {metric_col} across {time_or_cat_col}")

def render_correlation_heatmap(df: pd.DataFrame, numeric_cols: list, min_corr: float = 0.0):
    """Renders Pearson correlation between numeric variables."""
    corr_matrix = df[numeric_cols].corr().round(2)
    if min_corr > 0.0:
        corr_matrix = corr_matrix.where(corr_matrix.abs() >= min_corr, np.nan)
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues"
    )
    return polish_plot(fig, f"Pearson Correlation Matrix (|r| ≥ {min_corr})")