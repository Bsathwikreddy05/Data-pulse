import streamlit as st
import pandas as pd
from styles import CUSTOM_CSS
from cleaner import (
    get_basic_metrics,
    clean_dataset,
    get_column_summary,
    detect_outliers_iqr
)
from charts import (
    render_bar_chart,
    render_donut_chart,
    render_line_trend,
    render_correlation_heatmap
)
from codegen import generate_pipeline_code
from ai_summary import generate_ai_report

# 1. Page Configuration & Custom Styles
st.set_page_config(
    page_title="DataPulse | Data Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

NA_VALUES = [
    "?", "-", "--", "N/A", "n/a", "NA", "na",
    "null", "Null", "NULL", "None", "none",
    "missing", "Missing", " ", ""
]

# 2. Sidebar Configuration & Automated Secrets
with st.sidebar:
    st.title("⚡ DataPulse")
    st.caption("DATA PROFILING & PREPROCESSING PIPELINE")
    st.divider()

    st.subheader("🔑 AI Configuration")
    
    # Auto-load key from .streamlit/secrets.toml if present
    default_key = st.secrets.get("GEMINI_API_KEY", "")

    if default_key:
        st.success("API Key loaded automatically")
        api_key_input = default_key
    else:
        api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            help="Google AI Studio key for summaries"
        )

# 3. Session State
if "uploaded_dataset" not in st.session_state:
    st.session_state.uploaded_dataset = None

