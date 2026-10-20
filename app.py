import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Student Result Portal", page_icon="🎓", layout="wide")

st.title("🎓 Student Result & Marks Sheet Portal")
st.write("Upload a CSV/Excel file or use sample data to calculate total, percentage, grade, and rank.")

# Sample Data
sample_data = {
    "Roll No": [101, 102, 103, 104, 105],
    "Student Name": ["Aarav Sharma", "Priya Singh", "Rohan Verma", "Ananya Patel", "Kabir Mehta"],
    "Maths": [85, 42, 95, 68, 30],
    "Science": [90, 55, 88, 72, 45],
    "English": [88, 60, 92, 65, 50]
}

# Sidebar for Options
st.sidebar.header("Options")
use_sample = st.sidebar.checkbox("Use Sample Data", value=True)
uploaded_file = st.sidebar.file_uploader("Or Upload your own CSV/Excel file", type=["csv", "xlsx"])

df = None

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
elif use_sample:
    df = pd.DataFrame(sample_data)

if df is not None:
    # Key subject columns for calculation
    subject_cols = [col for col in df.columns if col not in ["Roll No", "Student Name"]]
    
    # Formula Calculations
    df["Total Marks"] = df[subject_cols].sum(axis=1)
    max_total = len(subject_cols) * 100
    df["Percentage (%)"] = round((df["Total Marks"] / max_total) * 100, 2)
    
    # Function to assign Grade
    def get_grade(pct):
        if pct >= 85:
            return "A+"
        elif pct >= 70:
            return "A"
        elif pct >= 55:
            return "B"
        elif pct >= 40:
            return "C"
        else:
            return "F (Fail)"

    df["Grade"] = df["Percentage (%)"].apply(get_grade)
    
    # Rank Calculation
    df["Rank"] = df["Total Marks"].rank(ascending=False, method="min").astype(int)
    
    # Sort by Rank
    df = df.sort_values("Rank")

    # Metrics Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", len(df))
    col2.metric("Class Average (%)", f"{df['Percentage (%)'].mean():.2f}%")
    col3.metric("Highest Scorer", df.iloc[0]["Student Name"])
    col4.metric("Pass Percentage", f"{(len(df[df['Grade'] != 'F (Fail)']) / len(df)) * 100:.1f}%")

    st.subheader("📊 Marks Sheet Table")
    
    # Editable Table (Bonus Feature: st.data_editor)
    edited_df = st.data_editor(df, hide_index=True, use_container_width=True)

    # Download Option
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Result CSV",
        data=csv,
        file_name='student_marksheet.csv',
        mime='text/csv',
    )
else:
    st.info("Please select 'Use Sample Data' or upload a CSV file to view the marks sheet.")