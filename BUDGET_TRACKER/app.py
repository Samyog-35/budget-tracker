import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date
# set background
st.markdown("""
    <style>
    .stApp {
        background-image: url("assets/Background.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)

# file path
DATA_FILE = "data/transactions.csv"

# load data
def load_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["id", "date", "description", "amount", "category", "tags", "type"])
        df.to_csv(DATA_FILE, index=False)
        return df
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])
    return df

# save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# get next id
def get_next_id(df):
    if len(df) == 0:
        return 1
    else:
        return int(df["id"].max()) + 1

# load data
df = load_data()

# title
st.title("💰 Budget Tracker")
st.write("Track your income and expenses easily")

# add transaction
st.subheader("Add Transaction")

desc = st.text_input("Description")
amount = st.number_input("Amount", min_value=0.0)
date_input = st.date_input("Date", value=date.today())
category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Income", "Other"])
tx_type = st.radio("Type", ["expense", "income"])
tags = st.text_input("Tags")
mood = st.selectbox("Spending Mood", ["😊 Happy", "😐 Neutral", "😟 Regretful"])
if st.button("Add"):
    if desc != "":
        new_data = {
            "id": get_next_id(df),
            "date": pd.Timestamp(date_input),
            "description": desc,
            "amount": amount,
            "category": category,
            "tags": tags,
            "type": tx_type,
            "mood": mood
        }

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        save_data(df)
        st.success("Transaction added!")
    else:
        st.error("Enter description")

# filters
st.subheader("Filter Transactions")
col1, col2 = st.columns(2)

with col1:
    filter_type = st.selectbox("Filter by Type", ["All", "income", "expense"])
with col2:
    filter_category = st.selectbox("Filter by Category", ["All", "Food", "Transport", "Shopping", "Income", "Other"])

filtered_df = df.copy()

if filter_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == filter_type]

if filter_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == filter_category]


# show data
st.subheader("All Transactions")
st.dataframe(filtered_df)
# delete transaction
st.subheader("Delete Transaction")
if len(df) > 0:
    delete_id = st.selectbox("Select transaction ID to delete", df["id"].astype(int))
    if st.button("Delete"):
        df = df[df["id"] != delete_id]
        save_data(df)
        st.success("Transaction deleted!")
        st.rerun()
else:
    st.write("No transactions to delete")

# delete all
if st.button("🗑️ Delete All Transactions"):
    df = pd.DataFrame(columns=["id", "date", "description", "amount", "category", "tags", "type", "mood"])
    save_data(df)
    st.success("All transactions deleted!")
    st.rerun()

# calculations
income = df[df["type"] == "income"]["amount"].sum()
expense = df[df["type"] == "expense"]["amount"].sum()
balance = income - expense

st.write("Total Income:", income)
st.write("Total Expense:", expense)
st.write("Balance:", balance)


# chart# chart
st.subheader("Expense Chart")

expense_data = df[df["type"] == "expense"]
expense_data = df[df["type"] == "expense"]

if len(expense_data) > 0:
    chart = px.pie(expense_data, values="amount", names="category", title="Expenses by Category")
    st.plotly_chart(chart)
else:
    st.write("No expense data yet")
# mood chart
st.subheader("😊 Spending by Mood")
if len(expense_data) > 0 and "mood" in df.columns:
    mood_chart = px.bar(
        expense_data.groupby("mood")["amount"].sum().reset_index(),
        x="mood", y="amount",
        title="How Much You Spend by Mood",
        color="mood"
    )
    st.plotly_chart(mood_chart)
    # income vs expense bar chart
st.subheader("📊 Income vs Expense")
summary = pd.DataFrame({
    "Type": ["Income", "Expense"],
    "Amount": [income, expense]
})
bar_chart = px.bar(summary, x="Type", y="Amount", color="Type",
                   color_discrete_map={"Income": "green", "Expense": "red"},
                   title="Income vs Expense")
st.plotly_chart(bar_chart)
