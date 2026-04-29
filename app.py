import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

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

if st.button("Add"):
    if desc != "":
        new_data = {
            "id": get_next_id(df),
            "date": pd.Timestamp(date_input),
            "description": desc,
            "amount": amount,
            "category": category,
            "tags": tags,
            "type": tx_type
        }

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        save_data(df)
        st.success("Transaction added!")
    else:
        st.error("Enter description")

# show data
st.subheader("All Transactions")
st.dataframe(df)

# calculations
income = df[df["type"] == "income"]["amount"].sum()
expense = df[df["type"] == "expense"]["amount"].sum()
balance = income - expense

st.write("Total Income:", income)
st.write("Total Expense:", expense)
st.write("Balance:", balance)

# chart
st.subheader("Expense Chart")

expense_data = df[df["type"] == "expense"]

if len(expense_data) > 0:
    chart = px.pie(expense_data, values="amount", names="category", title="Expenses by Category")
    st.plotly_chart(chart)
else:
    st.write("No expense data yet")