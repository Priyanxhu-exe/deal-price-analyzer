import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Deal Price Analyzer",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

  :root {
    --bg: #0d0f12;
    --panel: #14171b;
    --panel-alt: #191c21;
    --border: #23262b;
    --border-bright: #2f333a;
    --text: #e7e9ec;
    --text-dim: #8b909a;
    --text-faint: #565b64;
    --accent: #5b8ef2;
    --accent-dim: #7c8797;
    --green: #3ecf8e;
    --red: #f0625f;
  }

  html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
  .stApp { background: var(--bg); }
  [data-testid="stAppViewContainer"] { background: var(--bg); }
  [data-testid="stHeader"] { background: transparent; }

  * { font-variant-numeric: tabular-nums; }
  ::selection { background: rgba(91,142,242,0.25); color: var(--text); }
  a, button, input, select, textarea, [tabindex] { outline-color: var(--accent) !important; }

  @media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
  }

  .block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }

  /* ─── Sidebar ─────────────────────────────────────────────────────── */
  [data-testid="stSidebar"] {
    background: var(--panel) !important;
    border-right: 1px solid var(--border);
  }
  [data-testid="stSidebar"] label {
    color: var(--text-dim) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
  }
  [data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }

  .sidebar-logo {
    padding: 0 0 0.9rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.55rem;
  }
  .sidebar-logo-mark {
    width: 22px; height: 22px;
    border-radius: 2px;
    background: var(--accent);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; font-weight: 700; color: #0d0f12;
  }
  .sidebar-logo-text {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -0.01em;
  }
  .sidebar-section {
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--text-faint);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin: 1.25rem 0 0.4rem;
  }

  .col-info {
    background: var(--panel-alt);
    border: 1px solid var(--border);
    padding: 0.5rem 0.65rem;
    border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-dim);
    word-break: break-all;
    line-height: 1.5;
  }

  [data-testid="stFileUploadDropzone"] {
    background: var(--panel-alt) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
  }
  [data-testid="stSidebar"] input, [data-testid="stSidebar"] select,
  [data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: var(--panel-alt) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 2px !important;
    font-size: 0.85rem !important;
  }
  input[type="checkbox"] { accent-color: var(--accent); }

  /* Dark-theme fixes for Streamlit's baseweb popovers/menus — these render
     with a default light background unless explicitly overridden, which is
     the kind of inconsistency that quietly undercuts an otherwise dark UI. */
  [data-baseweb="popover"], [data-baseweb="menu"] {
    background: var(--panel-alt) !important;
    border: 1px solid var(--border-bright) !important;
  }
  [data-baseweb="menu"] li {
    color: var(--text) !important;
    font-size: 0.85rem !important;
  }
  [data-baseweb="menu"] li:hover { background: var(--border) !important; }

  [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background: var(--accent) !important;
  }
  [data-testid="stSlider"] [role="slider"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
  }
  [data-testid="stThumbValue"] {
    background: var(--panel-alt) !important;
    color: var(--text) !important;
    border: 1px solid var(--border-bright) !important;
  }
  [data-testid="stNumberInput"] button {
    background: var(--panel-alt) !important;
    border-color: var(--border) !important;
    color: var(--text-dim) !important;
  }

  /* ─── Masthead ──────────────────────────────────────────────────────
     Plain and quiet: title, one-line context, nothing performative. */
  .masthead {
    display: flex;
    align-items: baseline;
    gap: 0.9rem;
    flex-wrap: wrap;
    margin-bottom: 0.3rem;
  }
  .main-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
    margin: 0;
  }
  .masthead-mode {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-faint);
    padding-left: 0.9rem;
    border-left: 1px solid var(--border-bright);
  }
  .main-subtitle {
    color: var(--text-faint);
    font-size: 0.85rem;
    margin: 0.15rem 0 1.8rem;
  }

  /* ─── Rail panel ──────────────────────────────────────────────────── */
  .rail-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 1.1rem 1.25rem;
    height: 100%;
  }
  .rail-hero-label {
    display: block;
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--text-faint);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
  }
  .rail-hero-value {
    display: block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.7rem;
    font-weight: 600;
    color: var(--accent);
    line-height: 1.2;
    margin-bottom: 0.85rem;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid var(--border);
  }
  .rail-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 0.42rem 0.4rem;
    margin: 0 -0.4rem;
    border-radius: 2px;
    transition: background 0.12s ease;
  }
  .rail-row:hover { background: var(--panel-alt); }
  .rail-row-label {
    font-size: 0.78rem;
    color: var(--text-dim);
  }
  .rail-row-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.92rem;
    font-weight: 600;
  }
  .v-green { color: var(--green); }
  .v-red { color: var(--red); }
  .v-dim { color: var(--accent-dim); }
  .v-text { color: var(--text); }

  .chart-caption {
    font-size: 0.76rem;
    font-weight: 500;
    color: var(--text-faint);
    margin: 0 0 0.7rem 0.1rem;
  }

  /* ─── Tabs ──────────────────────────────────────────────────────── */
  [data-baseweb="tab-list"] {
    gap: 1.4rem;
    border-bottom: 1px solid var(--border);
    background: transparent;
  }
  [data-baseweb="tab"] {
    font-size: 0.8rem !important;
    font-weight: 500;
    color: var(--text-faint) !important;
    background: transparent !important;
    padding-bottom: 0.55rem !important;
    transition: color 0.12s ease;
  }
  [data-baseweb="tab"]:hover { color: var(--text-dim) !important; }
  [data-baseweb="tab"][aria-selected="true"] { color: var(--text) !important; }
  [data-baseweb="tab-highlight"] { background-color: var(--accent) !important; height: 2px !important; }
  [data-testid="stTabs"] { margin-top: 0.3rem; }

  [data-testid="stExpander"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
  }
  [data-testid="stAlert"] {
    background: var(--panel-alt) !important;
    border: 1px solid var(--border-bright) !important;
    border-left: 3px solid var(--red) !important;
    border-radius: 2px !important;
    font-size: 0.85rem !important;
  }
  [data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
  }

  hr.hairline { border: none; border-top: 1px solid var(--border); margin: 2.4rem 0 1.2rem; }

  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 3px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
