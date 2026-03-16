
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Capital Structure Theories | The Mountain Path",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Styling ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600&family=Roboto+Mono:wght@400;500&display=swap');

:root {
    --dark-blue: #003366;
    --mid-blue: #004d80;
    --card-bg: #112240;
    --light-blue: #ADD8E6;
    --gold: #FFD700;
    --text: #e6f1ff;
    --muted: #8892b0;
    --green: #28a745;
    --red: #dc3545;
    --bg-gradient: linear-gradient(135deg, #1a2332, #243447, #2a3f5f);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-gradient) !important;
    font-family: 'Source Sans 3', sans-serif;
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #0f2040 100%) !important;
    border-right: 2px solid var(--gold);
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3,
[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text) !important;
}

/* Sliders */
.stSlider label { color: var(--light-blue) !important; font-weight: 600; }
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--gold) !important;
    border-color: var(--gold) !important;
}

/* Selectbox & radio */
.stSelectbox label, .stRadio label { color: var(--light-blue) !important; font-weight: 600; }
[data-baseweb="select"] { background: #0a1628 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,51,102,0.6) !important;
    border-radius: 8px 8px 0 0;
    gap: 4px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    font-family: 'Source Sans 3', sans-serif;
    font-weight: 600;
    border-radius: 6px;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background: var(--gold) !important;
    color: #0a1628 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: rgba(17,34,64,0.7) !important;
    border-radius: 0 8px 8px 8px;
    padding: 20px;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #0f2040, #1a3a5c);
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.metric-card:hover { border-color: var(--gold); transform: translateY(-2px); }
.metric-label {
    font-size: 0.78rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
    font-family: 'Roboto Mono', monospace;
}
.metric-value {
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--gold);
    font-family: 'Roboto Mono', monospace;
}
.metric-delta {
    font-size: 0.75rem;
    margin-top: 4px;
}
.metric-delta.pos { color: var(--green); }
.metric-delta.neg { color: var(--red); }

/* Section headers */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: var(--gold);
    border-bottom: 2px solid rgba(255,215,0,0.3);
    padding-bottom: 8px;
    margin: 20px 0 16px 0;
}
.theory-tag {
    display: inline-block;
    background: rgba(0,51,102,0.8);
    border: 1px solid var(--gold);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.7rem;
    color: var(--gold);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: 'Roboto Mono', monospace;
    margin-bottom: 10px;
}

/* Info boxes */
.info-box {
    background: rgba(0,77,128,0.25);
    border-left: 4px solid var(--light-blue);
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 0.88rem;
    line-height: 1.6;
    color: var(--text);
}
.formula-box {
    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(255,215,0,0.4);
    border-radius: 8px;
    padding: 12px 18px;
    font-family: 'Roboto Mono', monospace;
    font-size: 0.82rem;
    color: #FFD700;
    margin: 8px 0;
    line-height: 1.8;
}
.insight-box {
    background: rgba(40,167,69,0.12);
    border-left: 4px solid var(--green);
    border-radius: 0 8px 8px 0;
    padding: 12px 18px;
    margin: 10px 0;
    font-size: 0.85rem;
    color: var(--text);
}
.warning-box {
    background: rgba(220,53,69,0.12);
    border-left: 4px solid var(--red);
    border-radius: 0 8px 8px 0;
    padding: 12px 18px;
    margin: 10px 0;
    font-size: 0.85rem;
    color: var(--text);
}

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, rgba(0,51,102,0.95), rgba(0,77,128,0.85));
    border: 1px solid rgba(255,215,0,0.5);
    border-radius: 16px;
    padding: 30px 40px;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '⛰️';
    position: absolute;
    right: 30px;
    top: 20px;
    font-size: 5rem;
    opacity: 0.12;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 900;
    color: var(--gold);
    margin: 0 0 6px 0;
    line-height: 1.2;
}
.hero-subtitle {
    color: var(--light-blue);
    font-size: 1rem;
    margin: 0;
    letter-spacing: 0.5px;
}
.hero-brand {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 12px;
}

/* Comparison table */
.comp-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 10px;
    overflow: hidden;
    font-size: 0.85rem;
}
.comp-table th {
    background: var(--dark-blue);
    color: var(--gold);
    padding: 10px 14px;
    font-family: 'Roboto Mono', monospace;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 2px solid var(--gold);
}
.comp-table td {
    padding: 9px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: var(--text);
    vertical-align: top;
}
.comp-table tr:nth-child(even) td { background: rgba(255,255,255,0.03); }
.comp-table tr:last-child td { border-bottom: none; }

/* Footer */
.footer {
    background: linear-gradient(90deg, #0a1628, #0f2040);
    border-top: 2px solid rgba(255,215,0,0.4);
    border-radius: 0 0 12px 12px;
    padding: 14px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 30px;
}
.footer-left { font-family: 'Roboto Mono', monospace; font-size: 0.78rem; color: var(--gold); }
.footer-right { font-size: 0.75rem; color: var(--muted); }
.footer a { color: var(--gold); text-decoration: none; margin: 0 6px; }
.footer a:hover { color: var(--light-blue); }

/* Sidebar theory nav */
.sidebar-theory {
    background: rgba(0,51,102,0.4);
    border: 1px solid rgba(255,215,0,0.25);
    border-radius: 8px;
    padding: 10px 14px;
    margin: 6px 0;
    cursor: pointer;
    font-size: 0.85rem;
    color: var(--text);
}

/* Hide streamlit default UI noise */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Plotly theme ───────────────────────────────────────────────────────────────
COLORS = {
    "gold": "#FFD700",
    "light_blue": "#ADD8E6",
    "dark_blue": "#003366",
    "mid_blue": "#004d80",
    "green": "#28a745",
    "red": "#dc3545",
    "purple": "#9B59B6",
    "orange": "#E67E22",
    "teal": "#17A589",
    "pink": "#E91E63",
}

def plotly_base_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(family="Playfair Display", size=18, color=COLORS["gold"])),
        paper_bgcolor="rgba(10,22,40,0.0)",
        plot_bgcolor="rgba(17,34,64,0.5)",
        font=dict(family="Source Sans 3", color="#e6f1ff", size=12),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False, title_font_color="#ADD8E6", tickfont_color="#8892b0"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False, title_font_color="#ADD8E6", tickfont_color="#8892b0"),
        legend=dict(bgcolor="rgba(0,0,0,0.4)", bordercolor="rgba(255,215,0,0.3)", borderwidth=1, font=dict(color="#e6f1ff")),
        margin=dict(l=50, r=30, t=60, b=50),
        hovermode="x unified",
    )

