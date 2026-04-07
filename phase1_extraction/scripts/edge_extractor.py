print("SCRIPT STRARTED")
import os
import shutil
import sqlite3
import pandas as pd

# ==============================
# 1️ PATHS
# ==============================

USER = os.getlogin()

EDGE_HISTORY_PATH = fr"C:\Users\{USER}\AppData\Local\Microsoft\Edge\User Data\Default\History"
OUTPUT_FOLDER = r"..\extracted_data"

TEMP_HISTORY = "temp_history.db"

# Create output folder if not exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==============================
# 2️ COPY DATABASE (Browser locks original file)
# ==============================

if not os.path.exists(EDGE_HISTORY_PATH):
    print(" Edge History file not found.")
    exit()

shutil.copy2(EDGE_HISTORY_PATH, TEMP_HISTORY)
print(" History database copied successfully.")

# ==============================
# 3️ CONNECT TO DATABASE
# ==============================

conn = sqlite3.connect(TEMP_HISTORY)
cursor = conn.cursor()

# ==============================
# 4️ EXTRACT BROWSING HISTORY
# ==============================

try:
    cursor.execute("""
        SELECT url, title, visit_count, last_visit_time
        FROM urls
    """)
    
    history_data = cursor.fetchall()
    history_df = pd.DataFrame(history_data, columns=[
        "URL", "Title", "Visit Count", "Last Visit Time"
    ])
    
    history_output_path = os.path.join(OUTPUT_FOLDER, "edge_history.csv")
    history_df.to_csv(history_output_path, index=False)
    
    print(" Browsing history extracted.")

except Exception as e:
    print(" Error extracting history:", e)

# ==============================
# 5 EXTRACT DOWNLOAD HISTORY
# ==============================

try:
    cursor.execute("""
        SELECT target_path, tab_url, total_bytes
        FROM downloads
    """)
    
    downloads_data = cursor.fetchall()
    downloads_df = pd.DataFrame(downloads_data, columns=[
        "File Path", "Source URL", "Size (Bytes)"
    ])
    
    downloads_output_path = os.path.join(OUTPUT_FOLDER, "edge_downloads.csv")
    downloads_df.to_csv(downloads_output_path, index=False)
    
    print(" Download history extracted.")

except Exception as e:
    print(" Error extracting downloads:", e)

# ==============================
# 6️ CLEANUP
# ==============================

conn.close()
os.remove(TEMP_HISTORY)

print("\n Phase 1 Extraction Completed Successfully!")