</style>
""", unsafe_allow_html=True)

C = {
    "accent": "#5b8ef2", "accent_dim": "#7c8797", "green": "#3ecf8e", "red": "#f0625f",
    "text": "#e7e9ec", "text_dim": "#8b909a", "grid": "rgba(255,255,255,0.045)",
    "border": "rgba(255,255,255,0.07)",
}

_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Sans, sans-serif", color=C["text_dim"], size=12),
    margin=dict(t=20, b=55, l=55, r=25),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
        borderwidth=0,
        font=dict(size=11),
    ),
    hoverlabel=dict(
        bgcolor="#191c21",
        bordercolor="var(--border-bright)",
        font=dict(family="IBM Plex Mono, monospace", size=12, color=C["text"]),
    ),
    xaxis=dict(gridcolor=C["grid"], zeroline=False, linecolor=C["border"], showline=True, tickfont=dict(family="IBM Plex Mono, monospace", size=11)),
    yaxis=dict(gridcolor=C["grid"], zeroline=False, linecolor=C["border"], showline=True, tickfont=dict(family="IBM Plex Mono, monospace", size=11)),
)


def layout(**overrides):
    merged = dict(_BASE)
    merged.update(overrides)
    return merged


def stats(prices):
    return prices.median(), prices.min(), prices.max()


def bar_color(margin):
    if margin <= 0:
        return C["green"]
    elif margin <= 5:
        return C["accent"]
    return C["red"]


def render_rail(hero_label, hero_value, rows):
    """rows: list of (label, value, css_class) tuples, ranked by importance."""
    rows_html = "".join(
        f'<div class="rail-row"><span class="rail-row-label">{label}</span>'
        f'<span class="rail-row-value {cls}">{value}</span></div>'
        for label, value, cls in rows
    )
    st.markdown(f"""
    <div class="rail-panel">
      <span class="rail-hero-label">{hero_label}</span>
      <span class="rail-hero-value">{hero_value}</span>
      {rows_html}
    </div>
    """, unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown(
        '<div class="sidebar-logo"><span class="sidebar-logo-mark">D</span>'
        '<span class="sidebar-logo-text">Deal Price Analyzer</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<p class="sidebar-section">Analysis Mode</p>', unsafe_allow_html=True)
    mode = st.selectbox("Mode", ["Seller Comparison", "Price Trend"], label_visibility="collapsed")
    st.markdown('<p class="sidebar-section">Data Source</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload .xlsx", type=["xlsx"])

# Header
st.markdown(f"""
<div class="masthead">
  <h1 class="main-title">Deal Price Analyzer</h1>
  <span class="masthead-mode">{mode}</span>
</div>
<p class="main-subtitle">Price intelligence and market comparison</p>
""", unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown("""
    <div style="text-align:center;padding:3.5rem 2rem;border:1px solid var(--border);border-radius:2px;background:var(--panel);">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#565b64" stroke-width="1.4"
           style="margin-bottom:1rem;">
        <path d="M3 17 L9 10 L13 14 L21 5" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M15 5 L21 5 L21 11" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M3 20 L21 20" stroke-linecap="round"/>
      </svg>
      <h3 style="color:var(--text);font-weight:600;font-size:1rem;margin-bottom:0.4rem;">No file loaded</h3>
      <p style="color:var(--text-dim);font-size:0.85rem;max-width:400px;margin:auto;">
        Upload an .xlsx file from the sidebar to start analyzing prices.
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

