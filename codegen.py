"""Script generator for exporting reproducible Pandas code."""

def generate_pipeline_code(filename: str, cast_dict: dict, drop_duplicates: bool, missing_strategy: str) -> str:
    """Produces ready-to-run Pandas script mirroring UI preprocessing selections."""
    code = f'import pandas as pd\nimport numpy as np\n\n# 1. Load Dataset\ndf = pd.read_csv("{filename}")\n'

    if cast_dict:
        code += "\n# 2. Type Casting\n"
        for col, target in cast_dict.items():
            if target == "String / Text":
                code += f'df["{col}"] = df["{col}"].astype(str)\n'
            elif target == "Category":
                code += f'df["{col}"] = df["{col}"].astype("category")\n'
            elif target == "Integer":
                code += f'df["{col}"] = pd.to_numeric(df["{col}"], errors="coerce").astype("Int64")\n'
            elif target == "Float":
                code += f'df["{col}"] = pd.to_numeric(df["{col}"], errors="coerce")\n'
            elif target == "Datetime":
                code += f'df["{col}"] = pd.to_datetime(df["{col}"], errors="coerce")\n'

    if drop_duplicates:
        code += "\n# 3. Deduplication\ndf = df.drop_duplicates()\n"

    if missing_strategy == "Drop Rows with Missing Values":
        code += "\n# 4. Drop Nulls\ndf = df.dropna()\n"
    elif missing_strategy == "Auto-Fill Missing Values (Mean / Mode)":
        code += "\n# 4. Impute Null Values\n"
        code += 'for col in df.columns:\n'
        code += '    if df[col].isna().sum() > 0:\n'
        code += '        if pd.api.types.is_numeric_dtype(df[col]):\n'
        code += '            df[col] = df[col].fillna(df[col].mean())\n'
        code += '        else:\n'
        code += '            mode_val = df[col].mode()\n'
        code += '            if not mode_val.empty:\n'
        code += '                df[col] = df[col].fillna(mode_val[0])\n'

    code += '\nprint(f"Data ready. Final shape: {df.shape}")\n'
    return code