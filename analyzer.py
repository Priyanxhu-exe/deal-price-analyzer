import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deal Price Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    background-attachment: fixed;
  }

  [data-testid="stSidebar"] {
    background: rgba(15, 12, 41, 0.85) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
  }
  [data-testid="stSidebar"] label {
    color: #a9b4ff !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  [data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, box-shadow 0.2s;
  }
  [data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(80,80,200,0.25);
  }
  [data-testid="metric-container"] label {
    color: #a9b4ff !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
  }

  .main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    margin: 0;
    text-align: center;
  }
  .main-subtitle {
    color: rgba(200,200,255,0.6);
    font-size: 1rem;
    text-align: center;
    margin-top: 0.3rem;
  }
  .gradient-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #7c3aed, #3b82f6, #10b981, transparent);
    border: none;
    margin: 1rem 0 2rem;
  }
  .mode-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(124,58,237,0.13), rgba(59,130,246,0.13));
    border: 1px solid rgba(124,58,237,0.4);
    color: #a78bfa;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.9rem;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1.5rem;
  }
  .sidebar-logo {
    text-align: center;
    padding: 1.2rem 0 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1rem;
  }
  .sidebar-logo-text {
    font-size: 1rem;
    font-weight: 700;
    color: #a78bfa;
    letter-spacing: 0.04em;
  }
  .sidebar-section {
    font-size: 0.7rem;
    font-weight: 700;
    color: rgba(169,180,255,0.5);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 1.2rem 0 0.4rem;
  }
  .col-info {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #7c3aed;
    padding: 0.45rem 0.75rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.78rem;
    color: rgba(200,200,255,0.65);
    word-break: break-all;
  }
  [data-testid="stFileUploadDropzone"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px dashed rgba(169,180,255,0.35) !important;
    border-radius: 12px !important;
  }
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.4); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ───────────────────────────────────────────────────────────────
C = {
    "purple": "#7c3aed", "blue": "#3b82f6", "green": "#10b981",
    "amber": "#f59e0b", "red": "#ef4444",
    "text": "#e0e0ff", "grid": "rgba(255,255,255,0.06)",
}

_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=C["text"]),
    margin=dict(t=70, b=60, l=60, r=30),
    legend=dict(
        bgcolor="rgba(255,255,255,0.05)",
        bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1,
    ),
    hoverlabel=dict(
        bgcolor="rgba(20,15,50,0.95)",
        bordercolor="rgba(124,58,237,0.6)",
        font=dict(family="Inter", size=13, color="#ffffff"),
    ),
    xaxis=dict(gridcolor=C["grid"], zeroline=False, linecolor="rgba(255,255,255,0.1)", showline=True),
    yaxis=dict(gridcolor=C["grid"], zeroline=False, linecolor="rgba(255,255,255,0.1)", showline=True),
)


def layout(**overrides):
    """Return a merged copy of _BASE with any overrides applied."""
    merged = dict(_BASE)          # shallow copy of top-level keys
    merged.update(overrides)      # overrides win — no duplicate-keyword error
    return merged


def stats(prices):
    return prices.median(), prices.min(), prices.max()


def metric_row(median, low, high, base=None):
    cols = st.columns(4 if base is not None else 3)
    cols[0].metric("📊 Median", f"{median:,.0f}")
    cols[1].metric("⬇ Lowest", f"{low:,.0f}")
    cols[2].metric("⬆ Highest", f"{high:,.0f}")
    if base is not None:
        cols[3].metric("↔ Spread", f"{high - low:,.0f}")


