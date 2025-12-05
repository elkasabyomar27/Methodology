import pandas as pd
import numpy as np

# ---------- Inspection helpers ----------
def missing_table(df: pd.DataFrame) -> pd.DataFrame:
    m = df.isna().mean().sort_values(ascending=False)
    return pd.DataFrame({"missing_pct": (m * 100).round(2), "n_missing": df.isna().sum()})

def iqr_bounds(s: pd.Series, k: float = 1.5):
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr

# ---------- Cleaning helpers ----------
def normalize_str(series: pd.Series):
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .replace({"nan": np.nan, "none": np.nan, "": np.nan})
    )

def winsorize_iqr(series: pd.Series, k: float = 1.5):
    if not np.issubdtype(series.dtype, np.number):
        return series
    lower, upper = iqr_bounds(series, k)
    return series.clip(lower=lower, upper=upper)

def drop_dupes(df: pd.DataFrame, subset):
    before = len(df)
    out = df.drop_duplicates(subset=subset)
    print(f"Deduped on {subset}: {before} -> {len(out)} rows")
    return out

# ---------- Dataset-specific cleaning for Open Brewery DB ----------
def clean_breweries(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()

    # Type fixes
    num_cols = ["latitude", "longitude"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # String normalizations
    str_cols = ["name", "brewery_type", "city", "state", "country", "street", "website_url"]
    for c in str_cols:
        if c in df.columns:
            df[c] = normalize_str(df[c])

    # Category normalization
    type_map = {
        "microbrewery": "micro",
        "nano": "nano",
        "regional": "regional",
        "brewpub": "brewpub",
        "large": "large",
        "planning": "planning",
        "contract": "contract",
        "proprietor": "proprietor",
        "bar": "bar",
        "taproom": "taproom",
    }
    if "brewery_type" in df.columns:
        df["brewery_type"] = df["brewery_type"].replace(type_map)

    # Outlier handling (lat/long)
    for c in ["latitude", "longitude"]:
        if c in df.columns:
            df[c] = winsorize_iqr(df[c], k=2.5)

    # Deduplication
    key_cols = [c for c in ["id", "name", "street", "city", "state"] if c in df.columns]
    if key_cols:
        df = drop_dupes(df, subset=key_cols)

    return df
