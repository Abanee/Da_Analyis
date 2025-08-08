import pandas as pd
import numpy as np

def analyze_data(df):
    """Generate basic insights from DataFrame."""
    insights = []

    # Basic statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if numeric_cols.size > 0:
        insights.append(f"Dataset has {len(df)} rows and {len(df.columns)} columns.")
        for col in numeric_cols:
            insights.append(f"Column '{col}' - Mean: {df[col].mean():.2f}, Std: {df[col].std():.2f}")

    # Sales-specific analysis
    sales_cols = [col for col in df.columns if "sales" in col.lower()]
    if sales_cols:
        date_cols = df.select_dtypes(include=['datetime']).columns
        for col in sales_cols:
            temp_df = df.copy()
            if date_cols.size > 0:
                temp_df = temp_df.sort_values(by=date_cols[0])
            trend = "increasing" if temp_df[col].diff().mean() > 0 else "decreasing"
            insights.append(f"Sales column '{col}' shows a {trend} trend.")
            anomalies = temp_df[col][(temp_df[col] > temp_df[col].mean() + 2 * temp_df[col].std()) | 
                                  (temp_df[col] < temp_df[col].mean() - 2 * temp_df[col].std())]
            if not anomalies.empty:
                insights.append(f"Anomalies detected in '{col}': {len(anomalies)} data points.")

    return insights
