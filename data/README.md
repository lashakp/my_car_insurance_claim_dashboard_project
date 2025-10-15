
Car Insurance Claim Dashboard Project

Overview

This repository contains a comprehensive data pipeline and interactive dashboard for analyzing and visualizing the Car_Insurance_Claim.csv dataset. The project focuses on cleaning, summarizing, and visualizing insurance claim data to support dashboard-ready insights. It includes scripts for data cleaning, metric generation, visualization, and a Dash-based web application.

Features

Data Cleaning: Standardizes column names, handles missing values, validates data ranges, and converts binary fields to readable categories.
Metric Generation: Computes standard (e.g., claim rate, average credit score) and extended metrics (e.g., claims by age, gender, vehicle ownership).
Visualization: Generates static plots (e.g., heatmaps, bar charts) and interactive Plotly visualizations.
Dashboard: A Dash app with filters for age, gender, driving experience, and vehicle year, displaying KPIs and dynamic charts.

Project Structure
text
my_dash_board_project/
│   Car_Insurance_Claim.csv        # Raw dataset
│   cleaned_data.csv              # Processed dataset
│   data_cleaning.py              # Data cleaning script
│   data_visualization.py         # Visualization script
│   metrics_summary.py            # Metrics generation script
│   requirements.txt              # Dependencies
│   tempCodeRunnerFile.py         # Temporary script
│   🚀 Comprehensive_dashboard_Project_Report.pdf  # Project report
│
├───data
│   app.py                        # Dashboard app script
│   cleaned_data.csv              # Processed data copy
│
├───logs
│   cleaning_log_20251015_142523.log  # Cleaning logs
│   dashboard.log                 # Dashboard logs
│
├───outputs
│   ├───logs
│   │   data_summary.log          # Summary logs
│   │   data_visualization.log    # Visualization logs
│   ├───metrics
│   │   claims_by_age.csv         # Age-based claims
│   │   claims_by_driving_experience.csv  # Experience-based claims
│   │   claims_by_gender.csv      # Gender-based claims
│   │   claims_by_vehicle_ownership.csv  # Ownership-based claims
│   │   claims_by_vehicle_year.csv  # Year-based claims
│   │   summary_metrics.csv       # Overall metrics
│   │   violations_by_claim_status.csv  # Violation stats
│   │   violations_by_outcome.csv  # Outcome-based violations
│   └───visualizations
│       ├───interactive
│       │   claims_by_driving_experience.html  # Interactive chart
│       │   claims_by_vehicle_ownership.html   # Interactive chart
│       │   claims_by_vehicle_year.html       # Interactive chart
│       │   claim_rate_by_driving_experience.html  # Interactive chart
│       │   claim_rate_by_education.html      # Interactive chart
│       │   mileage_vs_claim_rate.html        # Interactive chart
│       │   speeding_vs_claim_status.html     # Interactive chart
│       │   speeding_vs_outcome.html          # Interactive chart
│       └───static
│           claims_by_age.png                 # Static chart
│           claims_by_age_gender_heatmap.png  # Static chart
│           claims_by_gender.png             # Static chart
│           correlation_heatmap.png          # Static chart
│           vehicle_ownership.png            # Static chart
│
├───reports
│   data_cleaning_report.csv       # Cleaning summary
│   data_integrity_summary.csv     # Integrity report
│
└───visuals
    distribution_boxplots.png      # Boxplot visualization
    missing_values_heatmap.png      # Missing data heatmap

Installation

Clone the repository:
bash
git clone <https://github.com/lashakp/my_dash_board_project>
cd my_dash_board_project

Install dependencies:
bash
pip install -r requirements.txt
Required packages include pandas, numpy, matplotlib, seaborn, plotly, dash, dash-bootstrap-components.
Ensure Car_Insurance_Claim.csv is in the root directory.
Usage
Run Data Cleaning:
bash
python data_cleaning.py
Cleans data, saves to data/cleaned_data.csv, and generates reports/logs.
Generate Metrics:
bash
python metrics_summary.py
Computes and saves metrics to outputs/metrics/.
Create Visualizations:
bash
python data_visualization.py
Generates static and interactive plots in outputs/visualizations/.

Launch Dashboard:
bash
python data/app.py
Opens a web app at http://127.0.0.1:8050. Use filters to explore data.

Contributing
Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
MIT License. See LICENSE file for details (to be added).

Acknowledgments
Built with Python, Pandas, Matplotlib, Seaborn, Plotly, and Dash.

Dataset: Car_Insurance_Claim.csv (source not specified; assumed for educational use).