# Landing Screen
if st.session_state.uploaded_dataset is None:
    st.markdown("""
    <div class="hero-container">
        <h1>Welcome to DataPulse ⚡</h1>
        <p>An automated data profiling and preprocessing pipeline. Upload any CSV file below to inspect data health, clean anomalies, and generate visual analytics.</p>
    </div>

    <div class="feature-grid">
        <div class="feature-card">
            <h4>Automated Diagnostics</h4>
            <p>Instant identification of data types, null densities, duplicate records, and parametric metrics.</p>
        </div>
        <div class="feature-card">
            <h4>Data Cleaning Studio</h4>
            <p>One-click deduplication, numeric type casting, and configurable missing-value imputation.</p>
        </div>
        <div class="feature-card">
            <h4>Executive AI Reports</h4>
            <p>Automated consultant-grade narrative reports evaluating quality risks and prescriptive actions.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    center_file = st.file_uploader(
        "📁 Upload Dataset (CSV)",
        type=["csv"],
        key="uploader_center",
        help="200MB per file • CSV"
    )
    if center_file is not None:
        st.session_state.uploaded_dataset = center_file
        st.rerun()

# Dashboard Screen
if st.session_state.uploaded_dataset is not None:
    active_file = st.session_state.uploaded_dataset
    active_file.seek(0)
    
    try:
        df = pd.read_csv(active_file, na_values=NA_VALUES)
    except pd.errors.EmptyDataError:
        st.error("The uploaded file is empty or contains no readable columns.")
        if st.button("Upload Another File"):
            st.session_state.uploaded_dataset = None
            st.rerun()
        st.stop()

    raw_stats = get_basic_metrics(df)

    # Header Row
    col_head, col_btn = st.columns([5, 1])
    with col_head:
        st.title("Dataset Profiler")
        st.caption(f"Analyzing `{active_file.name}` • {raw_stats['rows']:,} Total Records • {raw_stats['cols']} Attributes")
    with col_btn:
        st.write("")
        if st.button("Change Dataset"):
            st.session_state.uploaded_dataset = None
            st.rerun()

    # KPI Metric Cards
    dup_card = "metric-card-alert" if raw_stats["duplicates"] > 0 else "metric-card"
    missing_card = "metric-card-alert" if raw_stats["missing"] > 0 else "metric-card"

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card"><h3>Total Records</h3><p>{raw_stats["rows"]:,}</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><h3>Total Attributes</h3><p>{raw_stats["cols"]}</p></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="{dup_card}"><h3>Duplicate Rows</h3><p>{raw_stats["duplicates"]:,}</p></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="{missing_card}"><h3>Missing Values</h3><p>{raw_stats["missing"]:,}</p></div>', unsafe_allow_html=True)

    st.write("")
    st.divider()

    # Main Tabs
    tab_overview, tab_cleaning, tab_visuals, tab_ai = st.tabs([
        "Overview", "Preprocessing", "Visualizations", "Summary Report"
    ])

    # --- TAB 1: OVERVIEW ---
    with tab_overview:
        st.subheader("Raw Data Preview")
        st.dataframe(df.head(15), use_container_width=True)

        col_schema, col_stats = st.columns(2)
        with col_schema:
            st.subheader("Schema Details")
            st.dataframe(get_column_summary(df), use_container_width=True)
        with col_stats:
            st.subheader("Descriptive Statistics")
            st.dataframe(df.describe(), use_container_width=True)

        st.subheader("Outlier Detection (Interquartile Range - IQR)")
        outlier_df = detect_outliers_iqr(df)
        if not outlier_df.empty:
            st.dataframe(outlier_df, use_container_width=True)
        else:
            st.info("No significant numeric outliers detected via IQR.")

    # --- TAB 2: PREPROCESSING ---
    with tab_cleaning:
        st.subheader("Automated Data Hygiene & Preprocessing")
        
        with st.expander("Type Casting Options", expanded=False):
            cast_dict = {}
            cast_cols = st.columns(min(len(df.columns), 4))
            for i, col in enumerate(df.columns):
                with cast_cols[i % 4]:
                    target = st.selectbox(
                        f"`{col}` ({df[col].dtype})",
                        ["No Change", "String / Text", "Category", "Integer", "Float", "Datetime"],
                        key=f"cast_{col}"
                    )
                    if target != "No Change":
                        cast_dict[col] = target

        c_left, c_right = st.columns(2)
        with c_left:
            drop_dups = st.checkbox("Deduplicate Records (Drop duplicate rows)", value=False)
        with c_right:
            strategy = st.radio("Missing Value Remediation", [
                "Keep As It Is (No Changes)",
                "Drop Rows with Missing Values",
                "Auto-Fill Missing Values (Mean / Mode)"
            ])

        clean_df = clean_dataset(df, drop_duplicates=drop_dups, missing_strategy=strategy, type_cast_dict=cast_dict)
        clean_stats = get_basic_metrics(clean_df)

        st.info(f"**Cleaned State:** `{clean_stats['rows']:,}` rows remaining | `{clean_stats['missing']:,}` missing values remaining.")

        with st.expander("View Generated Pandas Pipeline Code", expanded=False):
            code_text = generate_pipeline_code(active_file.name, cast_dict, drop_dups, strategy)
            st.code(code_text, language="python")

        st.download_button(
            label="Download Cleaned CSV",
            data=clean_df.to_csv(index=False).encode("utf-8"),
            file_name="cleaned_dataset.csv",
            mime="text/csv",
            type="primary"
        )
        st.dataframe(clean_df.head(10), use_container_width=True)

    # --- TAB 3: VISUALIZATIONS (POWER BI STYLE) ---
    with tab_visuals:
        st.subheader("Business Intelligence Visualizer")

        all_columns = clean_df.columns.tolist()
        numeric_cols = clean_df.select_dtypes(include=["number"]).columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns available to measure. Upload a dataset with numeric metrics.")
        else:
            chart_type = st.selectbox(
                "Select Visual Type:",
                ["Bar Chart (Category Comparison)", "Donut / Pie Chart (Share Breakdown)", "Line Trend", "Correlation Heatmap"]
            )

            if chart_type in ["Bar Chart (Category Comparison)", "Donut / Pie Chart (Share Breakdown)", "Line Trend"]:
                vc1, vc2, vc3 = st.columns(3)
                with vc1:
                    category_choice = st.selectbox("Category / Dimension:", all_columns, index=0)
                with vc2:
                    metric_choice = st.selectbox("Measurement / Metric:", numeric_cols, index=0)
                with vc3:
                    agg_choice = st.selectbox("Calculation:", ["Total (Sum)", "Average (Mean)", "Record Count"], index=0)

                if chart_type == "Bar Chart (Category Comparison)":
                    fig = render_bar_chart(clean_df, category_choice, metric_choice, agg_choice)
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Donut / Pie Chart (Share Breakdown)":
                    fig = render_donut_chart(clean_df, category_choice, metric_choice, agg_choice)
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Line Trend":
                    fig = render_line_trend(clean_df, category_choice, metric_choice, agg_choice)
                    st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Correlation Heatmap":
                if len(numeric_cols) >= 2:
                    min_corr = st.slider("Minimum Correlation Threshold (|r| ≥)", 0.0, 0.9, 0.0, step=0.05)
                    fig = render_correlation_heatmap(clean_df, numeric_cols, min_corr)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Correlation analysis requires at least 2 numerical attributes.")

    # --- TAB 4: EXECUTIVE REPORT ---
    with tab_ai:
        st.subheader("AI Data Summary")
        if st.button("Generate Summary", type="primary"):
            if not api_key_input:
                st.warning("Please provide a Gemini API Key in the left sidebar to generate the report.")
            else:
                with st.spinner("Analyzing dataset metrics and generating report..."):
                    try:
                        stats_summary = clean_df.describe().to_string()
                        report_content = generate_ai_report(api_key_input, clean_stats, stats_summary)
                        st.markdown(report_content)
                        st.download_button(
                            label="Export Report as Markdown",
                            data=report_content,
                            file_name="executive_data_report.md",
                            mime="text/markdown"
                        )
                    except Exception as err:
                        st.error(f"Error generating intelligence report: {err}")