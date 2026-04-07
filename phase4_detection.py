import pandas as pd
import os

print("Starting Phase 4: Suspicious Activity Detection...")

# Create reports folder if not exists
os.makedirs("reports", exist_ok=True)

# Load cleaned data
history_df = pd.read_csv("cleaned_data/cleaned_history.csv")
downloads_df = pd.read_csv("cleaned_data/cleaned_downloads.csv")

print("Loaded cleaned datasets.")

# Convert time column to datetime
history_df["Last Visit Time"] = pd.to_datetime(history_df["Last Visit Time"], errors="coerce")

# -------------------------------
#  Rule 1: Late Night Browsing
# -------------------------------
history_df["Hour"] = history_df["Last Visit Time"].dt.hour
late_night = history_df[(history_df["Hour"] >= 12) | (history_df["Hour"] <= 5)]

late_night_summary = late_night["domain"].value_counts().head(10)
late_night_summary.to_csv("reports/late_night_activity.csv")

print("Late night browsing analysis done.")

# -----------------------------------
#  Rule 2: Rare / Suspicious Domains
# -----------------------------------
domain_counts = history_df["domain"].value_counts()

rare_domains = domain_counts[domain_counts <= 2]
rare_domains.to_csv("reports/rare_domains.csv")

print("Rare domain detection done.")

# -----------------------------------
#  Rule 3: Suspicious Downloads
# -----------------------------------
# Flag large downloads (> 100MB)
downloads_df["Size_MB"] = downloads_df["Size (Bytes)"] / (1024 * 1024)

large_downloads = downloads_df[downloads_df["Size_MB"] > 100]
large_downloads.to_csv("reports/large_downloads.csv", index=False)

print("Large download detection done.")

# -----------------------------------
#  Rule 4: Simple Risk Scoring
# -----------------------------------
risk_score = 0

risk_score += len(late_night) * 1
risk_score += len(rare_domains) * 2
risk_score += len(large_downloads) * 3

with open("reports/risk_score.txt", "w") as f:
    f.write(f"Overall Risk Score: {risk_score}\n")

print(f"Risk scoring completed. Score = {risk_score}")

print("Phase 4 Completed Successfully.")
