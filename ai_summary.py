"""AI Summary generation module using the Google GenAI SDK."""

import re
import time
from google import genai
from google.genai.errors import APIError


def clean_markdown_latex(text: str) -> str:
    """Removes stray dollar signs that trigger unwanted LaTeX formatting in Streamlit."""
    # Replace currency dollar signs like $120 or $45,000 with clean text
    cleaned = re.sub(r"\$(\d+[\d,]*(?:\.\d+)?)", r"\1 USD", text)
    # Remove any stray single dollar signs that could still open math mode
    cleaned = cleaned.replace("$", "")
    return cleaned


def generate_ai_report(api_key: str, metrics_summary: dict, stats_overview: str) -> str:
    """Generates an executive, business-oriented dataset summary without LaTeX bugs.

    Args:
        api_key: Google Gemini API key.
        metrics_summary: Core counts including rows, cols, duplicates, and nulls.
        stats_overview: Formatted string of numeric summary statistics.

    Returns:
        Structured markdown report containing clear business findings and recommendations.
    """
    client = genai.Client(api_key=api_key)

    total_dups = metrics_summary.get("duplicate_rows", 0)
    total_missing = metrics_summary.get("missing_values", 0)

    if total_dups > 0 or total_missing > 0:
        focus_instruction = (
            "The dataset currently has data quality gaps (missing entries or duplicate rows). "
            "Highlight where the data is unreliable in plain terms, then provide practical "
            "steps to clean it up and protect business revenue reporting."
        )
    else:
        focus_instruction = (
            "The dataset is clean (no duplicates, zero missing values). "
            "Focus primarily on commercial strategy: identifying high-margin opportunities, "
            "volume drivers, pricing efficiency, and actions to maximize overall business profit."
        )

    prompt = f"""
You are a Principal Business Intelligence & Commercial Strategy Consultant.
Explain your findings in clear, direct, and actionable business language. 
Avoid overly dense academic statistics jargon.

CRITICAL FORMATTING RULE:
- DO NOT use the dollar symbol '$' anywhere in your response. Writing '$' causes markdown LaTeX math parsing errors that scramble text.
- Always use the word 'USD' or spell out 'dollars' for currency (e.g., write '120 USD' or '3,528 USD', NEVER '$120' or '$3,528').

Context:
{focus_instruction}

Dataset Metrics:
- Total Records: {metrics_summary.get('total_rows')}
- Total Attributes: {metrics_summary.get('total_cols')}
- Duplicate Records: {total_dups}
- Missing Values: {total_missing}

Statistical Summary:
{stats_overview}

Provide your report formatted strictly into these 3 sections:

### 1. Executive & Commercial Overview
- A crisp 2-to-3 sentence summary of what this dataset tracks.
- Detail the typical transaction volume, typical unit prices, and overall revenue scale using everyday terms.

### 2. Data Health & Anomaly Watch
- If duplicates or nulls exist, state exactly how many were found and why they distort sales figures. If clean, confirm the data is fully reliable.
- Call out extreme spikes, unusually large single orders, or unexpected values in plain language and explain their potential impact on reports.

### 3. Practical Strategy & Profit Recommendations
- List 3 concrete, high-impact recommendations for leadership.
- If data errors were detected, include practical fixes alongside a business initiative.
- If data is already clean, focus all 3 points on pricing optimization, margin protection, customer segmentation, and revenue growth.
"""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )
            return clean_markdown_latex(response.text)

        except APIError as e:
            err_msg = str(e)
            if ("429" in err_msg or "503" in err_msg) and attempt < max_retries - 1:
                time.sleep(3)
                continue
            raise Exception(f"API Error ({e.code}): {e.message}") from e
        except Exception as e:
            if attempt < max_retries - 1 and "503" in str(e):
                time.sleep(2)
                continue
            raise e