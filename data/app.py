# =====================================================
# INTERACTIVE DASHBOARD APP FOR CAR INSURANCE CLAIM DATA
# =====================================================

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import logging
import os

# -----------------------------------------------------
# SETUP & DIRECTORIES
# -----------------------------------------------------
os.makedirs("logs", exist_ok=True)
os.makedirs("outputs/interactive", exist_ok=True)

logging.basicConfig(
    filename="logs/dashboard.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------------------------------
# LOAD CLEANED DATA
# -----------------------------------------------------
try:
    df = pd.read_csv("cleaned_data.csv")
    logging.info("✅ Cleaned dataset loaded successfully. Shape: %s", df.shape)
except Exception as e:
    logging.error(f"❌ Failed to load cleaned data: {e}")
    raise SystemExit(f"Error: {e}")

# -----------------------------------------------------
# NORMALIZE / ENSURE COLUMN NAMES & CREATE NUMERIC FLAG
# -----------------------------------------------------
# If old file still uses 'outcome', rename it.
if "outcome" in df.columns and "claim_status" not in df.columns:
    df.rename(columns={"outcome": "claim_status"}, inplace=True)
    logging.info("Renamed 'outcome' -> 'claim_status' (compatibility)")

# If claim_status is numeric (0/1), map to human readable strings
if "claim_status" in df.columns:
    if pd.api.types.is_numeric_dtype(df["claim_status"]):
        df["claim_status"] = df["claim_status"].map({1: "claim", 0: "no claim"})
        logging.info("Mapped numeric claim_status 0/1 -> 'no claim'/'claim'")

# Create numeric helper column for aggregations
if "claim_status" in df.columns:
    df["claim_flag"] = df["claim_status"].astype(str).str.lower().map({"claim": 1, "no claim": 0})
    # if any unmapped values, coerce to NaN then fill with 0 for safety in dashboards (optional)
    df["claim_flag"] = pd.to_numeric(df["claim_flag"], errors="coerce")
    logging.info("Created 'claim_flag' numeric column for aggregations (1 = claim, 0 = no claim)")
else:
    logging.error("Column 'claim_status' not found after loading. Aborting.")
    raise SystemExit("Column 'claim_status' not found in dataset.")

# -----------------------------------------------------
# INITIAL METRIC CALCULATION FUNCTION (uses claim_flag)
# -----------------------------------------------------
def calculate_metrics(data: pd.DataFrame):
    total_customers = len(data)
    total_claims = int(data["claim_flag"].fillna(0).sum())
    # If there are rows with NaN claim_flag, we exclude them from the mean
    claim_rate = round(data["claim_flag"].dropna().mean() * 100, 2) if not data["claim_flag"].dropna().empty else 0.0
    avg_credit_score = round(data["credit_score"].mean(), 2) if "credit_score" in data.columns else None
    avg_mileage = round(data["annual_mileage"].mean(), 2) if "annual_mileage" in data.columns else None

    return {
        "total_customers": total_customers,
        "total_claims": total_claims,
        "claim_rate": claim_rate,
        "avg_credit_score": avg_credit_score,
        "avg_mileage": avg_mileage
    }

# -----------------------------------------------------
# KPI CARD FUNCTION
# -----------------------------------------------------
def create_kpi_card(title, value, color="primary"):
    return dbc.Card([
        dbc.CardHeader(title),
        dbc.CardBody(html.H4(value, className=f"text-{color}"))
    ], className="mb-2")

# -----------------------------------------------------
# CREATE DASH APP
# -----------------------------------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Car Insurance Claim Dashboard"

# -----------------------------------------------------
# APP LAYOUT
# -----------------------------------------------------
app.layout = dbc.Container([
    html.H1("🚗 Car Insurance Claim Dashboard", className="text-center my-4"),

    # ---------------- FILTER CONTROLS ----------------
    dbc.Row([
        dbc.Col([
            html.Label("Filter by Age"),
            dcc.Dropdown(
                options=[{"label": a, "value": a} for a in sorted(df["age"].dropna().unique())],
                id="filter-age",
                multi=True,
                placeholder="Select age group(s)"
            )
        ], width=3),

        dbc.Col([
            html.Label("Filter by Gender"),
            dcc.Dropdown(
                options=[{"label": g, "value": g} for g in sorted(df["gender"].dropna().unique())],
                id="filter-gender",
                multi=True,
                placeholder="Select gender(s)"
            )
        ], width=3),

        dbc.Col([
            html.Label("Filter by Driving Experience"),
            dcc.Dropdown(
                options=[{"label": e, "value": e} for e in sorted(df["driving_experience"].dropna().unique())],
                id="filter-experience",
                multi=True,
                placeholder="Select experience level(s)"
            )
        ], width=3),

        dbc.Col([
            html.Label("Filter by Vehicle Year"),
            dcc.Dropdown(
                options=[{"label": v, "value": v} for v in sorted(df["vehicle_year"].dropna().unique())],
                id="filter-year",
                multi=True,
                placeholder="Select vehicle year(s)"
            )
        ], width=3),
    ], className="mb-4"),

    # ---------------- KPI CARDS ----------------
    dbc.Row(id="kpi-cards", className="mb-4"),

    # ---------------- GRAPHS ----------------
    dbc.Row([
        dbc.Col(dcc.Graph(id="claims-by-age"), width=6),
        dbc.Col(dcc.Graph(id="claims-by-gender"), width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="experience-vs-claim"), width=6),
        dbc.Col(dcc.Graph(id="ownership-vs-claim"), width=6)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="vehicle-year-vs-claim"), width=6),
        dbc.Col(dcc.Graph(id="speeding-vs-claim"), width=6)
    ])
])