try:
    df = pd.read_excel(uploaded_file)
except Exception as e:
    st.error(f"Could not read the file: {e}")
    st.stop()

with st.sidebar:
    st.markdown('<p class="sidebar-section">Detected Columns</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="col-info">{" · ".join(df.columns.tolist())}</div>', unsafe_allow_html=True)

# MODE 1 — SELLER COMPARISON
if mode == "Seller Comparison":
    with st.sidebar:
        st.markdown('<p class="sidebar-section">Configuration</p>', unsafe_allow_html=True)
        price_col = st.text_input("Price column", "Price")
        label_col = st.text_input("Seller / source column", "Seller")
        base_price = st.number_input("Base price for comparison", value=1050.0, step=10.0)

    for col in (price_col, label_col):
        if col not in df.columns:
            st.error(f"Column '{col}' not found. Available: {list(df.columns)}")
            st.stop()

    df["Margin %"] = ((df[price_col] - base_price) / base_price) * 100
    sdf = df.sort_values(by=price_col).reset_index(drop=True)
    sdf["Margin % Display"] = sdf["Margin %"].map(lambda v: f"{v:+.2f}%")
    median_p, low_p, high_p = stats(sdf[price_col])

    chart_col, rail_col = st.columns([2.3, 1], gap="large")

    with chart_col:
        st.markdown(f'<p class="chart-caption">{price_col} by {label_col}</p>', unsafe_allow_html=True)

        colors = sdf["Margin %"].apply(bar_color).tolist()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=sdf[label_col], y=sdf[price_col],
            marker=dict(color=colors, opacity=0.92, line=dict(width=0)),
            customdata=sdf[["Margin % Display"]],
            hovertemplate="<b>%{x}</b><br>Price: <b>%{y:,.0f}</b><br>Margin: <b>%{customdata[0]}</b><extra></extra>",
            name="Price",
        ))

        fig.add_hline(y=base_price,
            line=dict(color=C["accent"], width=1.5, dash="dot"),
            annotation=dict(text=f"base {base_price:,.0f}", font=dict(color=C["accent"], size=11),
                            bgcolor="rgba(0,0,0,0)"),
            annotation_position="top right")

        fig.add_hline(y=median_p,
            line=dict(color=C["accent_dim"], width=1, dash="dash"),
            annotation=dict(text=f"median {median_p:,.0f}", font=dict(color=C["accent_dim"], size=11),
                            bgcolor="rgba(0,0,0,0)"),
            annotation_position="bottom right")

        fig.update_layout(**layout(
            xaxis_title=label_col, yaxis_title=price_col,
            showlegend=False, bargap=0.4, height=400,
        ))

        st.plotly_chart(fig, use_container_width=True)

    with rail_col:
        render_rail(
            hero_label="Base Price",
            hero_value=f"{base_price:,.0f}",
            rows=[
                ("Median", f"{median_p:,.0f}", "v-dim"),
                ("Lowest", f"{low_p:,.0f}", "v-green"),
                ("Highest", f"{high_p:,.0f}", "v-red"),
                ("Spread", f"{high_p - low_p:,.0f}", "v-text"),
            ],
        )

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Margin breakdown", "Raw data"])

    with tab1:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=sdf[label_col], y=sdf["Margin %"],
            marker=dict(color=sdf["Margin %"].apply(bar_color), opacity=0.9, line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>Margin: <b>%{y:+.2f}%</b><extra></extra>",
        ))
        fig2.add_hline(y=0, line=dict(color="rgba(231,233,236,0.2)", width=1))
        fig2.update_layout(**layout(
            xaxis_title=label_col, yaxis_title="Margin %",
            showlegend=False, bargap=0.4, height=300,
        ))
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
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
            st.error(f"Column '{col}' not found. Available: {list(df.columns)}")
            st.stop()

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(by=date_col).reset_index(drop=True)
    prices, dates = df[price_col], df[date_col]
    median_p, low_p, high_p = stats(prices)

    if show_ma and ma_win:
        df["MA"] = prices.rolling(ma_win, min_periods=1).mean()

    chart_col, rail_col = st.columns([2.3, 1], gap="large")

    with chart_col:
        st.markdown(f'<p class="chart-caption">{price_col} trend over time</p>', unsafe_allow_html=True)

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=dates, y=prices, mode="lines",
            line=dict(color=C["accent"], width=0),
            fill="tozeroy", fillcolor="rgba(91,142,242,0.06)",
            hoverinfo="skip", showlegend=False))

        fig.add_trace(go.Scatter(x=dates, y=prices,
            mode="lines+markers",
            line=dict(color=C["accent"], width=2),
            marker=dict(size=4.5, color=C["accent"], line=dict(color="#0d0f12", width=1)),
            hovertemplate=f"<b>%{{x|%b %d, %Y}}</b><br>{price_col}: <b>%{{y:,.0f}}</b><extra></extra>",
            name=price_col))

        if show_ma and ma_win and "MA" in df.columns:
            fig.add_trace(go.Scatter(x=dates, y=df["MA"],
                mode="lines", line=dict(color=C["accent_dim"], width=1.5, dash="dot"),
                hovertemplate=f"MA({ma_win}): <b>%{{y:,.0f}}</b><extra></extra>",
                name=f"MA({ma_win})"))

        fig.add_hline(y=median_p,
            line=dict(color=C["accent_dim"], width=1, dash="dash"),
            annotation=dict(text=f"median {median_p:,.0f}",
                font=dict(color=C["accent_dim"], size=11), bgcolor="rgba(0,0,0,0)"),
            annotation_position="top left")

        min_idx, max_idx = prices.idxmin(), prices.idxmax()
        fig.add_annotation(x=dates[min_idx], y=prices[min_idx],
            text=f"low {low_p:,.0f}", showarrow=True, arrowhead=0, arrowwidth=1,
            ax=0, ay=28, font=dict(color=C["green"], size=11),
            arrowcolor=C["green"], bgcolor="rgba(0,0,0,0)")
        fig.add_annotation(x=dates[max_idx], y=prices[max_idx],
            text=f"high {high_p:,.0f}", showarrow=True, arrowhead=0, arrowwidth=1,
            ax=0, ay=-28, font=dict(color=C["red"], size=11),
            arrowcolor=C["red"], bgcolor="rgba(0,0,0,0)")

        fig.update_layout(**layout(
            xaxis_title=date_col, yaxis_title=price_col,
            hovermode="x unified", height=400,
            legend=dict(**_BASE["legend"], orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        ))

        st.plotly_chart(fig, use_container_width=True)

    with rail_col:
        render_rail(
            hero_label="Median",
            hero_value=f"{median_p:,.0f}",
            rows=[
                ("Lowest", f"{low_p:,.0f}", "v-green"),
                ("Highest", f"{high_p:,.0f}", "v-red"),
                ("Range", f"{high_p - low_p:,.0f}", "v-text"),
            ],
        )

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Distribution", "Raw data"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig3 = go.Figure()
            fig3.add_trace(go.Histogram(x=prices, nbinsx=20,
                marker=dict(color=C["accent"], opacity=0.82, line=dict(width=0)),
                hovertemplate="Range: %{x}<br>Count: %{y}<extra></extra>"))
            fig3.add_vline(x=median_p, line=dict(color=C["accent_dim"], width=1.5, dash="dash"),
                annotation=dict(text=f"median {median_p:,.0f}", font=dict(color=C["accent_dim"])))
            fig3.update_layout(**layout(
                xaxis_title=price_col, yaxis_title="Count",
                showlegend=False, height=280, margin=dict(t=20, b=45, l=45, r=15),
            ))
            st.plotly_chart(fig3, use_container_width=True)

        with c2:
            fig4 = go.Figure()
            fig4.add_trace(go.Box(y=prices,
                marker=dict(color=C["accent"]), line=dict(color=C["accent"]),
                fillcolor="rgba(91,142,242,0.1)",
                hovertemplate="Price: %{y:,.0f}<extra></extra>",
                name=price_col))
            fig4.update_layout(**layout(
                yaxis_title=price_col, showlegend=False,
                height=280, margin=dict(t=20, b=45, l=45, r=15),
            ))
            st.plotly_chart(fig4, use_container_width=True)

    with tab2:
        disp = df[[date_col, price_col]].copy()
        disp[date_col] = disp[date_col].dt.strftime("%b %d, %Y")
        if "MA" in df.columns:
            disp[f"MA({ma_win})"] = df["MA"].round(0).astype("Int64")
        st.dataframe(disp, use_container_width=True, hide_index=True)

# Footer
st.markdown("""
<hr class="hairline"/>
<p style="text-align:center;color:var(--text-faint);font-size:0.75rem;padding-bottom:1rem;">
  Deal Price Analyzer &nbsp;·&nbsp; Built with Streamlit + Plotly
</p>
""", unsafe_allow_html=True)