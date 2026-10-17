"""Application styling and CSS definitions.

Theme: soft aurora background + frosted-glass surfaces.
Every surface (sidebar, cards, charts, inputs, tabs, tables) uses the same
translucent white + blur recipe so everything blends with the background.
"""

CUSTOM_CSS = """
<style>
    /* ---------- Design tokens ---------- */
    :root {
        --glass: rgba(255, 255, 255, 0.62);
        --glass-strong: rgba(255, 255, 255, 0.78);
        --glass-border: rgba(255, 255, 255, 0.85);
        --line: rgba(148, 163, 184, 0.35);
        --ink: #0f172a;
        --muted: #64748b;
        --blue: #2563eb;
        --blue-dark: #1d4ed8;
        --rose: #e11d48;
        --shadow: 0 8px 24px -8px rgba(30, 41, 99, 0.18);
    }

    /* ---------- App canvas ---------- */
    .stApp {
        background:
            radial-gradient(circle at 6% 8%, rgba(37, 99, 235, 0.16) 0, transparent 42%),
            radial-gradient(circle at 94% 4%, rgba(244, 63, 94, 0.10) 0, transparent 38%),
            radial-gradient(circle at 78% 96%, rgba(139, 92, 246, 0.14) 0, transparent 42%),
            radial-gradient(circle at 12% 92%, rgba(20, 184, 166, 0.10) 0, transparent 38%),
            radial-gradient(rgba(100, 116, 139, 0.16) 1px, transparent 1px),
            linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
        background-size: auto, auto, auto, auto, 24px 24px, auto;
        background-attachment: fixed;
        color: #1e293b;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Top bar blends into the canvas */
    [data-testid="stHeader"] {
        background: transparent;
    }

    /* ---------- Sidebar (frosted glass) ---------- */
    [data-testid="stSidebar"] {
        background: var(--glass);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-right: 1px solid var(--line);
    }

    /* ---------- Hero banner ---------- */
    .hero-container {
        background:
            radial-gradient(circle at 85% 20%, rgba(59, 130, 246, 0.35) 0, transparent 45%),
            linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 16px;
        padding: 32px 28px;
        color: #ffffff;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 12px 28px -10px rgba(15, 23, 42, 0.45);
    }
    .hero-container h1 {
        margin: 0 0 8px 0;
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff !important;
    }
    .hero-container p {
        margin: 0;
        font-size: 1rem;
        color: #cbd5e1 !important;
        line-height: 1.5;
    }

    /* ---------- Feature cards ---------- */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    .feature-card {
        background: var(--glass);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 14px;
        padding: 18px;
        box-shadow: var(--shadow);
    }
    .feature-card h4 {
        margin: 0 0 6px 0;
        font-size: 0.98rem;
        color: var(--ink) !important;
        font-weight: 700;
    }
    .feature-card p {
        margin: 0;
        font-size: 0.88rem;
        color: var(--muted) !important;
        line-height: 1.4;
    }

    /* ---------- KPI metric cards ---------- */
    .metric-card {
        background: var(--glass);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid var(--glass-border);
        border-top: 3px solid var(--blue);
        box-shadow: var(--shadow);
        text-align: left;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 0.78rem;
        color: var(--muted);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .metric-card p {
        margin: 6px 0 0 0;
        font-size: 2.1rem;
        font-weight: 800;
        color: var(--ink);
    }

    /* Red warning card for anomalies */
    .metric-card-alert {
        background: rgba(255, 241, 242, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid rgba(244, 63, 94, 0.45);
        border-top: 3px solid #f43f5e;
        box-shadow: 0 8px 24px -8px rgba(244, 63, 94, 0.25);
        text-align: left;
    }
    .metric-card-alert h3 {
        margin: 0;
        font-size: 0.78rem;
        color: #be123c;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .metric-card-alert p {
        margin: 6px 0 0 0;
        font-size: 2.1rem;
        font-weight: 800;
        color: var(--rose);
    }

    /* ---------- Button-style tabs ---------- */
    div[data-testid="stTabs"] div[role="tablist"] {
        display: flex !important;
        gap: 12px !important;
        background-color: transparent !important;
        border-bottom: none !important;
        padding: 6px 0 !important;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        background: var(--glass) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 10px 24px !important;
        border-radius: 10px !important;
        border: 1px solid var(--glass-border) !important;
        box-shadow: 0 2px 6px rgba(30, 41, 99, 0.08) !important;
        cursor: pointer !important;
    }
    div[data-testid="stTabs"] button[role="tab"]:hover {
        background: var(--glass-strong) !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: 1px solid var(--blue-dark) !important;
        box-shadow: 0 6px 14px rgba(37, 99, 235, 0.35) !important;
    }
    div[data-testid="stTabs"] div[data-baseweb="tab-highlight"] {
        display: none !important;
    }
    div[data-testid="stTabs"] div[data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ---------- Action buttons ---------- */
    .stButton>button,
    .stDownloadButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px;
        padding: 8px 20px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.28);
    }
    .stButton>button:hover,
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    }

    /* ---------- Inputs: select boxes, text, number ---------- */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background: var(--glass-strong) !important;
        border: 1px solid var(--line) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }

    /* ---------- File uploader ---------- */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--glass);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 2px dashed rgba(37, 99, 235, 0.4);
        border-radius: 14px;
    }

    /* ---------- Expanders ---------- */
    [data-testid="stExpander"] {
        background: var(--glass);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 14px;
        box-shadow: var(--shadow);
    }
    [data-testid="stExpander"] details {
        border: none;
    }

    /* ---------- Charts and tables ---------- */
    div[data-testid="stPlotlyChart"],
    div[data-testid="stDataFrame"] {
        background: var(--glass);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 14px;
        padding: 8px;
        box-shadow: var(--shadow);
    }

    /* ---------- Alerts (info / success / warning) ---------- */
    div[data-testid="stAlert"] {
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 12px;
    }

    /* ---------- Dividers ---------- */
    hr {
        border-color: var(--line) !important;
    }
</style>
"""