def bar_color(margin):
    if margin <= 0:
        return C["green"]
    elif margin <= 5:
        return C["amber"]
    return C["red"]


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo"><div style="font-size:2rem">📊</div><span class="sidebar-logo-text">Deal Price Analyzer</span></div>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-section">Analysis Mode</p>', unsafe_allow_html=True)
    mode = st.selectbox("Mode", ["Seller Comparison", "Price Trend"], label_visibility="collapsed")
    st.markdown('<p class="sidebar-section">Data Source</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload .xlsx", type=["xlsx"])

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown('<h1 class="main-title">Deal Price Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Interactive price intelligence & market comparison</p>', unsafe_allow_html=True)
st.markdown('<hr class="gradient-divider"/>', unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;">
      <div style="font-size:4rem;margin-bottom:1rem;">📂</div>
      <h3 style="color:#a78bfa;font-weight:700;margin-bottom:0.5rem;">No file uploaded yet</h3>
      <p style="color:rgba(200,200,255,0.55);max-width:400px;margin:auto;">
        Upload an <strong>.xlsx</strong> file from the sidebar to start analyzing prices interactively.
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

try:
    df = pd.read_excel(uploaded_file)
except Exception as e:
    st.error(f"⚠️ Could not read the file: {e}")
    st.stop()

with st.sidebar:
    st.markdown('<p class="sidebar-section">Detected Columns</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="col-info">{" · ".join(df.columns.tolist())}</div>', unsafe_allow_html=True)

icon = "🏷️" if mode == "Seller Comparison" else "📈"
st.markdown(f'<div class="mode-badge">{icon} &nbsp;{mode}</div>', unsafe_allow_html=True)

# MODE 1 — SELLER COMPARISON
if mode == "Seller Comparison":
    with st.sidebar:
        st.markdown('<p class="sidebar-section">Configuration</p>', unsafe_allow_html=True)
        price_col = st.text_input("Price column", "Price")
        label_col = st.text_input("Seller / source column", "Seller")
        base_price = st.number_input("Base price for comparison", value=1050.0, step=10.0)

    for col in (price_col, label_col):
        if col not in df.columns:
            st.error(f"Column **'{col}'** not found. Available: {list(df.columns)}")
            st.stop()

    df["Margin %"] = ((df[price_col] - base_price) / base_price) * 100
    sdf = df.sort_values(by=price_col).reset_index(drop=True)
    median_p, low_p, high_p = stats(sdf[price_col])

    metric_row(median_p, low_p, high_p, base_price)
    st.markdown("<br/>", unsafe_allow_html=True)

    colors = sdf["Margin %"].apply(bar_color).tolist()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sdf[label_col], y=sdf[price_col],
        marker=dict(color=colors, opacity=0.88, line=dict(width=0)),
        customdata=sdf[["Margin %"]],
        hovertemplate="<b>%{x}</b><br>Price: <b>%{y:,.0f}</b><br>Margin: <b>%{customdata[0]:+.1f}%</b><extra></extra>",
        name="Price",
    ))

    fig.add_hline(y=base_price,
        line=dict(color=C["green"], width=2, dash="dot"),
        annotation=dict(text=f"Base  {base_price:,.2f}", font=dict(color=C["green"], size=12),
                        bgcolor="rgba(16,185,129,0.12)", borderpad=4),
        annotation_position="top right")

    fig.add_hline(y=median_p,
        line=dict(color="rgba(200,200,255,0.5)", width=1.5, dash="dash"),
        annotation=dict(text=f"Median  {median_p:,.0f}", font=dict(color="rgba(200,200,255,0.7)", size=12),
                        bgcolor="rgba(30,30,80,0.6)", borderpad=4),
        annotation_position="bottom right")

    for _, row in sdf.iterrows():
        fig.add_annotation(
            x=row[label_col], y=row[price_col],
            text=f"{row['Margin %']:+.1f}%",
            showarrow=False, yshift=14,
            font=dict(size=11, color=bar_color(row["Margin %"])),
        )

    fig.update_layout(**layout(
        title=dict(text=f"<b>{price_col} by {label_col}</b>", font=dict(size=18), x=0.01),
        xaxis_title=label_col, yaxis_title=price_col,
        showlegend=False, bargap=0.35,
    ))

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📐 Margin breakdown", expanded=True):
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=sdf[label_col], y=sdf["Margin %"],
            marker=dict(color=sdf["Margin %"].apply(bar_color), opacity=0.85, line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>Margin: <b>%{y:+.2f}%</b><extra></extra>",
        ))
        fig2.add_hline(y=0, line=dict(color="rgba(255,255,255,0.3)", width=1))
        fig2.update_layout(**layout(
            title=dict(text="<b>Margin % vs. base price</b>", font=dict(size=15), x=0.01),
            xaxis_title=label_col, yaxis_title="Margin %",
            showlegend=False, bargap=0.35, height=290,
            margin=dict(t=60, b=50, l=55, r=20),
        ))
        st.plotly_chart(fig2, use_container_width=True)

    with st.expander("🗂️ Raw data table"):
        disp = sdf[[label_col, price_col, "Margin %"]].copy()
        disp["Margin %"] = disp["Margin %"].map(lambda v: f"{v:+.2f}%")
        st.dataframe(disp, use_container_width=True, hide_index=True)

