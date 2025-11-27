import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import base64
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from scipy.stats import norm

# ============================================================================
# THEME CONFIG
# ============================================================================
THEMES = {
    "Default Blue": {
        "primary_color": "#667EEA",
        "secondary_color": "#764BA2",
        "accent_color": "#f093fb",
        "background_gradient": "linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 50%, #e8f1ff 100%)",
        "card_bg": "#E3F2FD",
        "card_border": "#1976D2",
        "text_color": "#333",
        "highlight_color": "#1E90FF",
        "success_color": "#4CAF50",
        "warning_color": "#FF9800",
        "info_box_bg": "#E8F4F8",
        "section_colors": {
            "box1": "#E3F2FD",
            "box2": "#F3E5F5",
            "box3": "#E8F5E9",
            "box4": "#FFF3E0"
        }
    }
}

def get_current_theme():
    if "current_theme" not in st.session_state:
        st.session_state.current_theme = "Default Blue"
    return THEMES[st.session_state.current_theme]

def apply_theme_css():
    theme = get_current_theme()
    st.markdown(f"""
    <style>
    .main {{
        background: {theme['background_gradient']};
    }}
    h1, h2, h3 {{
        color: {theme['primary_color']} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
def create_pill_navigation():
    st.sidebar.markdown("### 📖 Navigation")
    st.sidebar.markdown("---")
    
    pages = [
        {"id": "📋 Cover Page", "label": "📋 Cover Page"},
        {"id": "📚 Theory Framework", "label": "📚 Theory Framework"},
        {"id": "📖 Main Story", "label": "📖 Main Story"},
        {"id": "💹 LIVE Portfolio Dashboard (beta)", "label": "💹 LIVE Portfolio Dashboard (beta)"},
        {"id": "📚 References", "label": "📚 References"},
    ]
    
    current_page = st.session_state.page
    
    st.sidebar.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 6px !important;
        padding: 5px 8px !important;
        font-size: 5px !important;
        font-weight: 500 !important;
        border: none !important;
        margin-bottom: 1px;
        transition: all 0.3s ease !important;
        height: auto !important;
        min-height: 15px !important;
        line-height: 1.2 !important;
    }
    .stButton > button[kind="primary"] {
        background-color: #1E40AF !important;
        border-color: #1E40AF !important;
        color: white !important;
        box-shadow: 0 2px 4px rgba(30, 64, 175, 0.2) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #1E3A8A !important;
        border-color: #1E3A8A !important;
        box-shadow: 0 4px 8px rgba(30, 64, 175, 0.3) !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind="secondary"] {
        background-color: #F3F4F6 !important;
        color: #374151 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #E5E7EB !important;
        border-color: #4A90E2 !important;
        box-shadow: 0 2px 4px rgba(74, 144, 226, 0.15) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    for idx, page in enumerate(pages):
        is_active = page["id"] == current_page
        if st.sidebar.button(
            page["label"],
            key=f"nav_pill_{idx}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = page["id"]
            st.rerun()

# ============================================================================
# COVER PAGE
# ============================================================================
def show_cover_page():
    st.markdown("""
    <style>
    .cover-wrapper {
        max-width: 1300px;
        margin: 0 auto;
        padding: 80px 60px;
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 50%, #e8f1ff 100%);
        border-radius: 20px;
    }
    .hero-section {
        text-align: center;
        margin-bottom: 50px;
        animation: fadeIn 0.8s ease-in;
    }
    .hero-label {
        font-size: 13px;
        letter-spacing: 4px;
        text-transform: uppercase;
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 15px;
    }
    .hero-title {
        font-size: 72px;
        font-weight: 900;
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 20px 0;
        line-height: 1.15;
    }
    .hero-subtitle {
        font-size: 20px;
        color: #555;
        margin-top: 20px;
        font-weight: 500;
    }
    .info-card {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        padding: 35px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 35px rgba(102, 126, 234, 0.25);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.35);
    }
    .info-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.9;
        margin-bottom: 12px;
        font-weight: 700;
    }
    .info-content {
        font-size: 22px;
        font-weight: 800;
    }
    .content-section {
        background: white;
        padding: 45px;
        border-radius: 15px;
        margin-bottom: 40px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
        border-left: 5px solid;
    }
    .section-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
    }
    .team-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 20px;
        margin-bottom: 30px;
    }
    .member-card {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    .cover-footer {
        text-align: center;
        padding-top: 40px;
        border-top: 2px solid #e0e7ff;
        color: #999;
        font-size: 13px;
        letter-spacing: 1px;
    }
    button[data-testid="stButton"][key="hero_cta_btn"] {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 50%, #F093FB 100%) !important;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        padding: 32px 100px !important;
        border-radius: 25px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
    }
    button[data-testid="stButton"][key="hero_cta_btn"]:hover {
        transform: translateY(-12px) scale(1.05) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="cover-wrapper">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <div class="hero-label">📚 Assignment</div>
        <div class="hero-title">Portfolio Analysis - Góc nhìn của newbie</div>
        <div class="hero-subtitle">Phân tích danh mục đầu tư với các phương pháp định lượng</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Navigate to Main Story Card", key="card_main_story"):
            st.session_state.page = "📖 Main Story"
            st.rerun()
        st.markdown("""
        <div class="info-card" style="cursor: pointer; margin-top: -52px;">
            <div class="info-label">Nhấn vào để xem</div>
            <div class="info-content">Phân tích danh mục đầu tư</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <a href="#team-section" style="text-decoration: none; display: block;">
            <div class="info-card" style="cursor: pointer;">
                <div class="info-label">Nhấn vào để xem</div>
                <div class="info-content">Danh sách thành viên nhóm</div>
            </div>
        </a>
        """, unsafe_allow_html=True)

    intro_text = """
    <div class="content-section overview-section">
        <div class="section-title">📖 Giới thiệu bài làm</div>
        <div style="margin-top: 20px; color: #1565C0; line-height: 1.8; font-size: 18px;">
            <p>Bài tập lớn này được nhóm chung em xây dựng dưới góc nhìn của một nhân vật đại diện là Nguyễn Văn Mười, một sinh viên 20 tuổi mới chập chững học về thị trường tài chính.</p>
            <p>Vì vậy, chúng xem mở đầu từ cách chọn Portfolio thật thận trọng, những danh mục ưu tiên an toàn và một số cách đánh giá còn đơn giản, phản ánh đúng mức độ hiểu biết của một nhà đầu tư mới.</p>
            <p>Chúng em cảm ơn cô rất nhiều vì đã cho chúng em cơ hội được freestyle làm một bài tập lớn thật tuyệt như này ạ 💕</p>
        </div>
    </div>
    """
    st.markdown(intro_text, unsafe_allow_html=True)

    team_text = """
    <div class="content-section team-section" id="team-section">
        <div class="section-title">👥 Thành viên nhóm</div>
        <div class="team-grid">
            <div class="member-card">
                <span style="font-size: 20px; font-weight: bold;">Nguyễn Ngọc Bảo Anh</span><br>
                <span style="font-size: 16px; opacity: 0.85;">MSSV: 11230419</span>
            </div>
            <div class="member-card">
                <span style="font-size: 20px; font-weight: bold;">Nguyễn Bảo Ngọc</span><br>
                <span style="font-size: 16px; opacity: 0.85;">MSSV: 11230473</span>
            </div>
            <div class="member-card">
                <span style="font-size: 20px; font-weight: bold;">Phạm Phương Thảo</span><br>
                <span style="font-size: 16px; opacity: 0.85;">MSSV: 11230493</span>
            </div>
        </div>
    </div>
    """
    st.markdown(team_text, unsafe_allow_html=True)
    
    if st.button("📖 Khám phá bài phân tích ngay →", key="hero_cta_btn"):
        st.session_state.page = "📖 Main Story"
        st.rerun()

    st.markdown("""
    <div class="cover-footer">
        © 2025 • Khoa Toán kinh tế • Đại học Kinh tế Quốc dân
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# LIVE DASHBOARD
# ============================================================================
def show_live_dashboard():
    st.title("💹 LIVE Portfolio Dashboard (beta)")
    st.markdown("---")
    st.info("Dự kiến sẽ hoàn thiện khi tìm được máy chủ 24/24!")

# ============================================================================
# REFERENCES
# ============================================================================
def show_references_page():
    st.title("📚 References & Bibliography")
    st.markdown("---")
    st.markdown("""
    **1. VaR & ES** - Investopedia – Value at Risk (VaR)
    **2. F-Score** - Piotroski F-Score Analysis
    **3. Z-Score** - Altman Z-Score: https://www.investopedia.com/terms/a/altmanzscore.asp
    **4. M-Score** - Beneish M-Score
    **5. CAPM** - Capital Asset Pricing Model
    **6. GBM** - Geometric Brownian Motion
    **7. ARCH/GARCH** - Volatility Models
    **8. Holt-Winters** - Exponential Smoothing
    **9. FCFE** - Free Cash Flow to Equity
    **10. Cholesky Decomposition** - Matrix Decomposition
    **11. Data Sources** - VCI/VietCap Database, HSX Historical Data
    """)

# ============================================================================
# PORTFOLIO DATA FUNCTIONS
# ============================================================================
PORTFOLIO_HOLDINGS = [
    {"ticker": "ACB", "name": "Asia Commercial Bank", "shares": 100, "purchase_price": 25.00, "sector": "Banking"},
    {"ticker": "HPG", "name": "Hoa Phat Group", "shares": 100, "purchase_price": 28.00, "sector": "Steel"},
    {"ticker": "VNM", "name": "Vietnam Beverage Group", "shares": 100, "purchase_price": 59.32, "sector": "Beverage"},
    {"ticker": "DBD", "name": "Diamond Brightest", "shares": 100, "purchase_price": 25.50, "sector": "Retail"},
]

def generate_portfolio_data(date_range_days=180):
    sample_prices = {'ACB': 25.80, 'HPG': 28.30, 'VNM': 59.32, 'DBD': 25.65}
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
    if days < 1:
        days = 1
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=days)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    sample_prices = {'ACB': 25.80, 'HPG': 28.30, 'VNM': 59.32, 'DBD': 25.65}
    
    close_data = {}
    for ticker, initial_price in sample_prices.items():
        np.random.seed(hash(ticker) % 2**32)
        close_data[ticker] = []
        for i in range(len(dates)):
            progress = i / len(dates) if len(dates) > 0 else 0
            price = initial_price * (1.12 + progress * 0.07 + np.sin(progress * 8) * 0.06)
            close_data[ticker].append(price)
    
    close_df = pd.DataFrame(close_data, index=dates)
    result_df = pd.DataFrame({
        'Date': dates,
        'Portfolio': [600000 * (1.15 + (i/len(dates)) * 0.08 + np.sin((i/len(dates)) * 6) * 0.05) for i in range(len(dates))],
        'Market': [600000 * (1.08 + (i/len(dates)) * 0.06 + np.sin((i/len(dates)) * 5) * 0.03) for i in range(len(dates))]
    })
    
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

# ============================================================================
# MAIN APPLICATION
# ============================================================================
st.set_page_config(page_title="Stock Portfolio Story", page_icon="📈", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "📋 Cover Page"

create_pill_navigation()
apply_theme_css()

page = st.session_state.page
portfolio_df = generate_portfolio_data()
extended_hist = generate_historical_data(days=365, start_date=None, end_date=None)

if page == "📋 Cover Page":
    show_cover_page()
elif page == "📖 Main Story":
    try:
        from main_story_page import show_draft_story_page
        show_draft_story_page(portfolio_df, extended_hist, PORTFOLIO_HOLDINGS)
    except ImportError:
        st.error("Main Story module not found. Please ensure main_story_page.py is in the same directory.")
elif page == "💹 LIVE Portfolio Dashboard (beta)":
    show_live_dashboard()
elif page == "📚 Theory Framework":
    try:
        from theory_page import show_theory_page
        show_theory_page()
    except ImportError:
        st.error("Theory module not found. Please ensure theory_page.py is in the same directory.")
elif page == "📚 References":
    show_references_page()