# ─── Hero Banner ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">Capital Structure Theories</div>
    <div class="hero-subtitle">Net Income · Net Operating Income · Modigliani-Miller (No Tax & Tax) · Firm Valuation</div>
    <div class="hero-brand">⛰️ The Mountain Path — World of Finance &nbsp;|&nbsp; Prof. V. Ravichandran</div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 20px 0;">
        <div style="font-family:'Playfair Display',serif; font-size:1.4rem; color:#FFD700; font-weight:900;">⛰️ Mountain Path</div>
        <div style="font-size:0.7rem; color:#8892b0; text-transform:uppercase; letter-spacing:2px;">Finance Education</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="color:#ADD8E6; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">📐 Base Parameters</div>', unsafe_allow_html=True)

    EBIT = st.slider("EBIT (₹ Lakhs)", min_value=10, max_value=500, value=100, step=5,
                     help="Earnings Before Interest & Taxes")
    ke_unlevered = st.slider("Equity Cap. Rate — Unlevered Firm (Kₑᵤ %)", 8.0, 25.0, 12.0, 0.5,
                              help="Required return for unlevered firm")
    kd = st.slider("Cost of Debt (Kd %)", 4.0, 18.0, 8.0, 0.5,
                   help="Interest rate on debt")
    tax_rate = st.slider("Corporate Tax Rate (%)", 0.0, 50.0, 30.0, 1.0)
    total_capital = st.slider("Total Capital (₹ Lakhs)", 100, 2000, 500, 50,
                               help="Total firm capital (Debt + Equity)")
    max_debt_pct = st.slider("Max Debt % of Capital", 10, 90, 80, 5)

    st.markdown("---")
    st.markdown('<div style="color:#ADD8E6; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">📈 NI Theory Parameters</div>', unsafe_allow_html=True)

    ke_ni = st.slider("Equity Cap. Rate — NI Theory (Kₑ %)", 8.0, 25.0, 12.0, 0.5,
                      help="Assumed constant in NI Approach")

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Roboto Mono',monospace; font-size:0.65rem; color:#8892b0; text-align:center; line-height:1.8;">
        Prof. V. Ravichandran<br>
        28+ Yrs Corporate Finance & Banking<br>
        10+ Yrs Academic Excellence<br><br>
        <a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="color:#FFD700; text-decoration:none;">🔗 LinkedIn</a>
        &nbsp;|&nbsp;
        <a href="https://github.com/trichyravis" target="_blank" style="color:#FFD700; text-decoration:none;">💻 GitHub</a>
    </div>
    """, unsafe_allow_html=True)

# ─── Computations ────────────────────────────────────────────────────────────────
debt_levels = np.arange(0, max_debt_pct + 1, 1) / 100
D_arr = total_capital * debt_levels
E_arr = total_capital - D_arr

# Safe equity array (avoid div zero)
E_safe = np.where(E_arr <= 0, 0.001, E_arr)

interest_arr = D_arr * (kd / 100)
EBT_arr = EBIT - interest_arr
EAT_arr = np.maximum(EBT_arr * (1 - tax_rate / 100), 0)

# ── NI Approach ─────────────────────────────────────────────────────────────────
# Vf = EAT/ke + D (market value)
Vf_NI = EAT_arr / (ke_ni / 100) + D_arr
WACC_NI = EBIT / Vf_NI * 100

# ── NOI Approach ────────────────────────────────────────────────────────────────
# Total firm value constant = EBIT / k0; WACC = k0 constant
Vf_NOI = np.full_like(D_arr, EBIT / (ke_unlevered / 100))
ke_NOI = (EBIT - interest_arr) / E_safe * 100  # residual for equity holders
WACC_NOI = np.full_like(D_arr, ke_unlevered)

# ── MM No Tax ────────────────────────────────────────────────────────────────────
# Proposition I: VL = VU (no tax)
Vu_MMnotax = EBIT / (ke_unlevered / 100)
Vf_MMnotax = np.full_like(D_arr, Vu_MMnotax)
# Proposition II: ke = ke_u + (ke_u - kd) * D/E
ke_MMnotax = ke_unlevered + (ke_unlevered - kd) * (D_arr / E_safe)
WACC_MMnotax = np.full_like(D_arr, ke_unlevered)

# ── MM With Tax ──────────────────────────────────────────────────────────────────
# Proposition I: VL = VU + T*D
Vu_MMtax = EBIT * (1 - tax_rate / 100) / (ke_unlevered / 100)
Vf_MMtax = Vu_MMtax + (tax_rate / 100) * D_arr
# Proposition II: ke = ke_u + (ke_u - kd)(1-T) * D/E
ke_MMtax = ke_unlevered + (ke_unlevered - kd) * (1 - tax_rate / 100) * (D_arr / E_safe)
# WACC with tax
WACC_MMtax = (ke_MMtax * E_safe / (E_safe + D_arr) + kd * (1 - tax_rate / 100) * D_arr / (E_safe + D_arr)) * 100

# ─── Tabs ────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview", "📘 NI Approach", "📗 NOI Approach",
    "📙 MM No Tax", "📕 MM With Tax", "🔬 Comparison", "🎓 Education Notes"
])

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Capital Structure Theories — At a Glance</div>', unsafe_allow_html=True)

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">EBIT</div>
            <div class="metric-value">₹{EBIT:,}</div>
            <div class="metric-delta pos">Earnings Before I & T</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Unlevered Firm Value (VU)</div>
            <div class="metric-value">₹{Vu_MMtax:,.0f}</div>
            <div class="metric-delta">EBIT(1-T) / Kₑᵤ</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Max Tax Shield</div>
            <div class="metric-value">₹{(tax_rate/100)*total_capital*(max_debt_pct/100):,.0f}</div>
            <div class="metric-delta pos">T × D at max leverage</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Capital</div>
            <div class="metric-value">₹{total_capital:,}</div>
            <div class="metric-delta">D + E Base</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # All theories firm value chart
    fig_ov = go.Figure()
    x_pct = debt_levels * 100
    fig_ov.add_trace(go.Scatter(x=x_pct, y=Vf_NI, name="NI Approach", line=dict(color=COLORS["gold"], width=2.5), mode="lines"))
    fig_ov.add_trace(go.Scatter(x=x_pct, y=Vf_NOI, name="NOI Approach", line=dict(color=COLORS["light_blue"], width=2.5, dash="dash"), mode="lines"))
    fig_ov.add_trace(go.Scatter(x=x_pct, y=Vf_MMnotax, name="MM (No Tax)", line=dict(color=COLORS["teal"], width=2.5, dash="dot"), mode="lines"))
    fig_ov.add_trace(go.Scatter(x=x_pct, y=Vf_MMtax, name="MM (With Tax)", line=dict(color=COLORS["green"], width=3), mode="lines"))
    fig_ov.add_hline(y=Vu_MMtax, line_dash="longdash", line_color=COLORS["red"], opacity=0.5,
                     annotation_text="Unlevered VU", annotation_font_color=COLORS["red"])
    layout = plotly_base_layout("Firm Value (V) vs Debt Level — All Theories")
    layout["xaxis"]["title"] = "Debt as % of Total Capital"
    layout["yaxis"]["title"] = "Firm Value (₹ Lakhs)"
    fig_ov.update_layout(**layout)
    st.plotly_chart(fig_ov, use_container_width=True)

    # Theory comparison table
    st.markdown('<div class="section-header">Theory Comparison Matrix</div>', unsafe_allow_html=True)
    st.markdown("""
    <table class="comp-table">
      <tr>
        <th>Dimension</th>
        <th>NI Approach</th>
        <th>NOI Approach</th>
        <th>MM (No Tax)</th>
        <th>MM (With Tax)</th>
      </tr>
      <tr>
        <td><b>Optimal Structure?</b></td>
        <td style="color:#FFD700">✔ 100% Debt</td>
        <td style="color:#dc3545">✘ None exists</td>
        <td style="color:#dc3545">✘ None exists</td>
        <td style="color:#FFD700">✔ 100% Debt</td>
      </tr>
      <tr>
        <td><b>Firm Value</b></td>
        <td>Rises with leverage</td>
        <td>Constant</td>
        <td>Constant (VL=VU)</td>
        <td>Rises (VL=VU+T·D)</td>
      </tr>
      <tr>
        <td><b>WACC</b></td>
        <td>Decreases with debt</td>
        <td>Constant (=K₀)</td>
        <td>Constant (=Kₑᵤ)</td>
        <td>Decreases with debt</td>
      </tr>
      <tr>
        <td><b>Ke assumption</b></td>
        <td>Constant</td>
        <td>Rises with leverage</td>
        <td>Rises with leverage</td>
        <td>Rises (lower slope, tax adjusted)</td>
      </tr>
      <tr>
        <td><b>Market Efficiency?</b></td>
        <td>Not assumed</td>
        <td>Not assumed</td>
        <td>Perfect markets</td>
        <td>Perfect markets</td>
      </tr>
      <tr>
        <td><b>Taxes</b></td>
        <td>Ignored</td>
        <td>Ignored</td>
        <td>Ignored</td>
        <td>Corporate tax included</td>
      </tr>
      <tr>
        <td><b>Key Insight</b></td>
        <td>Cheaper debt lowers WACC</td>
        <td>Financial risk offsets debt benefit</td>
        <td>Arbitrage ensures VL = VU</td>
        <td>Tax shield adds value</td>
      </tr>
    </table>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 2: NI APPROACH
