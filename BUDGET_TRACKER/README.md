# BUDGET_TRACKER
# 💰 Budget Tracker

A personal finance tracking web app built with Python and Streamlit.

## Description
Budget Tracker is a tool to help you manage your personal finances. You can track your income and expenses, analyze your spending habits by category and mood, and monitor your personal assets and net worth — all in one place.

## How to Run

Make sure you have Python and Streamlit installed:
```bash
pip install streamlit pandas plotly
```

Then run the app:
```bash
streamlit run dist/main.py
```

## Features
- Add, edit, and delete transactions
- Filter transactions by type and category
- Track spending mood (Happy, Neutral, Regretful)
- View expenses by category (pie chart)
- View income vs expense (bar chart)
- View spending by mood (bar chart)
- Track personal assets and net worth
- Background image for a professional look

## File Structure
BUDGET_TRACKER/
├── README.md           # Project documentation
├── demo.mp4            # App demo video
├── assets/             # Background image
├── src/                # Development code
│   ├── main.py         # Development version of app
│   └── data/           # Development data files
└── dist/               # Production code (this is graded)
├── main.py         # Stable version of app
└── data/           # Stable data files
## How to Use
1. Go to **Add Transaction** tab to add income or expenses
2. Go to **Transactions** tab to view, filter, and delete transactions
3. Go to **Charts** tab to see spending analysis
4. Go to **Assets** tab to track your assets and net worth

## Future Features
- Monthly budget goals with warnings when overspending
- Export transactions to CSV download
- Search transactions by description or tag
- Line chart showing income vs expense over time
- Email alerts when budget limit is reached
- Dark/light mode toggle
- Multi-currency support
- Recurring transactions support

## AI Usage
AI was used to help debug code, suggest features, and clean up code structure.
## Sources
- Streamlit documentation: https://docs.streamlit.io
- Plotly documentation: https://plotly.com/python
- Pandas documentation: https://pandas.pydata.org
