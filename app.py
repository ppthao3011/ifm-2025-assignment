import streamlit as st
import base64
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from theory_page import show_theory_page
from main_story_page import show_draft_story_page
from draft_2_page import show_draft_2_page
from cover_page import show_cover_page
from live_dashboard import show_live_dashboard
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


def gbm_monte_carlo(current_price, mu, sigma, days, num_simulations=1000):
    """
    Geometric Brownian Motion Monte Carlo simulation for price forecasting.
    
    Args:
        current_price: Current stock price
        mu: Expected return (drift)
        sigma: Volatility (annualized standard deviation)
        days: Number of days to forecast
        num_simulations: Number of Monte Carlo simulations
    
    Returns:
        tuple: (simulated_paths, percentiles_10_50_90)
    """
    dt = 1/252  # Daily time step
    paths = np.zeros((num_simulations, days + 1))
    paths[:, 0] = current_price
    
    for t in range(1, days + 1):
        z = np.random.standard_normal(num_simulations)
        paths[:, t] = paths[:, t-1] * np.exp(
            (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
        )
    
    # Calculate percentiles at final day
    final_prices = paths[:, -1]
    p10 = np.percentile(final_prices, 10)
    p50 = np.percentile(final_prices, 50)
    p90 = np.percentile(final_prices, 90)
    
    return paths, (p10, p50, p90)
total_gain_pct = (65000 - 60000)/60000 * 100

def calculate_capm_return(risk_free_rate, beta, market_risk_premium):
    """
    Calculate expected return using CAPM model.
    
    Formula: E(R) = Rf + β(Rm - Rf)
    
    Args:
        risk_free_rate: Risk-free rate (typically 10-year Treasury yield)
        beta: Stock's beta coefficient
        market_risk_premium: Expected market return - risk-free rate
    
    Returns:
        float: Expected return as a decimal
    """
    expected_return = risk_free_rate + beta * market_risk_premium
    return expected_return



def calculate_dcf_value(current_price, fcf_growth_rates, terminal_growth_rate, 
                        discount_rate, current_fcf=None):
    """
    Calculate intrinsic value using Discounted Cash Flow (DCF) method.
    
    Args:
        current_price: Current stock price
        fcf_growth_rates: List of FCF growth rates for projection years (typically 5 years)
        terminal_growth_rate: Growth rate for perpetuity (typically 2-3%)
        discount_rate: Discount rate from CAPM (expected return)
        current_fcf: Current annual FCF; if None, estimated from price
    
    Returns:
        dict: Contains intrinsic_value, upside/downside, and detailed breakdown
    """
    # Estimate current FCF if not provided (simplified: assume FCF margin of 10%)
    if current_fcf is None:
        # Using a simplified approach: estimate from earnings yield
        current_fcf = current_price * 0.10
    
    # Project FCF for next N years
    projected_fcf = []
    fcf = current_fcf
    
    for growth_rate in fcf_growth_rates:
        fcf = fcf * (1 + growth_rate)
        projected_fcf.append(fcf)
    
    # Calculate PV of projected FCF
    pv_fcf = 0
    for year, fcf_value in enumerate(projected_fcf, 1):
        pv = fcf_value / ((1 + discount_rate) ** year)
        pv_fcf += pv
    
    # Calculate terminal value
    terminal_fcf = projected_fcf[-1] * (1 + terminal_growth_rate)
    terminal_value = terminal_fcf / (discount_rate - terminal_growth_rate)
    
    # PV of terminal value
    pv_terminal = terminal_value / ((1 + discount_rate) ** len(fcf_growth_rates))
    
    # Total intrinsic value (per share)
    intrinsic_value = pv_fcf + pv_terminal
    
    # Calculate upside/downside
    upside_downside = ((intrinsic_value - current_price) / current_price) * 100
    
    return {
        'intrinsic_value': intrinsic_value,
        'current_price': current_price,
        'upside_downside_pct': upside_downside,
        'pv_fcf': pv_fcf,
        'pv_terminal': pv_terminal,
        'projected_fcf': projected_fcf
    }
    
if "page" not in st.session_state:
    st.session_state.page = "📋 Cover Page"

# Sidebar Navigation - Rounded Pill Buttons (Option 8)
create_pill_navigation()

# Apply theme CSS
apply_theme_css()

page = st.session_state.page

# Default date range parameters
days_range = 180
start_date_param = None
end_date_param = None

# Generate data with selected date range
portfolio_df = generate_portfolio_data()
historical_df = generate_historical_data(days=days_range,
                                         start_date=start_date_param,
                                         end_date=end_date_param)

# Generate extended historical data for use throughout pages
tickers = [stock['ticker'] for stock in PORTFOLIO_HOLDINGS]
extended_hist = generate_historical_data(days=365, start_date=None, end_date=None)

if page == "📋 Cover Page":
    show_cover_page()

# Route to appropriate page
if page == "📊 Main Story":
    
    # Main title
    st.title("📊 My Investment Journey: A Stock Portfolio Story")
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; font-size:12px; color:gray;'>( Bài viết này được lấy ý tưởng dựa trên cuốn sách Kế Toán Vỉa Hè.)</p>",
        unsafe_allow_html=True
    )
    st.write("")



    # Mở file ảnh đã upload
    with open("meo.png", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style="width:1100px; height:200px; position:relative; background:transparent; overflow:hidden;">
        <img src="data:image/png;base64,{b64}" style="
            position:absolute;
            width:200px;
            top:30px;
            left:600px;
            animation: run 6s linear infinite;">
    </div>

    <style>
    @keyframes run {{
      0% {{ left: 1100px; }}
      100% {{ left: -400px; }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Story Introduction
    st.markdown("# Chapter 1: The Beginning")
    
    # Dynamic time period text
    time_text = {
        "1 Month": "a month ago",
        "3 Months": "three months ago",
        "6 Months": "six months ago",
        "1 Year": "a year ago",
        "2 Years": "two years ago",
        "Custom Range": f"{days_range} days ago"
    }
    time_period_text = time_text.get(date_preset, "some time ago")
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <p style='font-size:18px;'>
        Đây là Nguyễn Văn Mười, một cậu bé hiếu động, luôn tò mò về mọi thứ xung quanh.
        Mười đang học đại học, ngày nào cũng cắp sách đến lớp, nhưng trong lòng luôn nhảy múa
        những ý tưởng về cách làm sao để tiền “làm việc” cho mình thay vì chỉ ngồi yên trong ví.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.pinimg.com/736x/2c/b5/d6/2cb5d6ebe6fbc60da58b140f8f50c6ff.jpg" width="400">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("")
    

    st.markdown(
        """
        <p style='font-size:18px;'>
        Mười thích thử những thứ mới, đôi khi vẽ ra những bảng số to đùng, đôi khi cầm điện thoại theo dõi cổ phiếu, vừa học vừa vui, vừa tò mò như một nhà thám hiểm nhỏ bé trong thế giới tài chính rộng lớn.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style='font-size:18px;'>
        Gần đây, Mười bắt đầu tò mò về cổ phiếu. Cậu nhìn thấy những con số nhảy múa trên màn hình điện thoại và tự hỏi: “Liệu mình có thể khiến tiền của mình tự lớn lên như vậy không nhỉ?”.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style='font-size:18px;'>
        Thế là Mười bắt đầu nghiên cứu, đọc sách, xem video, và ghi chú tất cả những gì mình học được về cách đầu tư. Cậu thích tự mình tìm hiểu, thử tính toán, và mường tượng viễn cảnh những khoản đầu tư nhỏ bé của mình sẽ “lớn lên” từng ngày. Mười biết rằng bước đi đầu tiên luôn là khó nhất, nhưng cậu tin: “Learning by doing – đầu tư càng sớm càng tốt!”.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='font-size:18px;'>
        Vì còn là “tân binh” trong thế giới cổ phiếu, Mười muốn an toàn, không dám mạo hiểm quá. Cậu bắt đầu tìm hiểu những công ty lớn, nổi tiếng và uy tín nhất trên thị trường. Vì vậy Mười đã đặt rút ra cho mình những quy tắc riêng khi chọn cổ phiếu để đầu tư như sau:
        </p>
        """,
        unsafe_allow_html=True
    )

    left, col1, col2, col3, right = st.columns([1,2,2,2,1])

    with col1:
        st.markdown("""
        <div style="background-color: #E6E6FA; padding: 10px; border-radius: 10px;">
            <h3 style="text-align: center;font-size: 23px;">1. Uy tín</h3>
            <p style="text-align: center;">Công ty có quy mô lớn, hoạt động lâu năm. </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background-color: #E6E6FA; padding: 10px; border-radius: 10px;">
            <h3 style="text-align: center;font-size: 23px;">2. Hiệu quả hoạt động</h3>
            <p style="text-align: center;">Công ty làm ăn ổn định, tăng trưởng đều. </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background-color: #E6E6FA; padding: 10px; border-radius: 10px;">
            <h3 style="text-align: center;font-size: 23px;">3. Giá stock</h3>
            <p style="text-align: center;">Phù hợp với giá trị thực của công ty, không quá “đắt đỏ. </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    st.markdown(
        """
        <p style='font-size:18px;'>
        Từ 3 quy tắc của mình, Mười bắt đầu “sàng lọc” các cổ phiếu cẩn thận. Cậu chọn những công ty đã lên sàn ít nhất 10 năm, có quy mô lớn hoặc được nhiều người biết tới, và tất nhiên là được IPO trên sàn HNX và HOSE. Mười biết rằng những công ty này thường hoạt động ổn định,nên dữ liệu về giá cổ phiếu ít bị thiếu (missing data), nhờ đó việc đánh giá giá trị thực của cổ phiếu sẽ chính xác hơn. Cậu cảm thấy như đang xếp từng mảnh ghép vào đúng chỗ, từng bước một tiến gần tới việc chọn được “viên ngọc quý” đầu tiên của mình.
        </p>
        """,
        unsafe_allow_html=True
    )


    # Portfolio Overview Metrics
    st.markdown("<h3 style='color: #FF6F61;'>📊 Qua sàng lọc, Mười thấy được:</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
            st.metric(
                label="🏢 Sàn HNX", 
                value="223 công ty IPO > 10 năm", 
                delta="Tổng 304 công ty", 
                delta_color="inverse" 
            )

    with col2:
            st.metric(
                label="🏦 Sàn HOSE", 
                value="468 công ty IPO > 10 năm", 
                delta="Tổng 721 công ty", 
                delta_color="inverse"
            )

        
    
    st.markdown("---")
    
    # Chapter 2: Performance Over Time
    st.markdown("# Chapter 2: The Growth Journey")
    st.markdown(
        """
        <p style='font-size:18px;'>
        Sau khi lọc được danh sách những công ty lớn, lâu đời và lên sàn trên HNX – HOSE đủ lâu, Mười hào hứng lắm. Nhưng rồi Mười nghĩ:
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style="text-align:center;font-size:18px ">
        “Ủa… chọn tên công ty thôi thì chưa đủ đâu.<br>
        Mình còn phải xem công ty đó có… khỏe mạnh không nữa!”
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.pinimg.com/736x/63/ab/b5/63abb588aff28905bcd20519e6cef487.jpg" width="520">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("")

    st.markdown(
        """
        <p style='font-size:18px;'>
        Giống như đi khám sức khỏe tổng quát, cổ phiếu cũng cần “khám” để biết có đáng đầu tư không. Thế là Mười bắt đầu học thêm ba “chỉ số sức khỏe” nổi tiếng:
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("### 🧠 M-score – Dò xem công ty có “nói hơi quá” không")

   
    st.markdown("""
    <p style='font-size:20px;'>

    - Có những công ty… thích “nổ”.  
    - Lợi nhuận nhìn thì đẹp, nhưng có thể bị “tô màu”.  
    - M-score giúp phát hiện rủi ro <i>thao túng báo cáo tài chính</i>.
    <br>
    Mười vừa tính vừa tưởng tượng:
    <br>
    “Nếu M-score cao quá thì khác gì khám bệnh mà bác sĩ ghi: 'Có dấu hiệu bất thường'.  
    Thôi, né cho chắc!”

    </p>
    """, unsafe_allow_html=True)

    st.markdown("### 💪 F-score – Kiểm tra độ khỏe & sức sống")
    st.markdown("""
    F-score nhìn vào:  
    - Lợi nhuận có tăng không  
    - Dòng tiền có tốt không  
    - Cơ cấu tài chính có lành mạnh không  

    Mười ghi vào sổ:

    “F-score cao nghĩa là công ty không chỉ sống… mà sống khỏe!”

    """)

    st.markdown("### 🛡️ Z-score – Xem nguy cơ phá sản")
    st.markdown("""
    - Chỉ số này dự đoán *nguy cơ công ty phá sản*.  

    Mười nghĩ:

    “Đầu tư mà công ty phá sản thì tiền mình đi bụi à…  
    Z-score phải đẹp thì mới yên tâm!”

    """)

    st.markdown("### ⚙️ Mười bắt tay đánh giá")
    st.markdown("""
    Mười lấy danh sách những công ty đã lọc, rồi:  
    1. Chạy tính *M-score*  
    2. Tính *F-score*  
    3. Tính *Z-score*  
    4. Ghi lại kết quả như khám sức khỏe tổng quát.

    Công ty nào:  
    - M-score xấu → Không chọn  
    - F-score yếu → Gạch  
    - Z-score nguy hiểm → Chạy ngay  

    Mười vừa làm vừa tự hào:

    “Đầu tư phải nghiêm túc như kiểm tra sức khỏe, mua cổ phiếu cũng phải xem công ty có khỏe hay không chứ!”

    """)
    
    # Historical Performance Chart
    try:
        if len(historical_df) > 0:
            fig_history = go.Figure()
            
            fig_history.add_trace(
                go.Scatter(x=historical_df['Date'],
                           y=historical_df['Portfolio'],
                           mode='lines',
                           name='My Portfolio',
                           line=dict(color='#00D9FF', width=3),
                           fill='tonexty',
                           fillcolor='rgba(0, 217, 255, 0.1)'))
            
            fig_history.add_trace(
                go.Scatter(x=historical_df['Date'],
                           y=historical_df['Market'],
                           mode='lines',
                           name='Market Benchmark',
                           line=dict(color='#FF6B6B', width=2, dash='dash')))
            
            fig_history.update_layout(
                title=f"Portfolio Performance vs Market ({date_preset})",
                xaxis_title="Date",
                yaxis_title="Value ($)",
                hovermode='x unified',
                height=500,
                template='plotly_dark')
            
            st.plotly_chart(fig_history, use_container_width=True)
        else:
            st.info("📊 No historical data available to display chart")
    except Exception as e:
        st.warning(f"Unable to display historical performance chart: {str(e)}")
    
    try:
        if len(historical_df) > 1:
            portfolio_return = ((historical_df['Portfolio'].iloc[-1] /
                                 historical_df['Portfolio'].iloc[0]) - 1) * 100
            market_return = (
                (historical_df['Market'].iloc[-1] / historical_df['Market'].iloc[0]) -
                1) * 100
            
            st.info(f"""
            **Key Insight:** Over the past **{date_preset.lower()}**, my portfolio has returned **N/A%** compared to 
            the market's **N/A%**, demonstrating a different risk profile in this investment approach.
            """)
        else:
            st.info("📊 Insufficient historical data to calculate returns.")
    except Exception as e:
        st.warning(f"Unable to calculate portfolio returns: {str(e)}")
    
    st.markdown("---")
    
    # Chapter 3: Asset Allocation
    st.header("Chapter 3: Diversification Strategy")
    st.markdown("""
    Diversification is the cornerstone of my strategy. By spreading investments across multiple sectors, 
    I aim to reduce risk while maintaining growth potential.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            if len(portfolio_df) > 0:
                sector_allocation = portfolio_df.groupby('sector')['current_value'].sum().reset_index()
                if len(sector_allocation) > 0:
                    fig_pie = px.pie(sector_allocation,
                                     values='current_value',
                                     names='sector',
                                     title='Portfolio Allocation by Sector',
                                     hole=0.4,
                                     color_discrete_sequence=px.colors.qualitative.Set3)
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                    fig_pie.update_layout(height=400, template='plotly_dark')
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("📊 No sector data available")
            else:
                st.info("📊 No portfolio data available")
        except Exception as e:
            st.warning(f"Unable to display sector allocation chart: {str(e)}")
    
    with col2:
        try:
            if len(portfolio_df) > 0:
                fig_bar = px.bar(portfolio_df.sort_values('current_value', ascending=False),
                                 x='ticker',
                                 y='current_value',
                                 title='Holdings by Stock',
                                 color='current_value',
                                 color_continuous_scale='Blues',
                                 labels={
                                     'current_value': 'Value ($)',
                                     'ticker': 'Stock Ticker'
                                 })
                fig_bar.update_layout(height=400, showlegend=False, template='plotly_dark')
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("📊 No holdings data available")
        except Exception as e:
            st.warning(f"Unable to display holdings chart: {str(e)}")
    
    st.markdown("---")
    
    # Chapter 3.5: Risk Metrics and Volatility Analysis
    st.header("Chapter 3.5: Understanding Risk")
    st.markdown("""
    Beyond returns, understanding risk is crucial for long-term investment success. 
    Here's a deep dive into the risk profile of this portfolio.
    """)
    
    # Calculate risk metrics with defensive checks
    try:
        if len(historical_df) > 0 and 'Portfolio' in historical_df.columns and 'Market' in historical_df.columns:
            portfolio_returns = historical_df['Portfolio'].pct_change().dropna()
            market_returns = historical_df['Market'].pct_change().dropna()
        else:
            portfolio_returns = pd.Series([])
            market_returns = pd.Series([])
    except:
        portfolio_returns = pd.Series([])
        market_returns = pd.Series([])
    
    # Check for sufficient data
    if len(portfolio_returns) < 2:
        st.warning(
            "⚠️ Insufficient data for risk analysis. Please select a longer time period."
        )
        portfolio_volatility = 0.0
        market_volatility = 0.0
        sharpe_ratio = 0.0
        beta = 1.0
        max_drawdown = 0.0
        # Initialize drawdown as zeros for plotting
        try:
            hist_index = historical_df.index if hasattr(historical_df, 'index') else None
        except:
            hist_index = None
        
        drawdown = pd.Series([0.0] * len(historical_df), index=hist_index)
        cumulative_returns = pd.Series([1.0] * len(historical_df), index=hist_index)
        rolling_vol = pd.Series([0.0] * max(1, len(historical_df) - 1))
    else:
        # Volatility (annualized standard deviation)
        portfolio_std = portfolio_returns.std()
        market_std = market_returns.std()
        portfolio_volatility = portfolio_std * np.sqrt(
            252) * 100 if portfolio_std > 0 else 0.0
        market_volatility = market_std * np.sqrt(
            252) * 100 if market_std > 0 else 0.0
    
        # Sharpe Ratio (assuming 3% risk-free rate)
        risk_free_rate = 0.03
        try:
            annualized_return = ((historical_df['Portfolio'].iloc[-1] /
                                  historical_df['Portfolio'].iloc[0])
                                 **(252 / len(portfolio_returns)) - 1)
            if portfolio_std > 0:
                sharpe_ratio = (annualized_return -
                                risk_free_rate) / (portfolio_std * np.sqrt(252))
            else:
                sharpe_ratio = 0.0
        except (ZeroDivisionError, ValueError):
            sharpe_ratio = 0.0
    
        # Beta (correlation with market)
        try:
            covariance = portfolio_returns.cov(market_returns)
            market_variance = market_returns.var()
            beta = covariance / market_variance if market_variance > 0 else 1.0
        except (ZeroDivisionError, ValueError):
            beta = 1.0
    
        # Maximum Drawdown
        try:
            cumulative_returns = (1 + portfolio_returns).cumprod()
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - running_max) / running_max
            max_drawdown = drawdown.min() * 100 if len(drawdown) > 0 else 0.0
        except (ZeroDivisionError, ValueError):
            try:
                hist_index = historical_df.index if hasattr(historical_df, 'index') else None
            except:
                hist_index = None
            
            cumulative_returns = pd.Series([1.0] * len(historical_df), index=hist_index)
            drawdown = pd.Series([0.0] * len(historical_df), index=hist_index)
            max_drawdown = 0.0
    
        # Rolling volatility for charts
        rolling_vol = portfolio_returns.rolling(
            window=30).std() * np.sqrt(252) * 100
    
    # Display risk metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Portfolio Volatility",
            "N/A %",
            help="Annualized standard deviation of returns. Lower is less risky.")
    
    with col2:
        st.metric(
            "Sharpe Ratio",
            "N/A",
            help=
            "Risk-adjusted return. Higher is better (> 1 is good, > 2 is excellent)."
        )
    
    with col3:
        st.metric(
            "Beta",
            "N/A",
            help=
            "Sensitivity to market movements. 1.0 = moves with market, > 1.0 = more volatile."
        )
    
    with col4:
        st.metric("Max Drawdown",
                  "N/A %",
                  help="Largest peak-to-trough decline. Measures worst-case loss.")
    
    # Volatility comparison chart
    if len(historical_df) > 1 and len(portfolio_returns) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                dates_subset = historical_df['Date'].iloc[1:len(rolling_vol) + 1].values if len(rolling_vol) > 0 else historical_df['Date'].iloc[1:].values
                rolling_vol_values = rolling_vol.values if hasattr(rolling_vol, 'values') else rolling_vol
                
                if len(rolling_vol_values) > 0:
                    fig_vol = go.Figure()
                    fig_vol.add_trace(
                        go.Scatter(x=dates_subset[:len(rolling_vol_values)],
                                   y=rolling_vol_values,
                                   mode='lines',
                                   name='30-Day Rolling Volatility',
                                   line=dict(color='#FF9900', width=2),
                                   fill='tonexty',
                                   fillcolor='rgba(255, 153, 0, 0.2)'))
                    
                    fig_vol.update_layout(title="Portfolio Volatility Over Time",
                                          xaxis_title="Date",
                                          yaxis_title="Annualized Volatility (%)",
                                          height=350,
                                          template='plotly_dark')
                    st.plotly_chart(fig_vol, use_container_width=True)
                else:
                    st.info("📊 No volatility data available")
            except Exception as e:
                st.warning(f"Unable to display volatility chart: {str(e)}")
        
        with col2:
            try:
                dates_subset = historical_df['Date'].iloc[1:len(drawdown) + 1].values if len(drawdown) > 0 else historical_df['Date'].iloc[1:].values
                drawdown_values = (drawdown * 100).values if hasattr(drawdown, 'values') else (drawdown * 100)
                
                if len(drawdown_values) > 0:
                    fig_dd = go.Figure()
                    fig_dd.add_trace(
                        go.Scatter(x=dates_subset[:len(drawdown_values)],
                                   y=drawdown_values,
                                   mode='lines',
                                   name='Drawdown',
                                   line=dict(color='#FF6B6B', width=2),
                                   fill='tonexty',
                                   fillcolor='rgba(255, 107, 107, 0.3)'))
                    
                    fig_dd.update_layout(title="Portfolio Drawdown",
                                         xaxis_title="Date",
                                         yaxis_title="Drawdown (%)",
                                         height=350,
                                         template='plotly_dark')
                    st.plotly_chart(fig_dd, use_container_width=True)
                else:
                    st.info("📊 No drawdown data available")
            except Exception as e:
                st.warning(f"Unable to display drawdown chart: {str(e)}")
    else:
        st.info("📊 Risk charts require at least 2 data points. Please select a longer time period.")
    
    # Risk interpretation
    st.subheader("📊 Risk Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Volatility Assessment:**")
        if portfolio_volatility < 15:
            st.success(
                f"✅ Low volatility ({portfolio_volatility:.1f}%) indicates a relatively stable portfolio with moderate price fluctuations."
            )
        elif portfolio_volatility < 25:
            st.info(
                f"📊 Moderate volatility ({portfolio_volatility:.1f}%) suggests balanced risk with room for growth."
            )
        else:
            st.warning(
                f"⚠️ High volatility ({portfolio_volatility:.1f}%) indicates significant price swings. Higher risk, higher potential reward."
            )
    
    with col2:
        st.markdown("**Sharpe Ratio Interpretation:**")
        if sharpe_ratio > 2:
            st.success(
                f"🌟 Excellent risk-adjusted returns (Sharpe: {sharpe_ratio:.2f}). You're being well compensated for the risk taken."
            )
        elif sharpe_ratio > 1:
            st.info(
                f"✅ Good risk-adjusted returns (Sharpe: {sharpe_ratio:.2f}). Portfolio is performing well relative to its risk."
            )
        elif sharpe_ratio > 0:
            st.warning(
                f"📊 Acceptable risk-adjusted returns (Sharpe: {sharpe_ratio:.2f}). Consider if the returns justify the risk."
            )
        else:
            st.error(
                f"⚠️ Poor risk-adjusted returns (Sharpe: {sharpe_ratio:.2f}). Returns may not justify the risk taken."
            )
    
    st.markdown("---")
    
    # Chapter 4: Individual Stock Performance
    st.header("Chapter 4: The Winners and Learnings")
    st.markdown("""
    Every investment tells a story. Here's how each holding has performed and what I've learned along the way.
    """)
    
    # Sort stocks by performance
    portfolio_sorted = portfolio_df.sort_values('gain_loss_pct', ascending=False)
    
    # Display stock cards
    for idx, row in portfolio_sorted.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
            with col1:
                st.subheader(f"{row['ticker']} - {row['name']}")
                st.caption(f"Sector: {row['sector']}")
    
            with col2:
                st.metric("Shares", int(row['shares']))
    
            with col3:
                st.metric("Purchase Price", f"${row['purchase_price']:.2f}")
    
            with col4:
                st.metric("Current Price", f"${row['current_price']:.2f}")
    
            with col5:
                delta_color = "normal" if row['gain_loss'] >= 0 else "inverse"
                st.metric("Gain/Loss", f"${row['gain_loss']:.2f}",
                          f"{row['gain_loss_pct']:.2f}%")
    
            # Progress bar for performance
            performance_normalized = (row['gain_loss_pct'] +
                                      50) / 100  # Normalize to 0-1 range
            performance_normalized = max(0, min(1, performance_normalized))
            st.progress(performance_normalized)
    
            st.markdown("---")
    
    # Chapter 4.5: Portfolio Optimization Insights
    st.header("Chapter 4.5: Optimization Opportunities")
    st.markdown("""
    Based on the portfolio's performance and risk profile, here are data-driven suggestions 
    to potentially improve returns while managing risk effectively.
    """)
    
    # Calculate total current portfolio value
    total_current = portfolio_df['current_value'].sum()
    
    # Calculate optimization metrics
    sector_allocation = portfolio_df.groupby('sector').agg({
        'current_value': 'sum',
        'gain_loss_pct': 'mean'
    }).reset_index()
    sector_allocation['allocation_pct'] = (
        sector_allocation['current_value'] /
        sector_allocation['current_value'].sum()) * 100
    
    # Individual stock analysis - guard against division by zero
    if portfolio_volatility > 0:
        portfolio_df['sharpe_proxy'] = portfolio_df['gain_loss_pct'] / (
            portfolio_volatility / np.sqrt(len(portfolio_df)))
    else:
        # Equal weighting when volatility is zero
        portfolio_df['sharpe_proxy'] = 1.0
    
    # Optimization suggestions
    st.subheader("🎯 Optimization Recommendations")
    
    # Sector concentration check
    max_sector_allocation = sector_allocation['allocation_pct'].max()
    dominant_sector = sector_allocation.loc[
        sector_allocation['allocation_pct'].idxmax(), 'sector']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**1. Sector Diversification**")
        if max_sector_allocation > 50:
            st.warning(f"""
            ⚠️ **High Concentration Alert**: {dominant_sector} represents {max_sector_allocation:.1f}% of your portfolio.
            
            **Recommendation**: Consider reducing exposure to limit sector-specific risk. Target: < 40% per sector.
            """)
        elif max_sector_allocation > 40:
            st.info(f"""
            📊 **Moderate Concentration**: {dominant_sector} represents {max_sector_allocation:.1f}% of your portfolio.
            
            **Suggestion**: Monitor this sector closely and consider gradual rebalancing.
            """)
        else:
            st.success(f"""
            ✅ **Well Diversified**: No single sector exceeds 40% allocation.
            
            **Current largest**: {dominant_sector} at {max_sector_allocation:.1f}%
            """)
    
    with col2:
        st.markdown("**2. Risk-Adjusted Performance**")
    
        # Find underperformers with high allocation
        underperformers = portfolio_df[portfolio_df['gain_loss_pct'] < 0].copy()
        if len(underperformers) > 0:
            total_underperformer_value = underperformers['current_value'].sum()
            underperformer_pct = (total_underperformer_value / total_current) * 100
    
            st.warning(f"""
            📉 **Underperforming Holdings**: {len(underperformers)} stocks with negative returns 
            represent {underperformer_pct:.1f}% of portfolio value.
            
            **Review needed**: Consider if these positions align with your long-term thesis.
            """)
    
            worst_performer = underperformers.nsmallest(1, 'gain_loss_pct').iloc[0]
            st.caption(
                f"Worst performer: {worst_performer['ticker']} ({worst_performer['gain_loss_pct']:.2f}%)"
            )
        else:
            st.success("""
            🌟 **All Positive**: Every position is showing gains!
            
            Continue monitoring for optimal exit points.
            """)
    
    # Rebalancing suggestions
    st.markdown("**3. Portfolio Rebalancing Suggestions**")
    
    # Calculate ideal allocation based on sharpe proxy
    total_sharpe = portfolio_df['sharpe_proxy'].sum()
    if total_sharpe > 0:
        portfolio_df['optimal_weight'] = (portfolio_df['sharpe_proxy'] /
                                          total_sharpe) * 100
        portfolio_df['current_weight'] = (portfolio_df['current_value'] /
                                          total_current) * 100
        portfolio_df['weight_diff'] = portfolio_df[
            'optimal_weight'] - portfolio_df['current_weight']
    else:
        portfolio_df['optimal_weight'] = 100 / len(portfolio_df)
        portfolio_df['current_weight'] = (portfolio_df['current_value'] /
                                          total_current) * 100
        portfolio_df['weight_diff'] = 0
    
    # Show top rebalancing opportunities
    rebalance_df = portfolio_df[[
        'ticker', 'name', 'current_weight', 'optimal_weight', 'weight_diff'
    ]].copy()
    rebalance_df = rebalance_df.sort_values('weight_diff', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Increase Allocation** (Top Opportunities):")
        increase_stocks = rebalance_df.head(3)
        for idx, row in increase_stocks.iterrows():
            if row['weight_diff'] > 2:
                st.info(f"""
                📈 **{row['ticker']}** - {row['name']}  
                Current: {row['current_weight']:.1f}% → Optimal: {row['optimal_weight']:.1f}%  
                *Suggested increase: {row['weight_diff']:.1f}%*
                """)
    
    with col2:
        st.markdown("**Decrease Allocation** (Consider Trimming):")
        decrease_stocks = rebalance_df.tail(3).iloc[::-1]
        for idx, row in decrease_stocks.iterrows():
            if row['weight_diff'] < -2:
                st.warning(f"""
                📉 **{row['ticker']}** - {row['name']}  
                Current: {row['current_weight']:.1f}% → Optimal: {row['optimal_weight']:.1f}%  
                *Suggested decrease: {abs(row['weight_diff']):.1f}%*
                """)
    
    # Visualization: Current vs Optimal Allocation
    try:
        if len(portfolio_df) > 0:
            fig_rebal = go.Figure()
            
            fig_rebal.add_trace(go.Bar(name='Current Allocation',
                                       x=portfolio_df['ticker'],
                                       y=portfolio_df['current_weight'],
                                       marker_color='lightblue'))
            fig_rebal.add_trace(go.Bar(name='Suggested Optimal',
                                       x=portfolio_df['ticker'],
                                       y=portfolio_df['optimal_weight'],
                                       marker_color='darkblue'))
            
            fig_rebal.update_layout(title='Current vs Optimal Portfolio Allocation',
                                    xaxis_title='Stock Ticker',
                                    yaxis_title='Portfolio Weight (%)',
                                    barmode='group',
                                    height=400,
                                    template='plotly_dark')
            
            st.plotly_chart(fig_rebal, use_container_width=True)
        else:
            st.info("📊 No rebalancing data available")
    except Exception as e:
        st.warning(f"Unable to display rebalancing chart: {str(e)}")
    
    st.info("""
    💡 **Note**: These optimization suggestions are based on historical performance and risk metrics. 
    They should be considered alongside your investment goals, risk tolerance, and market outlook. 
    Always conduct your own research before making investment decisions.
    """)
    
    st.markdown("---")
    
    # Chapter 4.6: GBM Monte Carlo Price Forecasting
    st.header("Chapter 4.6: Future Outlook - GBM Monte Carlo Predictions")
    st.markdown("""
    Using Geometric Brownian Motion (GBM) with Monte Carlo simulations, we forecast potential price 
    movements for each holding over different time horizons. These simulations run 1,000 scenarios based 
    on historical volatility and expected returns.
    """)
    
    # Calculate return and volatility for each stock
    try:
        forecast_horizons = {
            '1 Day': 1,
            '10 Days': 10,
            '30 Days': 30,
            '1 Year': 252
        }
        
        # Use extended_hist already defined at page start
        if extended_hist is not None and not extended_hist.empty:
            # Display GBM forecasts for each stock
            st.subheader("📈 Individual Stock Price Forecasts")
            
            for stock in PORTFOLIO_HOLDINGS:
                ticker = stock['ticker']
                current_price = portfolio_df[portfolio_df['ticker'] == ticker]['current_price'].values[0]
                
                # Calculate returns and volatility from historical data
                if isinstance(extended_hist['Close'], pd.DataFrame):
                    prices = extended_hist['Close'][ticker].dropna()
                else:
                    prices = extended_hist['Close'].dropna()
                
                if len(prices) > 1:
                    returns = prices.pct_change().dropna()
                    mu = returns.mean() * 252  # Annualized expected return
                    sigma = returns.std() * np.sqrt(252)  # Annualized volatility
                    
                    # Create expander for each stock
                    with st.expander(f"**{ticker}** - {stock['name']} (Current: $---)", 
                                    expanded=False):
                        
                        # Create columns for different time horizons
                        col1, col2, col3, col4 = st.columns(4)
                        
                        forecast_results = {}
                        for i, (horizon_name, days) in enumerate(forecast_horizons.items()):
                            # Run GBM simulation
                            paths, (p10, p50, p90) = gbm_monte_carlo(
                                current_price, mu, sigma, days, num_simulations=1000
                            )
                            forecast_results[horizon_name] = {
                                'paths': paths,
                                'p10': p10,
                                'p50': p50,
                                'p90': p90,
                                'current': current_price,
                                'days': days
                            }
                            
                            # Display metrics
                            cols = [col1, col2, col3, col4]
                            with cols[i]:
                                st.metric(
                                    horizon_name,
                                    "$---",
                                    "$---",
                                    delta_color="normal"
                                )
                                st.caption(f"Range: $--- - $---")
                        
                        try:
                            fig = go.Figure()
                            
                            one_year_result = forecast_results['1 Year']
                            paths = one_year_result['paths']
                            days = one_year_result['days']
                            
                            if paths.size > 0:
                                time_axis = np.linspace(0, days, paths.shape[1])
                                
                                p10_over_time = np.percentile(paths, 10, axis=0)
                                p50_over_time = np.percentile(paths, 50, axis=0)
                                p90_over_time = np.percentile(paths, 90, axis=0)
                                
                                sample_indices = np.random.choice(paths.shape[0], min(20, paths.shape[0]), replace=False)
                                for idx in sample_indices:
                                    fig.add_trace(go.Scatter(
                                        x=time_axis,
                                        y=paths[idx],
                                        mode='lines',
                                        line=dict(width=0.5, color='rgba(100, 150, 255, 0.1)'),
                                        hoverinfo='skip',
                                        showlegend=False
                                    ))
                                
                                fig.add_trace(go.Scatter(
                                    x=time_axis,
                                    y=p90_over_time,
                                    mode='lines',
                                    name='90th Percentile',
                                    line=dict(color='#00FF00', width=2, dash='dash')
                                ))
                                
                                fig.add_trace(go.Scatter(
                                    x=time_axis,
                                    y=p50_over_time,
                                    mode='lines',
                                    name='Median (50th)',
                                    line=dict(color='#FFD700', width=3)
                                ))
                                
                                fig.add_trace(go.Scatter(
                                    x=time_axis,
                                    y=p10_over_time,
                                    mode='lines',
                                    name='10th Percentile',
                                    line=dict(color='#FF6B6B', width=2, dash='dash')
                                ))
                                
                                fig.add_trace(go.Scatter(
                                    x=np.concatenate([time_axis, time_axis[::-1]]),
                                    y=np.concatenate([p90_over_time, p10_over_time[::-1]]),
                                    fill='toself',
                                    fillcolor='rgba(100, 150, 255, 0.2)',
                                    line=dict(color='rgba(255,255,255,0)'),
                                    name='80% Confidence Interval',
                                    hoverinfo='skip'
                                ))
                                
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("📊 No forecast data available")
                        except Exception as e:
                            st.warning(f"Unable to display GBM chart: {str(e)}")
                        
                        # Summary interpretation
                        st.markdown(f"""
                        **Forecast Summary:**
                        - **Current Price**: $---
                        - **Expected Return (μ)**: ---% annually
                        - **Volatility (σ)**: ---% annually
                        - **1-Year Median Forecast**: $---
                        - **Likely Range (10-90%)**: $--- - $---
                        
                        *These forecasts are probabilistic and based on historical patterns. 
                        Actual results may differ significantly.*
                        """)
            
            st.info("""
            💡 **GBM Methodology**: The Geometric Brownian Motion model assumes:
            - Log-normal distribution of returns
            - Constant volatility and drift
            - No transaction costs or dividends
            - Market efficiency
            
            Use these forecasts as one input among many for investment decisions.
            """)
        else:
            st.warning("Insufficient historical data to run GBM Monte Carlo forecasts.")
            
    except Exception as e:
        st.warning(f"Unable to generate GBM forecasts: {str(e)}")
    
    st.markdown("---")
    
    # Chapter 4.7: CAPM and DCF Valuation Analysis
    st.header("Chapter 4.7: Fundamental Analysis - CAPM & DCF Valuation")
    st.markdown("""
    Using the Capital Asset Pricing Model (CAPM) and Discounted Cash Flow (DCF) analysis, 
    we calculate the fair intrinsic value of each stock based on risk-adjusted returns and 
    projected cash flows.
    """)
    
    try:
        # Market parameters
        risk_free_rate = 0.045  # Current 10-year Treasury yield (4.5%)
        market_risk_premium = 0.06  # Historical average (6%)
        terminal_growth_rate = 0.025  # Long-term GDP growth (2.5%)
        
        st.subheader("💰 Individual Stock Valuation Analysis")
        
        for stock in PORTFOLIO_HOLDINGS:
            ticker = stock['ticker']
            current_price = portfolio_df[portfolio_df['ticker'] == ticker]['current_price'].values[0]
            
            # Get historical data for beta calculation
            if isinstance(extended_hist['Close'], pd.DataFrame):
                stock_prices = extended_hist['Close'][ticker].dropna()
            else:
                stock_prices = extended_hist['Close'].dropna()
            
            if len(stock_prices) > 60:
                # Calculate beta
                stock_returns = stock_prices.pct_change().dropna()
                
                # Generate example market returns (SPY proxy)
                np.random.seed(hash(ticker) % 2**32)
                spy_returns = pd.Series(
                    np.random.normal(0.0008, 0.015, len(stock_returns)),
                    index=stock_returns.index
                )
                
                if len(stock_returns) > 0:
                    covariance = stock_returns.cov(spy_returns)
                    market_variance = spy_returns.var()
                    beta = covariance / market_variance if market_variance > 0 else 1.0
                else:
                    beta = 1.0
                
                # Calculate CAPM expected return
                capm_return = calculate_capm_return(risk_free_rate, beta, market_risk_premium)
                
                # Estimate FCF growth rates (conservative: declining growth)
                fcf_growth_rates = [0.12, 0.10, 0.08, 0.06, 0.04]  # 5-year projection
                
                # Calculate DCF intrinsic value
                dcf_result = calculate_dcf_value(
                    current_price, 
                    fcf_growth_rates,
                    terminal_growth_rate,
                    capm_return
                )
                
                # Create expander for each stock
                with st.expander(f"**{ticker}** - {stock['name']}", expanded=False):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Current Price",
                            "$---"
                        )
                    
                    with col2:
                        st.metric(
                            "Intrinsic Value (DCF)",
                            "$---",
                            "N/A %",
                            delta_color="normal"
                        )
                    
                    with col3:
                        st.metric(
                            "Beta",
                            "N/A",
                            help="Stock's volatility vs market"
                        )
                    
                    with col4:
                        st.metric(
                            "Expected Return (CAPM)",
                            "N/A %",
                            help="Risk-adjusted expected annual return"
                        )
                    
                    # CAPM Breakdown
                    st.subheader("📊 CAPM Analysis")
                    capm_col1, capm_col2, capm_col3 = st.columns(3)
                    
                    with capm_col1:
                        st.markdown(f"""
                        **Risk-Free Rate (Rf)**  
                        N/A %
                        
                        *(10-year Treasury)*
                        """)
                    
                    with capm_col2:
                        st.markdown(f"""
                        **Beta (β)**  
                        N/A
                        
                        *(Market sensitivity)*
                        """)
                    
                    with capm_col3:
                        st.markdown(f"""
                        **Market Risk Premium**  
                        N/A %
                        
                        *(Rm - Rf)*
                        """)
                    
                    st.info(f"""
                    **CAPM Formula**: E(R) = Rf + β(Rm - Rf)  
                    **Calculation**: N/A % + N/A × N/A % = **N/A %**
                    """)
                    
                    # DCF Breakdown
                    st.subheader("💎 DCF Valuation Analysis")
                    
                    dcf_col1, dcf_col2, dcf_col3 = st.columns(3)
                    
                    with dcf_col1:
                        st.markdown(f"""
                        **PV of Projected FCF**  
                        $---
                        
                        *(5-year projection)*
                        """)
                    
                    with dcf_col2:
                        st.markdown(f"""
                        **PV of Terminal Value**  
                        $---
                        
                        *(Perpetual growth)*
                        """)
                    
                    with dcf_col3:
                        status = "⚠️ FAIRLY VALUED"
                        st.markdown(f"""
                        **Valuation Status**  
                        {status}
                        
                        *N/A % upside/downside*
                        """)
                    
                    # Projected FCF visualization
                    try:
                        if 'projected_fcf' in dcf_result and len(dcf_result['projected_fcf']) > 0:
                            fig_dcf = go.Figure()
                            
                            years = list(range(1, len(dcf_result['projected_fcf']) + 1))
                            
                            fig_dcf.add_trace(go.Bar(
                                x=years,
                                y=dcf_result['projected_fcf'],
                                name='Projected FCF',
                                marker=dict(color='#0066cc')
                            ))
                            
                            fig_dcf.update_layout(
                                title=f"{ticker} - Projected Free Cash Flows (5-Year)",
                                xaxis_title="Year",
                                yaxis_title="FCF ($)",
                                height=300,
                                template='plotly_dark'
                            )
                            
                            st.plotly_chart(fig_dcf, use_container_width=True)
                        else:
                            st.info("📊 No FCF data available")
                    except Exception as e:
                        st.warning(f"Unable to display DCF chart: {str(e)}")
                    
                    # Summary interpretation
                    upside_pct = dcf_result['upside_downside_pct']
                    if upside_pct > 20:
                        interpretation = "🚀 **Highly Undervalued** - Strong buy signal if fundamentals support growth"
                    elif upside_pct > 10:
                        interpretation = "📈 **Undervalued** - Potential value opportunity"
                    elif upside_pct > -10:
                        interpretation = "➡️ **Fairly Valued** - Market price reflects fundamentals"
                    elif upside_pct > -20:
                        interpretation = "📉 **Slightly Overvalued** - Limited upside, wait for pullback"
                    else:
                        interpretation = "⚠️ **Significantly Overvalued** - Consider reducing position"
                    
                    st.markdown(f"""
                    **Valuation Interpretation:**
                    
                    {interpretation}
                    
                    *Assumptions: Terminal growth N/A %, FCF margin N/A %, 5-year projection*
                    """)
            else:
                st.warning(f"Insufficient historical data for {ticker}")
        
        st.info("""
        💡 **Methodology Notes:**
        - **CAPM**: Estimates risk-adjusted required return based on beta and market premium
        - **DCF**: Projects 5-year cash flows with declining growth, then terminal value
        - **Assumptions**: Terminal growth (2.5%), Risk-free rate (4.5%), Market premium (6%)
        - These valuations are simplified estimates for educational purposes
        """)
        
    except Exception as e:
        st.warning(f"Unable to complete CAPM and DCF analysis: {str(e)}")
    
    st.markdown("---")
    
    # Chapter 4.8: Portfolio-Wide Analysis
    st.header("Chapter 4.8: The Big Picture - Portfolio-Wide Analysis")
    st.markdown("""
    Understanding your portfolio as a unified whole reveals diversification quality, correlation risks, 
    and valuation at the aggregate level. This section provides portfolio-level insights.
    """)
    
    try:
        tickers = [stock['ticker'] for stock in PORTFOLIO_HOLDINGS]
        
        # Calculate correlation matrix
        if isinstance(extended_hist['Close'], pd.DataFrame):
            stock_prices = extended_hist['Close'][tickers].dropna()
        else:
            stock_prices = extended_hist['Close'].to_frame().dropna()
        
        if len(stock_prices) > 30:
            # Calculate correlation
            correlation_matrix = stock_prices.pct_change().dropna().corr()
            
            # Display correlation heatmap
            st.subheader("📊 Stock Correlation Matrix")
            st.markdown("*Values close to 1 = move together, 0 = independent, -1 = opposite movements*")
            
            try:
                if correlation_matrix.size > 0:
                    fig_corr = go.Figure(data=go.Heatmap(
                        z=correlation_matrix.values,
                        x=correlation_matrix.columns,
                        y=correlation_matrix.index,
                        colorscale='RdBu',
                        zmid=0,
                        zmin=-1,
                        zmax=1,
                        colorbar=dict(title="Correlation")
                    ))
                    
                    fig_corr.update_layout(
                        title="Portfolio Correlation Matrix",
                        height=500,
                        xaxis_title="",
                        yaxis_title="",
                        template='plotly_dark'
                    )
                    
                    st.plotly_chart(fig_corr, use_container_width=True)
                else:
                    st.info("📊 No correlation data available")
            except Exception as e:
                st.warning(f"Unable to display correlation chart: {str(e)}")
            
            # Calculate diversification metrics
            st.subheader("🎯 Diversification Analysis")
            
            col1, col2, col3, col4 = st.columns(4)
            
            # Average correlation (excluding diagonal)
            corr_values = correlation_matrix.values
            np.fill_diagonal(corr_values, np.nan)
            avg_correlation = np.nanmean(corr_values)
            
            with col1:
                st.metric(
                    "Avg Correlation",
                    "N/A",
                    help="Lower is better for diversification"
                )
            
            # Number of holdings
            num_holdings = len(portfolio_df)
            with col2:
                st.metric(
                    "Number of Holdings",
                    num_holdings,
                    help="More holdings = better diversification"
                )
            
            # Herfindahl-Hirschman Index (concentration)
            portfolio_weights = portfolio_df['current_value'] / portfolio_df['current_value'].sum()
            hhi = (portfolio_weights ** 2).sum()
            
            with col3:
                hhi_pct = hhi * 100
                if hhi_pct < 15:
                    concentration = "✅ Low"
                elif hhi_pct < 25:
                    concentration = "⚠️ Moderate"
                else:
                    concentration = "❌ High"
                
                st.metric(
                    "Concentration (HHI)",
                    "N/A %",
                    "---"
                )
            
            # Effective number of holdings
            eff_holdings = 1 / hhi
            with col4:
                st.metric(
                    "Effective N Holdings",
                    "N/A",
                    help="Diversification strength"
                )
            
            # Diversification insights
            st.markdown("**Diversification Insights:**")
            
            if avg_correlation > 0.5:
                st.warning("⚠️ **High Correlation Alert** - Your holdings move together significantly. Consider adding uncorrelated assets.")
            elif avg_correlation > 0.3:
                st.info("📊 **Moderate Correlation** - Good diversification with some sector overlap.")
            else:
                st.success("✅ **Low Correlation** - Excellent diversification; holdings move independently.")
            
            if hhi_pct > 25:
                st.warning(f"⚠️ **Concentration Risk** - Top position(s) account for ---% of portfolio.")
            else:
                st.success("✅ **Well Balanced** - No single position dominates; risk is well-distributed.")
            
            # Sector diversification
            st.markdown("**Sector Concentration:**")
            sector_allocation = portfolio_df.groupby('sector')['current_value'].sum()
            sector_pct = (sector_allocation / sector_allocation.sum()) * 100
            
            try:
                if len(sector_pct) > 0:
                    fig_sector = go.Figure(data=[
                        go.Pie(
                            labels=sector_pct.index,
                            values=sector_pct.values,
                            hole=0.4,
                            marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
                        )
                    ])
                    
                    fig_sector.update_layout(
                        title="Sector Allocation",
                        height=350,
                        template='plotly_dark'
                    )
                    
                    st.plotly_chart(fig_sector, use_container_width=True)
                else:
                    st.info("📊 No sector data available")
            except Exception as e:
                st.warning(f"Unable to display sector chart: {str(e)}")
        
        # Portfolio-level valuation summary
        st.subheader("💎 Portfolio Valuation Summary")
        
        total_current_value = portfolio_df['current_value'].sum()
        total_intrinsic_value = 0
        valuation_breakdown = []
        
        try:
            for stock in PORTFOLIO_HOLDINGS:
                ticker = stock['ticker']
                current_price = portfolio_df[portfolio_df['ticker'] == ticker]['current_price'].values[0]
                shares = portfolio_df[portfolio_df['ticker'] == ticker]['shares'].values[0]
                
                # Get historical data
                if isinstance(extended_hist['Close'], pd.DataFrame):
                    stock_prices = extended_hist['Close'][ticker].dropna()
                else:
                    stock_prices = extended_hist['Close'].dropna()
                
                if len(stock_prices) > 60:
                    stock_returns = stock_prices.pct_change().dropna()
                    mu = stock_returns.mean() * 252
                    sigma = stock_returns.std() * np.sqrt(252)
                    
                    # Generate example market returns (SPY proxy)
                    np.random.seed(hash(ticker) % 2**32)
                    spy_returns = pd.Series(
                        np.random.normal(0.0008, 0.015, len(stock_returns)),
                        index=stock_returns.index
                    )
                    
                    if len(stock_returns) > 0:
                        covariance = stock_returns.cov(spy_returns)
                        market_variance = spy_returns.var()
                        beta = covariance / market_variance if market_variance > 0 else 1.0
                    else:
                        beta = 1.0
                    
                    # CAPM and DCF
                    capm_return = calculate_capm_return(0.045, beta, 0.06)
                    dcf_result = calculate_dcf_value(
                        current_price,
                        [0.12, 0.10, 0.08, 0.06, 0.04],
                        0.025,
                        capm_return
                    )
                    
                    intrinsic_value_per_share = dcf_result['intrinsic_value']
                    intrinsic_value_total = intrinsic_value_per_share * shares
                    total_intrinsic_value += intrinsic_value_total
                    
                    valuation_breakdown.append({
                        'ticker': ticker,
                        'shares': shares,
                        'current_price': current_price,
                        'intrinsic_price': intrinsic_value_per_share,
                        'current_total': current_price * shares,
                        'intrinsic_total': intrinsic_value_total,
                        'upside_downside_pct': dcf_result['upside_downside_pct']
                    })
        except:
            pass
        
        if valuation_breakdown:
            # Portfolio valuation metrics
            col1, col2, col3, col4 = st.columns(4)
            
            portfolio_upside = ((total_intrinsic_value - total_current_value) / total_current_value) * 100
            
            with col1:
                st.metric(
                    "Current Portfolio Value",
                    "$---"
                )
            
            with col2:
                st.metric(
                    "Intrinsic Value (DCF)",
                    "$---",
                    "N/A %",
                    delta_color="normal"
                )
            
            with col3:
                st.metric(
                    "Total Upside/Downside",
                    "$---",
                    help="Potential gain/loss if valuations reach intrinsic value"
                )
            
            with col4:
                if portfolio_upside > 15:
                    valuation_status = "🚀 Undervalued"
                elif portfolio_upside > 5:
                    valuation_status = "📈 Slightly Undervalued"
                elif portfolio_upside > -5:
                    valuation_status = "➡️ Fairly Valued"
                elif portfolio_upside > -15:
                    valuation_status = "📉 Slightly Overvalued"
                else:
                    valuation_status = "⚠️ Overvalued"
                
                st.metric(
                    "Valuation Status",
                    valuation_status
                )
            
            # Valuation breakdown table
            st.markdown("**Individual Stock Valuations:**")
            valuation_df = pd.DataFrame(valuation_breakdown)
            valuation_df['Current Value'] = valuation_df['current_total'].apply(lambda x: f"${x:,.0f}")
            valuation_df['Intrinsic Value'] = valuation_df['intrinsic_total'].apply(lambda x: f"${x:,.0f}")
            valuation_df['Upside %'] = valuation_df['upside_downside_pct'].apply(lambda x: f"{x:.1f}%")
            
            display_df = valuation_df[['ticker', 'shares', 'current_price', 'intrinsic_price', 'Current Value', 'Intrinsic Value', 'Upside %']]
            display_df.columns = ['Ticker', 'Shares', 'Current Price', 'Intrinsic Price', 'Current Value', 'Intrinsic Value', 'Upside/Downside %']
            
            st.dataframe(display_df, use_container_width=True)
            
            # Portfolio rebalancing recommendation based on valuations
            st.markdown("**Rebalancing Based on Valuations:**")
            
            valuation_df_sorted = valuation_df.sort_values('upside_downside_pct', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Most Undervalued (Buy Candidates):**")
                top_undervalued = valuation_df_sorted.head(3)
                for _, row in top_undervalued.iterrows():
                    if row['upside_downside_pct'] > 5:
                        st.info(f"📈 **{row['ticker']}** - {row['upside_downside_pct']:.1f}% upside")
            
            with col2:
                st.markdown("**Most Overvalued (Sell Candidates):**")
                top_overvalued = valuation_df_sorted.tail(3)
                for _, row in top_overvalued.iterrows():
                    if row['upside_downside_pct'] < -5:
                        st.warning(f"📉 **{row['ticker']}** - {row['upside_downside_pct']:.1f}% downside")
        
        st.info("""
        💡 **Portfolio Analysis Summary:**
        - **Correlation**: Shows how your stocks move together (lower = better diversification)
        - **HHI Index**: Measures concentration risk (lower = more balanced)
        - **Sector Allocation**: Ensures no sector dominance
        - **DCF Valuation**: Portfolio-wide intrinsic value based on aggregated stock valuations
        """)
        
    except Exception as e:
        st.warning(f"Unable to complete portfolio analysis: {str(e)}")
    
    st.markdown("---")
    
    # Chapter 4.9: Risk Metrics - VaR, ES, and Portfolio CAPM Expected Return
    st.header("Chapter 4.9: Advanced Risk Analysis - VaR, ES & Portfolio Expected Return")
    st.markdown("""
    Advanced risk metrics help quantify downside risk and expected returns. Value at Risk (VaR) shows 
    maximum potential loss, Expected Shortfall (ES) measures tail risk, and Portfolio CAPM calculates 
    the expected return based on the portfolio's overall risk profile.
    """)
    
    st.subheader("📊 Advanced Risk Metrics")
    st.info("🔧 **Note**: Advanced risk calculations (VaR, ES, Portfolio CAPM) interface placeholder. Data and calculations to be integrated separately.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Portfolio Beta",
            "—",
            help="Market sensitivity: >1 = more volatile, <1 = less volatile"
        )
    
    with col2:
        st.metric(
            "Expected Annual Return (CAPM)",
            "—",
            help="Risk-adjusted expected return"
        )
    
    with col3:
        st.metric(
            "VaR (95% confidence)",
            "—",
            help="Max daily loss in worst 5% of days"
        )
    
    with col4:
        st.metric(
            "Expected Shortfall (ES)",
            "—",
            help="Average loss on worst 5% of days"
        )
    
    # Risk analysis breakdown
    st.subheader("🎯 Risk Analysis Breakdown")
    
    risk_col1, risk_col2 = st.columns(2)
    
    with risk_col1:
        st.markdown("**CAPM Expected Return**")
        st.info("""
        **Formula**: E(R) = Rf + β(Rm - Rf)
        
        Components to be calculated:
        - Risk-Free Rate (Rf)
        - Portfolio Beta (β)
        - Market Risk Premium
        
        **Expected Annual Return**: *[To be calculated]*
        """)
    
    with risk_col2:
        st.markdown("**Value at Risk & Expected Shortfall**")
        st.warning("""
        **Daily Risk (at 95% confidence level):**
        - **VaR**: *[To be calculated]*
        - **ES (CVaR)**: *[To be calculated]*
        
        **Annualized Risk:**
        - **Annual VaR**: *[To be calculated]*
        - **Annual ES**: *[To be calculated]*
        """)
    
    # Risk distribution chart placeholder
    st.markdown("**Distribution of Daily Returns**")
    st.info("📈 Chart placeholder - Daily returns distribution with VaR, ES, and Mean indicators will be displayed here once data is integrated")
    
    # Scenario analysis placeholder
    st.markdown("**Risk Scenarios**")
    
    scenario_col1, scenario_col2 = st.columns(2)
    
    with scenario_col1:
        st.markdown("**One-Year Return Scenarios**")
        st.table({
            "Scenario": ["Best Case (+2σ)", "Base Case (Expected)", "Stress Case (-2σ)", "VaR Scenario", "ES Scenario"],
            "Return %": ["—", "—", "—", "—", "—"],
            "Portfolio Value": ["—", "—", "—", "—", "—"]
        })
    
    with scenario_col2:
        st.markdown("**Risk Interpretation**")
        st.markdown("""
        Portfolio risk metrics to be displayed:
        
        - **Expected Portfolio Return**: *[Calculated annually]*
        - **Portfolio Volatility**: *[Based on historical data]*
        - **Maximum Daily Loss (95% CI)**: *[VaR]*
        - **Typical Worst-Day Loss**: *[ES]*
        
        Frequency analysis:
        - Daily drops > *[VaR]* about once every 20 trading days
        - Annual volatility around *[σ]*
        """)
    
    st.markdown("---")
    
    # Chapter 5: Key Insights
    st.header("Chapter 5: Reflections and Next Steps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Top Performers")
        top_performers = portfolio_df.nlargest(
            3, 'gain_loss_pct')[['ticker', 'name', 'gain_loss_pct']]
        for idx, row in top_performers.iterrows():
            st.success(
                f"**{row['ticker']}** - {row['name']}: +{row['gain_loss_pct']:.2f}%"
            )
    
    with col2:
        st.subheader("📉 Learning Opportunities")
        bottom_performers = portfolio_df.nsmallest(
            3, 'gain_loss_pct')[['ticker', 'name', 'gain_loss_pct']]
        for idx, row in bottom_performers.iterrows():
            st.warning(
                f"**{row['ticker']}** - {row['name']}: {row['gain_loss_pct']:.2f}%"
            )
    
    st.markdown("---")
    
    # Final Summary
    st.header("The Journey Continues...")
    st.markdown(f"""
    This portfolio represents more than just numbers on a screen—it's a learning journey in financial markets. 
    With an overall return of **{total_gain_pct:.2f}%**, the experience has taught me valuable lessons about:
    
    - **Patience**: Markets fluctuate, but quality companies tend to recover and grow
    - **Diversification**: Spreading risk across sectors has helped cushion against volatility
    - **Research**: Understanding the businesses behind the stocks makes investing more meaningful
    - **Long-term thinking**: Focus on fundamentals rather than short-term price movements
    
    The journey is far from over, and I'm excited to continue learning and growing as an investor.
    """)
    
    # Footer
    st.markdown("---")
    st.caption(
        "📊 Portfolio visualization powered by example data. Interface demonstration."
    )




if page == "📖 Draft Story":
    show_draft_story_page(portfolio_df, extended_hist, PORTFOLIO_HOLDINGS)

if page == "📝 Draft 2":
    show_draft_2_page(portfolio_df, extended_hist, PORTFOLIO_HOLDINGS)

if page == "💹 LIVE Portfolio Dashboard (beta)":
    show_live_dashboard()

if page == "📚 Theory Framework":
    show_theory_page()

if page == "📚 References":
    from references_page import show_references_page
    show_references_page()