# MODE 2 — PRICE TREND
else:
    with st.sidebar:
        st.markdown('<p class="sidebar-section">Configuration</p>', unsafe_allow_html=True)
        price_col = st.text_input("Price column", "Price")
        date_col  = st.text_input("Date column",  "Date")
        show_ma   = st.checkbox("Show moving average", value=True)
        ma_win    = st.slider("MA window (periods)", 2, 30, 7) if show_ma else None

    for col in (price_col, date_col):
        if col not in df.columns:
            st.error(f"Column **'{col}'** not found. Available: {list(df.columns)}")
            st.stop()

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(by=date_col).reset_index(drop=True)
    prices, dates = df[price_col], df[date_col]
    median_p, low_p, high_p = stats(prices)

    if show_ma and ma_win:
        df["MA"] = prices.rolling(ma_win, min_periods=1).mean()

    metric_row(median_p, low_p, high_p)
    st.markdown("<br/>", unsafe_allow_html=True)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dates, y=prices, mode="lines",
        line=dict(color=C["purple"], width=0),
        fill="tozeroy", fillcolor="rgba(124,58,237,0.09)",
        hoverinfo="skip", showlegend=False))

    fig.add_trace(go.Scatter(x=dates, y=prices,
        mode="lines+markers",
        line=dict(color=C["purple"], width=2.5),
        marker=dict(size=5, color=C["purple"], line=dict(color="#fff", width=1)),
        hovertemplate=f"<b>%{{x|%b %d, %Y}}</b><br>{price_col}: <b>%{{y:,.0f}}</b><extra></extra>",
        name=price_col))

    if show_ma and ma_win and "MA" in df.columns:
        fig.add_trace(go.Scatter(x=dates, y=df["MA"],
            mode="lines", line=dict(color=C["amber"], width=2, dash="dot"),
            hovertemplate=f"MA({ma_win}): <b>%{{y:,.0f}}</b><extra></extra>",
            name=f"MA({ma_win})"))

    fig.add_hline(y=median_p,
        line=dict(color="rgba(200,200,255,0.45)", width=1.5, dash="dash"),
        annotation=dict(text=f"Median  {median_p:,.0f}",
            font=dict(color="rgba(200,200,255,0.65)", size=12),
            bgcolor="rgba(30,30,80,0.6)", borderpad=4),
        annotation_position="top left")

    min_idx, max_idx = prices.idxmin(), prices.idxmax()
    fig.add_annotation(x=dates[min_idx], y=prices[min_idx],
        text=f"⬇ Lowest: {low_p:,.0f}", showarrow=True, arrowhead=2,
        ax=0, ay=40, font=dict(color=C["green"], size=12),
        arrowcolor=C["green"], bgcolor="rgba(16,185,129,0.12)", borderpad=5)
    fig.add_annotation(x=dates[max_idx], y=prices[max_idx],
        text=f"⬆ Highest: {high_p:,.0f}", showarrow=True, arrowhead=2,
        ax=0, ay=-40, font=dict(color=C["red"], size=12),
        arrowcolor=C["red"], bgcolor="rgba(239,68,68,0.12)", borderpad=5)

    fig.update_layout(**layout(
        title=dict(text=f"<b>{price_col} Trend Over Time</b>", font=dict(size=18), x=0.01),
        xaxis_title=date_col, yaxis_title=price_col,
        hovermode="x unified",
        legend=dict(**_BASE["legend"], orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    ))

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📊 Price distribution", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            fig3 = go.Figure()
            fig3.add_trace(go.Histogram(x=prices, nbinsx=20,
                marker=dict(color=C["purple"], opacity=0.75, line=dict(width=0)),
                hovertemplate="Range: %{x}<br>Count: %{y}<extra></extra>"))
            fig3.add_vline(x=median_p, line=dict(color=C["amber"], width=2, dash="dash"),
                annotation=dict(text=f"Median {median_p:,.0f}", font=dict(color=C["amber"])))
            fig3.update_layout(**layout(
                title=dict(text="<b>Price Distribution</b>", font=dict(size=14), x=0.01),
                xaxis_title=price_col, yaxis_title="Count",
                showlegend=False, height=290, margin=dict(t=55, b=50, l=55, r=20),
            ))
            st.plotly_chart(fig3, use_container_width=True)

        with c2:
            fig4 = go.Figure()
            fig4.add_trace(go.Box(y=prices,
                marker=dict(color=C["blue"]), line=dict(color=C["blue"]),
                fillcolor="rgba(59,130,246,0.15)",
                hovertemplate="Price: %{y:,.0f}<extra></extra>",
                name=price_col))
            fig4.update_layout(**layout(
                title=dict(text="<b>Box Plot</b>", font=dict(size=14), x=0.01),
                yaxis_title=price_col, showlegend=False,
                height=290, margin=dict(t=55, b=50, l=55, r=20),
            ))
            st.plotly_chart(fig4, use_container_width=True)

    with st.expander("🗂️ Raw data table"):
        disp = df[[date_col, price_col]].copy()
        disp[date_col] = disp[date_col].dt.strftime("%b %d, %Y")
        if "MA" in df.columns:
            disp[f"MA({ma_win})"] = df["MA"].round(0).astype("Int64")
        st.dataframe(disp, use_container_width=True, hide_index=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin-top:3rem;"/>
<p style="text-align:center;color:rgba(200,200,255,0.3);font-size:0.75rem;padding-bottom:1rem;">
  Deal Price Analyzer &nbsp;·&nbsp; Built with Streamlit + Plotly
</p>
""", unsafe_allow_html=True)
