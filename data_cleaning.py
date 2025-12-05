"""
data_cleaning.py
----------------
Professional data cleaning and validation pipeline for the Car Insurance Claim dataset.
Focus: Dashboard readiness (preserve data integrity for visualization).

Author: Paul Akporarhe
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from datetime import datetime

# ---------------------------------------------------------------------
# 1️⃣  Setup: Directories, Logging, and File Paths
# ---------------------------------------------------------------------
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
VISUAL_DIR = os.path.join(BASE_DIR, "visuals")
LOG_DIR = os.path.join(BASE_DIR, "logs")

for d in [DATA_DIR, REPORT_DIR, VISUAL_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

# Logging setup
log_file = os.path.join(LOG_DIR, f"cleaning_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("🔹 Data Cleaning Process Started")

# ---------------------------------------------------------------------
# 2️⃣  Load Raw Data
# ---------------------------------------------------------------------
input_file = os.path.join(BASE_DIR, "Car_Insurance_Claim.csv")
df_raw = pd.read_csv(input_file)
df = df_raw.copy()

logging.info(f"Data loaded successfully with {df_raw.shape[0]} rows and {df_raw.shape[1]} columns.")

# Basic summary
raw_summary = {
    "rows": df_raw.shape[0],
    "columns": df_raw.shape[1],
    "missing_values": int(df_raw.isna().sum().sum()),
    "duplicates": int(df_raw.duplicated().sum())
}

print(f"RAW DATA SUMMARY: {raw_summary}")

# ---------------------------------------------------------------------
# 3️⃣  Column Standardization
# ---------------------------------------------------------------------
df = df_raw.copy()
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Rename 'outcome' → 'claim_status' for clarity
if 'outcome' in df.columns:
    df.rename(columns={'outcome': 'claim_status'}, inplace=True)
    logging.info("Renamed column 'outcome' → 'claim_status'")

# ---------------------------------------------------------------------
# 4️⃣  Clean Text Columns (trim spaces, standardize case)
# ---------------------------------------------------------------------
text_cols = df.select_dtypes(include="object").columns
for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.lower()

logging.info("Text columns standardized successfully.")

# ---------------------------------------------------------------------
# 5️⃣  Handle Missing Values
# ---------------------------------------------------------------------
df["credit_score"] = df["credit_score"].fillna(df["credit_score"].median())
df["annual_mileage"] = df["annual_mileage"].fillna(df["annual_mileage"].median())

# ---------------------------------------------------------------------
# 6️⃣  Data Validation Rules
# ---------------------------------------------------------------------
validation_issues = []

# --- Credit score range check ---
invalid_cs = df[(df["credit_score"] < 0) | (df["credit_score"] > 1)]
if not invalid_cs.empty:
    validation_issues.append(("credit_score", len(invalid_cs)))
    df["credit_score"] = df["credit_score"].clip(0, 1)

# --- Annual mileage positive check ---
invalid_mileage = df[df["annual_mileage"] <= 0]
if not invalid_mileage.empty:
    validation_issues.append(("annual_mileage", len(invalid_mileage)))
    df.loc[df["annual_mileage"] <= 0, "annual_mileage"] = df["annual_mileage"].median()

# ---------------------------------------------------------------------
# 🧩 Update Binary Columns to Readable Categories
# ---------------------------------------------------------------------

# Convert vehicle_ownership from numeric → categorical
if "vehicle_ownership" in df.columns:
    df["vehicle_ownership"] = df["vehicle_ownership"].replace({0: "leased", 1: "owned"})

# Convert claim_status from numeric → categorical
if "claim_status" in df.columns:
    df["claim_status"] = df["claim_status"].replace({0: "no claim", 1: "claim"})

# ---------------------------------------------------------------------
# 7️⃣  Validation for New String-based Categories
# ---------------------------------------------------------------------
if "vehicle_ownership" in df.columns:
    valid_ownership = ["leased", "owned"]
    invalid_vo = df[~df["vehicle_ownership"].isin(valid_ownership)]
    if not invalid_vo.empty:
        validation_issues.append(("vehicle_ownership", len(invalid_vo)))
        df.loc[~df["vehicle_ownership"].isin(valid_ownership), "vehicle_ownership"] = np.nan

if "claim_status" in df.columns:
    valid_claims = ["claim", "no claim"]
    invalid_claims = df[~df["claim_status"].isin(valid_claims)]
    if not invalid_claims.empty:
        validation_issues.append(("claim_status", len(invalid_claims)))
        df.loc[~df["claim_status"].isin(valid_claims), "claim_status"] = np.nan

logging.info(f"Validation checks completed. Issues found: {validation_issues if validation_issues else 'None'}")

# ---------------------------------------------------------------------
# 8️⃣  Duplicates and Index Handling
# ---------------------------------------------------------------------
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)

# ---------------------------------------------------------------------
# 9️⃣  Generate Before/After Summary
# ---------------------------------------------------------------------
clean_summary = {
    "rows": df.shape[0],
    "columns": df.shape[1],
    "missing_values": int(df.isna().sum().sum()),
    "duplicates": int(df.duplicated().sum())
}

summary_df = pd.DataFrame({
    "Metric": ["Rows", "Columns", "Missing Values", "Duplicates"],
    "Before Cleaning": list(raw_summary.values()),
    "After Cleaning": list(clean_summary.values())
})

print("\nCLEANING SUMMARY:\n", summary_df)

# ---------------------------------------------------------------------
# 🔟  Save Cleaned Data and Report
# ---------------------------------------------------------------------
cleaned_file = os.path.join(DATA_DIR, "cleaned_data.csv")
report_file = os.path.join(REPORT_DIR, "data_cleaning_report.csv")

df.to_csv(cleaned_file, index=False)
summary_df.to_csv(report_file, index=False)

logging.info(f"Cleaned data saved to {cleaned_file}")
logging.info(f"Cleaning report saved to {report_file}")

# ---------------------------------------------------------------------
# 🧠 11️⃣  Optional: Visual Diagnostics
# ---------------------------------------------------------------------
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
plt.title("Missing Values After Cleaning")
plt.tight_layout()
plt.savefig(os.path.join(VISUAL_DIR, "missing_values_heatmap.png"))
plt.close()

plt.figure(figsize=(10, 6))
sns.boxplot(data=df[["credit_score", "annual_mileage"]])
plt.title("Distribution Check: Credit Score & Annual Mileage")
plt.tight_layout()
plt.savefig(os.path.join(VISUAL_DIR, "distribution_boxplots.png"))
plt.close()

logging.info("Visual diagnostics saved successfully.")
logging.info("✅ Data Cleaning Completed Successfully.")

print("\n✅ Data cleaning, validation, and report generation completed successfully.")
