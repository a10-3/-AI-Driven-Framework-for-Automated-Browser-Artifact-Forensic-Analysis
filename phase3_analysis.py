import pandas as pd
import matplotlib.pyplot as plt

print("Starting Phase 3: Behavioral Analysis...")

# Load cleaned history
history_df = pd.read_csv("cleaned_data/cleaned_history.csv")
downloads_df = pd.read_csv("cleaned_data/cleaned_downloads.csv")

print("Loaded cleaned history data.")

# Top visited domains
print("\nTop 10 Most Visited Domains:")
top_domains = history_df['domain'].value_counts().head(10)
print(top_domains)

# Save results
top_domains.to_csv("reports/top_domains.csv")

print("\nPhase 3 Step 1 Completed.")

# ==============================
# Daily Browsing Activity
# ==============================

print("\nGenerating daily browsing activity graph...")

# Convert Last Visit Time to datetime (safety step)
history_df['Last Visit Time'] = pd.to_datetime(history_df['Last Visit Time'], errors='coerce')

# Drop invalid dates
history_df = history_df.dropna(subset=['Last Visit Time'])

# Extract date only
history_df['visit_date'] = history_df['Last Visit Time'].dt.date

# Count visits per day
daily_activity = history_df['visit_date'].value_counts().sort_index()

print("\nDaily Activity Data:")
print(daily_activity.head())

# Save to CSV
daily_activity.to_csv("reports/daily_activity.csv")

# Plot graph
plt.figure(figsize=(10,5))
daily_activity.plot(kind='bar')
plt.title("Daily Browsing Activity")
plt.xlabel("Date")
plt.ylabel("Number of Visits")
plt.tight_layout()
plt.savefig("reports/daily_activity_plot.png")
plt.show()

print("\nPhase 3 Step 2 Completed.")

# -----------------------------------------
# STEP 3: Download Source Analysis
# -----------------------------------------

print("\nAnalyzing download sources...")

# Extract domain from Source URL
from urllib.parse import urlparse

downloads_df['download_domain'] = downloads_df['Source URL'].apply( 
    lambda x: urlparse(str(x)).netloc if pd.notnull(x) else None
)

top_download_sources = downloads_df['download_domain'].value_counts().head(10) 

print("\nTop Download Sources:")
print(top_download_sources)

# Save results
top_download_sources.to_csv("reports/top_download_sources.csv")

# Plot
plt.figure(figsize=(8,4))
top_download_sources.plot(kind='bar')
plt.title("Top Download Sources")
plt.xlabel("Website")
plt.ylabel("Number of Downloads")
plt.tight_layout()
plt.savefig("reports/top_download_sources_plot.png")
plt.show()

print("\nPhase 3 Step 3 Completed")
