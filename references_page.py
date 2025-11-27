import streamlit as st

def show_references_page():
    st.title("📚 References & Bibliography")
    st.markdown("---")
    
    # Table of Contents in Sidebar
    with st.sidebar:
        st.markdown("### 📚 Sections")
        st.markdown("---")
        sections = [
            ("Academic Books", "#sach-dai-hoc"),
            ("Investment Books", "#sach-dau-tu"),
            ("Financial Articles", "#bai-viet-tai-chinh"),
            ("Data Sources", "#nguon-du-lieu"),
            ("Tools & Software", "#cong-cu-va-phan-mem"),
        ]
        for label, anchor in sections:
            st.markdown(f"[{label}]({anchor})")
        st.markdown("---")
    
    # Books Section
    st.header("📖 Sách Đại Học (Academic Books)", anchor="sach-dai-hoc")
    st.markdown("""
    1. **"Corporate Finance"** - Stephen A. Ross, Randolph W. Westerfield, Jeffrey F. Jaffe
       - Giáo trình chuẩn về định giá công ty, CAPM, và DCF
       - Sách gốc cho các mô hình tài chính hiện đại
    
    2. **"Equity Valuation Methods: An Overview and Comparative Analysis"** - Roger Damodaran
       - Bao quát đầy đủ các phương pháp định giá cổ phiếu
       - Giải thích chi tiết về DCF, Multiples, và các cách tiếp cận khác
    
    3. **"Advances in Financial Machine Learning"** - Marcos López de Prado
       - Ứng dụng machine learning trong phân tích tài chính
       - Hữu ích cho việc dự báo giá cổ phiếu
    
    4. **"An Introduction to Statistical Learning"** - Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani
       - Nền tảng thống kê cho các mô hình GARCH, DCC
       - Cơ bản cho tất cả phương pháp dự báo
    """)
    
    st.header("💼 Sách Đầu Tư (Investment Books)", anchor="sach-dau-tu")
    st.markdown("""
    1. **"The Intelligent Investor"** - Benjamin Graham
       - Tác phẩm kinh điển về đầu tư giá trị
       - Cảm hứng cho cách tiếp cận của Nguyễn Văn Mười
    
    2. **"One Up on Wall Street"** - Peter Lynch
       - Phương pháp phân tích công ty từ góc độ nhà đầu tư bình thường
       - Thích hợp cho newbie investors
    
    3. **"Security Analysis"** - Benjamin Graham & David L. Dodd
       - Kinh thánh về phân tích chứng khoán
       - Để hiểu sâu về F-score, Z-score, M-score
    
    4. **"The Essays of Warren Buffett"** - Warren Buffett
       - Tập hợp các bức thư gửi cổ đông
       - Chứa đựng triết lý DCF và định giá của Buffett
    """)
    
    st.header("📰 Bài Viết Tài Chính (Financial Articles)", anchor="bai-viet-tai-chinh")
    st.markdown("""
    1. **Valuation Methods:**
       - Damodaran, A. (2012). "DCF Valuation: Fundamentals and Application"
       - Fernandez, P. (2004). "Valuation Methods and Shareholder Value Creation"
    
    2. **Risk Analysis:**
       - Dowd, K. (2007). "Measuring Market Risk" (2nd edition)
       - Jorion, P. (2006). "Value at Risk: The New Benchmark for Managing Financial Risk"
    
    3. **Time Series Forecasting:**
       - Hyndman, R. J., & Athanasopoulos, G. (2021). "Forecasting: Principles and Practice" (3rd edition)
       - Tuyến tính cho các mô hình Holt-Winters
    
    4. **Volatility Modeling:**
       - Engle, R. F. (2002). "Dynamic Conditional Correlation"
       - Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity"
    """)
    
    st.header("📊 Nguồn Dữ Liệu (Data Sources)", anchor="nguon-du-lieu")
    st.markdown("""
    1. **Dữ liệu Giá Cổ Phiếu:**
       - Yahoo Finance API (yfinance)
       - Sàn HOSE & HNX Official Database
       - Công ty Cổ phần Sàn Giao dịch Chứng khoán TP. HCM (HOSE)
       - Công ty Cổ phần Sàn Giao dịch Chứng khoán Hà Nội (HNX)
    
    2. **Báo Cáo Tài Chính:**
       - Sở Giao dịch Chứng khoán TP. Hồ Chí Minh (HOSE) - https://hose.vn
       - Sở Giao dịch Chứng khoán Hà Nội (HNX) - https://hnx.vn
       - Ủy ban Chứng khoán Nhà nước (SSC) - https://www.ssc.gov.vn
    
    3. **Lãi Suất Phi Rủi Ro:**
       - World Bank Data
       - Ngân hàng Trung ương Việt Nam (SBV)
       - Lợi suất trái phiếu chính phủ Việt Nam
    """)
    
    st.header("📚 References (cập nhật)", anchor="references-capnhat")
    st.markdown("""
    **1. VaR & ES**
    - Investopedia – Value at Risk (VaR): https://www.investopedia.com/terms/v/var.asp
    - Investopedia – Expected Shortfall (ES): https://www.investopedia.com/terms/e/expected-shortfall.asp
    
    **2. F-Score (Piotroski F-Score)**
    - Investopedia – Piotroski F-Score: https://www.investopedia.com/terms/p/piotroski-f-score.asp
    
    **3. Z-Score (Altman Z-Score)**
    - Investopedia – Altman Z-Score: https://www.investopedia.com/terms/a/altmanzscore.asp
    
    **4. M-Score (Beneish M-Score)**
    - Investopedia – Beneish M-Score: https://www.investopedia.com/terms/b/beneish-m-score.asp
    - Burgess, N. (2022). Correlated Monte Carlo Simulation using Cholesky Decomposition. SSRN. https://ssrn.com/abstract=4066115
    
    **5. CAPM**
    - Investopedia – Capital Asset Pricing Model (CAPM): https://www.investopedia.com/terms/c/capm.asp
    
    **6. GBM (Geometric Brownian Motion)**
    - Investopedia – Geometric Brownian Motion: https://www.investopedia.com/terms/g/geometricbrownianmotion.asp
    - SSRN – Burgess, N. (2022). Correlated Monte Carlo Simulation using Cholesky Decomposition: https://ssrn.com/abstract=4066115
    
    **7. ARCH/GARCH & DCC**
    - Investopedia – GARCH Model: https://www.investopedia.com/terms/g/garch.asp
    - Wikipedia – ARCH: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity
    
    **8. Holt-Winters**
    - Investopedia – Holt-Winters Forecasting: https://www.investopedia.com/terms/h/holtwinters-method.asp
    
    **9. FCFE (Free Cash Flow to Equity)**
    - Investopedia – Free Cash Flow to Equity (FCFE): https://www.investopedia.com/terms/f/freecashflowtoequity.asp
    
    **10. Cholesky Decomposition**
    - Wikipedia – Cholesky Decomposition: https://en.wikipedia.org/wiki/Cholesky_decomposition
    
    **11. Dữ liệu thực tế**
    - VCI / VietCap Database – dữ liệu chứng khoán Việt Nam, giá cổ phiếu, lịch sử giao dịch, cơ sở dữ liệu tài chính: https://vietcap.vn
    - Báo cáo tài chính các công ty niêm yết trên HSX – nguồn dữ liệu gốc để tính FCFE, F-Score, Z-Score, M-Score: https://www.hsx.vn
    """)
    
   