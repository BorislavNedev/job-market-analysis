import streamlit as st
import pandas as pd
import os
import plotly.express as px

# -----------------------------
# 🗂️ Load Data
# -----------------------------
data_path = os.path.join("..", "data", "jobs_cleaned.json")
df = pd.read_json(data_path)

# -----------------------------
# 🎨 Page Config
# -----------------------------
st.set_page_config(page_title="Job Market Dashboard", layout="wide")

# -----------------------------
# 🧭 Sidebar Navigation
# -----------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Overview", "Salary Analysis", "Job Distribution"])

# -----------------------------
# 📊 Main Content
# -----------------------------
st.title("💼 Job Market Dashboard")

if section == "Overview":
    st.subheader("📍 Overview")
    st.dataframe(df.head())
    st.markdown("- Total Jobs: **{}**".format(len(df)))
    st.markdown("- Unique Companies: **{}**".format(df['Company'].nunique()))
    st.markdown("- Locations: **{}**".format(df['Location'].nunique()))

elif section == "Salary Analysis":
    st.header("💰 Salary Analysis")

    # Drop rows where both salary_min and salary_max are NaN
    salary_df = df.dropna(subset=["salary_min", "salary_max"], how='all')

    if salary_df.empty:
        st.warning("No salary data available to display.")
    else:
        # Fill missing salary_min/max with the available value
        salary_df["salary_min"] = salary_df["salary_min"].fillna(salary_df["salary_max"])
        salary_df["salary_max"] = salary_df["salary_max"].fillna(salary_df["salary_min"])
        salary_df["avg_salary"] = (salary_df["salary_min"] + salary_df["salary_max"]) / 2

        # 1. Summary statistics
        st.subheader("📊 Summary Statistics")
        st.write(salary_df[["salary_min", "salary_max", "avg_salary"]].describe().loc[["min", "mean", "max"]])

        # 2. Histogram
        st.subheader("📈 Salary Distribution")
        fig1 = px.histogram(salary_df, x="avg_salary", nbins=30,
                            title="Salary Distribution", labels={"avg_salary": "Average Salary"})
        st.plotly_chart(fig1)

        # 3. Box plot
        st.subheader("📦 Salary Range – Box Plot")
        fig2 = px.box(salary_df, y="avg_salary", points="all",
                      title="Salary Range Overview")
        st.plotly_chart(fig2)

        # 4. Salary by Location
        st.subheader("📍 Average Salary by Location (Top 10)")
        top_locations = salary_df.groupby("Location")["avg_salary"].mean().sort_values(ascending=False).head(10)
        fig3 = px.bar(top_locations, x=top_locations.values, y=top_locations.index,
                      orientation='h', labels={"x": "Average Salary", "y": "Location"},
                      title="Top 10 Locations by Average Salary")
        st.plotly_chart(fig3)

elif section == "Job Distribution":
    st.subheader("🌍 Job Distribution by Location")
    st.write("(Add location-based charts here)")

# -----------------------------
# 📌 Footer
# -----------------------------
st.markdown("---")
st.markdown("Made with ❤️ by Borislav Nedev")