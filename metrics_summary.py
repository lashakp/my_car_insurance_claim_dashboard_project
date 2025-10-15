"""
STEP 2: DATA SUMMARY & METRICS GENERATION
------------------------------------------
This script:
- Loads the cleaned dataset
- Computes standard + extended summary metrics
- Saves detailed results in organized directories
- Logs all outputs for traceability
"""

import pandas as pd
import os
import logging

# ======================================================
# 1. SETUP DIRECTORIES AND LOGGING
# ======================================================
os.makedirs("outputs/logs", exist_ok=True)
os.makedirs("outputs/metrics", exist_ok=True)

logging.basicConfig(
    filename="outputs/logs/data_summary.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("===== STEP 2: DATA SUMMARY STARTED =====")

# ======================================================
# 2. LOAD CLEANED DATA
# ======================================================
try:
    df = pd.read_csv("cleaned_data.csv")
    logging.info("Cleaned dataset loaded successfully.")
    print(f"✅ Cleaned dataset loaded successfully. Shape: {df.shape}")
except Exception as e:
    logging.error(f"Error loading cleaned data: {e}")
    print(f"❌ Error loading cleaned data: {e}")
    raise SystemExit


# ======================================================
# 3. STANDARD METRICS
# ======================================================
try:
    # --- Handle claim_status as either text ("claim"/"no claim") or numeric (1/0)
    if df["claim_status"].dtype == "object":
        total_claims = (df["claim_status"].str.lower() == "claim").sum()
        claim_rate = (df["claim_status"].str.lower() == "claim").mean() * 100
    else:
        total_claims = df["claim_status"].sum()
        claim_rate = df["claim_status"].mean() * 100

    total_customers = len(df)
    avg_credit_score = df["credit_score"].mean()
    avg_mileage = df["annual_mileage"].mean()

    # --- Breakdown metrics
    claims_by_age = (
        df.groupby("age")["claim_status"]
        .apply(lambda x: (x.str.lower() == "claim").mean() * 100 if x.dtype == "object" else x.mean() * 100)
        .sort_index()
    )
    claims_by_gender = (
        df.groupby("gender")["claim_status"]
        .apply(lambda x: (x.str.lower() == "claim").mean() * 100 if x.dtype == "object" else x.mean() * 100)
        .sort_index()
    )
    violations_by_claim_status = df.groupby("claim_status")["speeding_violations"].mean().sort_index()

    # --- Summary table
    summary_metrics = pd.DataFrame({
        "Metric": ["Total Customers", "Total Claims", "Claim Rate (%)", "Avg Credit Score", "Avg Annual Mileage"],
        "Value": [total_customers, total_claims, round(claim_rate, 2),
                  round(avg_credit_score, 2), round(avg_mileage, 2)]
    })

    # --- Save outputs
    summary_metrics.to_csv("outputs/metrics/summary_metrics.csv", index=False)
    claims_by_age.to_csv("outputs/metrics/claims_by_age.csv", header=True)
    claims_by_gender.to_csv("outputs/metrics/claims_by_gender.csv", header=True)
    violations_by_claim_status.to_csv("outputs/metrics/violations_by_claim_status.csv", header=True)

    logging.info("Standard summary metrics generated successfully.")
    logging.info(f"\n{summary_metrics}")
    print("\n✅ Standard metrics calculated successfully.")

except Exception as e:
    logging.error(f"Error during summary generation: {e}")
    print(f"❌ Error during summary generation: {e}")
    raise


# ======================================================
# 4. EXTENDED SUMMARIES
# ======================================================
try:
    # --- Claims by vehicle ownership (leased / owned)
    claims_by_vehicle_ownership = (
        df.groupby("vehicle_ownership")["claim_status"]
        .apply(lambda x: (x.str.lower() == "claim").mean() * 100 if x.dtype == "object" else x.mean() * 100)
        .sort_index()
    )
    claims_by_vehicle_ownership.to_csv("outputs/metrics/claims_by_vehicle_ownership.csv", header=True)

    # --- Claims by driving experience
    claims_by_driving_exp = (
        df.groupby("driving_experience")["claim_status"]
        .apply(lambda x: (x.str.lower() == "claim").mean() * 100 if x.dtype == "object" else x.mean() * 100)
        .sort_index()
    )
    claims_by_driving_exp.to_csv("outputs/metrics/claims_by_driving_experience.csv", header=True)

    # --- Claims by vehicle year
    claims_by_vehicle_year = (
        df.groupby("vehicle_year")["claim_status"]
        .apply(lambda x: (x.str.lower() == "claim").mean() * 100 if x.dtype == "object" else x.mean() * 100)
        .sort_index()
    )
    claims_by_vehicle_year.to_csv("outputs/metrics/claims_by_vehicle_year.csv", header=True)

    # --- Risk behavior averages
    avg_speeding = df["speeding_violations"].mean()
    avg_duis = df["duis"].mean()
    avg_past_accidents = df["past_accidents"].mean()

    logging.info("===== EXTENDED METRICS =====")
    logging.info(f"Claims by Vehicle Ownership:\n{claims_by_vehicle_ownership.to_string()}")
    logging.info(f"Claims by Driving Experience:\n{claims_by_driving_exp.to_string()}")
    logging.info(f"Claims by Vehicle Year:\n{claims_by_vehicle_year.to_string()}")
    logging.info(f"Avg Speeding Violations: {avg_speeding:.2f}")
    logging.info(f"Avg DUIs: {avg_duis:.2f}")
    logging.info(f"Avg Past Accidents: {avg_past_accidents:.2f}")

    print("\n✅ Extended metrics calculated successfully.")
    print("📁 Saved detailed breakdowns under 'outputs/metrics/'.")

except Exception as e:
    logging.error(f"Error generating extended summaries: {e}")
    print(f"❌ Error generating extended summaries: {e}")
    raise


# ======================================================
# 5. COMPLETION MESSAGE
# ======================================================
logging.info("===== STEP 2: DATA SUMMARY COMPLETED SUCCESSFULLY =====")
print("\n🎯 All summaries and logs generated successfully!")
print("Check 'outputs/logs/data_summary.log' for full details.")