# -----------------------------------------------------
# CALLBACK: FILTER LOGIC & DASH UPDATES
# -----------------------------------------------------
@app.callback(
    [
        Output("kpi-cards", "children"),
        Output("claims-by-age", "figure"),
        Output("claims-by-gender", "figure"),
        Output("experience-vs-claim", "figure"),
        Output("ownership-vs-claim", "figure"),
        Output("vehicle-year-vs-claim", "figure"),
        Output("speeding-vs-claim", "figure")
    ],
    [
        Input("filter-age", "value"),
        Input("filter-gender", "value"),
        Input("filter-experience", "value"),
        Input("filter-year", "value")
    ]
)
def update_dashboard(selected_age, selected_gender, selected_experience, selected_year):
    try:
        filtered_df = df.copy()

        if selected_age:
            filtered_df = filtered_df[filtered_df["age"].isin(selected_age)]
        if selected_gender:
            filtered_df = filtered_df[filtered_df["gender"].isin(selected_gender)]
        if selected_experience:
            filtered_df = filtered_df[filtered_df["driving_experience"].isin(selected_experience)]
        if selected_year:
            filtered_df = filtered_df[filtered_df["vehicle_year"].isin(selected_year)]

        metrics = calculate_metrics(filtered_df)

        # KPI cards
        kpi_cards = dbc.Row([
            dbc.Col(create_kpi_card("Total Customers", f"{metrics['total_customers']:,}", "primary"), width=2),
            dbc.Col(create_kpi_card("Total Claims", f"{metrics['total_claims']:,}", "danger"), width=2),
            dbc.Col(create_kpi_card("Claim Rate (%)", f"{metrics['claim_rate']}%", "success"), width=2),
            dbc.Col(create_kpi_card("Avg Credit Score", f"{metrics['avg_credit_score']}", "info"), width=3),
            dbc.Col(create_kpi_card("Avg Mileage", f"{metrics['avg_mileage']:,}", "warning"), width=3)
        ])

        # ----------------- FIGURES (use claim_flag mean -> percent) -----------------

        # Age
        age_grouped = (
            filtered_df.groupby("age", dropna=False)["claim_flag"]
            .mean()
            .reset_index()
            .rename(columns={"claim_flag": "claim_rate"})
        )
        age_grouped["claim_rate"] = age_grouped["claim_rate"] * 100

        fig_age = px.bar(
            age_grouped,
            x="age", y="claim_rate",
            title="Claim Rate by Age (%)",
            color="age", text_auto=".2f"
        )
        fig_age.update_layout(yaxis_title="Claim Rate (%)")

        # Gender
        gender_grouped = (
            filtered_df.groupby("gender", dropna=False)["claim_flag"]
            .mean()
            .reset_index()
            .rename(columns={"claim_flag": "claim_rate"})
        )
        gender_grouped["claim_rate"] = gender_grouped["claim_rate"] * 100

        fig_gender = px.bar(
            gender_grouped,
            x="gender", y="claim_rate",
            title="Claim Rate by Gender (%)",
            color="gender", text_auto=".2f"
        )
        fig_gender.update_layout(yaxis_title="Claim Rate (%)")

        # Driving experience
        exp_grouped = (
            filtered_df.groupby("driving_experience", dropna=False)["claim_flag"]
            .mean()
            .reset_index()
            .rename(columns={"claim_flag": "claim_rate"})
        )
        exp_grouped["claim_rate"] = exp_grouped["claim_rate"] * 100

        fig_experience = px.bar(
            exp_grouped,
            x="driving_experience", y="claim_rate",
            title="Driving Experience vs Claim Rate (%)",
            color="driving_experience", text_auto=".2f"
        )
        fig_experience.update_layout(yaxis_title="Claim Rate (%)")

        # Vehicle ownership
        owner_grouped = (
            filtered_df.groupby("vehicle_ownership", dropna=False)["claim_flag"]
            .mean()
            .reset_index()
            .rename(columns={"claim_flag": "claim_rate"})
        )
        owner_grouped["claim_rate"] = owner_grouped["claim_rate"] * 100

        fig_ownership = px.bar(
            owner_grouped,
            x="vehicle_ownership", y="claim_rate",
            title="Vehicle Ownership vs Claim Rate (%)",
            color="vehicle_ownership", text_auto=".2f"
        )
        fig_ownership.update_layout(yaxis_title="Claim Rate (%)")

        # Vehicle year
        year_grouped = (
            filtered_df.groupby("vehicle_year", dropna=False)["claim_flag"]
            .mean()
            .reset_index()
            .rename(columns={"claim_flag": "claim_rate"})
        )
        year_grouped["claim_rate"] = year_grouped["claim_rate"] * 100

        fig_year = px.bar(
            year_grouped,
            x="vehicle_year", y="claim_rate",
            title="Vehicle Year vs Claim Rate (%)",
            color="vehicle_year", text_auto=".2f"
        )
        fig_year.update_layout(yaxis_title="Claim Rate (%)")

        # Speeding violations vs claim_status (categorical)
        fig_speeding = px.box(
            filtered_df,
            x="claim_status", y="speeding_violations",
            title="Speeding Violations by Claim Status",
            color="claim_status"
        )

        logging.info("✅ Dashboard updated successfully with current filter selection.")

        return (
            kpi_cards,
            fig_age, fig_gender,
            fig_experience, fig_ownership,
            fig_year, fig_speeding
        )

    except Exception as e:
        logging.error(f"❌ Dashboard update failed: {e}")
        raise

# -----------------------------------------------------
# RUN SERVER
# -----------------------------------------------------
if __name__ == "__main__":
    logging.info("🚀 Dashboard starting on http://127.0.0.1:8050")
    app.run(debug=True, port=8050)
# ======================================================
