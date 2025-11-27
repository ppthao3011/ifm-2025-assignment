import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from theory_page import show_theory_page
from main_story_page import show_draft_story_page
from cover_page import show_cover_page
from sidebar_navigation import create_pill_navigation
from theme_config import apply_theme_css

# Page configuration
st.set_page_config(page_title="Stock Portfolio Story",
                   page_icon="📈",
                   layout="wide")

# Portfolio holdings definition
PORTFOLIO_HOLDINGS = [
    {
        "ticker": "ACB",
        "name": "Asia Commercial Bank",
        "shares": 100,
        "purchase_price": 25.00,
        "sector": "Banking"
    },
    {
        "ticker": "HPG",
        "name": "Hoa Phat Group",
        "shares": 100,
        "purchase_price": 28.00,
        "sector": "Steel"
    },
    {
        "ticker": "VNM",
        "name": "Vietnam Beverage Group",
        "shares": 100,
        "purchase_price": 59.32,
        "sector": "Beverage"
    },
    {
        "ticker": "DBD",
        "name": "Diamond Brightest",
        "shares": 100,
        "purchase_price": 25.50,
        "sector": "Retail"
    },
]


def generate_portfolio_data(date_range_days=180):
    """Generate example portfolio data with sample prices"""
    # Sample current prices
    sample_prices = {
        'ACB': 25.80,
        'HPG': 28.30,
        'VNM': 59.32,
        'DBD': 25.65
    }

    # Build portfolio dataframe
    portfolio_data = []
    for stock in PORTFOLIO_HOLDINGS:
        ticker = stock['ticker']
        current_price = sample_prices.get(ticker, stock['purchase_price'] * 1.2)

        portfolio_data.append({
            'ticker': ticker,
            'name': stock['name'],
            'shares': stock['shares'],
            'purchase_price': stock['purchase_price'],
            'current_price': current_price,
            'sector': stock['sector']
        })

    df = pd.DataFrame(portfolio_data)
    df['initial_investment'] = df['shares'] * df['purchase_price']
    df['current_value'] = df['shares'] * df['current_price']
    df['gain_loss'] = df['current_value'] - df['initial_investment']
    df['gain_loss_pct'] = (df['gain_loss'] / df['initial_investment']) * 100

    return df


def generate_historical_data(days=180, start_date=None, end_date=None):
    """Generate example historical portfolio performance data"""
    if days < 1:
        days = 1

    # Generate date range
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=days)

    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate Close prices for each stock
    sample_prices = {
        'ACB': 25.80,
        'HPG': 28.30,
        'VNM': 59.32,
        'DBD': 25.65
    }
    
    # Create Close prices DataFrame (like yfinance structure)
    close_data = {}
    for ticker, initial_price in sample_prices.items():
        np.random.seed(hash(ticker) % 2**32)
        close_data[ticker] = []
        for i in range(len(dates)):
            progress = i / len(dates) if len(dates) > 0 else 0
            price = initial_price * (1.12 + progress * 0.07 + np.sin(progress * 8) * 0.06)
            close_data[ticker].append(price)
    
    # Create Close prices DataFrame
    close_df = pd.DataFrame(close_data, index=dates)
    
    # Create main dataframe
    result_df = pd.DataFrame({
        'Date': dates,
        'Portfolio': [600000 * (1.15 + (i/len(dates)) * 0.08 + np.sin((i/len(dates)) * 6) * 0.05) for i in range(len(dates))],
        'Market': [600000 * (1.08 + (i/len(dates)) * 0.06 + np.sin((i/len(dates)) * 5) * 0.03) for i in range(len(dates))]
    })
    
    # Create a wrapper object that supports both DataFrame and Close access
    class HistoricalData:
        def __init__(self, df, close_df):
            self._df = df
            self.Close = close_df
            self.empty = df.empty
        
        def __len__(self):
            return len(self._df)
        
        def __getitem__(self, key):
            if key == 'Close':
                return self.Close
            return self._df[key]
        
        def __setitem__(self, key, value):
            self._df[key] = value
        
        def __getattr__(self, name):
            return getattr(self._df, name)
    
    return HistoricalData(result_df, close_df)


# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "📋 Cover Page"

# Sidebar Navigation - Rounded Pill Buttons
create_pill_navigation()

# Apply theme CSS
apply_theme_css()

page = st.session_state.page

# Generate data for use throughout pages
portfolio_df = generate_portfolio_data()
extended_hist = generate_historical_data(days=365, start_date=None, end_date=None)

# Route to appropriate page
if page == "📋 Cover Page":
    show_cover_page()

if page == "📖 Main Story":
    show_draft_story_page(portfolio_df, extended_hist, PORTFOLIO_HOLDINGS)

if page == "📚 Theory Framework":
    show_theory_page()

if page == "📚 References":
    from references_page import show_references_page
    show_references_page()