# ══════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="theory-tag">Net Income Approach</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Net Income (NI) Approach — David Durand</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <b>Core Premise:</b> Both Kd (cost of debt) and Ke (cost of equity) remain <u>constant</u> regardless
        of leverage. Since debt is cheaper than equity, increasing debt lowers WACC and increases firm value.
        The optimal structure is 100% debt financing.
    </div>
    <div class="formula-box">
        V_F  =  EAT / Kₑ  +  D<br>
        WACC =  EBIT / V_F<br>
        EAT  =  (EBIT − Interest) × (1 − T)
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_ni1 = go.Figure()
        fig_ni1.add_trace(go.Scatter(x=x_pct, y=Vf_NI, name="Firm Value (V_F)", fill="tozeroy",
                                      fillcolor="rgba(255,215,0,0.08)", line=dict(color=COLORS["gold"], width=3)))
        layout1 = plotly_base_layout("NI: Firm Value vs Leverage")
        layout1["xaxis"]["title"] = "Debt % of Capital"
        layout1["yaxis"]["title"] = "Firm Value (₹ Lakhs)"
        fig_ni1.update_layout(**layout1)
        st.plotly_chart(fig_ni1, use_container_width=True)

    with c2:
        fig_ni2 = go.Figure()
        fig_ni2.add_trace(go.Scatter(x=x_pct, y=np.full_like(x_pct, ke_ni), name="Kₑ (constant)",
                                      line=dict(color=COLORS["gold"], width=2.5, dash="dot")))
        fig_ni2.add_trace(go.Scatter(x=x_pct, y=np.full_like(x_pct, kd), name="Kd (constant)",
                                      line=dict(color=COLORS["light_blue"], width=2.5, dash="dot")))
        fig_ni2.add_trace(go.Scatter(x=x_pct, y=WACC_NI, name="WACC (declining)",
                                      line=dict(color=COLORS["green"], width=3)))
        layout2 = plotly_base_layout("NI: Cost of Capital vs Leverage")
        layout2["xaxis"]["title"] = "Debt % of Capital"
        layout2["yaxis"]["title"] = "Cost of Capital (%)"
        fig_ni2.update_layout(**layout2)
        st.plotly_chart(fig_ni2, use_container_width=True)

    # Data table
    st.markdown('<div class="section-header">NI Approach — Data Table</div>', unsafe_allow_html=True)
    steps = np.arange(0, max_debt_pct + 1, 10)
    ni_rows = []
    for s in steps:
        i = s
        d = total_capital * i / 100
        e = total_capital - d
        intr = d * kd / 100
        eat = max((EBIT - intr) * (1 - tax_rate / 100), 0)
        v = eat / (ke_ni / 100) + d if e > 0 else 0
        w = EBIT / v * 100 if v > 0 else 0
        ni_rows.append({"Debt %": f"{i}%", "Debt (D)": f"₹{d:,.0f}", "Equity (E)": f"₹{e:,.0f}",
                        "Interest": f"₹{intr:,.0f}", "EAT": f"₹{eat:,.0f}",
                        "Firm Value": f"₹{v:,.0f}", "WACC %": f"{w:.2f}%"})
    df_ni = pd.DataFrame(ni_rows)
    st.dataframe(df_ni, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="insight-box">
        <b>💡 Key Insight:</b> Under NI approach, WACC consistently falls as leverage increases — driving up firm value.
        The firm should maximise debt. However, this ignores the rising financial risk premium demanded by equity holders.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 3: NOI APPROACH
# ══════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="theory-tag">Net Operating Income Approach</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Net Operating Income (NOI) Approach — David Durand</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <b>Core Premise:</b> The overall capitalization rate (K₀ = WACC) remains <b>constant</b> regardless of leverage.
        Firm value is determined solely by EBIT. As debt rises, equity holders demand higher returns (Ke rises)
        to compensate for financial risk — exactly offsetting the cheap debt benefit.
    </div>
    <div class="formula-box">
        V_F  =  EBIT / K₀  (constant)<br>
        Kₑ   =  (EBIT − Interest) / (V_F − D)  → rises with leverage<br>
        WACC =  K₀  (constant = Kₑᵤ)
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_noi1 = go.Figure()
        fig_noi1.add_trace(go.Scatter(x=x_pct, y=Vf_NOI, name="Firm Value (constant)",
                                       fill="tozeroy", fillcolor="rgba(173,216,230,0.08)",
                                       line=dict(color=COLORS["light_blue"], width=3, dash="dash")))
        layout3 = plotly_base_layout("NOI: Firm Value vs Leverage")
        layout3["xaxis"]["title"] = "Debt % of Capital"
        layout3["yaxis"]["title"] = "Firm Value (₹ Lakhs)"
        fig_noi1.update_layout(**layout3)
        st.plotly_chart(fig_noi1, use_container_width=True)

    with c2:
        # Clip ke_NOI to reasonable range for display
        ke_NOI_clipped = np.clip(ke_NOI, 0, 100)
        fig_noi2 = go.Figure()
        fig_noi2.add_trace(go.Scatter(x=x_pct, y=ke_NOI_clipped, name="Kₑ (rising)",
                                       line=dict(color=COLORS["gold"], width=2.5)))
        fig_noi2.add_trace(go.Scatter(x=x_pct, y=np.full_like(x_pct, kd), name="Kd (constant)",
                                       line=dict(color=COLORS["light_blue"], width=2.5, dash="dot")))
        fig_noi2.add_trace(go.Scatter(x=x_pct, y=WACC_NOI, name="WACC = K₀ (constant)",
                                       line=dict(color=COLORS["teal"], width=3, dash="dash")))
        layout4 = plotly_base_layout("NOI: Cost of Capital vs Leverage")
        layout4["xaxis"]["title"] = "Debt % of Capital"
        layout4["yaxis"]["title"] = "Cost of Capital (%)"
        fig_noi2.update_layout(**layout4)
        st.plotly_chart(fig_noi2, use_container_width=True)

    st.markdown('<div class="section-header">NOI Approach — Data Table</div>', unsafe_allow_html=True)
    steps = np.arange(0, max_debt_pct + 1, 10)
    noi_rows = []
    for s in steps:
        d = total_capital * s / 100
        e_val = total_capital - d
        intr = d * kd / 100
        v = EBIT / (ke_unlevered / 100)
        ke_r = (EBIT - intr) / max(e_val, 0.001) * 100
        noi_rows.append({"Debt %": f"{s}%", "Debt (D)": f"₹{d:,.0f}", "Equity (E)": f"₹{e_val:,.0f}",
                         "Interest": f"₹{intr:,.0f}", "Firm Value": f"₹{v:,.0f}",
                         "Kₑ (%)": f"{ke_r:.2f}%", "WACC %": f"{ke_unlevered:.2f}%"})
    df_noi = pd.DataFrame(noi_rows)
    st.dataframe(df_noi, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="warning-box">
        <b>⚠️ Key Implication:</b> Under NOI, no optimal capital structure exists. Any gain from cheap debt is
        exactly nullified by a rise in Ke. Financial structure is irrelevant to firm value.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 4: MM NO TAX
# ══════════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="theory-tag">Modigliani-Miller — No Tax (1958)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">MM Model Without Taxes — Proposition I & II</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <b>MM 1958 (Perfect Markets, No Taxes):</b> In perfect capital markets, firm value is independent
        of capital structure. Investors can use <b>homemade leverage</b> (arbitrage) to replicate any
        capital structure, so V_L = V_U. The WACC remains constant at Kₑᵤ.
    </div>
    <div class="formula-box">
        Proposition I :  V_L = V_U = EBIT / Kₑᵤ<br>
        Proposition II:  Kₑ  = Kₑᵤ + (Kₑᵤ − Kd) × (D/E)<br>
        WACC           =  Kₑᵤ  (invariant to leverage)
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        # Proposition I
        fig_mm1_v = go.Figure()
        fig_mm1_v.add_trace(go.Scatter(x=x_pct, y=Vf_MMnotax, name="V_L = V_U (constant)",
                                        fill="tozeroy", fillcolor="rgba(23,165,137,0.07)",
                                        line=dict(color=COLORS["teal"], width=3, dash="dot")))
        fig_mm1_v.add_annotation(x=max_debt_pct/2, y=Vu_MMnotax,
                                  text=f"V_U = V_L = ₹{Vu_MMnotax:,.0f}",
                                  showarrow=False, font=dict(color=COLORS["gold"], size=13))
        layout5 = plotly_base_layout("MM (No Tax) Prop. I — Firm Value")
        layout5["xaxis"]["title"] = "Debt % of Capital"
        layout5["yaxis"]["title"] = "Firm Value (₹ Lakhs)"
        fig_mm1_v.update_layout(**layout5)
        st.plotly_chart(fig_mm1_v, use_container_width=True)

    with col2:
        # Proposition II
        ke_MMnotax_clipped = np.clip(ke_MMnotax, 0, 80)
        fig_mm1_k = go.Figure()
        fig_mm1_k.add_trace(go.Scatter(x=x_pct, y=ke_MMnotax_clipped, name="Kₑ = Kₑᵤ+(Kₑᵤ-Kd)×D/E",
                                        line=dict(color=COLORS["gold"], width=2.5)))
        fig_mm1_k.add_trace(go.Scatter(x=x_pct, y=np.full_like(x_pct, kd), name="Kd (constant)",
                                        line=dict(color=COLORS["light_blue"], width=2.5, dash="dot")))
        fig_mm1_k.add_trace(go.Scatter(x=x_pct, y=np.full_like(x_pct, ke_unlevered), name="WACC = Kₑᵤ",
                                        line=dict(color=COLORS["teal"], width=3, dash="dash")))
        layout6 = plotly_base_layout("MM (No Tax) Prop. II — Cost of Capital")
        layout6["xaxis"]["title"] = "Debt % of Capital"
        layout6["yaxis"]["title"] = "Cost of Capital (%)"
        fig_mm1_k.update_layout(**layout6)
        st.plotly_chart(fig_mm1_k, use_container_width=True)

    st.markdown('<div class="section-header">MM No Tax — Data Table</div>', unsafe_allow_html=True)
    mm_notax_rows = []
    for s in np.arange(0, max_debt_pct + 1, 10):
        d = total_capital * s / 100
        e_val = max(total_capital - d, 0.001)
        ke_r = ke_unlevered + (ke_unlevered - kd) * (d / e_val)
        mm_notax_rows.append({"Debt %": f"{s}%", "Debt (D)": f"₹{d:,.0f}",
                               "V_L = V_U": f"₹{Vu_MMnotax:,.0f}",
                               "Kₑ (%)": f"{min(ke_r, 999):.2f}%",
                               "Kd (%)": f"{kd:.2f}%",
                               "WACC %": f"{ke_unlevered:.2f}%",
                               "D/E Ratio": f"{d/e_val:.2f}"})
    df_mm_notax = pd.DataFrame(mm_notax_rows)
    st.dataframe(df_mm_notax, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="insight-box">
        <b>💡 Arbitrage Enforcement:</b> If two firms with identical EBIT have different values, rational investors
        will sell the overvalued firm and buy the undervalued one — restoring V_L = V_U. 
        This "homemade leverage" argument is the cornerstone of MM's irrelevance theorem.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 5: MM WITH TAX
# ══════════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="theory-tag">Modigliani-Miller — With Tax (1963)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">MM Model With Corporate Taxes — Proposition I & II</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <b>MM 1963 (With Corporate Taxes):</b> The tax deductibility of interest creates a <b>tax shield</b>
        that adds value to levered firms. V_L = V_U + T×D. The WACC declines as leverage increases.
        The optimal structure is 100% debt (corner solution).
    </div>
    <div class="formula-box">
        Proposition I :  V_L = V_U + T·D  where  V_U = EBIT(1−T) / Kₑᵤ<br>
        Proposition II:  Kₑ  = Kₑᵤ + (Kₑᵤ − Kd)(1−T) × (D/E)<br>
        Tax Shield     =  T × D  (present value of interest deductions)<br>
        WACC           =  Kₑ·(E/V) + Kd·(1−T)·(D/V)
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_mmt_v = go.Figure()
        fig_mmt_v.add_trace(go.Scatter(x=x_pct, y=Vf_MMtax, name="V_L (with tax)",
                                        fill="tozeroy", fillcolor="rgba(40,167,69,0.07)",
                                        line=dict(color=COLORS["green"], width=3)))
        fig_mmt_v.add_trace(go.Scatter(x=x_pct, y=np.full_like(x_pct, Vu_MMtax),
                                        name=f"V_U = ₹{Vu_MMtax:,.0f}",
                                        line=dict(color=COLORS["red"], width=2, dash="dash")))
        tax_shield = (tax_rate / 100) * D_arr
        fig_mmt_v.add_trace(go.Scatter(x=x_pct, y=tax_shield, name="Tax Shield (T·D)",
                                        fill="tozeroy", fillcolor="rgba(255,215,0,0.05)",
                                        line=dict(color=COLORS["gold"], width=2, dash="dot")))
        layout7 = plotly_base_layout("MM (Tax) Prop. I — Firm Value & Tax Shield")
        layout7["xaxis"]["title"] = "Debt % of Capital"
        layout7["yaxis"]["title"] = "Value (₹ Lakhs)"
        fig_mmt_v.update_layout(**layout7)
        st.plotly_chart(fig_mmt_v, use_container_width=True)

    with col2:
        ke_MMtax_clipped = np.clip(ke_MMtax, 0, 80)
        fig_mmt_k = go.Figure()
        fig_mmt_k.add_trace(go.Scatter(x=x_pct, y=ke_MMtax_clipped, name="Kₑ (Prop II)",
                                        line=dict(color=COLORS["gold"], width=2.5)))
        fig_mmt_k.add_trace(go.Scatter(x=x_pct, y=np.full_like(x_pct, kd * (1 - tax_rate / 100)),
                                        name=f"Kd(1-T) = {kd*(1-tax_rate/100):.1f}%",
                                        line=dict(color=COLORS["light_blue"], width=2.5, dash="dot")))
        fig_mmt_k.add_trace(go.Scatter(x=x_pct, y=WACC_MMtax, name="WACC (declining)",
                                        line=dict(color=COLORS["green"], width=3)))
        layout8 = plotly_base_layout("MM (Tax) Prop. II — Cost of Capital")
        layout8["xaxis"]["title"] = "Debt % of Capital"
        layout8["yaxis"]["title"] = "Cost of Capital (%)"
        fig_mmt_k.update_layout(**layout8)
        st.plotly_chart(fig_mmt_k, use_container_width=True)

    # Sensitivity: Tax rate effect on VL
    st.markdown('<div class="section-header">Tax Rate Sensitivity — Impact on Firm Value</div>', unsafe_allow_html=True)
    fig_tax_sens = go.Figure()
    for t_rate in [0, 15, 25, 35, 50]:
        Vu_t = EBIT * (1 - t_rate / 100) / (ke_unlevered / 100)
        Vf_t = Vu_t + (t_rate / 100) * D_arr
        fig_tax_sens.add_trace(go.Scatter(x=x_pct, y=Vf_t, name=f"Tax = {t_rate}%",
                                           line=dict(width=2)))
    layout9 = plotly_base_layout("Firm Value Sensitivity to Corporate Tax Rate")
    layout9["xaxis"]["title"] = "Debt %"
    layout9["yaxis"]["title"] = "Firm Value (₹ Lakhs)"
    fig_tax_sens.update_layout(**layout9)
    st.plotly_chart(fig_tax_sens, use_container_width=True)

    st.markdown('<div class="section-header">MM With Tax — Data Table</div>', unsafe_allow_html=True)
    mmt_rows = []
    for s in np.arange(0, max_debt_pct + 1, 10):
        d = total_capital * s / 100
        e_val = max(total_capital - d, 0.001)
        ts = (tax_rate / 100) * d
        vl = Vu_MMtax + ts
        ke_r = ke_unlevered + (ke_unlevered - kd) * (1 - tax_rate / 100) * (d / e_val)
        wacc_r = ke_r * e_val / (e_val + d) + kd * (1 - tax_rate / 100) * d / (e_val + d)
        mmt_rows.append({"Debt %": f"{s}%", "Debt (D)": f"₹{d:,.0f}",
                          "V_U": f"₹{Vu_MMtax:,.0f}", "Tax Shield": f"₹{ts:,.0f}",
                          "V_L": f"₹{vl:,.0f}", "Kₑ (%)": f"{min(ke_r,999):.2f}%",
                          "WACC %": f"{wacc_r:.2f}%"})
    df_mmt = pd.DataFrame(mmt_rows)
    st.dataframe(df_mmt, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="insight-box">
        <b>💡 Tax Shield Value:</b> Each rupee of debt adds T × ₹1 to firm value. With a 30% tax rate,
        ₹100L of debt creates ₹30L in present value of tax savings.
        This creates a powerful incentive for leverage — addressed by Trade-Off Theory extensions.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 6: COMPARISON
# ══════════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="theory-tag">Multi-Theory Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Cross-Theory Analysis & Valuation Dashboard</div>', unsafe_allow_html=True)

    # 4-panel subplot
    fig_comp = make_subplots(
        rows=2, cols=2,
        subplot_titles=["Firm Value vs Leverage", "WACC vs Leverage",
                        "Cost of Equity (Kₑ) vs Leverage", "Tax Shield Benefit"],
        vertical_spacing=0.15, horizontal_spacing=0.1,
    )

    # Panel 1: Firm Value
    fig_comp.add_trace(go.Scatter(x=x_pct, y=Vf_NI, name="NI", line=dict(color=COLORS["gold"], width=2)), row=1, col=1)
    fig_comp.add_trace(go.Scatter(x=x_pct, y=Vf_NOI, name="NOI", line=dict(color=COLORS["light_blue"], width=2, dash="dash")), row=1, col=1)
    fig_comp.add_trace(go.Scatter(x=x_pct, y=Vf_MMnotax, name="MM No Tax", line=dict(color=COLORS["teal"], width=2, dash="dot")), row=1, col=1)
    fig_comp.add_trace(go.Scatter(x=x_pct, y=Vf_MMtax, name="MM Tax", line=dict(color=COLORS["green"], width=2.5)), row=1, col=1)

    # Panel 2: WACC
    fig_comp.add_trace(go.Scatter(x=x_pct, y=WACC_NI, name="NI WACC", line=dict(color=COLORS["gold"], width=2), showlegend=False), row=1, col=2)
    fig_comp.add_trace(go.Scatter(x=x_pct, y=WACC_NOI, name="NOI WACC", line=dict(color=COLORS["light_blue"], width=2, dash="dash"), showlegend=False), row=1, col=2)
    fig_comp.add_trace(go.Scatter(x=x_pct, y=WACC_MMnotax, name="MM No Tax WACC", line=dict(color=COLORS["teal"], width=2, dash="dot"), showlegend=False), row=1, col=2)
    fig_comp.add_trace(go.Scatter(x=x_pct, y=np.clip(WACC_MMtax, 0, 50), name="MM Tax WACC", line=dict(color=COLORS["green"], width=2.5), showlegend=False), row=1, col=2)

    # Panel 3: Ke
    fig_comp.add_trace(go.Scatter(x=x_pct, y=np.full_like(x_pct, ke_ni), name="Kₑ NI (const)", line=dict(color=COLORS["gold"], width=2), showlegend=False), row=2, col=1)
    fig_comp.add_trace(go.Scatter(x=x_pct, y=np.clip(ke_NOI, 0, 80), name="Kₑ NOI", line=dict(color=COLORS["light_blue"], width=2, dash="dash"), showlegend=False), row=2, col=1)
    fig_comp.add_trace(go.Scatter(x=x_pct, y=np.clip(ke_MMnotax, 0, 80), name="Kₑ MM No Tax", line=dict(color=COLORS["teal"], width=2, dash="dot"), showlegend=False), row=2, col=1)
    fig_comp.add_trace(go.Scatter(x=x_pct, y=np.clip(ke_MMtax, 0, 80), name="Kₑ MM Tax", line=dict(color=COLORS["green"], width=2.5), showlegend=False), row=2, col=1)

    # Panel 4: Tax Shield
    tax_shield_arr = (tax_rate / 100) * D_arr
    fig_comp.add_trace(go.Bar(x=x_pct[::5], y=tax_shield_arr[::5], name="PV Tax Shield",
                               marker_color=COLORS["gold"], opacity=0.7, showlegend=False), row=2, col=2)

    fig_comp.update_layout(
        paper_bgcolor="rgba(10,22,40,0.0)",
        plot_bgcolor="rgba(17,34,64,0.5)",
        font=dict(family="Source Sans 3", color="#e6f1ff", size=11),
        height=680,
        title=dict(text="Capital Structure Theories — Multi-Panel Dashboard", font=dict(family="Playfair Display", size=16, color=COLORS["gold"])),
        legend=dict(bgcolor="rgba(0,0,0,0.4)", bordercolor="rgba(255,215,0,0.3)", borderwidth=1),
        margin=dict(l=40, r=20, t=80, b=40),
    )
    for i in range(1, 5):
        r, c = ((i - 1) // 2) + 1, ((i - 1) % 2) + 1
        fig_comp.update_xaxes(gridcolor="rgba(255,255,255,0.06)", row=r, col=c)
        fig_comp.update_yaxes(gridcolor="rgba(255,255,255,0.06)", row=r, col=c)
    st.plotly_chart(fig_comp, use_container_width=True)

    # Snapshot comparison at chosen leverage
    st.markdown('<div class="section-header">Point-in-Time Valuation Snapshot</div>', unsafe_allow_html=True)
    chosen_debt_pct = st.slider("Select Debt % for Snapshot Comparison", 0, max_debt_pct, 40)
    idx = min(chosen_debt_pct, len(D_arr) - 1)

    snap_cols = st.columns(4)
    theories = [
        ("NI Approach", Vf_NI[idx], WACC_NI[idx], COLORS["gold"]),
        ("NOI Approach", Vf_NOI[idx], WACC_NOI[idx], COLORS["light_blue"]),
        ("MM No Tax", Vf_MMnotax[idx], WACC_MMnotax[idx], COLORS["teal"]),
        ("MM With Tax", Vf_MMtax[idx], float(np.clip(WACC_MMtax[idx], 0, 50)), COLORS["green"]),
    ]
    for col, (name, vf, wacc, color) in zip(snap_cols, theories):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-color:{color}40">
                <div class="metric-label" style="color:{color}">{name}</div>
                <div class="metric-value" style="color:{color}">₹{vf:,.0f}L</div>
                <div class="metric-delta">WACC: {wacc:.2f}%</div>
            </div>""", unsafe_allow_html=True)

    # Valuation summary bar chart
    vf_values = [t[1] for t in theories]
    theory_names = [t[0] for t in theories]
    colors_bar = [t[3] for t in theories]

    fig_bar = go.Figure(go.Bar(
        x=theory_names, y=vf_values,
        marker_color=colors_bar,
        text=[f"₹{v:,.0f}L" for v in vf_values],
        textposition="outside",
        textfont=dict(color="#e6f1ff"),
    ))
    layout_bar = plotly_base_layout(f"Firm Value at {chosen_debt_pct}% Debt — Theory Comparison")
    layout_bar["xaxis"]["title"] = "Capital Structure Theory"
    layout_bar["yaxis"]["title"] = "Firm Value (₹ Lakhs)"
    layout_bar["showlegend"] = False
    fig_bar.update_layout(**layout_bar)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("""
    <div class="info-box">
        <b>Institutional Context:</b> Real-world capital structure is guided by the <b>Trade-Off Theory</b>
        (balancing tax shield against distress costs), <b>Pecking Order Theory</b> (internal > debt > equity),
        and <b>Market Timing Theory</b>. The MM models serve as theoretical benchmarks — the "frictionless"
        baselines from which real-world deviations are measured.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 7: EDUCATION NOTES
# ══════════════════════════════════════════════════════════════════════════════════
with tab7:
    st.markdown('<div class="theory-tag">Comprehensive Study Notes</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📚 Capital Structure Theories — Complete Education Notes</div>', unsafe_allow_html=True)

    edu1, edu2, edu3, edu4 = st.tabs([
        "🏛️ Foundations", "📘 NI & NOI", "📙 MM Models", "🌍 Real-World Extensions"
    ])

    # ── FOUNDATIONS ─────────────────────────────────────────────────────────────
    with edu1:
        st.markdown("""
        <div class="section-header">What is Capital Structure?</div>
        <div class="info-box">
            <b>Definition:</b> Capital structure refers to the specific mix of <u>debt</u> and <u>equity</u>
            a firm uses to finance its assets and operations. The central question in corporate finance is:
            <i>"Does the financing mix affect the total value of the firm?"</i>
        </div>

        <div class="section-header">Key Components</div>
        <table class="comp-table">
          <tr><th>Component</th><th>Description</th><th>Cost</th><th>Tax Treatment</th></tr>
          <tr>
            <td><b>Debt (D)</b></td>
            <td>Bonds, debentures, bank loans, commercial paper</td>
            <td>Kd — Interest rate</td>
            <td>Interest is tax-deductible → creates tax shield</td>
          </tr>
          <tr>
            <td><b>Equity (E)</b></td>
            <td>Common shares, retained earnings, preference shares</td>
            <td>Ke — Required return by shareholders</td>
            <td>Dividends are NOT tax-deductible</td>
          </tr>
          <tr>
            <td><b>WACC</b></td>
            <td>Weighted Average Cost of Capital</td>
            <td>Ke·(E/V) + Kd(1-T)·(D/V)</td>
            <td>Blended cost of all financing sources</td>
          </tr>
        </table>

        <div class="section-header">Core Terminology</div>
        <table class="comp-table">
          <tr><th>Term</th><th>Formula</th><th>Meaning</th></tr>
          <tr><td><b>Financial Leverage</b></td><td>D/E or D/V</td><td>Degree to which a firm uses debt financing</td></tr>
          <tr><td><b>Levered Firm (V_L)</b></td><td>E + D</td><td>Firm with debt in its capital structure</td></tr>
          <tr><td><b>Unlevered Firm (V_U)</b></td><td>E only</td><td>All-equity financed firm (no debt)</td></tr>
          <tr><td><b>EBIT</b></td><td>Revenue − COGS − OPEX</td><td>Earnings before interest and taxes</td></tr>
          <tr><td><b>EBT</b></td><td>EBIT − Interest</td><td>Earnings before tax</td></tr>
          <tr><td><b>EAT / NI</b></td><td>EBT × (1−T)</td><td>Net income available to equity holders</td></tr>
          <tr><td><b>Tax Shield</b></td><td>T × Interest = T × Kd × D</td><td>Tax savings from debt financing</td></tr>
          <tr><td><b>Interest Coverage</b></td><td>EBIT / Interest</td><td>Ability to service debt obligations</td></tr>
          <tr><td><b>Financial Distress</b></td><td>—</td><td>Inability to meet debt obligations; triggers costs</td></tr>
        </table>

        <div class="section-header">Why Capital Structure Matters</div>
        <div class="info-box">
            The optimal capital structure minimises WACC and maximises firm value. Since debt is cheaper
            than equity (due to tax deductibility and lower risk for lenders), some debt is typically beneficial.
            However, excessive debt raises financial distress costs and increases equity risk premium demanded
            by shareholders — creating a <b>trade-off</b>.
        </div>

        <div class="formula-box">
            Firm Value  V  =  D + E  =  PV of future cash flows discounted at WACC<br>
            WACC  =  Ke · (E/V)  +  Kd · (1−T) · (D/V)<br>
            ↑ Debt  →  ↓ WACC  →  ↑ Firm Value  [up to the optimal point]<br>
            ↑ Debt  →  ↑ Financial Risk  →  ↑ Ke  →  partially offsets WACC benefit
        </div>

        <div class="section-header">Historical Evolution of Theories</div>
        <table class="comp-table">
          <tr><th>Year</th><th>Theory</th><th>Authors</th><th>Key Proposition</th></tr>
          <tr><td>1952</td><td>NI & NOI Approach</td><td>David Durand</td><td>Two extreme views on leverage relevance</td></tr>
          <tr><td>1958</td><td>MM (No Tax)</td><td>Modigliani & Miller</td><td>Capital structure irrelevance in perfect markets</td></tr>
          <tr><td>1963</td><td>MM (With Tax)</td><td>Modigliani & Miller</td><td>Tax shield adds value; optimal = 100% debt</td></tr>
          <tr><td>1973</td><td>Trade-Off Theory</td><td>Various</td><td>Balance tax shield vs distress costs</td></tr>
          <tr><td>1976</td><td>Agency Cost Theory</td><td>Jensen & Meckling</td><td>Debt reduces agency costs of equity</td></tr>
          <tr><td>1984</td><td>Pecking Order Theory</td><td>Myers & Majluf</td><td>Firms prefer internal > debt > equity financing</td></tr>
          <tr><td>1986</td><td>Market Timing Theory</td><td>Various</td><td>Firms issue equity when market overvalues them</td></tr>
        </table>
        """, unsafe_allow_html=True)

    # ── NI & NOI ─────────────────────────────────────────────────────────────────
    with edu2:
        st.markdown("""
        <div class="section-header">Net Income (NI) Approach — David Durand (1952)</div>
        <div class="info-box">
            The NI approach assumes that both the cost of debt (Kd) and cost of equity (Ke) remain
            <b>constant and independent</b> of the degree of financial leverage. As a firm takes on more
            debt (which is cheaper), the overall WACC falls, causing firm value to rise.
        </div>

        <div class="formula-box">
            Assumptions:<br>
            &nbsp;&nbsp;1. Ke = constant (investors do not perceive increased financial risk)<br>
            &nbsp;&nbsp;2. Kd = constant (lenders do not increase rates with more debt)<br>
            &nbsp;&nbsp;3. No taxes (original formulation)<br><br>
            Key Equations:<br>
            &nbsp;&nbsp;Market Value of Equity  S = EAT / Ke<br>
            &nbsp;&nbsp;Firm Value              V = S + D<br>
            &nbsp;&nbsp;WACC = Ko             = EBIT / V  →  decreases as D increases<br>
            &nbsp;&nbsp;Optimal Structure       →  100% Debt (V is maximised)
        </div>

        <div class="insight-box">
            <b>💡 Implication:</b> Firms should borrow as much as possible. Every rupee of equity replaced
            by cheaper debt reduces WACC and increases V. The NI approach suggests an unambiguous corner
            solution at maximum leverage.
        </div>

        <div class="warning-box">
            <b>⚠️ Criticism:</b> Unrealistic assumption that Ke stays constant. In practice, shareholders
            demand a higher return as financial risk rises with leverage — making constant Ke implausible.
        </div>

        <div class="section-header">Net Operating Income (NOI) Approach — David Durand (1952)</div>
        <div class="info-box">
            The NOI approach is the polar opposite. It argues that the overall capitalisation rate (Ko = WACC)
            remains <b>constant</b> regardless of leverage. Firm value is determined solely by operating income (EBIT)
            and is independent of the financing mix.
        </div>

        <div class="formula-box">
            Assumptions:<br>
            &nbsp;&nbsp;1. Ko = WACC = constant (the market capitalises total firm earnings at a fixed rate)<br>
            &nbsp;&nbsp;2. Kd = constant (debt cost unchanged)<br>
            &nbsp;&nbsp;3. Ke rises automatically to offset cheap debt benefit<br><br>
            Key Equations:<br>
            &nbsp;&nbsp;Firm Value    V  = EBIT / Ko  →  constant regardless of D/E<br>
            &nbsp;&nbsp;Equity Value  S  = V − D<br>
            &nbsp;&nbsp;Ke            = (EBIT − Interest) / S  →  rises with leverage<br>
            &nbsp;&nbsp;No optimal capital structure exists
        </div>

        <div class="insight-box">
            <b>💡 Implication:</b> Financial leverage is irrelevant. Any benefit from cheap debt is exactly
            cancelled by a rise in Ke demanded by equity holders to compensate for increased financial risk.
            This is conceptually the precursor to MM (1958).
        </div>

        <div class="section-header">NI vs NOI — Head-to-Head Comparison</div>
        <table class="comp-table">
          <tr><th>Feature</th><th>NI Approach</th><th>NOI Approach</th></tr>
          <tr><td>Ke with leverage</td><td>Constant</td><td>Rises proportionally</td></tr>
          <tr><td>Kd with leverage</td><td>Constant</td><td>Constant</td></tr>
          <tr><td>WACC with leverage</td><td>Falls</td><td>Constant</td></tr>
          <tr><td>Firm Value with leverage</td><td>Rises</td><td>Constant</td></tr>
          <tr><td>Optimal Capital Structure?</td><td>Yes — 100% debt</td><td>No — irrelevant</td></tr>
          <tr><td>Underlying assumption</td><td>Markets ignore financial risk in Ke</td><td>Markets fully price financial risk in Ke</td></tr>
          <tr><td>Realism</td><td>Low</td><td>Moderate</td></tr>
        </table>

        <div class="section-header">Traditional / Intermediate Approach</div>
        <div class="info-box">
            A middle ground: up to a moderate level of debt, Ke rises slowly (investors tolerate some financial risk)
            and Kd stays stable → WACC falls, V rises. Beyond a threshold, Ke rises sharply and Kd increases
            (lenders demand risk premium) → WACC rises, V falls. An <b>optimal capital structure exists</b>
            at the debt level where WACC is minimised.
        </div>
        <div class="formula-box">
            Zone 1 (Low Debt):  Ke rises slowly, Kd stable → WACC ↓ → V ↑<br>
            Zone 2 (Optimal):   WACC is minimised → V is maximised<br>
            Zone 3 (High Debt): Ke rises sharply, Kd rises → WACC ↑ → V ↓
        </div>
        """, unsafe_allow_html=True)

    # ── MM MODELS ────────────────────────────────────────────────────────────────
    with edu3:
        st.markdown("""
        <div class="section-header">MM Theorem — Background & Assumptions</div>
        <div class="info-box">
            Franco Modigliani and Merton Miller published their landmark theorem in 1958 (American Economic Review).
            They used a rigorous arbitrage argument to prove that in <b>perfect capital markets</b>,
            firm value is independent of capital structure. They won the Nobel Prize in Economics
            (Miller 1990, Modigliani 1985) partly for this work.
        </div>

        <div class="formula-box">
            MM Perfect Market Assumptions (1958):<br>
            &nbsp;&nbsp;1. No corporate or personal taxes<br>
            &nbsp;&nbsp;2. No transaction costs or flotation costs<br>
            &nbsp;&nbsp;3. No bankruptcy or financial distress costs<br>
            &nbsp;&nbsp;4. Perfect information — all investors have identical information<br>
            &nbsp;&nbsp;5. Investors can borrow/lend at the same rate as firms (homemade leverage)<br>
            &nbsp;&nbsp;6. EBIT is independent of capital structure<br>
            &nbsp;&nbsp;7. Firms can be classified into homogeneous risk classes
        </div>

        <div class="section-header">MM Proposition I — No Tax (1958)</div>
        <div class="info-box">
            <b>Statement:</b> The total market value of a firm is independent of its capital structure
            and is determined solely by capitalising its expected EBIT at the rate appropriate for its risk class.
        </div>
        <div class="formula-box">
            V_L  =  V_U  =  EBIT / Kₑᵤ<br><br>
            Proof (Arbitrage):<br>
            Suppose V_L > V_U (levered firm overvalued):<br>
            &nbsp;&nbsp;→ Investor sells shares in levered firm<br>
            &nbsp;&nbsp;→ Borrows personally (homemade leverage) at same rate Kd<br>
            &nbsp;&nbsp;→ Buys equivalent shares in unlevered firm<br>
            &nbsp;&nbsp;→ Same income, lower cost → arbitrage profit<br>
            &nbsp;&nbsp;→ Process continues until V_L = V_U
        </div>

        <div class="section-header">MM Proposition II — No Tax (1958)</div>
        <div class="info-box">
            <b>Statement:</b> The required return on equity (Ke) increases linearly with the debt-to-equity
            ratio to exactly offset the benefit of cheap debt. WACC remains constant.
        </div>
        <div class="formula-box">
            Ke  =  Kₑᵤ  +  (Kₑᵤ − Kd) × (D/E)<br><br>
            where:<br>
            &nbsp;&nbsp;Kₑᵤ = required return on unlevered equity (risk class rate)<br>
            &nbsp;&nbsp;Kd  = cost of debt<br>
            &nbsp;&nbsp;D/E = financial leverage ratio<br><br>
            Interpretation:<br>
            &nbsp;&nbsp;Ke = Business Risk Premium + Financial Risk Premium<br>
            &nbsp;&nbsp;Financial Risk Premium = (Kₑᵤ − Kd) × D/E
        </div>
        <div class="insight-box">
            <b>💡 Intuition:</b> As a firm adds debt, equity becomes riskier (residual claim after fixed debt payments).
            Shareholders demand higher returns. The rise in Ke exactly neutralises the lower Kd benefit → WACC stays flat.
        </div>

        <div class="section-header">MM Proposition I — With Tax (1963)</div>
        <div class="info-box">
            In 1963, MM corrected their model to include corporate taxes. Interest payments are tax-deductible,
            creating a <b>perpetual tax shield</b> whose present value adds directly to firm value.
        </div>
        <div class="formula-box">
            V_L  =  V_U  +  PV(Tax Shield)<br>
            V_L  =  V_U  +  T × D  (assuming debt is permanent)<br><br>
            where:<br>
            &nbsp;&nbsp;V_U = EBIT(1−T) / Kₑᵤ  (unlevered firm value after tax)<br>
            &nbsp;&nbsp;T   = corporate tax rate<br>
            &nbsp;&nbsp;D   = market value of debt<br>
            &nbsp;&nbsp;T×D = PV of tax shield (discounted at Kd assuming perpetual debt)<br><br>
            Annual Tax Shield  =  T × Kd × D<br>
            PV(Tax Shield)     =  (T × Kd × D) / Kd  =  T × D
        </div>

        <div class="section-header">MM Proposition II — With Tax (1963)</div>
        <div class="formula-box">
            Ke  =  Kₑᵤ  +  (Kₑᵤ − Kd) × (1−T) × (D/E)<br><br>
            WACC  =  Ke·(E/V)  +  Kd·(1−T)·(D/V)<br>
            WACC  =  Kₑᵤ × (1 − T·D/V)  →  falls as D/V rises<br><br>
            Key difference from No-Tax version:<br>
            &nbsp;&nbsp;Financial risk premium is moderated by (1−T)<br>
            &nbsp;&nbsp;Ke rises more slowly → WACC actually falls with leverage<br>
            &nbsp;&nbsp;Optimal structure → 100% debt (corner solution again)
        </div>
        <div class="warning-box">
            <b>⚠️ Limitation:</b> The 100% debt prescription is unrealistic. In reality, high debt triggers
            bankruptcy risk, agency costs, and loss of financial flexibility — costs not captured in MM (1963).
            This motivated Trade-Off Theory.
        </div>

        <div class="section-header">MM Models — Complete Comparison</div>
        <table class="comp-table">
          <tr><th>Feature</th><th>MM No Tax (1958)</th><th>MM With Tax (1963)</th></tr>
          <tr><td>Proposition I</td><td>V_L = V_U</td><td>V_L = V_U + T·D</td></tr>
          <tr><td>Proposition II</td><td>Ke = Kₑᵤ + (Kₑᵤ−Kd)·D/E</td><td>Ke = Kₑᵤ + (Kₑᵤ−Kd)(1−T)·D/E</td></tr>
          <tr><td>WACC</td><td>Constant = Kₑᵤ</td><td>Decreases with leverage</td></tr>
          <tr><td>Firm Value</td><td>Constant</td><td>Increases with D</td></tr>
          <tr><td>Tax Shield</td><td>None</td><td>T × D</td></tr>
          <tr><td>Optimal D/E</td><td>Indeterminate</td><td>100% debt</td></tr>
          <tr><td>Key mechanism</td><td>Arbitrage eliminates V differences</td><td>Tax deductibility of interest</td></tr>
          <tr><td>Ke slope</td><td>(Kₑᵤ − Kd)</td><td>(Kₑᵤ − Kd)(1−T) — flatter</td></tr>
        </table>
        """, unsafe_allow_html=True)

    # ── REAL WORLD EXTENSIONS ────────────────────────────────────────────────────
    with edu4:
        st.markdown("""
        <div class="section-header">Trade-Off Theory</div>
        <div class="info-box">
            The Trade-Off Theory extends MM (1963) by introducing <b>costs of financial distress</b>.
            Firms balance the tax shield benefit of debt against the rising probability and cost of
            financial distress as leverage increases. An <b>interior optimal capital structure</b> exists.
        </div>
        <div class="formula-box">
            V_L  =  V_U  +  PV(Tax Shield)  −  PV(Financial Distress Costs)<br><br>
            Financial Distress Costs include:<br>
            &nbsp;&nbsp;Direct:  Legal fees, restructuring costs, administrative expenses (~3–5% of firm value)<br>
            &nbsp;&nbsp;Indirect: Lost customers, key employee departure, supplier credit withdrawal,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;underinvestment problems, asset fire sales (~10–20% of firm value)<br><br>
            Optimal D*: where ΔPV(Tax Shield) = ΔPVCFD (marginal benefit = marginal cost)
        </div>
        <div class="insight-box">
            <b>💡 Prediction:</b> Firms with stable, predictable cash flows (utilities, telecoms) can support
            more debt. Firms with volatile earnings or intangible assets (tech, pharma) should use less debt.
            Target D/E ratios exist and firms gradually move toward them.
        </div>

        <div class="section-header">Pecking Order Theory — Myers & Majluf (1984)</div>
        <div class="info-box">
            Based on <b>information asymmetry</b> between managers (who know true firm value) and investors.
            Managers avoid issuing undervalued equity. Instead, firms follow a financing hierarchy:
            <b>Internal funds → Debt → Equity (last resort)</b>
        </div>
        <div class="formula-box">
            Pecking Order Hierarchy:<br>
            &nbsp;&nbsp;1st: Retained earnings / internal cash flows (no information problem)<br>
            &nbsp;&nbsp;2nd: Debt (lenders have priority claim; less information sensitivity)<br>
            &nbsp;&nbsp;3rd: Equity (most sensitive to asymmetric information; signals overvaluation)<br><br>
            Signal: Equity issuance → market interprets as "stock is overpriced" → share price falls<br>
            Signal: Debt issuance → market interprets as management confidence in future cash flows
        </div>
        <div class="insight-box">
            <b>💡 Empirical Evidence:</b> Most firms fund investment primarily from retained earnings.
            Large, established firms (low information asymmetry) use more debt. High-growth firms
            with high information asymmetry rely more on equity.
        </div>

        <div class="section-header">Agency Cost Theory — Jensen & Meckling (1976)</div>
        <div class="info-box">
            Agency costs arise from conflicts of interest between <b>shareholders vs managers</b>
            (equity agency costs) and <b>shareholders vs bondholders</b> (debt agency costs).
            Debt can reduce equity agency costs (free cash flow problem) but creates debt agency costs.
        </div>
        <div class="formula-box">
            Equity Agency Costs (Manager–Shareholder conflict):<br>
            &nbsp;&nbsp;• Empire building, excessive perks, risk aversion by managers<br>
            &nbsp;&nbsp;• Debt REDUCES these: interest payments force discipline on free cash flows<br><br>
            Debt Agency Costs (Shareholder–Bondholder conflict):<br>
            &nbsp;&nbsp;• Underinvestment: shareholders skip positive NPV projects if gains go to bondholders<br>
            &nbsp;&nbsp;• Asset substitution: shareholders prefer riskier projects (option-like payoff)<br>
            &nbsp;&nbsp;• Debt INCREASES these as leverage rises<br><br>
            Optimal D*: Minimises total agency costs (equity + debt agency costs)
        </div>

        <div class="section-header">Market Timing Theory</div>
        <div class="info-box">
            Firms issue equity when their stock appears <b>overvalued</b> relative to book or intrinsic value,
            and repurchase shares when undervalued. Capital structure is the cumulative result of past
            market timing decisions — no target D/E ratio exists.
        </div>
        <div class="formula-box">
            Issue equity when:  Market-to-Book ratio is high (stock appears overvalued)<br>
            Issue debt when:    Interest rates are low / stock appears undervalued<br><br>
            Baker & Wurgler (2002): Historical M/B ratios have significant negative effect on leverage<br>
            → Past financing windows permanently affect current capital structure
        </div>

        <div class="section-header">Signalling Theory</div>
        <div class="info-box">
            Capital structure decisions convey information signals to the market:
        </div>
        <table class="comp-table">
          <tr><th>Action</th><th>Signal to Market</th><th>Expected Share Price Reaction</th></tr>
          <tr><td>Equity issuance</td><td>Stock may be overvalued; dilution risk</td><td style="color:#dc3545">Negative (↓ ~3%)</td></tr>
          <tr><td>Debt issuance</td><td>Management confident in future cash flows</td><td style="color:#28a745">Mildly positive</td></tr>
          <tr><td>Share buyback</td><td>Stock is undervalued; excess cash available</td><td style="color:#28a745">Positive (↑ ~3–4%)</td></tr>
          <tr><td>Dividend increase</td><td>Sustainable earnings; strong cash position</td><td style="color:#28a745">Positive</td></tr>
          <tr><td>Leverage increase</td><td>Management expects strong future EBIT</td><td style="color:#28a745">Positive</td></tr>
          <tr><td>Leverage decrease (equity for debt)</td><td>Possible financial stress signal</td><td style="color:#dc3545">Negative</td></tr>
        </table>

        <div class="section-header">Indian Market Context</div>
        <div class="info-box">
            Indian firms face unique capital structure considerations:
        </div>
        <table class="comp-table">
          <tr><th>Factor</th><th>Indian Context</th><th>Impact on Capital Structure</th></tr>
          <tr><td>Tax Rate</td><td>Corporate tax ~25.17% (incl. surcharge) post 2019</td><td>Moderate tax shield benefit</td></tr>
          <tr><td>Promoter Holdings</td><td>High promoter stakes (~50–70%)</td><td>Preference for debt to avoid dilution</td></tr>
          <tr><td>Banking Sector</td><td>PSU banks; NPA issues; Basel III compliance</td><td>Credit availability affects optimal D</td></tr>
          <tr><td>Capital Markets</td><td>SEBI regulations; growing bond market depth</td><td>Equity more accessible post reforms</td></tr>
          <tr><td>Family-owned businesses</td><td>Majority of listed firms</td><td>Control aversion → pecking order preference</td></tr>
          <tr><td>Growth opportunities</td><td>High-growth sectors (IT, pharma, fintech)</td><td>Lower debt; prefer equity/internal funds</td></tr>
          <tr><td>Interest rates</td><td>RBI repo rate cycles</td><td>Timing of debt issuance; floating vs fixed</td></tr>
        </table>

        <div class="section-header">Integrated Framework — Theory to Practice</div>
        <div class="formula-box">
            Practical Capital Structure Decision Framework:<br><br>
            Step 1: Establish V_U  =  EBIT(1−T) / Kₑᵤ  [MM baseline]<br>
            Step 2: Add Tax Shield  →  + T × D<br>
            Step 3: Subtract Distress Costs  →  − PV(FDC)  [Trade-Off]<br>
            Step 4: Consider Agency Costs  →  − AC(debt) + AC(equity savings)<br>
            Step 5: Check Pecking Order  →  Use internal funds first<br>
            Step 6: Assess Signalling  →  What does each choice signal?<br>
            Step 7: Consider Market Timing  →  Is equity over/undervalued?<br><br>
            V_L* = V_U + T·D − PV(FDC) − Net Agency Costs  [Full Model]
        </div>

        <div class="section-header">Key Examination Points</div>
        <table class="comp-table">
          <tr><th>#</th><th>Concept</th><th>Key Formula / Statement</th></tr>
          <tr><td>1</td><td>NI Approach</td><td>Ke & Kd constant; WACC falls; V rises; optimal = 100% D</td></tr>
          <tr><td>2</td><td>NOI Approach</td><td>WACC constant; Ke rises; V constant; no optimal structure</td></tr>
          <tr><td>3</td><td>MM Prop I (No Tax)</td><td>V_L = V_U; proven by arbitrage / homemade leverage</td></tr>
          <tr><td>4</td><td>MM Prop II (No Tax)</td><td>Ke = Kₑᵤ + (Kₑᵤ−Kd)·D/E; WACC = Kₑᵤ</td></tr>
          <tr><td>5</td><td>MM Prop I (Tax)</td><td>V_L = V_U + T·D; PV tax shield = T·D</td></tr>
          <tr><td>6</td><td>MM Prop II (Tax)</td><td>Ke = Kₑᵤ + (Kₑᵤ−Kd)(1−T)·D/E; WACC falls</td></tr>
          <tr><td>7</td><td>Trade-Off Theory</td><td>V_L = V_U + T·D − PV(FDC); interior optimum</td></tr>
          <tr><td>8</td><td>Pecking Order</td><td>Internal > Debt > Equity; information asymmetry driven</td></tr>
          <tr><td>9</td><td>Agency Costs</td><td>Debt reduces equity agency cost; raises debt agency cost</td></tr>
          <tr><td>10</td><td>Tax Shield</td><td>Annual TS = T·Kd·D; PV(TS) = T·D (perpetual debt)</td></tr>
        </table>

        <div class="insight-box" style="margin-top:20px;">
            <b>📝 Prof. Ravichandran's Note:</b> In examinations, always begin capital structure problems by
            identifying which theory applies. State assumptions explicitly. For MM problems, always compute
            V_U first, then add T·D for the with-tax case. Remember: MM (1963) gives a corner solution —
            real-world optimal structure requires Trade-Off Theory adjustments.
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-left">
        ⛰️ Prof. V. Ravichandran &nbsp;|&nbsp; 28+ Yrs Corporate Finance &amp; Banking &nbsp;|&nbsp; 10+ Yrs Academic Excellence
        &nbsp;|&nbsp;
        <a href="https://www.linkedin.com/in/trichyravis" target="_blank">🔗 LinkedIn</a>
        <a href="https://github.com/trichyravis" target="_blank">💻 GitHub</a>
    </div>
    <div class="footer-right">The Mountain Path — World of Finance &nbsp;|&nbsp; Capital Structure Theories</div>
</div>
""", unsafe_allow_html=True)
