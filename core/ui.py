# -*- coding: utf-8 -*-
"""
core/ui.py
Theme styling, CSS injection, and Plotly visualization factory.
Strict quality standards: zero emojis, colorblind-safe palettes, no UI clutter.
"""
from __future__ import annotations
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

from core.config import COLORS


def apply_custom_css() -> None:
    """Injects scoped, polished academic CSS styling without breaking icon fonts."""
    st.markdown(
        f"""
        <style>
        /* Base typography & containers */
        .stApp {{
            background-color: {COLORS['neutral_light']};
            color: {COLORS['neutral_dark']};
        }}
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: #ffffff;
            border-right: 1px solid {COLORS['border']};
        }}
        
        /* Metric cards */
        .metric-card {{
            background-color: {COLORS['card_bg']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }}
        .metric-card-title {{
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {COLORS['neutral_muted']};
            font-weight: 600;
            margin-bottom: 4px;
        }}
        .metric-card-value {{
            font-size: 1.85rem;
            font-weight: 700;
            color: {COLORS['neutral_dark']};
            line-height: 1.2;
        }}
        .metric-card-sub {{
            font-size: 0.80rem;
            color: {COLORS['neutral_muted']};
            margin-top: 4px;
        }}
        
        /* Callout alert boxes */
        .alert-box {{
            padding: 12px 16px;
            border-radius: 6px;
            margin: 12px 0;
            font-size: 0.88rem;
            line-height: 1.5;
        }}
        .alert-info {{
            background-color: {COLORS['primary_light']};
            border-left: 4px solid {COLORS['primary']};
            color: #1e1b4b;
        }}
        .alert-warning {{
            background-color: {COLORS['at_risk_bg']};
            border-left: 4px solid {COLORS['at_risk']};
            color: #881337;
        }}
        .alert-success {{
            background-color: {COLORS['safe_bg']};
            border-left: 4px solid {COLORS['safe']};
            color: #064e3b;
        }}

        /* Table styling polish */
        .dataframe {{
            font-size: 0.85rem !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(
    title: str,
    value: str,
    subtitle: str = "",
    status: str = "normal",
) -> None:
    """Renders an elegant KPI card."""
    value_color = COLORS["neutral_dark"]
    if status == "at_risk":
        value_color = COLORS["at_risk"]
    elif status == "safe":
        value_color = COLORS["safe"]
    elif status == "primary":
        value_color = COLORS["primary"]

    html = f"""
    <div class="metric-card">
        <div class="metric-card-title">{title}</div>
        <div class="metric-card-value" style="color: {value_color};">{value}</div>
        <div class="metric-card-sub">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def plot_illusion_gap_scatter(df: pd.DataFrame) -> go.Figure:
    """
    Scatter plot of Assignment Score (With AI) vs Exam Score (No AI).
    Highlights the Illusion of Competence Gap.
    """
    fig = go.Figure()

    # Reference parity line (x = y)
    fig.add_trace(go.Scatter(
        x=[0.3, 1.05],
        y=[0.3, 1.05],
        mode="lines",
        name="Paritas Sempurna (Tugas = Ujian)",
        line=dict(color="#94a3b8", dash="dash", width=1.5),
        hoverinfo="skip"
    ))

    # At-risk students
    df_risk = df[df["at_risk"] == 1]
    fig.add_trace(go.Scatter(
        x=df_risk["llm_score"] * 100,
        y=df_risk["no_llm_score"] * 100,
        mode="markers",
        name="Academic At-Risk (< 85%)",
        marker=dict(size=8, color=COLORS["at_risk"], opacity=0.85),
        text=df_risk["userId"],
        hovertemplate="User: %{text}<br>Nilai Tugas: %{x:.1f}%<br>Nilai Ujian: %{y:.1f}%<extra></extra>"
    ))

    # Good standing students
    df_safe = df[df["at_risk"] == 0]
    fig.add_trace(go.Scatter(
        x=df_safe["llm_score"] * 100,
        y=df_safe["no_llm_score"] * 100,
        mode="markers",
        name="Good Standing (>= 85%)",
        marker=dict(size=8, color=COLORS["safe"], opacity=0.85),
        text=df_safe["userId"],
        hovertemplate="User: %{text}<br>Nilai Tugas: %{x:.1f}%<br>Nilai Ujian: %{y:.1f}%<extra></extra>"
    ))

    fig.update_layout(
        title="Disparitas Nilai Tugas (Dengan AI) vs Nilai Ujian Mandiri (Tanpa AI)",
        xaxis_title="Rata-rata Nilai Tugas Pemrograman dengan AI (%)",
        yaxis_title="Rata-rata Nilai Ujian Mandiri Tanpa AI (%)",
        template="plotly_white",
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="#ffffff",
        paper_bgcolor="rgba(0,0,0,0)",
        height=420,
    )
    fig.update_xaxes(showgrid=True, gridcolor=COLORS["grid"])
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid"])
    return fig


def plot_dialogue_landscape(df: pd.DataFrame) -> go.Figure:
    """
    Hero Visual: Cognitive Dialogue Landscape.
    Conceptual Inquiry Ratio vs Error Message Pasting Ratio.
    """
    fig = px.scatter(
        df,
        x="conceptual_ratio",
        y="error_msg_ratio",
        color=df["at_risk"].map({1: "Academic At-Risk", 0: "Good Standing"}),
        color_discrete_map={"Academic At-Risk": COLORS["at_risk"], "Good Standing": COLORS["safe"]},
        size="total_turns",
        size_max=16,
        hover_data=["userId", "no_llm_score", "total_turns"],
        labels={
            "conceptual_ratio": "Proporsi Pertanyaan Konseptual (Conceptual Ratio)",
            "error_msg_ratio": "Proporsi Paste Pesan Error (Error Msg Ratio)",
            "color": "Status Akademik"
        },
        title="Lansekap Kognitif: Pertanyaan Konseptual vs Jebakan Pesan Error",
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="#ffffff",
        paper_bgcolor="rgba(0,0,0,0)",
        height=420,
    )
    fig.update_xaxes(showgrid=True, gridcolor=COLORS["grid"])
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid"])
    return fig


def plot_confusion_matrix(cm: list[list[int]], cm_norm: list[list[float]]) -> go.Figure:
    """Heatmap for normalized Confusion Matrix."""
    labels = ["Good Standing (0)", "Academic At-Risk (1)"]
    z_text = [[f"{cm[i][j]}<br>({cm_norm[i][j]*100:.1f}%)" for j in range(2)] for i in range(2)]

    fig = go.Figure(data=go.Heatmap(
        z=cm_norm,
        x=labels,
        y=labels,
        text=z_text,
        texttemplate="%{text}",
        textfont={"size": 14},
        colorscale=[[0, "#f8fafc"], [1, COLORS["primary"]]],
        showscale=False,
    ))

    fig.update_layout(
        title="Confusion Matrix (Ternormalisasi & Jumlah Sampel Uji)",
        xaxis_title="Prediksi Model",
        yaxis_title="Kondisi Sebenarnya (Ground Truth)",
        template="plotly_white",
        margin=dict(l=40, r=20, t=50, b=40),
        height=380,
    )
    return fig


def plot_roc_pr_curves(
    fpr: list[float],
    tpr: list[float],
    roc_auc: float,
    recall: list[float],
    precision: list[float],
) -> go.Figure:
    """Side-by-side ROC curve and Precision-Recall curve."""
    fig = go.Figure()

    # ROC trace
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode="lines",
        name=f"ROC Curve (AUC = {roc_auc:.3f})",
        line=dict(color=COLORS["primary"], width=2.5)
    ))
    # Random baseline
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode="lines",
        name="Baseline Acak (AUC = 0.500)",
        line=dict(color="#94a3b8", dash="dash", width=1.5)
    ))

    fig.update_layout(
        title=f"Kurva ROC-AUC Model Terpilih (Skor: {roc_auc:.3f})",
        xaxis_title="False Positive Rate (1 - Specificity)",
        yaxis_title="True Positive Rate (Sensitivity / Recall)",
        template="plotly_white",
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="#ffffff",
        height=380,
    )
    fig.update_xaxes(showgrid=True, gridcolor=COLORS["grid"])
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid"])
    return fig


def plot_permutation_importance(df_imp: pd.DataFrame) -> go.Figure:
    """Bar chart for Permutation Feature Importance."""
    top_df = df_imp.head(8).iloc[::-1]

    fig = go.Figure(go.Bar(
        x=top_df["Importance (Mean)"],
        y=top_df["Fitur"],
        orientation="h",
        marker=dict(color=COLORS["primary"]),
        error_x=dict(type="data", array=top_df["Importance (Std)"], visible=True),
        hovertemplate="Fitur: %{y}<br>Penurunan F1: %{x:.4f}<extra></extra>"
    ))

    fig.update_layout(
        title="Permutation Feature Importance (Dampak Penurunan F1-Macro)",
        xaxis_title="Penurunan Rata-rata Skor F1-Macro saat Fitur Diacak",
        yaxis_title="Fitur Perilaku",
        template="plotly_white",
        margin=dict(l=40, r=20, t=50, b=40),
        plot_bgcolor="#ffffff",
        height=380,
    )
    fig.update_xaxes(showgrid=True, gridcolor=COLORS["grid"])
    return fig
