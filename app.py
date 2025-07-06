
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
@st.cache_data
def load_data():
    data = [
        {"Task": "Design", "Week": "2025-07-06", "Scheduled Hours": 2.5, "Max Hours": 100.0},
        {"Task": "Design", "Week": "2025-07-13", "Scheduled Hours": 160.0, "Max Hours": 100.0},
        {"Task": "Design", "Week": "2025-07-20", "Scheduled Hours": 0.0, "Max Hours": 100.0},
        {"Task": "Design", "Week": "2025-07-27", "Scheduled Hours": 0.0, "Max Hours": 100.0},
        {"Task": "Design", "Week": "2025-08-03", "Scheduled Hours": 0.0, "Max Hours": 100.0}
    ]
    df = pd.DataFrame(data)
    df["Week"] = pd.to_datetime(df["Week"])
    return df

df = load_data()
view = st.radio("Select View", ["Overall Shop Loading", "Individual Task Utilization"])

st.title("Resource Scheduling Dashboard")

if view == "Overall Shop Loading":
    summary = df.groupby("Week").agg({"Scheduled Hours": "sum", "Max Hours": "sum"}).reset_index()
    fig, ax = plt.subplots()
    ax.bar(summary["Week"].dt.strftime("%Y-%m-%d"), summary["Max Hours"], label="Max Hours", alpha=0.5)
    ax.bar(summary["Week"].dt.strftime("%Y-%m-%d"), summary["Scheduled Hours"], label="Scheduled Hours", alpha=0.9)
    ax.set_title("Overall Shop Loading")
    ax.set_ylabel("Hours")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    task_list = df["Task"].unique()
    selected_task = st.selectbox("Select a Task", task_list)
    task_df = df[df["Task"] == selected_task]
    fig, ax = plt.subplots()
    ax.bar(task_df["Week"].dt.strftime("%Y-%m-%d"), task_df["Max Hours"], label="Max Hours", alpha=0.5)
    ax.bar(task_df["Week"].dt.strftime("%Y-%m-%d"), task_df["Scheduled Hours"], label="Scheduled Hours", alpha=0.9)
    ax.set_title(f"Utilization for: {selected_task}")
    ax.set_ylabel("Hours")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)
