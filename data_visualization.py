"""
STEP 3: DATA VISUALIZATION
--------------------------
This script:
- Loads the cleaned dataset
- Generates professional static and interactive visualizations
- Logs each visualization step
- Saves all plots under organized folders
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import logging

# ======================================================
# 1. SETUP DIRECTORIES AND LOGGING
# ======================================================
os.makedirs("outputs/visualizations/static", exist_ok=True)
os.makedirs("outputs/visualizations/interactive", exist_ok=True)
os.makedirs("outputs/logs", exist_ok=True)

logging.basicConfig(
    filename="outputs/logs/data_visualization.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("===== STEP 3: VISUALIZATION STARTED =====")

# ======================================================
# 2. LOAD CLEANED DATA
# ======================================================
try:
    df = pd.read_csv("cleaned_data.csv")
    logging.info(f"Dataset loaded successfully with shape: {df.shape}")
    print(f"✅ Dataset loaded successfully: {df.shape}")
except Exception as e:
    logging.error(f"Error loading dataset: {e}")
    print(f"❌ Error loading dataset: {e}")
    raise SystemExit

# ======================================================
# 3. PREPROCESS FOR VISUALIZATION
# ======================================================
# Convert claim_status to numeric safely (1 = claim, 0 = no claim)
if df["claim_status"].dtype == "object":
    df["claim_status_num"] = df["claim_status"].apply(
        lambda x: 1 if str(x).lower() in ["yes", "claim", "1", "true"] else 0
    )
else:
    df["claim_status_num"] = df["claim_status"]

# ======================================================
# 4. STATIC VISUALIZATIONS (Matplotlib + Seaborn)
# ======================================================
try:
    # --- Claims by Age Group ---
    plt.figure(figsize=(8, 5))
    sns.barplot(
        x="age", y="claim_status_num", data=df,
        estimator="mean", color="skyblue"
    )
    plt.title("Claims by Age Group")
    plt.ylabel("Claim Rate (%)")
    plt.xlabel("Age Group")
    plt.xticks(rotation=45)
    plt.gca().set_ylim(0, 1)
    plt.gca().yaxis.set_major_formatter(lambda y, _: f"{y*100:.0f}%")
    plt.tight_layout()
    plt.savefig("outputs/visualizations/static/claims_by_age.png")
    plt.close()
    logging.info("Saved static chart: claims_by_age.png")

    # --- Claims by Gender ---
    plt.figure(figsize=(6, 4))
    sns.barplot(
        x="gender", y="claim_status_num", data=df,
        estimator="mean", color="lightcoral"
    )
    plt.title("Claims by Gender")
    plt.ylabel("Claim Rate (%)")
    plt.xlabel("Gender")
    plt.gca().set_ylim(0, 1)
    plt.gca().yaxis.set_major_formatter(lambda y, _: f"{y*100:.0f}%")
    plt.tight_layout()
    plt.savefig("outputs/visualizations/static/claims_by_gender.png")
    plt.close()
    logging.info("Saved static chart: claims_by_gender.png")

    # --- Vehicle Ownership Distribution ---
    plt.figure(figsize=(6, 4))
    sns.countplot(x="vehicle_ownership", data=df, hue="vehicle_ownership", palette="pastel", legend=False)
    plt.title("Vehicle Ownership Distribution")
    plt.xlabel("Ownership (Owned vs Leased)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("outputs/visualizations/static/vehicle_ownership.png")
    plt.close()
    logging.info("Saved static chart: vehicle_ownership.png")

    # --- Correlation Heatmap ---
    plt.figure(figsize=(10, 8))
    numeric_cols = df.select_dtypes(include=['number']).corr()
    sns.heatmap(numeric_cols, annot=True, fmt=".2f", cmap="Blues")
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("outputs/visualizations/static/correlation_heatmap.png")
    plt.close()
    logging.info("Saved static chart: correlation_heatmap.png")

    # --- NEW: Claims by Age and Gender (Heatmap) ---
    plt.figure(figsize=(8, 6))
    heatmap_data = df.pivot_table(
        values="claim_status_num",
        index="age", columns="gender", aggfunc="mean"
    )
    sns.heatmap(heatmap_data * 100, cmap="coolwarm", annot=True, fmt=".1f")
    plt.title("Claims by Age and Gender (%)")
    plt.tight_layout()
    plt.savefig("outputs/visualizations/static/claims_by_age_gender_heatmap.png")
    plt.close()
    logging.info("Saved static chart: claims_by_age_gender_heatmap.png")

    print("✅ Static visualizations generated and saved.")
except Exception as e:
    logging.error(f"Error generating static plots: {e}")
    print(f"❌ Error generating static plots: {e}")

# ======================================================
# 5. INTERACTIVE VISUALIZATIONS (Plotly)
# ======================================================
try:
    # --- Interactive: Claims by Driving Experience ---
    df_grouped_exp = (
        df.groupby("driving_experience", as_index=False)["claim_status_num"]
        .mean().sort_values("driving_experience")
    )
    df_grouped_exp["claim_status_num"] *= 100
    fig1 = px.bar(
        df_grouped_exp, x="driving_experience", y="claim_status_num",
        title="Claims by Driving Experience (%)",
        text_auto=".2f", color="claim_status_num", color_continuous_scale="Blues"
    )
    fig1.update_layout(yaxis_title="Claim Rate (%)")
    fig1.write_html("outputs/visualizations/interactive/claims_by_driving_experience.html")
    logging.info("Saved interactive chart: claims_by_driving_experience.html")

    # --- Interactive: Claims by Vehicle Year ---
    df_grouped_year = (
        df.groupby("vehicle_year", as_index=False)["claim_status_num"]
        .mean().sort_values("vehicle_year")
    )
    df_grouped_year["claim_status_num"] *= 100
    fig2 = px.bar(
        df_grouped_year, x="vehicle_year", y="claim_status_num",
        title="Claims by Vehicle Year (%)",
        text_auto=".2f", color="claim_status_num", color_continuous_scale="Purples"
    )
    fig2.update_layout(yaxis_title="Claim Rate (%)")
    fig2.write_html("outputs/visualizations/interactive/claims_by_vehicle_year.html")
    logging.info("Saved interactive chart: claims_by_vehicle_year.html")

    # --- Interactive: Claims by Vehicle Ownership (NEW) ---
    df_grouped_owner = (
        df.groupby("vehicle_ownership", as_index=False)["claim_status_num"]
        .mean().sort_values("vehicle_ownership")
    )
    df_grouped_owner["claim_status_num"] *= 100
    fig3 = px.bar(
        df_grouped_owner, x="vehicle_ownership", y="claim_status_num",
        title="Claims by Vehicle Ownership (%)",
        text_auto=".2f", color="claim_status_num", color_continuous_scale="Greens"
    )
    fig3.update_layout(yaxis_title="Claim Rate (%)")
    fig3.write_html("outputs/visualizations/interactive/claims_by_vehicle_ownership.html")
    logging.info("Saved interactive chart: claims_by_vehicle_ownership.html")

    # --- Interactive: Speeding Violations vs. Claim Status ---
    fig4 = px.box(
        df, x="claim_status", y="speeding_violations",
        title="Speeding Violations by Claim Status",
        color="claim_status"
    )
    fig4.write_html("outputs/visualizations/interactive/speeding_vs_claim_status.html")
    logging.info("Saved interactive chart: speeding_vs_claim_status.html")

    print("✅ Interactive visualizations generated and saved.")
except Exception as e:
    logging.error(f"Error generating interactive plots: {e}")
    print(f"❌ Error generating interactive plots: {e}")

# ======================================================
# 6. COMPLETION
# ======================================================
logging.info("===== STEP 3: VISUALIZATION COMPLETED SUCCESSFULLY =====")
print("\n🎯 Visualization step completed successfully.")
print("Check 'outputs/visualizations' and 'outputs/logs/data_visualization.log'.")
