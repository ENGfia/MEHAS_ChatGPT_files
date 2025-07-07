
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Resource Scheduling Dashboard with Excel Upload")

uploaded_file = st.file_uploader("Upload your scheduling Excel file", type=["xlsx"])

if uploaded_file:
    try:
        excel = pd.ExcelFile(uploaded_file)
        df = excel.parse("Week of 2025 06 29", header=2).dropna(how="all").reset_index(drop=True)

        week_headers = df.columns[5:15]
        week_dates = pd.to_datetime(df.loc[0, week_headers].values)

        df_sched = df.iloc[1::2].copy()
        df_sched["Task"] = df_sched["Task"].fillna(method="ffill")
        df_sched = df_sched[df_sched["Task"].notna()]

        records = []
        for _, row in df_sched.iterrows():
            task = row["Task"]
            max_hours = float(row["Max Hours\nAvailable"])
            for col, week in zip(week_headers, week_dates):
                scheduled = float(row[col])
                records.append({
                    "Task": task,
                    "Week": week,
                    "Scheduled Hours": scheduled,
                    "Max Hours": max_hours
                })

        df_final = pd.DataFrame(records)
        view = st.radio("Select View", ["Overall Shop Loading", "Individual Task Utilization"])

        if view == "Overall Shop Loading":
            summary = df_final.groupby("Week").agg({
                "Scheduled Hours": "sum",
                "Max Hours": "sum"
            }).reset_index()
            fig, ax = plt.subplots()
            ax.bar(summary["Week"].dt.strftime("%Y-%m-%d"), summary["Max Hours"], label="Max Hours", alpha=0.5)
            ax.bar(summary["Week"].dt.strftime("%Y-%m-%d"), summary["Scheduled Hours"], label="Scheduled Hours", alpha=0.9)
            ax.set_title("Overall Shop Loading")
            ax.set_ylabel("Hours")
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

        else:
            task_list = df_final["Task"].unique()
            selected_task = st.selectbox("Select a Task", task_list)
            task_df = df_final[df_final["Task"] == selected_task]
            fig, ax = plt.subplots()
            ax.bar(task_df["Week"].dt.strftime("%Y-%m-%d"), task_df["Max Hours"], label="Max Hours", alpha=0.5)
            ax.bar(task_df["Week"].dt.strftime("%Y-%m-%d"), task_df["Scheduled Hours"], label="Scheduled Hours", alpha=0.9)
            ax.set_title(f"Utilization for: {selected_task}")
            ax.set_ylabel("Hours")
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
