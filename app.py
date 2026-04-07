import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Browser Forensics Dashboard", layout="wide")

st.title(" AI-Powered Browser Forensics Dashboard")

# -----------------------------
# Load Data
# -----------------------------
history_path = "cleaned_data/cleaned_history.csv"
downloads_path = "cleaned_data/cleaned_downloads.csv"

try:
    history_df = pd.read_csv(history_path)
    downloads_df = pd.read_csv(downloads_path)
except:
    st.error("Cleaned data files not found. Run Phase 2 first.")
    st.stop()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Dashboard Controls")
show_raw = st.sidebar.checkbox("Show Raw Data")

# -----------------------------
# Section 1 — Top Domains
# -----------------------------
st.header(" Top Visited Domains")

if "domain" in history_df.columns:
    top_domains = history_df["domain"].value_counts().head(10)

    fig1, ax1 = plt.subplots()
    top_domains.plot(kind="bar", ax=ax1)
    ax1.set_ylabel("Visit Count")
    ax1.set_xlabel("Domain")
    st.pyplot(fig1)
else:
    st.warning("Domain column not found in history data.")

# -----------------------------
# Section 2 — Daily Activity
# -----------------------------
st.header(" Daily Browsing Activity")

if "Last Visit Time" in history_df.columns:
    history_df["Last Visit Time"] = pd.to_datetime(history_df["Last Visit Time"], errors="coerce")
    daily_activity = history_df.dropna(subset=["Last Visit Time"])
    daily_activity["date"] = daily_activity["Last Visit Time"].dt.date

    daily_counts = daily_activity["date"].value_counts().sort_index()

    if not daily_counts.empty:
        fig2, ax2 = plt.subplots()
        daily_counts.plot(kind="line", marker="o", ax=ax2)
        ax2.set_ylabel("Number of Visits")
        ax2.set_xlabel("Date")
        st.pyplot(fig2)
    else:
        st.info("No valid timestamps available.")
else:
    st.warning("Last Visit Time column missing.")

# -----------------------------
# Section 3 — Downloads Analysis
# -----------------------------
st.header(" Downloaded Files Analysis")

if "Size (Bytes)" in downloads_df.columns:
    downloads_df["Size (Bytes)"] = pd.to_numeric(downloads_df["Size (Bytes)"], errors="coerce")
    large_downloads = downloads_df.sort_values(by="Size (Bytes)", ascending=False).head(10)

    st.subheader("Top 10 Largest Downloads")
    st.dataframe(large_downloads)
else:
    st.warning("Size (Bytes) column missing in downloads data.")

# -----------------------------
# Section 4 — Suspicious Activity Summary
# -----------------------------
st.header(" Suspicious Activity Summary")

risk_score = 0

# Late Night Browsing
if "Last Visit Time" in history_df.columns:
    late_night = history_df["Last Visit Time"].dropna()
    late_night = pd.to_datetime(late_night, errors="coerce")
    late_night_count = late_night[late_night.dt.hour.isin(range(0,5))].count()
    st.write(f" Late Night Activity Count: {late_night_count}")
    if late_night_count > 20:
        risk_score += 1

# Rare Domains
if "domain" in history_df.columns:
    rare_domains = history_df["domain"].value_counts()
    rare_count = (rare_domains == 1).sum()
    st.write(f" Rarely Visited Domains: {rare_count}")
    if rare_count > 10:
        risk_score += 1

# Large Downloads
if "Size (Bytes)" in downloads_df.columns:
    big_files = downloads_df[downloads_df["Size (Bytes)"] > 50_000_000]
    st.write(f" Large Downloads (>50MB): {len(big_files)}")
    if len(big_files) > 5:
        risk_score += 1

# Risk Level
st.subheader(" Overall Risk Score")

if risk_score == 0:
    st.success("Low Risk User Activity")
elif risk_score == 1:
    st.warning("Moderate Risk Activity Detected")
else:
    st.error("High Risk Suspicious Activity")

# -----------------------------
# Raw Data Viewer
# -----------------------------
if show_raw:
    st.header("Raw Data Preview")
    st.subheader("History Data")
    st.dataframe(history_df.head())
    st.subheader("Downloads Data")
    st.dataframe(downloads_df.head())
