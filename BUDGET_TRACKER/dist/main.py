# set working directory to app location
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import date

# ── Background ────────────────────────────────────────────────────────────────
img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "Background.png")
with open(img_path, "rb") as f:
    data = base64.b64encode(f.read()).decode()
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
""", unsafe_allow_html=True)

# ── File Path ─────────────────────────────────────────────────────────────────
DATA_FILE = "data/transactions.csv"
ASSETS_FILE = "data/assets.csv"

# ── Data Functions ─────────────────────────────────────────────────────────────
def load_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["id", "date", "description", "amount", "category", "tags", "type"])
        df.to_csv(DATA_FILE, index=False)
        return df
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def get_next_id(df):
    if len(df) == 0:
        return 1
    else:
        return int(df["id"].max()) + 1

# ── Load Data ─────────────────────────────────────────────────────────────────
df = load_data()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("💰 Budget Tracker")
st.write("Track your income and expenses easily")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Transaction", "📋 Transactions", "📊 Charts", "📈Assets"])

# ── Tab 1: Add Transaction ────────────────────────────────────────────────────
with tab1:
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
            st.rerun()
        else:
            st.error("Enter description")

# ── Tab 2: Transactions ───────────────────────────────────────────────────────
with tab2:
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

    st.subheader("All Transactions")
    st.dataframe(filtered_df)

    st.subheader("Delete Transaction")
    if len(df) > 0:
        delete_id = st.selectbox("Select transaction ID to delete", df["id"].astype(int))
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Delete"):
                df = df[df["id"] != delete_id]
                save_data(df)
                st.success("Transaction deleted!")
                st.rerun()
        with col2:
            if st.button("🗑️ Delete All"):
                df = pd.DataFrame(columns=["id", "date", "description", "amount", "category", "tags", "type", "mood"])
                save_data(df)
                st.success("All transactions deleted!")
                st.rerun()
    else:
        st.write("No transactions to delete")

# ── Tab 3: Charts ─────────────────────────────────────────────────────────────
with tab3:
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    balance = income - expense

    st.write("Total Income:", income)
    st.write("Total Expense:", expense)
    st.write("Balance:", balance)

    expense_data = df[df["type"] == "expense"]

    st.subheader("Expense Chart")
    if len(expense_data) > 0:
        chart = px.pie(expense_data, values="amount", names="category", title="Expenses by Category")
        st.plotly_chart(chart)
    else:
        st.write("No expense data yet")

    st.subheader("😊 Spending by Mood")
    if len(expense_data) > 0 and "mood" in df.columns:
        mood_chart = px.bar(
            expense_data.groupby("mood")["amount"].sum().reset_index(),
            x="mood", y="amount",
            title="How Much You Spend by Mood",
            color="mood"
        )
        st.plotly_chart(mood_chart)

    st.subheader("📊 Income vs Expense")
    summary = pd.DataFrame({
        "Type": ["Income", "Expense"],
        "Amount": [income, expense]
    })
    bar_chart = px.bar(summary, x="Type", y="Amount", color="Type",
                    color_discrete_map={"Income": "green", "Expense": "red"},
                    title="Income vs Expense")
    st.plotly_chart(bar_chart)

# ── Tab 4: Assets ─────────────────────────────────────────────────────────────
with tab4:
    st.subheader("🏦 My Assets")

    assets_file = "data/assets.csv"
    if os.path.exists(assets_file):
        assets_df = pd.read_csv(assets_file)
    else:
        assets_df = pd.DataFrame(columns=["name", "value", "type"])

    asset_name = st.text_input("Asset Name")
    asset_value = st.number_input("Asset Value ($)", min_value=0.0)
    asset_type = st.selectbox("Asset Type", ["Cash", "Property", "Vehicle", "Investment", "Other"])

    if st.button("Add Asset"):
        if asset_name != "":
            new_asset = {"name": asset_name, "value": asset_value, "type": asset_type}
            assets_df = pd.concat([assets_df, pd.DataFrame([new_asset])], ignore_index=True)
            assets_df.to_csv(assets_file, index=False)
            st.success("Asset added!")
        else:
            st.error("Enter asset name")

    st.dataframe(assets_df)

    st.subheader("Delete Asset")
    if len(assets_df) > 0:
        delete_asset = st.selectbox("Select asset to delete", assets_df["name"])
        if st.button("Delete Asset"):
            assets_df = assets_df[assets_df["name"] != delete_asset]
            assets_df.to_csv(assets_file, index=False)
            st.success("Asset deleted!")
            st.rerun()
    else:
        st.write("No assets to delete")

    st.subheader("📊 Net Worth Breakdown")
    if len(assets_df) > 0:
        total = assets_df["value"].sum()
        st.metric("Total Net Worth", f"${total}")
        asset_chart = px.pie(assets_df, values="value", names="name", title="Assets Breakdown")
        st.plotly_chart(asset_chart)
    else:
        st.write("No assets yet")