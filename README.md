📌 AI-Driven Browser Artifact Forensic Analysis


🚀 Overview

This project presents an AI-driven framework designed to automate browser forensic analysis by transforming raw browser artifacts into meaningful behavioral insights. It addresses the limitations of traditional manual forensic methods, which are often time-consuming and prone to human error.

The system extracts, processes, and analyzes browser data such as history, cookies, and download records to detect suspicious user behavior using anomaly detection and behavioral analytics.


🎯 Key Features

🔍 Automated extraction of browser artifacts (history, cookies, downloads)

🧹 Data preprocessing and feature engineering

📊 Behavioral analysis using multiple anomaly indicators

⚠️ Suspicion score calculation for prioritizing risky activities

📈 Interactive dashboard using Streamlit

🧠 AI-assisted anomaly detection (rule-based + ML-supported)

📌 Visual insights: browsing activity, domain analysis, download trends


🧠 Methodology

The system follows a structured pipeline:

Data Extraction

Retrieves browser artifacts from SQLite databases

Data Preprocessing

Cleans and transforms raw data into structured format

Feature Engineering

Extracts meaningful attributes such as:

Visit frequency

Access time patterns

Domain categorization

Behavioral Analysis

Detects anomalies using:

Late-night activity

Rare domain visits

High download activity

Suspicion Score Calculation

Combines multiple indicators into a unified risk score

Visualization

Displays results through an interactive dashboard


📊 Output Visualizations

Suspicious Risk Score Distribution

Daily Browsing Activity

Top Visited Domains

Top Download Sources


🛠️ Tech Stack

Languages & Libraries:

Python

Pandas, NumPy

Scikit-learn

Tools & Frameworks:

Streamlit (Dashboard)

SQLite (Browser Data Storage)

Jupyter Notebook

VS Code

Git


📂 Project Structure

project/
│── data/
│   ├── raw_data/
│   ├── processed_data/
│
│── scripts/
│   ├── extraction.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── model.py
│   ├── scoring.py
│
│── app/
│   ├── dashboard.py
│
│── models/
│── outputs/
│── main.py


⚠️ Important Note on Dataset

"Dataset files were excluded from the repository due to security policies and potential presence of sensitive patterns (e.g., API keys)."

To run this project:

Use your own browser data (Chrome/Edge/Firefox SQLite files)
OR create a sample dataset with similar structure


▶️ How to Run

1. Clone the Repository
git clone https://github.com/your-username/project-name.git
cd project-name

2. Install Dependencies
pip install -r requirements.txt

4. Run the Application
streamlit run app/dashboard.py


📌 Applications

Digital Forensics Investigation

Cybersecurity Monitoring

Insider Threat Detection

User Behavior Analysis


📈 Results

The system successfully:

Identifies unusual browsing patterns

Detects suspicious downloads and domains

Generates interpretable risk scores

Provides clear visual insights for analysis


🚀 Future Improvements

Real-time monitoring of browser activity

Integration with threat intelligence systems

Advanced ML/DL models for anomaly detection

Multi-browser and cross-platform support


👩‍💻 Author

Akansha Srivastava


⭐ If you found this useful

Give it a ⭐ on GitHub and feel free to connect!
