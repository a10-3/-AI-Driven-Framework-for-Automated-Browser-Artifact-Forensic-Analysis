import pandas as pd
from urllib.parse import urlparse
import os

print(" Starting Phase 2: Data Cleaning...")

# ---------------------------
# 1️ INPUT FILES (same folder as script)
# ---------------------------
history_input = "extracted_data/edge_history.csv"
downloads_input = "extracted_data/edge_downloads.csv"

# Check if input files exist
for f in [history_input, downloads_input]:
    if not os.path.exists(f):
        print(f" File not found: {f}")
        exit()

# ---------------------------
# 2️ OUTPUT FOLDER
# ---------------------------
output_folder = "cleaned_data"
os.makedirs(output_folder, exist_ok=True)

# ---------------------------
# 3️ CLEAN BROWSING HISTORY
# ---------------------------
print(" Cleaning browsing history...")

history_df = pd.read_csv(history_input)

# Remove rows with missing URLs
history_df.dropna(subset=['URL'], inplace=True)

# Convert visit_count to numeric
history_df['Visit Count'] = pd.to_numeric(history_df['Visit Count'], errors='coerce')

# Extract domain from URL
history_df['domain'] = history_df['URL'].apply(lambda x: urlparse(str(x)).netloc)

# Convert last_visit_time to datetime if exists
print("\nConverting 'Last Visit Time' to proper datetime format...")

# Step 1: Force column to numeric
history_df['Last Visit Time'] = pd.to_numeric(history_df['Last Visit Time'], errors='coerce')

# Step 2: Remove invalid or very small timestamps
history_df = history_df[history_df['Last Visit Time'] > 1000000000000000]

# Step 3: Convert from WebKit microseconds (since 1601)
history_df['Last Visit Time'] = pd.to_datetime(
    history_df['Last Visit Time'] - 11644473600000000,
    unit='us',
    errors='coerce'
)
print("Total valid timestamps:", history_df['Last Visit Time'].notna().sum())

print("\nSample converted timestamps:")
print(history_df['Last Visit Time'].head())

# Remove duplicate URLs keeping latest visit
if 'Last Visit Time' in history_df.columns:
    history_df.sort_values('Last Visit Time', ascending=False, inplace=True)
history_df.drop_duplicates(subset='URL', keep='first', inplace=True)

# Save cleaned history
history_output = os.path.join(output_folder, "cleaned_history.csv")
history_df.to_csv(history_output, index=False)

print(f" Browsing history cleaned: {history_output}")

# ---------------------------
# 4️ CLEAN DOWNLOAD HISTORY
# ---------------------------
print(" Cleaning download history...")

downloads_df = pd.read_csv(downloads_input)

# Remove rows without target_path
if 'target_path' in downloads_df.columns:
    downloads_df.dropna(subset=['target_path'], inplace=True)
    # Extract file type
    downloads_df['file_type'] = downloads_df['target_path'].apply(lambda x: x.split('.')[-1] if '.' in str(x) else 'unknown')

# Convert time columns if they exist
for col in ['start_time', 'end_time']:
    if col in downloads_df.columns:
        downloads_df[col] = pd.to_datetime(downloads_df[col], errors='coerce')

# Remove duplicates
downloads_df.drop_duplicates(inplace=True)

# Save cleaned downloads
downloads_output = os.path.join(output_folder, "cleaned_downloads.csv")
downloads_df.to_csv(downloads_output, index=False)

print(f" Download history cleaned: {downloads_output}")

print("\n Phase 2 Completed Successfully! All cleaned files are in 'cleaned_data' folder.")

