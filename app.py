import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide"
)

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("HR_comma_sep.csv")

df = load_data()

st.title("HR Analytics Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

department = st.sidebar.multiselect(
    "Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

salary = st.sidebar.multiselect(
    "Salary Level",
    df["salary"].unique(),
    default=df["salary"].unique()
)

filtered_df = df[
    (df["Department"].isin(department))
    &
    (df["salary"].isin(salary))
]

# KPIs
total_emp = len(filtered_df)
left_emp = filtered_df["left"].sum()
retained_emp = total_emp - left_emp
attrition_rate = (left_emp / total_emp) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Employees", total_emp)
col2.metric("Employees Left", left_emp)
col3.metric("Retained", retained_emp)
col4.metric("Attrition Rate", f"{attrition_rate:.2f}%")

st.divider()

# Department-wise Attrition
st.subheader("Attrition by Department")

dept_attrition = (
    filtered_df.groupby("Department")["left"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8,4))
dept_attrition.plot(kind="bar", ax=ax)
ax.set_ylabel("Attrition Rate")
st.pyplot(fig)

# Salary Distribution
st.subheader("Salary Distribution")

salary_count = filtered_df["salary"].value_counts()

fig, ax = plt.subplots()
ax.pie(
    salary_count,
    labels=salary_count.index,
    autopct="%1.1f%%"
)
st.pyplot(fig)

# Satisfaction Analysis
st.subheader("Satisfaction Level Distribution")

fig, ax = plt.subplots()
filtered_df["satisfaction_level"].hist(
    bins=20,
    ax=ax
)
st.pyplot(fig)

# Scatter Plot
st.subheader("Satisfaction vs Evaluation")

fig, ax = plt.subplots(figsize=(8,5))

scatter = ax.scatter(
    filtered_df["satisfaction_level"],
    filtered_df["last_evaluation"],
    c=filtered_df["left"],
    alpha=0.5
)

ax.set_xlabel("Satisfaction Level")
ax.set_ylabel("Last Evaluation")

st.pyplot(fig)

# Raw Data
st.subheader("Employee Data")

st.dataframe(filtered_df)