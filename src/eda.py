import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_missing(df: pd.DataFrame, max_rows: int = 500):
    sample = df.sample(min(len(df), max_rows), random_state=42)
    plt.figure(figsize=(10, 4))
    sns.heatmap(sample.isna(), cbar=False)
    plt.title("Missingness (sample)")
    plt.tight_layout()

def plot_numeric_distributions(df: pd.DataFrame, num_cols=None):
    if num_cols is None:
        num_cols = df.select_dtypes(include="number").columns.tolist()
    for c in num_cols:
        fig, axes = plt.subplots(1, 2, figsize=(10, 3))
        sns.histplot(df[c].dropna(), kde=True, ax=axes[0])
        axes[0].set_title(f"{c} distribution")
        sns.boxplot(x=df[c], ax=axes[1])
        axes[1].set_title(f"{c} boxplot")
        fig.tight_layout()

def plot_categoricals(df: pd.DataFrame, cat_cols=None, top_n=15):
    if cat_cols is None:
        cat_cols = df.select_dtypes(include="object").columns.tolist()
    for c in cat_cols:
        plt.figure(figsize=(8, 4))
        counts = df[c].value_counts().head(top_n)
        sns.barplot(x=counts.values, y=counts.index, orient="h")
        plt.title(f"Top {top_n} categories for {c}")
        plt.tight_layout()

def plot_correlations(df: pd.DataFrame):
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols) < 2:
        return
    corr = df[num_cols].corr()
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr, annot=False, cmap="vlag", center=0)
    plt.title("Numeric correlations")
    plt.tight_layout()
