# DataPulse: Data Intelligence & Automated Preprocessing Platform

DataPulse is an interactive data engineering and business intelligence web app built with **Python**, **Streamlit**, and **Plotly**. It automates dataset health profiling, missing value imputation, and record deduplication. It also builds dynamic visualizations and generates executive business summaries powered by Google's Gemini API.

---

## Key Features

- **Automated Data Profiling:** Instantly view record counts, column data types, missing value percentages, duplicate entries, and statistical outliers detected with the Interquartile Range (IQR) method.
- **Data Preprocessing Studio:** Clean data in seconds with one-click deduplication, flexible null imputation (mean/mode fill or row deletion), and custom data type casting.
- **Dynamic Code Export:** Automatically generates copy-pasteable Pandas code that mirrors every cleaning action selected in the interface.
- **Business Intelligence Visuals:** Build interactive, Power BI-style charts, including category comparison bars, share breakdown donut charts, line trends, and Pearson correlation heatmaps with an adjustable threshold slider.
- **AI Executive Summary:** Integrates with Gemini (`gemini-3.8-flash`) to generate structured commercial insights, data quality risk assessments, and practical profit optimization recommendations.
- **File Export Support:** Download cleaned datasets as CSV and save generated AI reports as Markdown documents.

---

## Tech Stack

| Purpose | Technology |
|---|---|
| Dashboard Framework | Streamlit |
| Data Analysis & Processing | Pandas, NumPy |
| Interactive Visualizations | Plotly Express |
| AI Model Integration | Google GenAI SDK (`google-genai`) |

---

## Project Structure

```
Data-pulse/
├── .streamlit/            # Local config directory holding private API credentials
├── .gitignore             # Keeps local secrets and Python caches out of version control
├── app.py                 # Main Streamlit application and user interface
├── cleaner.py             # Data profiling, cleaning, imputation, and outlier detection logic
├── charts.py              # Plotly visualization chart builders
├── codegen.py             # Dynamic Pandas pipeline code generator
├── styles.py              # Custom CSS for the glassmorphic user interface
├── ai_summary.py          # Gemini LLM integration for executive summary reporting
├── retail_test_data.csv   # Demo dataset for immediate pipeline testing
└── requirements.txt       # Python dependencies
```

---

## Local Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Bsathwikreddy05/Data-pulse.git
cd Data-pulse
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API secrets

Create a `.streamlit/secrets.toml` file in the project root:

```toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

> **Note:** Never commit this file. It is already excluded by `.gitignore`.

### 4. Run the application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Quick Start

Want to try it right away? Upload `retail_test_data.csv` in the app to explore profiling, cleaning, charts, and the AI summary with sample data.