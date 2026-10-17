import pandas as pd
import numpy as np

def get_basic_metrics(df: pd.DataFrame) -> dict:
    return {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "duplicates": int(df.duplicated().sum()),
        "missing": int(df.isna().sum().sum())
    }

def get_column_summary(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isna().sum(),
        "Missing (%)": (df.isna().mean() * 100).round(2),
        "Unique Values": df.nunique()
    })

def detect_outliers_iqr(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=["number"]).columns
    outlier_records = []
    
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 4:
            continue
        q25, q75 = np.percentile(series, 25), np.percentile(series, 75)
        iqr = q75 - q25
        lower_bound = q25 - (1.5 * iqr)
        upper_bound = q75 + (1.5 * iqr)
        outlier_count = int(((series < lower_bound) | (series > upper_bound)).sum())
        
        if outlier_count > 0:
            outlier_records.append({
                "Column": col,
                "Outliers Count": outlier_count,
                "Outliers (%)": round((outlier_count / len(series)) * 100, 2),
                "Valid Range": f"[{round(lower_bound, 2)} to {round(upper_bound, 2)}]"
            })
            
    if not outlier_records:
        return pd.DataFrame(columns=["Column", "Outliers Count", "Outliers (%)", "Valid Range"])
    return pd.DataFrame(outlier_records)

def clean_dataset(
    df: pd.DataFrame, 
    drop_duplicates: bool = False, 
    missing_strategy: str = "Keep As It Is (No Changes)",
    type_cast_dict: dict = None
) -> pd.DataFrame:
    cleaned = df.copy()

    # 1. Type Casting
    if type_cast_dict:
        for col, new_type in type_cast_dict.items():
            if col in cleaned.columns and new_type != "No Change":
                try:
                    if new_type == "String / Text":
                        cleaned[col] = cleaned[col].astype(str)
                    elif new_type == "Category":
                        cleaned[col] = cleaned[col].astype("category")
                    elif new_type == "Integer":
                        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce").astype("Int64")
                    elif new_type == "Float":
                        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
                    elif new_type == "Datetime":
                        cleaned[col] = pd.to_datetime(cleaned[col], errors="coerce")
                except Exception:
                    pass

    # 2. Deduplication
    if drop_duplicates:
        cleaned = cleaned.drop_duplicates()

    # 3. Missing Value Remediation
    if missing_strategy == "Drop Rows with Missing Values":
        cleaned = cleaned.dropna()
    elif missing_strategy == "Auto-Fill Missing Values (Mean / Mode)":
        for col in cleaned.columns:
            if cleaned[col].isna().sum() > 0:
                if pd.api.types.is_numeric_dtype(cleaned[col]):
                    col_mean = cleaned[col].mean()
                    cleaned[col] = cleaned[col].fillna(col_mean)
                else:
                    mode_val = cleaned[col].mode()
                    if not mode_val.empty:
                        cleaned[col] = cleaned[col].fillna(mode_val[0])

    return cleaned

def generate_insights(clean_stats: dict) -> list:
    insights = []
    if clean_stats["missing"] == 0:
        insights.append("No missing data detected across the active records.")
    else:
        insights.append(f"{clean_stats['missing']} missing entries still require imputation.")
    if clean_stats["duplicates"] == 0:
        insights.append("All rows are unique.")
    return insights