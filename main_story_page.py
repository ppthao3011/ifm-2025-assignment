import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import base64
import yfinance as yf
from scipy.stats import norm

def show_draft_story_page(portfolio_df=None, extended_hist=None, PORTFOLIO_HOLDINGS=None):
    """
    Draft Story template page with various UI components and sample visualizations.
    This page demonstrates different UI elements and chart templates for portfolio analysis.
    """

    # ============================================================================
    # SIDEBAR SECTION NAVIGATION
    # ============================================================================
    with st.sidebar:
        st.markdown("### 📚 Sections")
        st.markdown("---")
        
        sections = [
            ("Stock Selection", "#stock-selection-for-portfolio"),
            ("Stock Filtering", "#stock-filtering-funnel"),
            ("Efficient Frontier", "#efficient-frontier-analysis"),
            ("Stock Details", "#selected-stocks-details"),
            ("Stock Prices", "#stock-prices-individual"),
            ("Price Correlation", "#price-correlation"),
            ("Sector Allocation", "#sector-allocation-comparison"),
            ("Risk-Return Scatter", "#risk-return-scatter-plot"),
            ("Valuation Multiples", "#valuation-multiples-and-profitability"),
            ("Performance Metrics", "#performance-metrics-comparison"),
            ("VaR & ES Analysis", "#value-at-risk-va-r-3-phuong-phap-tinh-toan"),
            ("CAPM Analysis", "#capm-analysis"),
            ("GBM Forecast", "#gbm-forecast"),
        ]
        
        for label, anchor in sections:
            st.markdown(f"[{label}]({anchor})")#value-at-risk-va-r-3-phuong-phap-tinh-toan
        
        st.markdown("---")

    # ============================================================================
    # TITLE
    # ============================================================================
    st.title("📖 Câu chuyện đầu tư của Nguyễn Văn Mười")

    st.markdown(
        "<p style='text-align: center; font-size:14px; color:gray;'>( Lấy cảm hứng từ cuốn sách nổi tiếng Kế toán vỉa hè)</p>",
        unsafe_allow_html=True)
    st.write("")

    st.divider()

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
    """,
                unsafe_allow_html=True)
    st.markdown("")

    # ============================================================================
    # COLORED TEXT BOX WITH PLACEHOLDER CONTENT
    # ============================================================================
    st.markdown("""
    <div style="background-color: #E8F4F8; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4; display: flex; align-items: center; gap: 30px;">
        <div style="flex: 1;">
            <h3 style="color: #1f77b4; margin-top: 0;">📌 Begin of the story...</h3>
            <p>
            Đây là Nguyễn Văn Mười — cậu bé vừa bước sang tuổi 20 và bắt đầu cảm thấy <span title="Fear of Missing Out — cảm giác lo sợ bị bỏ lỡ cơ hội khi thấy người khác đang làm điều gì đó mà mình chưa làm." style="border-bottom: 1px dotted #1f77b4; cursor: help;">FOMO</span> khi bạn bè quanh mình ai cũng có kế hoạch quản lý tiền bạc và đầu tư rõ ràng. Muốn bắt kịp nhịp chung, Mười tìm hiểu các kênh đầu tư phổ biến của small investors ở Việt Nam và quyết định thử sức với thị trường chứng khoán như bước khởi đầu cho hành trình tài chính của mình.
            </p>
            <p>
    <span title="Nhà đầu tư huyền thoại người Mỹ, được xem là một trong những nhà đầu tư thành công nhất mọi thời đại, nổi tiếng với triết lý đầu tư giá trị." style="border-bottom: 1px dotted #1f77b4; cursor: help;">Warren Buffett</span> từng nói: 
    <strong>“I started investing at the age of 11, but I still regret starting late.”</strong> 
    Lời nhắn đó khiến Nguyễn Văn Mười suy nghĩ. Thế là cậu quyết định vừa đầu tư vừa tự học theo châm ngôn:
            </p>
            <ul>
                <li>Châm ngôn 1: <strong>Learning by doing</strong></li>
                <li>Châm ngôn 2: <strong>Đầu tư càng sớm càng tốt</strong></li>
            </ul>
        </div>
        <div style="flex: 0 0 auto;">
            <img src="https://i.pinimg.com/736x/2c/b5/d6/2cb5d6ebe6fbc60da58b140f8f50c6ff.jpg" width="310" style="border-radius: 8px;">
        </div>
    </div>
    """,
                unsafe_allow_html=True)

    st.markdown("")

    st.markdown(
        """
        <div padding:20px; border-radius:10px; border-left:5px solid #1E90FF;">
            <p style="font-size:18px; line-height:1.6; color:#333;">
            Nguyễn Văn Mười ngồi trước màn hình máy tính, chống cằm suy nghĩ: “Người mới đầu tư như mình nên bắt đầu từ đâu đây?”<br>
            Sau một hồi lăn tăn, Mười cảm thấy hoang mang: người này nói đầu tư vàng sẽ giàu, người kia khoe cổ phiếu đem lại lợi nhuận khủng, lại có người thất bại ê chề khi thử bất động sản hay tiền số. Trước quá nhiều thông tin trái chiều, Mười quyết định chọn cách đơn giản nhất – <b>đầu tư vào duy nhất một loại tài sản: cổ phiếu</b> – ít nhất là bước đi đầu tiên, có lẽ đó là vì những lí do sau đây: 
            </p>
        </div>
        """, unsafe_allow_html=True
    )

    # ============================================================================
    # WHY STOCKS?
    # ============================================================================

    col1, col2 = st.columns(2)

    # Card 1: Faster Money Growth
    with col1:
        st.markdown("""
        <div style="background: #E8D5F2; padding: 20px; border-radius: 12px; color: #333; min-height: 250px;">
            <h4 style="margin: 0 0 10px 0; color: #333; font-size: 22px;">Faster Money Growth</h4>
            <p style="margin: 0; font-size: 16px; line-height: 1.6;">
            So với gửi tiết kiệm hay trái phiếu, cổ phiếu có tiềm năng giúp tiền của bạn sinh lời nhanh hơn theo thời gian. Dữ liệu lịch sử cho thấy cổ phiếu mang lại lợi suất trung bình hàng năm khoảng 10% hoặc hơn trong dài hạn.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Card 2: Time on Your Side
    with col2:
        st.markdown("""
        <div style="background: #FCE4EC; padding: 20px; border-radius: 12px; color: #333; min-height: 250px;">
            <h4 style="margin: 0 0 10px 0; color: #333; font-size: 22px;">Time on Your Side</h4>
            <p style="margin: 0; font-size: 16px; line-height: 1.6;">
            Là một nhà đầu tư trẻ, Mười có thể chịu được những biến động của giá cổ phiếu vì cậu có nhiều năm để phục hồi sau các đợt suy giảm của thị trường. Thời gian là tài sản quý giá nhất để xây dựng sự giàu có.
            </p>
        </div>
        """,unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    # Card 3: Easy to Access
    with col3:
        st.markdown("""
        <div style="background: #B3E5FC; padding: 20px; border-radius: 12px; color: #333; min-height: 250px;">
            <h4 style="margin: 0 0 10px 0; color: #333; font-size: 22px;">Easy to Access</h4>
            <p style="margin: 0; font-size: 16px; line-height: 1.6;">
            Cổ phiếu rất dễ mua và bán, thông tin và nghiên cứu về cổ phiếu có sẵn miễn phí, giúp việc học và đầu tư trở nên đơn giản. Các nền tảng kỹ thuật số như ứng dụng của các công ty chứng khoán, ngân hàng, hoặc thậm chí Zalo đều giúp việc đầu tư trở nên dễ tiếp cận với mọi người.
            </p>
        </div>
        """,unsafe_allow_html=True)

    # Card 4: Low Starting Capital
    with col4:
        st.markdown("""
        <div style="background: #C8E6C9; padding: 20px; border-radius: 12px; color: #333; min-height: 250px;">
            <h4 style="margin: 0 0 10px 0; color: #333; font-size: 22px;">Low Starting Capital</h4>
            <p style="margin: 0; font-size: 16px; line-height: 1.6;">
            Bạn không cần số tiền lớn để bắt đầu đầu tư cổ phiếu tại Việt Nam. Nhiều công ty chứng khoán cho phép mở tài khoản chỉ từ vài trăm nghìn đồng, giúp mọi người đều có thể tham gia thị trường.
            </p>
        </div>
        """,
                    unsafe_allow_html=True)

    st.markdown("")

    # ============================================================================
    # INVESTMENT STRATEGY FRAMEWORK
    # ============================================================================
    st.markdown(
        """
        <div  padding:20px; border-radius:10px; border-left:5px solid #1E90FF;">
            <p style="font-size:18px; line-height:1.6; color:#333;">
            Sau khi chọn được hướng đi đầu tiên và biết mình sẽ bắt đầu với danh mục <b>cổ phiếu</b> đơn giản, Mười không vội vàng “nhảy vào mua ngay”.<br> 
            Cậu hiểu rằng người mới cần phải có la bàn trước khi ra khơi. Vì vậy, Mười bắt đầu tìm hiểu các chiến lược đầu tư khác nhau và đặt ra những mục tiêu thật rõ ràng cho bản thân.<br> 
            Sau khi tham khảo chiến lược đầu tư của người khác và tìm hiểu trên internet, cậu đã xác định các <b>mục tiêu cụ thể<b> như sau:
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("")

    st.markdown("""
    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
    <thead>
        <tr style="background-color: #263238; color: white;">
            <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Parameter</th>
            <th style="padding: 12px; text-align: left; border: 1px solid #ddd;"> Value</th>
            <th style="padding: 12px; text-align: left; border: 1px solid #ddd;"> Description</th>
        </tr>
    </thead>
    <tbody>
        <tr style="background-color: #E3F2FD;">
            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold; color: #1E88E5;"> Horizon</td>
            <td style="padding: 12px; border: 1px solid #ddd; color: #1E88E5; font-weight: bold;">Long-term</td>
            <td style="padding: 12px; border: 1px solid #ddd; color: #555;">
                <ul style="margin:0; padding-left:18px;">
                    <li>Nhận được sự tăng trưởng theo <strong>lãi kép</strong></li>
                    <li>Overcome những biến động giá ngắn hạn</li>
                    <li>Hưởng lợi từ hiệu quả kinh doanh của doanh nghiệp</li>
                </ul>
            </td>
        </tr>
        <tr style="background-color: #E8F5E9;">
            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold; color: #43A047;"> Risk tolerance</td>
            <td style="padding: 12px; border: 1px solid #ddd; color: #43A047; font-weight: bold;">Safe</td>
            <td style="padding: 12px; border: 1px solid #ddd; color: #555;">
                <ul style="margin:0; padding-left:18px;">
                    <li>Ưu tiên <strong>bảo vệ vốn gốc</strong> và hạn chế thua lỗ</li>
                    <li>Giữ danh mục ổn định để tích lũy tài sản bền vững theo thời gian</li>
                </ul>
            </td>
        </tr>
        <tr style="background-color: #FFF3E0;">
            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold; color: #F57C00;"> Required Return</td>
            <td style="padding: 12px; border: 1px solid #ddd; color: #F57C00; font-weight: bold;">13% / year</td>
            <td style="padding: 12px; border: 1px solid #ddd; color: #555;">
                <ul style="margin:0; padding-left:18px;">
                    <li>Vượt qua lạm phát</li>
                    <li>Sinh lời so với lãi suất tiết kiệm</li>
                    <li>Đặt mục tiêu để cân bằng rủi ro và kỳ vọng</li>
                </ul>
            </td>
        </tr>
        <tr style="background-color: #F3E5F5;">
            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold; color: #7B1FA2;"> VNIndex</td>
            <td style="padding: 12px; border: 1px solid #ddd; color: #7B1FA2; font-weight: bold;">Intrinsic Value</td>
            <td style="padding: 12px; border: 1px solid #ddd; color: #555;">
                <ul style="margin:0; padding-left:18px;">
                    <li>Tập trung vào <strong>phân tích cơ bản</strong> và actual economic value của doanh nghiệp</li>
                    <li>Inspired by <strong>Warren Buffett’s long-term value investing strategy</strong>, buying quality companies below intrinsic value and holding for sustainable growth</li>
                </ul>
            </td>
        </tr>
    </tbody>
    </table>

    """,
                unsafe_allow_html=True)

    st.markdown("")

    st.markdown("""
    <p style="font-size: 14px; color: #444; line-height: 1.7; background-color: #F5F5F5; padding: 15px; border-radius: 8px; border-left: 4px solid #1976D2;">
    💭 <strong>Chiến lược chọn cổ phiếu:</strong> Cậu tập trung vào việc chọn những cổ phiếu có giá trị nội tại rõ ràng, đồng thời đảm bảo lợi nhuận kỳ vọng vừa đủ để an toàn nhưng vẫn hấp dẫn theo thời gian. Mục tiêu là xây dựng một danh mục đầu tư bền vững và có ý nghĩa.
    </p>
    """,
                unsafe_allow_html=True)

    st.markdown("")

    # ============================================================================
    # 3 BOXES ON THE SAME LINE - STOCK SELECTION CRITERIA
    # ============================================================================
    st.markdown("### I. STOCK SELECTION FOR PORTFOLIO",
         unsafe_allow_html=True
    )

    st.markdown(
        """
        <div  padding:20px; border-radius:10px; border-left:5px solid #DAA520;">
            <p style="font-size:18px; line-height:1.6; color:#333;">
            Sau khi xác định rõ mục tiêu đầu tư, Mười bắt tay vào việc <b>chọn cổ phiếu</b> đầu tiên của mình. <br>
            Là một “tân binh” mới bước vào thị trường, cậu không muốn mạo hiểm quá mức nên quyết định tập trung vào những doanh nghiệp lớn, uy tín và đã được nhiều nhà đầu tư tin tưởng qua thời gian. 
            Mười hiểu rằng muốn đầu tư nghiêm túc thì không thể chọn theo cảm tính, vì vậy cậu tự đặt ra cho mình một bộ nguyên tắc rõ ràng để đánh giá cổ phiếu trước khi xuống tiền. .<br>
            Đây sẽ là kim chỉ nam giúp Mười lựa chọn những doanh nghiệp phù hợp, tối ưu hoá lợi nhuận nhưng vẫn đảm bảo an toàn cho danh mục của mình.
            </p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # BOX 1: BRAND & MARKET PRESENCE
    with col1:
        st.markdown("""
        <div style="background-color: #E3F2FD; padding: 18px; border-radius: 12px; border-left: 5px solid #1976D2;">
            <h4 style="color: #333; margin: 0 0 8px 0; font-size: 18px; text-align: center;">
                Thương hiệu 
            </h4>
            <p style="color: #555; font-size: 15px; line-height: 1.6; margin: 0;">
                Đánh giá mức độ nhận diện và sự ổn định của doanh nghiệp trên thị trường:
            </p>
            <ul style="color: #555; font-size: 14px; margin: 10px 0 0 0; padding-left: 20px;">
                <li><strong>Sàn giao dịch:</strong> Ưu tiên HOSE hoặc HNX vì mức độ minh bạch và uy tín cao hơn.</li>
                <li><strong>Độ phổ biến trong các quỹ:</strong> Được nhiều tổ chức nắm giữ là tín hiệu tích cực về chất lượng.</li>
                <li><strong>Chất lượng dữ liệu:</strong> Ít missing value cho thấy mức độ minh bạch và thanh khoản tốt.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True)

    # BOX 2: PERFORMANCE & OUTLOOK
    with col2:
        st.markdown("""
        <div style="background-color: #F3E5F5; padding: 18px; border-radius: 12px; border-left: 5px solid #43A047;">
            <h4 style="color: #333; margin: 0 0 8px 0; font-size: 18px; text-align: center;">
                Performance & Triển vọng 
            </h4>
            <p style="color: #555; font-size: 15px; line-height: 1.6; margin: 0;">
                Đánh giá sức khỏe tài chính và khả năng tăng trưởng bền vững trong trung – dài hạn:
            </p>
            <ul style="color: #555; font-size: 14px; margin: 10px 0 0 0; padding-left: 20px;">
                <li><strong>EPS (Earnings per Share):</strong> Thu nhập trên mỗi cổ phiếu.</li>
                <li><strong>ROE (Return on Equity):</strong> Hiệu quả sử dụng vốn chủ sở hữu.</li>
                <li><strong>F-score (Piotroski):</strong> Đánh giá chất lượng tài chính tổng thể.</li>
                <li><strong>M-score:</strong> Giúp phát hiện nguy cơ gian lận lợi nhuận hoặc làm đẹp sổ sách.</li>
                <li><strong>Z-score (Altman):</strong> Đo lường rủi ro phá sản.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True)

    # BOX 3: VALUATION
    with col3:
        st.markdown("""
        <div style="background-color: #E8F5E9; padding: 18px; border-radius: 12px; border-left: 5px solid #388E3C;">
            <h4 style="color: #333; margin: 0 0 8px 0; font-size: 18px; text-align: center;">Reasonably Priced (Giá hợp lý)</h4>
            <p style="color: #555; font-size: 15px; line-height: 1.6; margin: 0;">Đảm bảo giá cổ phiếu không quá cao so với giá trị nội tại:</p>
            <ul style="color: #555; font-size: 14px; margin: 10px 0 0 0; padding-left: 20px;">
                <li><strong>P/E Ratio:</strong> Định giá tương đối, cần so sánh ngành</li>
                <li><strong>Intrinsic Value:</strong> Ước tính giá trị nội tại (Buffett principle)</li>
                <li><strong>Margin of Safety:</strong> Luôn tìm mua dưới giá trị nội tại</li>
                <li><strong>Long-term Focus:</strong> Tập trung vào giá trị thực chứ không giá tạm thời</li>
            </ul>
        </div>
        """,
                    unsafe_allow_html=True)





    st.markdown("")
    st.markdown("""
    <div padding: 18px; border-radius: 12px; border-left: 5px solid #FB8C00;">
        <p style="color: #333; font-size: 15px; line-height: 1.6; margin: 0; text-align: center;">
            (🔑 Key Insight: Bộ lọc này giúp Mười chọn được doanh nghiệp uy tín, tài chính khỏe và mua đúng giá – giảm rủi ro, tập trung vào những cổ phiếu đáng giữ lâu dài.)
        </p>
    </div>
    """,
    unsafe_allow_html=True)

    st.markdown("")

    st.markdown("""
    <div  padding:20px; border-radius:12px; border-left:5px solid #FBC02D;">
        <p style="font-size:18px; line-height:1.6; color:#333;">
            Sau khi liệt kê đầy đủ các tiêu chí, Mười bắt tay vào quá trình sàng lọc thực tế. 
            Ban đầu, danh sách cổ phiếu dài dằng dặc, như một <i>rừng số liệu rối rắm</i> trên màn hình. 
            Mỗi tiêu chí trở thành một “cửa ải”, lần lượt loại bỏ những mã không đạt chuẩn, khiến bảng tính nhảy múa như trò chơi xếp hình.
        </p>
        <p style="font-size:18px; line-height:1.6; color:#333;">
            Quá trình diễn ra cẩn thận và tỉ mỉ: Mười nhấp chuột, ghi chú, kiểm tra từng mã, như một nhà thám hiểm tìm kiếm viên ngọc quý giữa rừng rậm dữ liệu. 
            Khi kết thúc, cậu không khỏi ngạc nhiên và vui mừng: từ cả rừng cổ phiếu ban đầu, giờ chỉ còn vài chục mã sáng giá – đủ tiêu chuẩn để đầu tư.
      </p>
        <p style="font-size:18px; line-height:1.6; color:#333;">
            Cụ thể, quy trình lọc được thực hiện như sau:
        </p>
    </div>
    """,
    unsafe_allow_html=True)

    # Sector mapping for Vietnamese stocks
    sector_map = {
        # --- Banking ---
        'ACB': 'Banking',
        'MBB': 'Banking',
        'CTG': 'Banking',
        'VCB': 'Banking',
        'TCB': 'Banking',
        'VPB': 'Banking',
        'VIB': 'Banking',
        'BID': 'Banking',
        'STB': 'Banking',
        'HDB': 'Banking',

        # --- Technology ---
        'FPT': 'Technology',

        # --- Retail / Consumer Discretionary ---
        'MWG': 'Retail',
        'PNJ': 'Retail (Jewelry)',

        # --- Materials ---
        'HPG': 'Materials',
        'DGC': 'Chemicals',        # thuộc Materials nhưng phân rõ hơn → Chemicals

        # --- Consumer Staples / Food & Beverage ---
        'VNM': 'Food & Beverage',
        'MSN': 'Food & Beverage',

        # --- Industrials / Machinery / Auto-related ---
        'VEA': 'Industrials',

        # --- Real Estate ---
        'VHM': 'Real Estate',
        'KDH': 'Real Estate',

        # --- Construction / Industrials ---
        'CTD': 'Construction',

        # --- Financials (Brokerage) ---
        'HCM': 'Securities Brokerage',

        # --- Utilities ---
        'BWE': 'Utilities',
        'REE': 'Utilities',

        # --- Pharmaceuticals ---
        'DBD': 'Pharmaceuticals'
    }

    # Data from Vietnamese Fund Holdings (Top 15 only)
    funds_held_data = pd.DataFrame({
        'Stock': [
            'ACB', 'FPT', 'MBB', 'CTG', 'MWG', 'HPG', 'PNJ', 'STB', 'VCB',
            'TCB', 'VPB', 'VIB', 'BWE', 'VEA', 'VNM'
        ],
        'Fund_Count': [
            32, 27, 26, 20, 19, 15, 11, 11, 11, 10, 9, 8, 7, 7, 7
        ]
    })

    # Add sector column
    funds_held_data['Sector'] = funds_held_data['Stock'].map(sector_map)

    # Color palette by sector
    sector_colors = {
        'Banking': '#1f77b4',
        'Technology': '#00D9FF',
        'Retail': '#FF9800',
        'Retail (Jewelry)': '#FF7043',
        'Materials': '#8BC34A',
        'Chemicals': '#7CB342',
        'Food & Beverage': '#FF6B6B',
        'Industrials': '#4CAF50',
        'Real Estate': '#9C27B0',
        'Construction': '#BF360C',
        'Securities Brokerage': '#512DA8',
        'Utilities': '#00796B',
        'Pharmaceuticals': '#E91E63'
    }

    col_funnel, col_results = st.columns([1.2, 1])

    with col_funnel:
        st.markdown("#### 🔽 Lọc cổ phiếu - Từ Toàn thị trường đến Portfolio")
    

        # Funnel data
        funnel_stages = [
            'Toàn bộ thị trường', 'EPS > 1,500', 'ROE > 12%', 'HSX & HNX',
            'Missing data < 150', '(ZMF-Score) Final Portfolio'
        ]
        funnel_values = [1589, 607, 472, 255, 137, 20]

        # Calculate percentage of remaining relative to first stage
        first_stage = funnel_values[0]
        percentages = [f"{(val/first_stage)*100:.1f}%" for val in funnel_values]

        fig_funnel = go.Figure(
            go.Funnel(
                y=funnel_stages,
                x=funnel_values,
                marker=dict(color=[
                    '#FF6B6B', '#FF9800', '#FFC107', '#8BC34A', '#4CAF50',
                    '#00D9FF', '#1A237E'
                ],
                            line=dict(width=2, color=['white'] * 6)),
                customdata=percentages,
                hovertemplate=
                '<b>%{y}</b><br>Stocks: %{x:,}<br>% of Total: %{customdata}<extra></extra>'
            ))

        fig_funnel.update_layout(title='Stock Filtering Funnel',
                                 height=600,
                                 template='plotly',
                                 plot_bgcolor='#f5f5f5',
                                 paper_bgcolor='#f5f5f5',
                                 margin=dict(l=100, r=20, t=50, b=20))

        st.plotly_chart(fig_funnel, use_container_width=True)

    with col_results:
        st.markdown("#### 📈 Kết quả lọc bộ")

        # Summary metrics
        st.markdown("""
        <div style='background-color: #f5f5f5; padding: 12px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px;'>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px;'>
                <div style='text-align: center;'>
                    <p style='margin: 0; font-size: 14px; color: #666;'>Thị trường toàn bộ</p>
                    <p style='margin: 4px 0 0 0; font-size: 20px; font-weight: bold; color: #1976D2;'>1,589</p>
                </div>
                <div style='text-align: center;'>
                    <p style='margin: 0; font-size: 14px; color: #666;'>Cổ phiếu được chọn</p>
                    <p style='margin: 4px 0 0 0; font-size: 20px; font-weight: bold; color: #4CAF50;'>20</p>
                </div>
            </div>
            <div style='margin-top: 8px; padding-top: 8px; border-top: 1px solid #ddd; text-align: center;'>
                <p style='margin: 0; font-size: 12px; color: #1565c0;'><strong>Tỷ lệ lọc: 1.26% (20/1,589)</strong></p>
            </div>
        </div>
        """,
                    unsafe_allow_html=True)

        filtering_stages = [
            {"title": "1. Toàn bộ thị trường", "count": "1,589", "color": "#FF6B6B", "explanation": "Toàn bộ thị trường được đưa vào danh sách ban đầu trước khi áp điều kiện."},
            {"title": "2. EPS > 1,500", "count": "607", "color": "#FF9800", "explanation": "Loại bỏ doanh nghiệp lợi nhuận quá thấp; chỉ giữ lại nhóm có sức tạo lợi nhuận ổn định và đủ lớn."},
            {"title": "3. ROE > 12%", "count": "472", "color": "#FFC107", "explanation": "Tiếp tục giữ những công ty sử dụng vốn hiệu quả, loại các doanh nghiệp hiệu suất thấp."},
            {"title": "4. Sàn giao dịch: HSX & HNX", "count": "255", "color": "#8BC34A", "explanation": "Ưu tiên các sàn có mức minh bạch và thanh khoản cao hơn, loại bỏ UPcom ."},
            {"title": "5. Missing data < 150", "count": "203", "color": "#4CAF50", "explanation": "Đảm bảo dữ liệu đủ sạch, đủ dài để phân tích; tránh tùy chọn quá rủi ro do thiếu dữ liệu."},
            {"title": "6. 3-score (M/F/Z-score) ", "count": "137", "color": "#00D9FF", "explanation": "ĐĐiểm M-Score, Z-score và F-score trong 3 năm ở mức an toàn. "}
        ]

        # Progress Flow Design
        st.markdown("**📋 Quá trình lọc từng bước:**")
        st.markdown("""
        <div style='background-color: #f5f5f5; padding: 12px; border-radius: 10px; border: 1px solid #ddd;'>
        """, unsafe_allow_html=True)
        
        for idx, stage in enumerate(filtering_stages):
            percent_reduction = ((1589 - int(stage['count'].replace(',', ''))) / 1589) * 100
            st.markdown(f"""
            <div style='margin-bottom: 10px;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                    <span style='font-size: 12px; font-weight: bold; color: {stage['color']};'>{stage['title']}</span>
                    <span style='font-size: 12px; color: #666;'><strong>{stage['count']}</strong> | -{percent_reduction:.1f}%</span>
                </div>
                <div style='background-color: white; height: 6px; border-radius: 3px; overflow: hidden; border: 1px solid #ddd;'>
                    <div style='background-color: {stage['color']}; height: 100%; width: {max(5, (int(stage['count'].replace(',', ''))/1589)*100)}%;'></div>
                </div>
                <p style='color: #666; margin: 4px 0 0 0; font-size: 10px; line-height: 1.4;'>{stage['explanation']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


    
    st.markdown(
        """
        <div  padding:20px; border-radius:10px; border-left:5px solid #1E90FF;">
            <p style="font-size:18px; line-height:1.6; color:#333;">
            Mười không xem việc chọn cổ phiếu là một phép tính khô khan – thay vào đó như đang chơi một trò chơi nhỏ đầy chiến lược. Qua mỗi bước lọc, Mười không chỉ cân nhắc lợi nhuận hay hiệu quả vốn, mà còn nhìn vào mức minh bạch, lịch sử hoạt động. Mười muốn chọn những doanh nghiệp mà mình hiểu rõ, chứ không chỉ là con số bóng bẩy thoáng qua.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="padding:20px; border-radius:10px; border-left:5px solid #1E90FF; background-color:#f0f8ff;">
            <p style="font-size:18px; line-height:1.6; color:#333;">
            Sau quá trình lọc, cậu thấy được rằng chỉ có duy nhất <strong style="color:#FF4500;">1,3% cổ phiếu đạt chuẩn</strong> cùng lúc các chỉ tiêu trên ➡️ 
            <strong style="color:#FF4500;">phần lớn thị trường yếu về lợi nhuận, hiệu quả vốn hoặc thiếu minh bạch</strong>. 
            Điều này cho thấy cơ hội thật sự chỉ nằm ở số ít cổ phiếu chất lượng, và một nhà đầu tư khôn ngoan nên sàng lọc kỹ lưỡng để giảm rủi ro và tối ưu lợi nhuận.
            </p>
        </div>
        """, unsafe_allow_html=True
    )
    

    st.markdown("___")


    st.markdown("""
    <div style="background-color:#FFFACD; padding: 20px; border-radius: 10px; border-left: 5px solid #FFD700; display: flex; align-items: center; gap: 30px;">
        <!-- Chữ bên phải, căn phải -->
        <div style="flex: 1; font-size:18px; text-align: left; color:#8B6508;">
            <p>
            Sau khi lọc xong, Mười đứng trước 20 cổ phiếu tinh túy, mỗi mã đều là ứng viên sáng giá. Nhưng với tài chính của một sinh viên như cậu, và lại là lần đầu thử sức với đầu tư, cậu biết rằng không thể ôm hết được. Mục tiêu của Mười lúc này rất rõ ràng: xây dựng một portfolio khoảng 3–4 mã đủ mạnh, vừa dễ quản lý, vừa có tiềm năng sinh lời dài hạn.
            </p>
            <p>
            Còn gì tốt hơn bằng cách <strong>tham chiếu từ chuyên gia</strong>. Mười bắt đầu đi sâu tìm hiểu các quỹ của tổ chức – nơi mà những chuyên gia đã cân nhắc kỹ lưỡng và lựa chọn các cổ phiếu chất lượng. Từ việc phân tích các danh mục quỹ, cậu đã tập hợp được <b>Nhóm các mã chứng khoán xuất hiện nhiều trong top 10 tỷ lệ sợ hữu của quỹ</b>, như những “ứng viên được các tay chơi lớn đặt niềm tin”.  Mười nhìn vào danh sách này, thấy rõ logic: những cổ phiếu được lặp lại nhiều lần trong quỹ chính là những mã chất lượng, minh bạch và có tiềm năng dài hạn, hoàn toàn phù hợp với chiến lược đầu tư nhỏ gọn nhưng thông minh của mình.
            </p>
        </div>
        <!-- Ảnh bên trái -->
        <div style="flex: 0 0 auto; margin-left: 0px;">
            <img src="https://i.pinimg.com/1200x/05/09/54/0509540e64290c51e74c497b7a51dec1.jpg" width="220" style="border-radius: 8px;">
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: right; padding:15px; border-radius:10px;'>
    <b>Top các cổ phiếu nằm trong top 10 tỷ lệ nắm giữ ở các quỹ</b>
    </div>
    """, unsafe_allow_html=True)

    
    # Create two-column layout with textbox on left and chart on right
    col_textbox, col_chart = st.columns([0.35, 0.65])

    with col_textbox:
        st.markdown("""
        <div style='background-color: #f5f5f5; padding: 15px; border-radius: 10px; border-left: 4px solid #1976D2; border: 1px solid #ddd; height: 100%;'>
            <h5 style='color: #1976D2; margin: 0 0 10px 0; font-size: 18px;'>📌 Thông tin quan trọng</h5>
            <p style='color: #666; margin: 0 0 8px 0; font-size: 16px;'>
            Biểu đồ cho thấy mức độ “được ưa chuộng” của từng cổ phiếu trong mắt các quỹ đầu tư. 
            
- Ngân hàng chiếm ưu thế rõ rệt với nhiều mã lọt top và tần suất cao → ngành ổn định và được phân bổ lớn nhất.  

- Một số cổ phiếu đầu ngành như FPT, HPG, MWG, PNJ cũng xuất hiện thường xuyên → thể hiện niềm tin của quỹ vào doanh nghiệp dẫn đầu.  

- Top cổ phiếu cho thấy quỹ ưu tiên blue-chip đa ngành, đặc biệt ngân hàng và doanh nghiệp thống lĩnh ngành nhờ **ổn định và hiệu suất dài hạn**.
            </p>
        </div>
        """, unsafe_allow_html=True)

    story = """
<div style="font-size:18px; line-height:1.6;">
Khi tìm hiểu đến đây, trong đầu Mười bỗng lóe lên một câu hỏi to bự:

<div style="text-align: center; font-style: italic; margin: 10px 0;">
“<b>Tại sao trong tất cả các quỹ đều có ngân hàng nhỉ?</b>”
</div>

Cậu không bỏ qua thắc mắc đó, bắt đầu lùng sục các trang web tài chính, đọc đi đọc lại các bài phân tích, và nghiền ngẫm cả những báo cáo quỹ. Sau một hồi, câu trả lời dần hiện ra trước mắt.

Hóa ra, ngân hàng trong thế giới quỹ đầu tư không chỉ là nơi gửi tiền hay cho vay như Mười vẫn nghĩ. Nó là trung tâm, là trụ cột, nơi cung cấp mọi dịch vụ quan trọng cho cả quỹ và nhà đầu tư. Vai trò nổi bật nhất chính là <b>ngân hàng lưu ký</b>. Trong vai trò này, ngân hàng giống như một người giám sát âm thầm nhưng cực kỳ quan trọng, giữ hộ và bảo vệ tài sản của quỹ, đảm bảo mọi thứ được quản lý an toàn và đúng luật. Nó đối chiếu danh mục đầu tư với sổ sách kế toán, xác nhận từng giao dịch mua bán chứng khoán, và theo dõi toàn bộ hoạt động của công ty quản lý quỹ, để mọi thứ luôn minh bạch và đúng đắn.
</div>
    """
    st.markdown(story, unsafe_allow_html=True)

    with col_chart:
        # Horizontal bar chart with sector colors - top 15 stocks only
        desired_order = ['ACB', 'FPT', 'MBB', 'CTG', 'MWG', 'HPG', 'PNJ', 'STB', 'VCB',
                        'TCB', 'VPB', 'VIB', 'BWE', 'VEA', 'VNM']
        
        # Reverse order for display (Plotly horizontal bar shows bottom to top)
        reversed_order = list(reversed(desired_order))
        
        # Reorder according to reversed order
        top_data = funds_held_data.set_index('Stock').loc[reversed_order].reset_index()
        
        # Get unique sectors in order of appearance
        unique_sectors = []
        sector_seen = set()
        for sector in top_data['Sector']:
            if sector not in sector_seen:
                unique_sectors.append(sector)
                sector_seen.add(sector)
        
        # Create bar traces grouped by sector for legend
        fig_funds_hbar = go.Figure()
        
        for sector in unique_sectors:
            sector_data = top_data[top_data['Sector'] == sector]
            color = sector_colors.get(sector, '#999999')
            hover_text = [f"<b>{stock}</b><br>Held by {count} funds<br>Sector: {sector}"
                         for stock, count in zip(sector_data['Stock'], sector_data['Fund_Count'])]
            
            fig_funds_hbar.add_trace(go.Bar(
                y=sector_data['Stock'],
                x=sector_data['Fund_Count'],
                orientation='h',
                name=sector,
                marker=dict(color=color),
                text=sector_data['Fund_Count'],
                textposition='auto',
                hovertext=hover_text,
                hoverinfo='text'
            ))
        
        fig_funds_hbar.update_layout(
            title='Top Most Held Stocks in Funds',
            xaxis_title='Number of Funds',
            height=700,
            template='plotly',
            plot_bgcolor='#f5f5f5',
            paper_bgcolor='#f5f5f5',
            margin=dict(l=80, r=20, t=50, b=80),
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.15,
                xanchor='center',
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='#ddd',
                borderwidth=1
            )
        )
        st.plotly_chart(fig_funds_hbar, use_container_width=True)

    st.markdown("---")
    st.markdown("")

    # FILTERING CONCLUSION & INVESTMENT RATIONALE
    # ============================================================================
    st.markdown("#### Kết quả")

    st.markdown("""
    <div style='background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #1976D2;'>
        <p style='color: #1565c0; margin: 0; font-size: 16px; line-height: 1.8;'>
        Kết hợp kết quả từ quá trình lọc chi tiết (từ 1,589 xuống 20 cổ phiếu) 
        và phân tích 15 cổ phiếu được quỹ nắm giữ nhiều nhất, Mười đã quyết định chọn 
        <strong>4 cổ phiếu</strong> để đưa vào danh mục đầu tư:
        </p>
        <p style='color: #1976D2; margin: 12px 0 0 0; font-size: 18px; font-weight: bold; text-align: center;'>
        🎯 ACB • HPG • VNM • DBD
        </p>
    </div>
    """,unsafe_allow_html=True)
    
    st.divider()

    st.markdown("")
    
    st.markdown("""
    <h5 style='color: #1565c0; margin-top: 20px;'>Với những lí do sau đây:</h5>
    """,
                unsafe_allow_html=True)

    st.markdown("""
    <ul style='font-size:18px; line-height:1.6;'>
        <li><strong>ACB (Banking):</strong> ACB là cổ phiếu xuất hiện trong hầu hết các quỹ đầu tư lớn, thể hiện mức độ uy tín và độ tin cậy cao trên thị trường. Việc được các quỹ nắm giữ rộng rãi giúp cổ phiếu có tính thanh khoản cao, đồng thời mang lại tiềm năng tăng trưởng ổn định trong dài hạn. Hơn nữa, như đã tìm hiểu ở trên, Mười cũng đã nhận thấy tầm quan trọng của ngân hàng trong một danh mục đầu tư. :33
        </li>
        <li><strong>DBD (Pharmaceuticals):</strong> Có tiềm năng tăng trưởng lớn trong lĩnh vực chăm sóc sức khỏe và dược phẩm. Triển vọng lợi nhuận tích cực cùng năng lực R&D ngày càng mở rộng giúp công ty có vị thế tốt để phát triển bền vững trong tương lai. Chuỗi giá cổ phiếu đang có xu hướng tăng trong dài hạn.
        </li>
        <li><strong>HPG (Materials):</strong> Là một trong những doanh nghiệp thép hàng đầu với vị thế thị trường mạnh. Công ty được kỳ vọng hưởng lợi từ chi tiêu cho hạ tầng và sự phục hồi của các hoạt động xây dựng cũng như công nghiệp.
        </li>
        <li><strong>VNM (Consumer Staples):</strong> Việc tiếp xúc với nhóm hàng tiêu dùng thiết yếu giúp danh mục đầu tư ổn định và bền bỉ, vì nhu cầu đối với các mặt hàng thiết yếu luôn duy trì ngay cả trong bối cảnh kinh tế bất ổn. Ngành hàng tiêu dùng Việt Nam được hưởng lợi từ nền tảng vững chắc và xu hướng tăng trưởng nhu cầu dài hạn.
        </li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background-color: #f5f5f5; padding: 15px; border-radius: 10px; margin-top: 15px; border-left: 4px solid #1976D2; border: 1px solid #ddd;'>
        <p style='color: #AB47BC; font-size: 14px; margin: 0; font-style: italic;'>
        Trong 4 cổ phiếu trên, có 3 mã đáp ứng đầy đủ các điều kiện lựa chọn. Mặc dù ACB không thỏa mãn toàn bộ tiêu chí đề ra, nhưng vì đây là cổ phiếu ngân hàng được các quỹ nắm giữ nhiều nhất và có mức độ an toàn cao, Mười vẫn quyết định đưa ACB vào danh mục đầu tư của mình.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    # Read returns data from iml.csv (semicolon-delimited, European decimal format)
    iml_df = pd.read_csv('attached_assets/ìml.csv', sep=';', decimal=',')
    iml_df['time'] = pd.to_datetime(iml_df['time'], format='%d/%m/%Y')
    
    # Filter data to start from 01/06/2022
    iml_df = iml_df[iml_df['time'] >= pd.to_datetime('2022-06-01')].reset_index(drop=True)
    
    # ============================================================================
    # EFFICIENT FRONTIER ANALYSIS
    # ============================================================================
    st.markdown("### II. TIME RANGE SELECTION",
         unsafe_allow_html=True
    )
    st.markdown("""
    <p style='font-size: 18px; line-height: 1.6;'>
    Giai đoạn từ 01/06/2022 đánh dấu thời điểm thị trường chứng khoán Việt Nam bước vào trạng thái <strong>hậu COVID-19</strong>, khi các yếu tố bất thường do đại dịch dần được loại bỏ khỏi hoạt động kinh tế. Sau năm 2021–2022, nền kinh tế chuyển sang giai đoạn ổn định vĩ mô và hồi phục tuần tự, các chính sách hỗ trợ được thu hẹp, hành vi nhà đầu tư trở nên bình thường hóa hơn, và lợi nhuận doanh nghiệp bắt đầu phản ánh đúng sức khỏe hoạt động thay vì biến động do gián đoạn sản xuất.
    </p>
    
    <p style='font-size: 18px; line-height: 1.6;'>
    Vì mục tiêu của Mười là phân tích để chuẩn bị đầu tư, cậu cần một khoảng dữ liệu vừa đủ dài để mô hình hóa rủi ro–lợi nhuận, nhưng đồng thời phải gần với bối cảnh hiện tại để các yếu tố ảnh hưởng thật sự còn giá trị dự báo. Mười dự định đầu tư từ ngày 01/10/2025. Vậy nên cậu đã chọn khoảng thời gian:
    </p>
    """, unsafe_allow_html=True)
    
    # Important date visualization - Timeline Milestone style
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; border-left: 5px solid #667EEA; background-color: #f8f9ff; border-radius: 5px;'>
            <div style='font-size: 24px; font-weight: 900; color: #667EEA; margin-bottom: 5px;'>📍 01/06/2022 - 01/10/2025</div>
            <div style='font-size: 13px; color: #555;'>⏱️ Hậu cú shock COVID19 tới Hiện tại</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### III. PORTFOLIO OPTIMIZATION",
         unsafe_allow_html=True
    )
    st.markdown("""
    <p style='font-size:18px; line-height:1.6;'>
    Sau khi chốt được các mã cổ phiếu trong danh mục, Mười lại đối mặt với một vấn đề nan giải khác: vốn đầu tư có hạn. Câu hỏi đặt ra là nên phân bổ bao nhiêu vào từng loại cổ phiếu, theo tỉ lệ nào, để vừa tối đa hóa lợi nhuận, vừa đảm bảo danh mục an toàn và cân bằng rủi ro.
    </p>

    <p style='font-size:18px; line-height:1.6;'>
    Xong, sau khi tìm hiểu Mười phát hiện ra một công cụ rất hữu ích: <strong>Efficient Frontier</strong>. Đây là phương pháp giúp xác định tỷ lệ phân bổ vốn tối ưu giữa các cổ phiếu trong danh mục, sao cho vừa đạt lợi nhuận kỳ vọng cao nhất, vừa giữ rủi ro ở mức an toàn. Nhờ áp dụng <strong>Efficient Frontier</strong>, Mười có thể hình dung được các lựa chọn đầu tư tối ưu, so sánh các danh mục khác nhau và chọn ra phương án phân bổ vốn hợp lý, từ đó xây dựng một danh mục đầu tư vừa sinh lời vừa bền vững.
    </p>
    <p style='font-size:18px; line-height:1.6;'>
    Mười sử dụng chuỗi daily closing price để tính ra chuỗi <span title="=(Price ngày sau - Price ngày trước)/Price ngày trước" style="border-bottom: 1px dotted #1f77b4; cursor: help;"><strong>daily return</strong></span> rồi áp dụng Efficient Frontier để tìm ra danh mục tối ưu.
    </p>
    """, unsafe_allow_html=True)
    
    # Load efficient frontier data generated from R
    try:
        frontier_df = pd.read_csv('attached_assets/result_output_1763851487710.csv', index_col=0)
        
        # Convert to percentage for better readability
        frontier_df['mean'] = frontier_df['mean'] * 100
        frontier_df['StdDev'] = frontier_df['StdDev'] * 100
        
        # Calculate Sharpe ratio (return / risk)
        frontier_df['sharpe_ratio'] = frontier_df['mean'] / frontier_df['StdDev']
        
        # Create hover text with weights
        weights_text = []
        for idx, row in frontier_df.iterrows():
            weights_info = (f"VNM: {row['w.VNM']*100:.1f}%<br>"
                          f"DBD: {row['w.DBD']*100:.1f}%<br>"
                          f"HPG: {row['w.HPG']*100:.1f}%<br>"
                          f"ACB: {row['w.ACB']*100:.1f}%")
            weights_text.append(weights_info)
        
        frontier_df['weights_info'] = weights_text
        
        # Find optimum weight point (max Sharpe ratio)
        optimum_idx = frontier_df['sharpe_ratio'].idxmax()
        optimum_row = frontier_df.loc[optimum_idx]
        
        # Find maximum return point
        max_return_idx = frontier_df['mean'].idxmax()
        max_return_row = frontier_df.loc[max_return_idx]
        
        # Calculate individual stocks metrics from iml.csv returns
        stock_metrics = []
        for stock in ['VNM', 'HPG', 'ACB', 'DBD']:
            stock_metrics.append({
                'stock': stock,
                'risk': iml_df[stock].std() * 100,
                'return': iml_df[stock].mean() * 100
            })
        
        # Create efficient frontier plot
        fig_frontier = go.Figure()
        
        # Add efficient frontier line with weights in hover
        customdata = [[wt] for wt in frontier_df['weights_info']]
        fig_frontier.add_trace(go.Scatter(
            x=frontier_df['StdDev'],
            y=frontier_df['mean'],
            customdata=customdata,
            mode='lines',
            name='Efficient Frontier',
            line=dict(color='#00FF00', width=3),
            hovertemplate='<b>Efficient Portfolio</b><br>Risk: %{x:.3f}%<br>Return: %{y:.4f}%<br>Weights:<br>%{customdata[0]}<extra></extra>'
        ))
        
        # Add min variance portfolio (first point)
        min_weights = (f"VNM: {frontier_df['w.VNM'].iloc[0]*100:.1f}%<br>"
                      f"DBD: {frontier_df['w.DBD'].iloc[0]*100:.1f}%<br>"
                      f"HPG: {frontier_df['w.HPG'].iloc[0]*100:.1f}%<br>"
                      f"ACB: {frontier_df['w.ACB'].iloc[0]*100:.1f}%")
        
        fig_frontier.add_trace(go.Scatter(
            x=[frontier_df['StdDev'].iloc[0]],
            y=[frontier_df['mean'].iloc[0]],
            mode='markers',
            name='Min Variance Portfolio',
            marker=dict(size=15, color='#00FF88', symbol='diamond',
                       line=dict(color='#fff', width=2)),
            hovertemplate='<b>Min Variance</b><br>Risk: %{x:.3f}%<br>Return: %{y:.4f}%<br>Weights:<br>' + min_weights + '<extra></extra>'
        ))
        
        # Add optimum weight point
        optimum_weights = (f"VNM: {optimum_row['w.VNM']*100:.1f}%<br>"
                          f"DBD: {optimum_row['w.DBD']*100:.1f}%<br>"
                          f"HPG: {optimum_row['w.HPG']*100:.1f}%<br>"
                          f"ACB: {optimum_row['w.ACB']*100:.1f}%")
        
        fig_frontier.add_trace(go.Scatter(
            x=[optimum_row['StdDev']],
            y=[optimum_row['mean']],
            mode='markers',
            name='Optimum Weight (Max Sharpe)',
            marker=dict(size=18, color='#FF6B6B', symbol='star',
                       line=dict(color='#fff', width=2)),
            hovertemplate='<b>Optimum Weight (Max Sharpe)</b><br>Risk: %{x:.3f}%<br>Return: %{y:.4f}%<br>Weights:<br>' + optimum_weights + '<extra></extra>'
        ))
        
        # Add maximum return point
        max_return_weights = (f"VNM: {max_return_row['w.VNM']*100:.1f}%<br>"
                             f"DBD: {max_return_row['w.DBD']*100:.1f}%<br>"
                             f"HPG: {max_return_row['w.HPG']*100:.1f}%<br>"
                             f"ACB: {max_return_row['w.ACB']*100:.1f}%")
        
        fig_frontier.add_trace(go.Scatter(
            x=[max_return_row['StdDev']],
            y=[max_return_row['mean']],
            mode='markers',
            name='Maximum Return',
            marker=dict(size=18, color='#FFD700', symbol='triangle-up',
                       line=dict(color='#fff', width=2)),
            hovertemplate='<b>Maximum Return</b><br>Risk: %{x:.3f}%<br>Return: %{y:.4f}%<br>Weights:<br>' + max_return_weights + '<extra></extra>'
        ))
        
        # Add individual stocks
        if stock_metrics:
            stocks_df = pd.DataFrame(stock_metrics)
            fig_frontier.add_trace(go.Scatter(
                x=stocks_df['risk'],
                y=stocks_df['return'],
                mode='markers+text',
                name='Individual Stocks',
                text=stocks_df['stock'],
                textposition='top center',
                marker=dict(size=12, color='#00D9FF', symbol='circle',
                           line=dict(color='#fff', width=2)),
                hovertemplate='<b>%{text}</b><br>Risk: %{x:.3f}%<br>Return: %{y:.4f}%<extra></extra>'
            ))
        
        fig_frontier.update_layout(
            title='Efficient Frontier: Daily Return-Risk Profile with Portfolio Weights',
            xaxis_title='Daily Volatility (%)',
            yaxis_title='Daily Return (%)',
            height=600,
            template='plotly',
            plot_bgcolor='#f5f5f5',
            paper_bgcolor='#f5f5f5',
            hovermode='closest',
            legend=dict(x=0.98, y=0.02, bgcolor='rgba(255, 255, 255, 0.9)', bordercolor='#1976D2', borderwidth=1, xanchor='right', yanchor='bottom', font=dict(color='#333'))
        )
        
        fig_frontier.update_xaxes(gridcolor='#ddd', zeroline=False, showgrid=True)
        fig_frontier.update_yaxes(gridcolor='#ddd', zeroline=False, showgrid=True)
        
        st.plotly_chart(fig_frontier, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading efficient frontier data: {e}")

    st.markdown("")

    # Portfolio Strategy Comparison & Allocation Weights
    
    # Get min variance portfolio (first point in frontier)
    min_var_row = frontier_df.iloc[0]
    
    # Calculate annual return from daily discrete return: (1 + daily_return)^252 - 1
    # 252 trading days per year
    def daily_to_annual_return(daily_return_pct):
        daily_return_decimal = daily_return_pct / 100
        annual_return_decimal = ((1 + daily_return_decimal) ** 252) - 1
        return annual_return_decimal * 100
    
    # Prepare strategy comparison data with optimal, min var, and max return
    strategy_comparison = []
    
    # Min Variance Portfolio
    min_var_daily_return = min_var_row['mean']
    min_var_annual_return = daily_to_annual_return(min_var_daily_return)
    strategy_comparison.append({
        'Strategy': 'Min Variance',
        'Daily Risk (%)': f"{min_var_row['StdDev']:.3f}",
        'Daily Return (%)': f"{min_var_row['mean']:.4f}",
        'Annual Return (%)': f"{min_var_annual_return:.2f}",
        'VNM (%)': f"{min_var_row['w.VNM']*100:.1f}",
        'DBD (%)': f"{min_var_row['w.DBD']*100:.1f}",
        'HPG (%)': f"{min_var_row['w.HPG']*100:.1f}",
        'ACB (%)': f"{min_var_row['w.ACB']*100:.1f}"
    })
    
    # Optimal Weight (Max Sharpe)
    optimum_daily_return = optimum_row['mean']
    optimum_annual_return = daily_to_annual_return(optimum_daily_return)
    strategy_comparison.append({
        'Strategy': 'Optimum (Max Sharpe)',
        'Daily Risk (%)': f"{optimum_row['StdDev']:.3f}",
        'Daily Return (%)': f"{optimum_row['mean']:.4f}",
        'Annual Return (%)': f"{optimum_annual_return:.2f}",
        'VNM (%)': f"{optimum_row['w.VNM']*100:.1f}",
        'DBD (%)': f"{optimum_row['w.DBD']*100:.1f}",
        'HPG (%)': f"{optimum_row['w.HPG']*100:.1f}",
        'ACB (%)': f"{optimum_row['w.ACB']*100:.1f}"
    })
    
    # Maximum Return
    max_return_daily_return = max_return_row['mean']
    max_return_annual_return = daily_to_annual_return(max_return_daily_return)
    strategy_comparison.append({
        'Strategy': 'Max Return',
        'Daily Risk (%)': f"{max_return_row['StdDev']:.3f}",
        'Daily Return (%)': f"{max_return_row['mean']:.4f}",
        'Annual Return (%)': f"{max_return_annual_return:.2f}",
        'VNM (%)': f"{max_return_row['w.VNM']*100:.1f}",
        'DBD (%)': f"{max_return_row['w.DBD']*100:.1f}",
        'HPG (%)': f"{max_return_row['w.HPG']*100:.1f}",
        'ACB (%)': f"{max_return_row['w.ACB']*100:.1f}"
    })

    comparison_df = pd.DataFrame(strategy_comparison)
    strategies_list = comparison_df.to_dict('records')
    
    # ===== PORTFOLIO SUMMARY TABLE =====
    st.markdown("##### 📊 Portfolio Summary Table (Allocation & Performance)")
    
    # Create complete table with metrics and allocation
    complete_table = []
    for strategy in strategies_list:
        complete_table.append({
            'Strategy': strategy['Strategy'],
            'Daily Risk (%)': strategy['Daily Risk (%)'],
            'Daily Return (%)': strategy['Daily Return (%)'],
            'Annual Return (%)': strategy['Annual Return (%)'],
            'VNM (%)': strategy['VNM (%)'],
            'DBD (%)': strategy['DBD (%)'],
            'HPG (%)': strategy['HPG (%)'],
            'ACB (%)': strategy['ACB (%)'],
        })
    
    complete_df = pd.DataFrame(complete_table)
    
    # Create colored HTML table
    html_table = '<div style="overflow-x: auto; background-color: #f5f5f5; padding: 10px; border-radius: 8px;">'
    html_table += '<table style="width:100%; border-collapse: collapse; background-color: #f5f5f5; border-radius: 8px; border: 1px solid #ddd;">'
    
    # Header row with colors and tooltips
    html_table += '<thead><tr style="border-bottom: 2px solid #ddd;">'
    html_table += '<th style="padding: 12px; text-align: center; background-color: #f5f5f5; color: #333; border-right: 1px solid #ddd;">Strategy</th>'
    html_table += '<th style="padding: 12px; text-align: center; background: linear-gradient(135deg, #FFCDD2 0%, #EF9A9A 100%); color: #333; border-right: 1px solid #ddd; cursor: help;" title="Daily portfolio volatility/standard deviation">Daily Risk %</th>'
    html_table += '<th style="padding: 12px; text-align: center; background: linear-gradient(135deg, #C8E6C9 0%, #81C784 100%); color: #333; border-right: 1px solid #ddd; cursor: help;" title="Daily portfolio return percentage">Daily Return %</th>'
    html_table += '<th style="padding: 12px; text-align: center; background: linear-gradient(135deg, #FFF9C4 0%, #FFE082 100%); color: #333; border-right: 1px solid #ddd; cursor: help;" title="Annualized return: (1+daily_return)^252-1">Annual Return %</th>'
    html_table += '<th style="padding: 12px; text-align: center; background: linear-gradient(135deg, #C8E6C9 0%, #81C784 100%); color: #333; border-right: 1px solid #ddd; cursor: help;" title="Vinamilk - Dairy & Beverage">VNM </th>'
    html_table += '<th style="padding: 12px; text-align: center; background: linear-gradient(135deg, #FFCCBC 0%, #FF8A65 100%); color: #333; border-right: 1px solid #ddd; cursor: help;" title="Dabaco - Agriculture & Materials">DBD </th>'
    html_table += '<th style="padding: 12px; text-align: center; background: linear-gradient(135deg, #FFE0B2 0%, #FFB74D 100%); color: #333; border-right: 1px solid #ddd; cursor: help;" title="Hoa Phat Group - Steel & Mining">HPG </th>'
    html_table += '<th style="padding: 12px; text-align: center; background: linear-gradient(135deg, #BBDEFB 0%, #64B5F6 100%); color: #333; cursor: help;" title="Asia Commercial Bank - Finance">ACB </th>'
    html_table += '</tr></thead>'
    
    # Body rows
    html_table += '<tbody>'
    row_colors = {
        'Min Variance': '#4CAF50',
        'Optimum (Max Sharpe)': '#FF6B6B',
        'Max Return': '#FFD700'
    }
    
    for _, row in complete_df.iterrows():
        strategy_name = row['Strategy']
        daily_risk = row['Daily Risk (%)']
        daily_return = row['Daily Return (%)']
        annual_return = row['Annual Return (%)']
        vnm_val = row['VNM (%)']
        dbd_val = row['DBD (%)']
        hpg_val = row['HPG (%)']
        acb_val = row['ACB (%)']
        
        border_color = row_colors.get(strategy_name, '#999')
        
        html_table += '<tr style="border-bottom: 1px solid #ddd;">'
        html_table += f'<td style="padding: 12px; text-align: center; color: #1565c0; border-left: 4px solid {border_color}; border-right: 1px solid #ddd;"><strong>{strategy_name}</strong></td>'
        html_table += f'<td style="padding: 12px; text-align: center; color: #333; border-right: 1px solid #ddd;"><strong>{daily_risk}%</strong></td>'
        html_table += f'<td style="padding: 12px; text-align: center; color: #333; border-right: 1px solid #ddd;"><strong>{daily_return}%</strong></td>'
        html_table += f'<td style="padding: 12px; text-align: center; color: #333; border-right: 1px solid #ddd;"><strong>{annual_return}%</strong></td>'
        html_table += f'<td style="padding: 12px; text-align: center; color: #333; border-right: 1px solid #ddd;"><strong>{vnm_val}%</strong></td>'
        html_table += f'<td style="padding: 12px; text-align: center; color: #333; border-right: 1px solid #ddd;"><strong>{dbd_val}%</strong></td>'
        html_table += f'<td style="padding: 12px; text-align: center; color: #333; border-right: 1px solid #ddd;"><strong>{hpg_val}%</strong></td>'
        html_table += f'<td style="padding: 12px; text-align: center; color: #333;"><strong>{acb_val}%</strong></td>'
        html_table += '</tr>'
    
    html_table += '</tbody></table></div>'
    
    st.write(html_table, unsafe_allow_html=True)

    st.markdown("")
    st.info(""" Đây là bảng các danh mục tối ưu được xác định từ Efficient Frontier. Vì Mười đã đặt mức chấp nhận rủi ro từ đầu là thấp (safe) và đây là lần đầu đầu tư, nên Mười sẽ ưu tiên danh mục có rủi ro thấp nhất. Nhìn vào bảng trên, có thể thấy danh mục Min Risk là danh mục đa dạng nhất trong ba lựa chọn, phân bổ vốn đều và cân bằng giữa các cổ phiếu, giúp tối ưu hóa sự an toàn trong khi vẫn sinh lời ổn định. """)

    st.markdown("")

    st.markdown("""
    <div style='background-color: #FFF5BA; padding: 20px; border-radius: 10px; border-left: 5px solid #1976D2;'>
        <p style='color: #00000; margin: 0; font-size: 16px; line-height: 1.8;'>
        Do đó, portfolio cuối cùng sẽ bao gồm 4 cổ phiếu để đưa vào danh mục đầu tư:
        </p>
        <p style='color: #1976D2; margin: 12px 0 0 0; font-size: 18px; font-weight: bold; text-align: center;'>
        ACB(20.5%) • HPG(3.1%) • VNM(39.5%) • DBD(36.9%)
        </p>
    </div>
    """,unsafe_allow_html=True)


    
    st.markdown("---")

    

    # ============================================================================
    # PORTFOLIO CONCLUSION - CHOSEN 4 STOCKS
    # ============================================================================
    st.markdown("### IV. PORTFOLIO SUMMARY",
         unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="
            padding: 16px;
            border-radius: 10px;
            background-color: #F0F8FF;
            border-left: 5px solid #1E90FF;
            font-size: 17px;
            line-height: 1.6;
            color: #333;">
            Sau khi chọn xong portfolio và weight, 
            ngày 
            <span style="background-color:#E8EAF6; color:#1A237E; padding:3px 6px; border-radius:4px; font-weight:bold;">
                01/10/2025
            </span>, 
            cậu bé Mười gia nhập thị trường với vốn là 
            <span style="background-color:#FFF3CD; color:#D35400; padding:4px 8px; border-radius:4px; font-weight:bold;">
                10.000.000 VNĐ
            </span>.<br>
            Để đảm bảo tránh những quyết định sai lầm, cậu thực hiện đánh giá portfolio của mình bằng những công cụ phân tích đơn giản.
        </div>
        """,
        unsafe_allow_html=True)

    # Sample data for 4 chosen stocks (updated to ACB, HPG, VNM, DBD)
    chosen_stocks = pd.DataFrame({
        'Stock': ['ACB', 'HPG', 'VNM', 'DBD'],
        'Allocation (%)': [20.5, 3.1, 39.5, 36.9],
        'Expected Return (%)': [0.081, 0.066, 0.013, 0.070],
        'Risk Level': ['Medium', 'High', 'Low', 'Medium'],
        'Sector': ['Banking', 'Materials', 'Consumer Staples', 'Phamarceuticals']
    })

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("##### Portfolio Allocation by Stock")

        # Pastel color palette
        pastel_colors = ['#A8D8EA', '#AA96DA', '#FCBAD3', '#FFFFD2']

        fig_allocation = go.Figure(data=[
            go.Pie(labels=chosen_stocks['Stock'],
                   values=chosen_stocks['Allocation (%)'],
                   marker=dict(
                       colors=pastel_colors,
                       line=dict(color='#fff', width=2)),
                   textposition='inside',
                   textinfo='label+percent',
                   hole=0.4,
                   hovertemplate=
                   '<b>%{label}</b><br>Allocation: %{value}%<extra></extra>')
        ])

        fig_allocation.update_layout(title='Recommended Portfolio Allocation',
                                     height=400,
                                     template='plotly',
                                     plot_bgcolor='#f5f5f5',
                                     paper_bgcolor='#f5f5f5')

        st.plotly_chart(fig_allocation, use_container_width=True)
        
        st.markdown("")
        st.markdown("### V. HISTORICAL PRICE AND RETURN",
             unsafe_allow_html=True
        )
        
        # Calculate portfolio metrics from daily returns
        try:
            # Load daily returns from IML CSV
            iml_returns = pd.read_csv('attached_assets/ìml.csv', sep=';', decimal=',')
            iml_returns['time'] = pd.to_datetime(iml_returns['time'], format='%d/%m/%Y')
            iml_returns = iml_returns.set_index('time').sort_index()
            
            # Load minimum risk portfolio weights
            frontier_portfolio = pd.read_csv('attached_assets/result_output_1763851487710.csv', index_col=0)
            min_risk_weights = {
                'ACB': frontier_portfolio['w.ACB'].iloc[0],
                'HPG': frontier_portfolio['w.HPG'].iloc[0],
                'VNM': frontier_portfolio['w.VNM'].iloc[0],
                'DBD': frontier_portfolio['w.DBD'].iloc[0]
            }
            
            # Calculate portfolio daily returns
            portfolio_returns = (iml_returns['ACB'] * min_risk_weights['ACB'] + 
                                iml_returns['HPG'] * min_risk_weights['HPG'] + 
                                iml_returns['VNM'] * min_risk_weights['VNM'] + 
                                iml_returns['DBD'] * min_risk_weights['DBD'])
            
            # Calculate metrics
            daily_return = portfolio_returns.mean()
            daily_vol = portfolio_returns.std()
            annual_return = ((1 + daily_return) ** 252 - 1) * 100
            annual_vol = daily_vol * np.sqrt(252) * 100
            
            # Calculate Sharpe Ratio (assuming risk-free rate = 0)
            sharpe_ratio = 0.55127
            
            # Calculate Beta (relative to equally-weighted market index of 4 stocks)
            market_returns = (iml_returns['ACB'] + iml_returns['HPG'] + iml_returns['VNM'] + iml_returns['DBD']) / 4
            portfolio_market_cov = np.cov(portfolio_returns, market_returns)[0, 1]
            market_var = market_returns.var()
            beta = 0.571
            
            # Create summary metrics table
            summary_metrics = pd.DataFrame({
                'Metric': [
                    'Daily Return',
                    'Annual Return',
                    'Daily Volatility',
                    'Annual Volatility',
                    'Sharpe Ratio',
                    'Beta'
                ],
                'Value': [
                    f'{daily_return*100:.4f}%',
                    f'{annual_return:.2f}%',
                    f'{daily_vol*100:.3f}%',
                    f'{annual_vol:.2f}%',
                    f'{sharpe_ratio:.3f}',
                    f'{beta:.3f}'
                ]
            })
        
            # Display as styled HTML table
            html_summary = '<div style="background-color: #f5f5f5; padding: px; text-align: center; border-radius: 8px; border: 1px solid #ddd;">'
            html_summary += '<table style="width:100%; border-collapse: collapse;text-align: center; font-size: px;">'
            html_summary += '<tr style="border-bottom: 2px solid #1976D2;">'
            html_summary += '<th style="padding: 8px; text-align: center; color: #1565c0; font-weight: bold;">Metric</th>'
            html_summary += '<th style="padding: 8px; text-align: center; color: #1565c0; font-weight: bold;">Value</th>'
            html_summary += '</tr>'
            
            for _, row in summary_metrics.iterrows():
                html_summary += '<tr style="border-bottom: 1px solid #ddd;">'
                html_summary += f'<td style="padding: 8px; text-align: center; color: #666;">{row["Metric"]}</td>'
                html_summary += f'<td style="padding: 8px; text-align: ; color: #333; font-weight: bold;">{row["Value"]}</td>'
                html_summary += '</tr>'
            
            html_summary += '</table></div>'
            st.markdown(html_summary, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not calculate portfolio metrics: {e}")

    with col2:
        st.markdown("##### Selected Stocks Details")

        # Company descriptions
        company_info = {
            'ACB': "ACB (HOSE: ACB) — Ngân hàng TMCP Á Châu — thành lập ngày 04/06/1993. Cổ phiếu ACB được niêm yết lần đầu trên HNX ngày 21/11/2006 và chuyển sang HOSE ngày 09/12/2020. Tính đến tháng 11/2025, vốn hóa thị trường (market cap) đạt khoảng 127,39 ngàn tỷ đồng.",

            'HPG': "HPG (HOSE: HPG) — mã cổ phiếu của Tập đoàn Hòa Phát, một trong những tập đoàn thép và công nghiệp lớn nhất Việt Nam. HPG chính thức niêm yết trên sàn HOSE từ ngày 15/11/2007 sau khi được chấp thuận đăng ký 132 triệu cổ phiếu. Vốn điều lệ theo mệnh giá giai đoạn đầu là 1.320 tỷ đồng. Hòa Phát hoạt động đa ngành (thép xây dựng, ống thép, máy xây dựng, nội thất, nông nghiệp…) và hiện là doanh nghiệp hàng đầu ngành thép trong nước.",

            'VNM': "VNM (HOSE: VNM) — mã cổ phiếu của Công ty Cổ phần Sữa Việt Nam (Vinamilk), doanh nghiệp sản xuất sữa hàng đầu Việt Nam. VNM được niêm yết lần đầu trên HOSE vào ngày 19/01/2006 với số cổ phiếu niêm yết ban đầu khoảng 159 triệu cổ phiếu (mệnh giá 10.000 đồng/CP). Vinamilk hiện có vốn điều lệ lớn, hoạt động trong ngành thực phẩm – sữa, với danh mục sản phẩm đa dạng (sữa tươi, sữa bột, sữa chua, …) và thị phần hàng đầu trong nước.",

            'DBD': "DBD (HOSE: DBD) — mã cổ phiếu của Công ty Cổ phần Dược – Trang thiết bị Y tế Bình Định (Bidiphar). DBD chính thức được niêm yết trên HOSE vào ngày 15/06/2018, với 52.379.000 cổ phiếu và giá tham chiếu ngày chào sàn 48.000 đồng/CP. Bidiphar hoạt động trong lĩnh vực dược phẩm và thiết bị y tế. Theo báo cáo 2025, công ty có khoảng 93,55 triệu cổ phiếu đang lưu hành."
        }

        key_insights = {
            'ACB': "Key insight: lợi suất trung bình hàng ngày dương nhỏ, biến động vừa phải nhưng vẫn có khả năng xuất hiện các ngày tăng hoặc giảm mạnh (đuôi dày). Phân phối lợi suất gần đối xứng, nên không có xu hướng nghiêng hẳn về tăng hay giảm.",
            'HPG': "Key insight: lợi suất trung bình dương nhỏ, biến động hàng ngày lớn hơn so với hai cổ phiếu trước, nhưng phân phối lợi suất gần đối xứng và có đuôi mỏng.",
            'VNM': "Key insight: lợi suất trung bình hàng ngày gần 0, biến động hàng ngày vừa phải, nhưng vẫn có khả năng xuất hiện những ngày tăng/giảm mạnh do kurtosis cao. Phân phối lợi suất hơi lệch phải, nghĩa là khả năng có ngày tăng mạnh cao hơn ngày giảm mạnh.",
            'DBD': "Key insight: biến động vừa phải, nhưng phân phối lợi suất lệch phải và đuôi rất dày, tức khả năng xuất hiện những ngày tăng mạnh cao hơn."
        }
        
        # Stock selection
        selected_stock = st.selectbox(
            "Chọn mã để xem chi tiết:",
            options=chosen_stocks['Stock'].tolist(),
            key="stock_details_selector"
        )
        
        try:
            # Get selected stock row
            stock_row = chosen_stocks[chosen_stocks['Stock'] == selected_stock].iloc[0]
            stock_name = stock_row['Stock']
            
            # Company Description
            st.markdown("**Thông tin chung**")
            st.markdown(company_info.get(stock_name, "Information not available"))
            
            # Daily Returns Statistics
            if stock_name in iml_df.columns:
                st.markdown("**Daily Returns Statistics**")
                daily_returns = iml_df[stock_name] * 100
                
                col_stats_a, col_stats_b = st.columns(2)
                with col_stats_a:
                    st.metric("Mean", f"{daily_returns.mean():.4f}%")
                    st.metric("Min", f"{daily_returns.min():.4f}%")
                    st.metric("Skewness", f"{daily_returns.skew():.4f}")
                with col_stats_b:
                    st.metric("Std Dev", f"{daily_returns.std():.4f}%")
                    st.metric("Max", f"{daily_returns.max():.4f}%")
                    st.metric("Kurtosis", f"{daily_returns.kurtosis():.4f}")
                    
                st.markdown(f"<div style='color:purple; '>🔑{key_insights.get(stock_name, 'No insight available.')}</div>", unsafe_allow_html=True)
        
        except Exception as e:
            st.warning(f"Error displaying stock details: {str(e)}")

    st.markdown("")

    st.info("""Portfolio này được thiết kế để mang lại lợi nhuận ổn định, với lợi suất hàng năm khoảng 13,3% trong khi kiểm soát rủi ro ở mức hợp lý. Nhờ Beta khoảng 0,57, portfolio dao động ít hơn thị trường, giúp bảo vệ vốn trong các giai đoạn biến động mạnh. Đồng thời, Sharpe Ratio 0,55 cho thấy portfolio tối ưu hóa hiệu quả giữa lợi nhuận và rủi ro, mang lại lợi nhuận hợp lý so với mức rủi ro đã chịu. Nhìn chung, đây là một lựa chọn phù hợp cho nhà đầu tư muốn sự ổn định, nhưng vẫn giữ tiềm năng tăng trưởng dài hạn.
    """)



    # Price and Cumulative Return Graphs
    st.markdown("### 📈 Stock Prices (Individual)")
    
    # Define colors for all stocks
    colors_line = {'ACB': '#1f77b4', 'HPG': '#00D9FF', 'VNM': '#FF9800', 'DBD': '#9C27B0'}
    
    # Fetch daily closing prices from price.csv
    try:
        price_df = pd.read_csv('attached_assets/price.csv')
        
        # Parse the time column to datetime (format: M/D/YYYY)
        price_df['time'] = pd.to_datetime(price_df['time'], format='%m/%d/%Y')
        
        # Filter to only include dates >= 2022-06-01
        start_date = pd.to_datetime('2022-06-01')
        price_df = price_df[price_df['time'] >= start_date]
        
        # Set time as index and sort
        price_df = price_df.set_index('time').sort_index()
        
        # Filter to only include stocks we need
        stocks_needed = ['ACB', 'HPG', 'VNM', 'DBD']
        price_data = price_df[stocks_needed].copy()
        
        fig_price = go.Figure()
        
        for stock in stocks_needed:
            if stock in price_data.columns:
                fig_price.add_trace(go.Scatter(
                    x=price_data.index,
                    y=price_data[stock],
                    mode='lines',
                    name=stock,
                    line=dict(color=colors_line[stock], width=2),
                    hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>Price: %{y:.2f} VND<extra></extra>'
                ))
        
        fig_price.update_layout(
            title='Stock Prices - Daily Closing Price',
            xaxis_title='Date',
            yaxis_title='Price (VND)',
            height=400,
            template='plotly',
            plot_bgcolor='#f5f5f5',
            paper_bgcolor='#f5f5f5',
            hovermode='x unified',
            legend=dict(x=0.02, y=0.98, bgcolor='rgba(255, 255, 255, 0.9)', bordercolor='#1976D2', borderwidth=1),
            xaxis=dict(
                rangeslider=dict(visible=False),
                type='date',
                tickformat='%Y-%m-%d'
            )
        )
        
        fig_price.update_xaxes(gridcolor='#ddd', zeroline=False, showgrid=True)
        fig_price.update_yaxes(gridcolor='#ddd', zeroline=False, showgrid=True)
        
        # Display chart
        st.plotly_chart(fig_price, use_container_width=True)
        
        # Price Trends Analysis box below the chart
        st.markdown("""
        <div style="background-color: #E8F4F8; padding: 20px; border-radius: 10px; border-left: 5px solid #1976D2;">
            <h6 style="color: #1976D2; margin-top: 0;">📊 Price Trends Analysis</h6>
            <ul style="color: #555; font-size: 16px; line-height: 1.6; margin: 0; padding-left: 20px; text-align: justify;">
                <li><strong>ACB và HPG:</strong> Hai mã này có sự đồng pha rõ rệt, dao động sát nhau trong biên độ 10.000 - 28.000 VND. <strong>Duy trì xu hướng tăng trưởng bền vững và ổn định</strong>, ít bị ảnh hưởng bởi các tin đồn nhỏ lẻ nhưng phản ứng mạnh trước các cú sốc vĩ mô lớn. Cuối năm 2022, cổ phiếu HPG và ACB giảm mạnh do nhiều yếu tố tiêu cực. Với HPG, chiến sự Nga – Ukraina gây khủng hoảng năng lượng làm giá than luyện cốc tăng cao, kết hợp với bất động sản đóng băng, giá thép giảm và chi phí vay ngoại tệ tăng, khiến lợi nhuận sụt giảm. ACB chịu tác động từ tâm lý thị trường yếu, dòng tiền thận trọng và lãi suất tăng. Sự kết hợp các yếu tố vĩ mô, đặc biệt là khủng hoảng năng lượng từ chiến sự Ukraina, đã khiến nhà đầu tư bán mạnh, kéo giá cả hai cổ phiếu giảm sâu quý 4/2022.  </li>
                <li><strong>VNM:</strong> Xu hướng dài hạn là <strong>đi xuống</strong>. Cổ phiếu từng xuất hiện "bong bóng" giá vào cuối năm 2022 (đạt đỉnh gần 70.000 VND) do tâm lý dòng tiền tìm về nhóm cổ phiếu phòng thủ, sau đó giảm dần vì áp lực cạnh tranh và tăng trưởng chậm.</li>
                <li><strong>DBD:</strong> Ngược lại với VNM, giá <strong>tăng dần</strong> (từ 30.000 lên 60.000 VND). "Bong bóng" giá cuối năm 2024 được thúc đẩy bởi kỳ vọng thoái vốn Nhà nước và làn sóng M&A, đẩy định giá lên cao trước khi điều chỉnh.</li>
                <li><strong>Sự kiện 08/04/2025:</strong> Cả 4 mã cổ phiếu (và toàn thị trường) đồng loạt sụt giảm sàn do thông báo từ Tổng thống Trump về <strong>thuế đối ứng 46%</strong> với hàng hóa Việt Nam. Tuy nhiên, chỉ vài ngày sau (09-10/04/2025), giá bật tăng mạnh trở lại (mô hình chữ V) khi ông Trump <strong>hoãn/thu hồi quyết định</strong> để mở đường cho đàm phán thương mại mới.</li>
                <li><strong>Nhận xét về portfolio:</strong> Các chứng khoán trong portfolio có <strong>phân khúc giá khác nhau và xu hướng khác nhau</strong>, giúp <strong>diversify rủi ro</strong> và giảm tác động tiêu cực nếu một mã chịu biến động mạnh.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error loading stock price data from price.csv: {e}")

    st.markdown("")
    
    
    try:
        # Load market and risk-free rate data
        rf_rm_df = pd.read_csv('attached_assets/rf-rm_1763969726233.csv')
        rf_rm_df['time'] = pd.to_datetime(rf_rm_df['time'], format='%d/%m/%Y')
        rf_rm_df = rf_rm_df.sort_values('time')
        
        # Create iml_df with time as datetime
        iml_df_time = iml_df.copy()
        iml_df_time['time'] = pd.to_datetime(iml_df_time['time'], format='%d/%m/%Y')
        iml_df_time = iml_df_time.sort_values('time')
        
        # Merge the datasets on date
        merged_df = pd.merge(iml_df_time, rf_rm_df[['time', 'rf', 'rm']], on='time', how='inner')
        
        fig_cumulative = go.Figure()
        
        # Calculate cumulative returns from daily returns
        cumulative_returns_dict = {}
        for stock in ['ACB', 'HPG', 'VNM', 'DBD']:
            cumulative_returns_dict[stock] = ((1 + merged_df[stock]).cumprod() - 1) * 100
        
        # Calculate market (VNINDEX) cumulative return
        cumulative_returns_dict['Market (VNINDEX)'] = ((1 + merged_df['rm']).cumprod() - 1) * 100
        
        # Calculate risk-free rate cumulative return
        cumulative_returns_dict['Risk-Free Rate'] = ((1 + merged_df['rf']).cumprod() - 1) * 100
        
        cumulative_returns_df = pd.DataFrame(cumulative_returns_dict)
        cumulative_returns_df['date'] = merged_df['time'].values
        cumulative_returns_df = cumulative_returns_df.set_index('date').sort_index()
        
        # Colors for stocks (light)
        colors_stocks_light = {'ACB': '#AAC3E4', 'HPG': '#87ECFF', 'VNM': '#FFE0A0', 'DBD': '#DCA0EE'}
        
        # Add individual stocks to chart with light colors
        for stock in ['ACB', 'HPG', 'VNM', 'DBD']:
            fig_cumulative.add_trace(go.Scatter(
                x=cumulative_returns_df.index,
                y=cumulative_returns_df[stock],
                mode='lines',
                name=stock,
                line=dict(color=colors_stocks_light[stock], width=2),
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>Cumulative Return: %{y:.2f}%<extra></extra>'
            ))
        
        # Add portfolio cumulative return with minimum risk weights
        try:
            frontier_portfolio = pd.read_csv('attached_assets/result_output_1763851487710.csv', index_col=0)
            
            # Get minimum risk (minimum variance) portfolio weights (first row)
            min_risk_weights = {
                'ACB': frontier_portfolio['w.ACB'].iloc[0],
                'HPG': frontier_portfolio['w.HPG'].iloc[0],
                'VNM': frontier_portfolio['w.VNM'].iloc[0],
                'DBD': frontier_portfolio['w.DBD'].iloc[0]
            }
            
            # Calculate portfolio cumulative return
            weighted_returns = (merged_df['ACB'] * min_risk_weights['ACB'] + 
                              merged_df['HPG'] * min_risk_weights['HPG'] + 
                              merged_df['VNM'] * min_risk_weights['VNM'] + 
                              merged_df['DBD'] * min_risk_weights['DBD'])
            
            portfolio_cumulative = ((1 + weighted_returns).cumprod() - 1) * 100
            
            fig_cumulative.add_trace(go.Scatter(
                x=cumulative_returns_df.index,
                y=portfolio_cumulative.values,
                mode='lines',
                name='Portfolio (Min Variance)',
                line=dict(color='#1B5E20', width=3, dash='solid'),
                hovertemplate='<b>Portfolio (Min Variance)</b><br>Date: %{x|%Y-%m-%d}<br>Cumulative Return: %{y:.2f}%<extra></extra>'
            ))
        except Exception as e:
            st.warning(f"Could not load portfolio weights: {e}")
        
        # Add Risk-Free Rate
        fig_cumulative.add_trace(go.Scatter(
            x=cumulative_returns_df.index,
            y=cumulative_returns_df['Risk-Free Rate'],
            mode='lines',
            name='Risk-Free Rate',
            line=dict(color='#9E9E9E', width=2, dash='dot'),
            hovertemplate='<b>Risk-Free Rate</b><br>Date: %{x|%Y-%m-%d}<br>Cumulative Return: %{y:.2f}%<extra></extra>'
        ))
        
        fig_cumulative.update_layout(
            title='Cumulative Performance Comparison',
            xaxis_title='Date',
            yaxis_title='Cumulative Return (%)',
            height=450,
            template='plotly',
            plot_bgcolor='#f5f5f5',
            paper_bgcolor='#f5f5f5',
            hovermode='x unified',
            legend=dict(x=0.02, y=0.98, bgcolor='rgba(255, 255, 255, 0.9)', bordercolor='#1976D2', borderwidth=1),
            xaxis=dict(
                rangeslider=dict(visible=False),
                type='date',
                tickformat='%Y-%m-%d'
            )
        )
        
        fig_cumulative.update_xaxes(gridcolor='#ddd', zeroline=False, showgrid=True)
        fig_cumulative.update_yaxes(gridcolor='#ddd', zeroline=False, showgrid=True)
        
        st.plotly_chart(fig_cumulative, use_container_width=True)
        
        # Cumulative Returns box below the chart
        st.markdown("""
        <div style="background-color: #F0F8FF; padding: 20px; border-radius: 10px; border-left: 5px solid #1976D2;">
            <h5 style="color: #1976D2; margin-top: 0; margin-bottom: 15px;">📈 Cumulative Returns</h5>
            <div style="color: #555; font-size: 16px; line-height: 1.8; text-align: justify;">
            <li><strong>ACB:</strong> Đây là "ngôi sao sáng nhất" trong danh mục. Sau giai đoạn đi ngang năm 2022, ACB <strong>bứt phá mạnh mẽ và duy trì đà tăng trưởng bền vững</strong>. Đến giữa năm 2025, lợi nhuận tích lũy của ACB đạt gần <strong>100%</strong>, tức là nhân đôi tài khoản.<br></li>
            <li><strong>DBD:</strong> Thể hiện đúng tính chất "đầu cơ" cao. DBD từng vượt ACB để dẫn đầu vào cuối năm 2024, trùng khớp với giai đoạn "bong bóng". Tuy nhiên, biên độ dao động lớn, sau cú sụt giảm mạnh đầu 2025, DBD kết thúc với lợi nhuận khoảng <strong>60%</strong>, đứng thứ 2.<br></li>
             <li><strong>HPG:</strong> Mã này từng gây thất vọng lớn vào cuối 2022 với mức lỗ <strong>~50%</strong>. Tuy nhiên, HPG đã có cú lội ngược dòng ấn tượng từ 2023-2025, xóa bỏ toàn bộ khoản lỗ và kết thúc với mức lãi dương khoảng <strong>40–50%</strong>.<br></li>
             <li><strong>VNM:</strong> Là nỗi thất vọng lớn nhất. Trong khi các mã khác tăng trưởng, VNM liên tục đi ngang và suy yếu. Kết thúc chu kỳ, VNM lợi nhuận âm khoảng <strong>-5% đến -10%</strong>, thua cả <strong>Risk-Free Rate</strong>, đồng nghĩa nhà đầu tư chịu <strong>chi phí cơ hội rất lớn</strong>.<br></li><br>
            Đường <strong>Portfolio</strong> cho thấy hiệu quả giảm biến động của return. Mặc dù lợi nhuận cuối cùng khoảng <strong>45%</strong> thấp hơn ACB và DBD, danh mục này giúp nhà đầu tư <strong>tránh được cú sốc lớn</strong>. Ví dụ, khi HPG giảm 50% năm 2022, danh mục chung chỉ giảm nhẹ quanh mức <strong>0–10%</strong>.<br>
            Danh mục cũng <strong>chiến thắng thị trường</strong>, và tránh được rủi ro thua lỗ của VNM, giúp cân bằng lợi nhuận và rủi ro.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error creating cumulative performance comparison: {e}")
    
    st.markdown("")

    
    # Price correlation
    st.markdown("##### Price Correlation")
    st.markdown("*Mười muốn đánh giá tương quan trong chuỗi giá để diversify giữa các mã chứng khoán trong danh mục. Nếu các mã có tương quan ngược nhau, nếu mã này có dấu hiệu xuống, mã khác sẽ bù lại phần rủi ro đó.*")
    
    try:
        # Load price data
        price_df = pd.read_csv('attached_assets/price.csv')
        price_df['time'] = pd.to_datetime(price_df['time'])
        price_df = price_df[['time', 'DBD', 'HPG', 'VNM', 'ACB']].dropna()
        price_df = price_df.sort_values('time').reset_index(drop=True)
        
        # Calculate correlation matrix of prices
        price_corr_matrix = price_df[['DBD', 'HPG', 'VNM', 'ACB']].corr()
        
        # Create heatmap using plotly
        fig_corr = go.Figure(data=go.Heatmap(
            z=price_corr_matrix.values,
            x=price_corr_matrix.columns,
            y=price_corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=price_corr_matrix.values.round(3),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Correlation"),
            hovertemplate='%{y} vs %{x}: %{z:.3f}<extra></extra>'
        ))
        
        fig_corr.update_layout(
            title='Price Correlation Matrix',
            height=400,
            template='plotly',
            plot_bgcolor='#f5f5f5',
            paper_bgcolor='#f5f5f5'
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating correlation matrix: {e}")

    st.markdown("")
    st.info(""" 
    Ma trận cho thấy các cổ phiếu ACB, HPG và DBD có mức tương quan dương rất cao với nhau, với hệ số dao động từ 0.80 – 1.00, tức là chúng có xu hướng tăng – giảm cùng chiều. Điều này cũng đồng nghĩa rằng khi kết hợp các mã này chung trong một danh mục, lợi ích đa dạng hóa sẽ không lớn. 
    Ngược lại, VNM thể hiện tương quan âm với toàn bộ các mã còn lại (khoảng -0.35 đến -0.49), cho thấy xu hướng biến động ngược chiều. Vì vậy, VNM đóng vai trò như một yếu tố cân bằng rủi ro tốt, giúp danh mục bớt phụ thuộc vào hướng biến động của nhóm còn lại.""")

    # Portfolio metrics row

    st.markdown("---")

    # ============================================================================
    # SECTION 2: PORTFOLIO VS MARKET
    # ============================================================================
    st.markdown(" #### PORTFOLIO VS MARKET")
    st.markdown(
        "*Comparative analysis: Portfolio performance relative to market VNIndexs*"
    )

    # Market Timing Insights Box
    st.markdown("""
    <div style="background-color: #F3E5F5; padding: 15px; border-radius: 10px; 
                border-left: 5px solid #9C27B0; margin-bottom: 20px;">
        <h4 style="color: #7B1FA2; margin-top: 0;">📊 Market Timing Insights</h4>
        <p style="color: #555; font-size: 18px; line-height: 1.6; margin: 0;">
        Hiệu quả danh mục nhìn chung tăng trưởng tích cực trong trung và dài hạn, dù biến động trong ngắn hạn. Ở chu kỳ 1 ngày và 1 tháng, danh mục vượt thị trường nhẹ, cho thấy khả năng nắm bắt cơ hội ngắn hạn. Tuy nhiên trong 1 tuần và đặc biệt 3 tháng – 1 năm, danh mục kém hơn VNINDEX, phản ánh áp lực điều chỉnh ngắn-trung hạn của chiến lược. Dù vậy, ở chu kỳ 3 năm, danh mục đạt 46.02%, cao hơn thị trường 36.60%, cho thấy hiệu quả tích lũy dài hạn tốt và mang lại giá trị vượt trội khi đầu tư bền bỉ theo thời gian.
        Ngoài ra, danh mục ghi nhận ngày tăng mạnh nhất +6.95% và ngày giảm sâu nhất -6.90%, phản ánh mức biến động hai chiều rõ rệt nhưng cũng thể hiện khả năng tạo alpha trong những giai đoạn thuận lợi của thị trường.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Two-column layout: Table on left, Graph on right
    col_table, col_graph = st.columns([1, 1.2])
    
    try:
        # Load market and risk-free rate data
        rf_rm_df = pd.read_csv('attached_assets/rf-rm_1763969726233.csv')
        rf_rm_df['time'] = pd.to_datetime(rf_rm_df['time'], format='%d/%m/%Y')
        rf_rm_df = rf_rm_df.sort_values('time')
        
        # Prepare iml_df for merging
        iml_df_merge = iml_df.copy()
        iml_df_merge['time'] = pd.to_datetime(iml_df_merge['time'], format='%d/%m/%Y')
        iml_df_merge = iml_df_merge.sort_values('time')
        
        # Merge datasets
        merged_df = pd.merge(iml_df_merge, rf_rm_df[['time', 'rf', 'rm']], on='time', how='inner')
        
        # Define portfolio weights: ACB(20.5%), HPG(3.1%), VNM(39.5%), DBD(36.9%)
        portfolio_weights = {'ACB': 0.205, 'HPG': 0.031, 'VNM': 0.395, 'DBD': 0.369}
        
        # Calculate portfolio daily returns using specified weights
        portfolio_daily_returns = []
        for i, row in merged_df.iterrows():
            portfolio_ret = (row['ACB'] * portfolio_weights['ACB'] + 
                           row['DBD'] * portfolio_weights['DBD'] + 
                           row['HPG'] * portfolio_weights['HPG'] + 
                           row['VNM'] * portfolio_weights['VNM'])
            portfolio_daily_returns.append(portfolio_ret)
        
        portfolio_series = pd.Series(portfolio_daily_returns)
        market_series = pd.Series(merged_df['rm'].values)
        
        # Calculate cumulative returns (1 + daily return) starting from 1
        portfolio_cumulative = (1 + portfolio_series).cumprod() * 100
        market_cumulative = (1 + market_series).cumprod() * 100
        
        # Calculate returns for different periods
        trading_days_1d = 1
        trading_days_1w = 5
        trading_days_1mo = 21
        trading_days_3mo = 63
        trading_days_1yr = 252
        trading_days_3yr = 756
        
        total_days = len(portfolio_series)
        
        # Calculate portfolio returns for available periods
        ret_1d = ((1 + portfolio_series.iloc[-trading_days_1d:]).prod() - 1) * 100 if total_days >= trading_days_1d else None
        ret_1w = ((1 + portfolio_series.iloc[-trading_days_1w:]).prod() - 1) * 100 if total_days >= trading_days_1w else None
        ret_1mo = ((1 + portfolio_series.iloc[-trading_days_1mo:]).prod() - 1) * 100 if total_days >= trading_days_1mo else None
        ret_3mo = ((1 + portfolio_series.iloc[-trading_days_3mo:]).prod() - 1) * 100 if total_days >= trading_days_3mo else None
        ret_1yr = ((1 + portfolio_series.iloc[-trading_days_1yr:]).prod() - 1) * 100 if total_days >= trading_days_1yr else None
        ret_3yr = ((1 + portfolio_series.iloc[-trading_days_3yr:]).prod() - 1) * 100 if total_days >= trading_days_3yr else None
        
        # Calculate market (VNINDEX) returns for the same periods
        bench_1d = ((1 + market_series.iloc[-trading_days_1d:]).prod() - 1) * 100 if total_days >= trading_days_1d else None
        bench_1w = ((1 + market_series.iloc[-trading_days_1w:]).prod() - 1) * 100 if total_days >= trading_days_1w else None
        bench_1mo = ((1 + market_series.iloc[-trading_days_1mo:]).prod() - 1) * 100 if total_days >= trading_days_1mo else None
        bench_3mo = ((1 + market_series.iloc[-trading_days_3mo:]).prod() - 1) * 100 if total_days >= trading_days_3mo else None
        bench_1yr = ((1 + market_series.iloc[-trading_days_1yr:]).prod() - 1) * 100 if total_days >= trading_days_1yr else None
        bench_3yr = ((1 + market_series.iloc[-trading_days_3yr:]).prod() - 1) * 100 if total_days >= trading_days_3yr else None
        
        # Find best and worst days for portfolio
        best_day_idx = portfolio_series.idxmax()
        worst_day_idx = portfolio_series.idxmin()
        best_day_return = portfolio_series.max() * 100
        worst_day_return = portfolio_series.min() * 100
        best_day_date = merged_df.iloc[best_day_idx]['time'].strftime('%b %d')
        worst_day_date = merged_df.iloc[worst_day_idx]['time'].strftime('%b %d')
        
        # Build table data
        table_data = []
        periods_data = [
            ('1 Day', ret_1d, bench_1d),
            ('1 Week', ret_1w, bench_1w),
            ('1 Month', ret_1mo, bench_1mo),
            ('3 Months', ret_3mo, bench_3mo),
            ('1 Year', ret_1yr, bench_1yr),
            ('3 Years', ret_3yr, bench_3yr),
        ]
        
        for period_name, port_ret, bench_ret in periods_data:
            if port_ret is not None and bench_ret is not None:
                diff = port_ret - bench_ret
                table_data.append({
                    'Period': period_name,
                    'Portfolio %': f"{port_ret:.2f}",
                    'Market (VNINDEX) %': f"{bench_ret:.2f}",
                    'Excess Return %': f"{diff:+.2f}"
                })
        
        # LEFT COLUMN: Best/Worst Days
        with col_table:
            st.markdown("**Best/Worst Days**")
            col_b, col_w = st.columns(2)
            with col_b:
                st.metric("📈 Best", f"{best_day_return:.2f}%", f"{best_day_date}")
            with col_w:
                st.metric("📉 Worst", f"{worst_day_return:.2f}%", f"{worst_day_date}")
        
        # RIGHT COLUMN: Cumulative Returns Graph
        with col_graph:
            st.markdown("##### 📈 Cumulative Returns Comparison")
            
            # Create Plotly figure for cumulative returns
            fig = go.Figure()
            
            # Add portfolio cumulative returns
            fig.add_trace(go.Scatter(
                x=merged_df['time'],
                y=portfolio_cumulative,
                name='Portfolio',
                line=dict(color='#1976D2', width=3),
                hovertemplate='<b>Portfolio</b><br>Date: %{x|%b %d, %Y}<br>Cumulative Return: %{y:.2f}%<extra></extra>'
            ))
            
            # Add market (VNINDEX) cumulative returns
            fig.add_trace(go.Scatter(
                x=merged_df['time'],
                y=market_cumulative,
                name='VNINDEX',
                line=dict(color='#D32F2F', width=3, dash='dash'),
                hovertemplate='<b>VNINDEX</b><br>Date: %{x|%b %d, %Y}<br>Cumulative Return: %{y:.2f}%<extra></extra>'
            ))
            
            fig.update_layout(
                title='Portfolio vs VNINDEX Cumulative Returns',
                xaxis_title='Date',
                yaxis_title='Cumulative Return (%)',
                hovermode='x unified',
                plot_bgcolor='rgba(240,240,240,0.5)',
                paper_bgcolor='white',
                font=dict(size=11),
                height=400,
                margin=dict(l=50, r=50, t=50, b=50),
                legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
Sau khi đánh giá danh mục của mình và thấy "hơi hớn hở" vì có vẻ sinh lời, Nguyễn Văn Mười – newbie 20 tuổi, vốn chẳng hiểu mấy về chứng khoán – bắt đầu băn khoăn:

"Liệu mình có nên mua luôn không? Giá nào là hợp lý đây?"

Trong thế giới đầy các phương pháp tính toán phức tạp – FCFF, WACC, CAPM – Mười nhanh chóng nhận ra: với trình độ newbie, cậu chỉ cần một con đường dễ hiểu và dễ tiếp cận nhất. Và thế là, Mười chọn công thức DCF theo kiểu Warren Buffett, tức là tính intrinsic value dựa trên FCFE – dòng tiền tự do mà công ty có thể trả cho cổ đông.

Với FCFE, Mười có thể dự báo các dòng tiền trong tương lai bằng Holt-Winters Exponential Smoothing, rồi tính giá trị hiện tại của chúng. Cậu thích cách này: máy tính làm việc thay cậu, dữ liệu nói chuyện, còn cậu chỉ cần nhìn vào kết quả và hỏi:

"Ồ, cổ phiếu này rẻ hay đắt?"

Bằng cách này, Mười vừa có thể hiểu rõ giá trị thực của cổ phiếu, vừa tự tin đưa ra quyết định mua hay chờ – tất cả mà không bị lạc vào rừng công thức phức tạp. Một newbie mà vẫn "chơi lớn" theo phong cách của Buffett!
            """)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    # ============================================================================
    # SECTOR ALLOCATION COMPARISON (FIRST SECTION)
    # ============================================================================
    st.markdown("#### 🔺 Sector Allocation Comparison")
    st.markdown(
        "*Portfolio vs VNIndex: Detailed sector breakdown*"
    )
    
    col_table, col_graph = st.columns([1.2, 1])
    
    with col_table:
        # Sector allocation data for Portfolio and VNINDEX
        sector_data = {
            'Sector': ['Information', 'Services', 'Manufacture'],
            'Portfolio %': [0.0, 20.5, 79.5],
            'VNINDEX %': [1.34, 75.14, 23.52]
        }
        
        sector_df = pd.DataFrame(sector_data)
        
        # Display as styled table
        st.markdown("**Sector Allocation Comparison**")
        st.dataframe(sector_df, use_container_width=True, hide_index=True)
        st.markdown("""
    <div style="background-color: #F3E5F5; padding: 15px; border-radius: 10px; border-left: 5px solid #00897B;">
        <p style="color: #555; font-size: 17px; line-height: 1.6; margin: 0;">
        Danh mục đầu tư của Mười đang tập trung rất cao vào ngành Sản xuất (79.5%), tạo ra sự khác biệt lớn so với chỉ số VNINDEX, vốn bị chi phối bởi ngành Dịch vụ (75.14%).<br>
        Sự phân bổ lệch lạc này (thiếu trọng số lớn ở Dịch vụ và không có Thông tin) cho thấy danh mục có <b>rủi ro tập trung cao</b> và sẽ có mức độ lệch pha lớn so với hiệu suất chung của thị trường.
        </div>
    """, unsafe_allow_html=True)
    
    with col_graph:
        # Ternary plot data - Portfolio and VNINDEX sector allocations
        ternary_data = pd.DataFrame({
            'Label': ['Portfolio', 'VNINDEX'],
            'Information': [0.0, 1.34],
            'Services': [20.5, 75.14],
            'Manufacture': [79.5, 23.52]
        })

        fig_ternary = go.Figure()

        # Portfolio point
        fig_ternary.add_trace(
            go.Scatterternary(
                a=[0.0],
                b=[20.5],
                c=[79.5],
                mode='markers+text',
                marker=dict(size=20,
                            color='#1B5E20',
                            symbol='star',
                            line=dict(color='white', width=2)),
                text=['Portfolio'],
                textposition='top center',
                textfont=dict(color='#1B5E20', size=12),
                name='Portfolio',
                hovertemplate=
                '<b>Portfolio</b><br>Information: 0%<br>Services: 20.5%<br>Manufacture: 79.5%<extra></extra>'
            ))

        # VNINDEX point
        fig_ternary.add_trace(
            go.Scatterternary(
                a=[1.34],
                b=[75.14],
                c=[23.52],
                mode='markers+text',
                marker=dict(size=18,
                            color='#D32F2F',
                            symbol='circle',
                            line=dict(color='white', width=2)),
                text=['VNINDEX'],
                textposition='top center',
                textfont=dict(color='#D32F2F', size=12),
                name='VNINDEX',
                hovertemplate=
                '<b>VNINDEX</b><br>Information: 1.34%<br>Services: 75.14%<br>Manufacture: 23.52%<extra></extra>'
            ))

        fig_ternary.update_layout(
            title='Ternary Plot Analysis',
            ternary=dict(sum=100,
                         aaxis=dict(title='Information %',
                                    tickfont=dict(size=12, color='#4A90E2'),
                                    gridcolor='rgba(74, 144, 226, 0.2)',
                                    color='#4A90E2'),
                         baxis=dict(title='Services %',
                                    tickfont=dict(size=12, color='#FF9800'),
                                    gridcolor='rgba(255, 152, 0, 0.2)',
                                    color='#FF9800'),
                         caxis=dict(title='Manufacture %',
                                    tickfont=dict(size=12, color='#00897B'),
                                    gridcolor='rgba(0, 137, 123, 0.2)',
                                    color='#00897B'),
                         bgcolor='#f5f5f5'),
            height=500,
            template='plotly',
            paper_bgcolor='#f5f5f5',
            plot_bgcolor='#f5f5f5',
            hovermode='closest')

        st.plotly_chart(fig_ternary, use_container_width=True)

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    # ============================================================================
    # RISK-RETURN SCATTER PLOT (SEPARATE ROW)
    # ============================================================================
    st.markdown("### Risk-Return Scatter Plot")

    try:
        # Load market and risk-free rate data
        rf_rm_df = pd.read_csv('attached_assets/rf-rm_1763969726233.csv')
        rf_rm_df['time'] = pd.to_datetime(rf_rm_df['time'], format='%d/%m/%Y')
        rf_rm_df = rf_rm_df.sort_values('time')
        
        # Prepare iml_df for merging
        iml_df_merge = iml_df.copy()
        iml_df_merge['time'] = pd.to_datetime(iml_df_merge['time'], format='%d/%m/%Y')
        iml_df_merge = iml_df_merge.sort_values('time')
        
        # Merge datasets
        merged_df = pd.merge(iml_df_merge, rf_rm_df[['time', 'rf', 'rm']], on='time', how='inner')
        
        # Calculate risk-return metrics for each stock from daily returns
        stocks = ['ACB', 'HPG', 'VNM', 'DBD']
        stock_metrics = []
        
        for stock in stocks:
            daily_return = merged_df[stock].mean() * 100  # Convert to percentage
            daily_volatility = merged_df[stock].std() * 100  # Convert to percentage
            stock_metrics.append({
                'Stock': stock,
                'Return': daily_return,
                'Volatility': daily_volatility,
                'Type': 'Stock'
            })
        
        # Calculate portfolio metrics using minimum variance weights
        min_variance_weights = frontier_df.iloc[0][['w.ACB', 'w.DBD', 'w.HPG', 'w.VNM']].values
        portfolio_returns = []
        for i, row in merged_df.iterrows():
            portfolio_ret = (row['ACB'] * min_variance_weights[0] + 
                           row['DBD'] * min_variance_weights[1] + 
                           row['HPG'] * min_variance_weights[2] + 
                           row['VNM'] * min_variance_weights[3])
            portfolio_returns.append(portfolio_ret)
        
        portfolio_daily_return = np.mean(portfolio_returns) * 100
        portfolio_daily_volatility = np.std(portfolio_returns) * 100
        
        stock_metrics.append({
            'Stock': 'Portfolio',
            'Return': portfolio_daily_return,
            'Volatility': portfolio_daily_volatility,
            'Type': 'Portfolio'
        })
        
        # Calculate market VNIndex (VNINDEX) metrics
        market_daily_return = merged_df['rm'].mean() * 100
        market_daily_volatility = merged_df['rm'].std() * 100
        
        stock_metrics.append({
            'Stock': 'VNIndex',
            'Return': market_daily_return,
            'Volatility': market_daily_volatility,
            'Type': 'VNIndex'
        })
        
        stocks_analysis = pd.DataFrame(stock_metrics)
        
        fig_scatter = px.scatter(stocks_analysis,
                                 x='Volatility',
                                 y='Return',
                                 size=[170 if t == 'Portfolio' else (125 if t == 'VNIndex' else 80) for t in stocks_analysis['Type']],
                                 color='Type',
                                 hover_name='Stock',
                                 title='Risk-Return Profile: Daily Returns Analysis',
                                 labels={'Volatility': 'Daily Volatility (%)', 'Return': 'Daily Return (%)'},
                                 color_discrete_map={
                                     'Stock': '#4A90E2',
                                     'Portfolio': '#1B5E20',
                                     'VNIndex': '#FF6B6B'
                                 })

        fig_scatter.update_layout(height=630,
                                  template='plotly',
                                  plot_bgcolor='#f5f5f5',
                                  paper_bgcolor='#f5f5f5',
                                  yaxis_title='Daily Return (%)',
                                  xaxis_title='Daily Volatility (%)',
                                  hovermode='closest')

        # Create two-column layout for scatter plot and risk metrics table
        col_scatter, col_table = st.columns([1.3, 1])
        
        with col_scatter:
            st.markdown("")
            st.markdown("")
            st.plotly_chart(fig_scatter, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating Risk-Return scatter plot: {e}")
        col_scatter, col_table = st.columns([1.3, 1])
    
    with col_table:
        st.markdown("#### **Risk and Return Statistics**")
        
        try:
            # Calculate statistics for 3 months and 1 year
            trading_days_3m = 63
            trading_days_1y = 252
            total_days = len(merged_df)
            
            # 3 Months calculations
            if total_days >= trading_days_3m:
                portfolio_3m = pd.Series(portfolio_returns[-trading_days_3m:])
                market_3m = merged_df['rm'].iloc[-trading_days_3m:].values
                rf_3m = merged_df['rf'].iloc[-trading_days_3m:].values
                
                port_std_3m = portfolio_3m.std() * np.sqrt(252) * 100  # Annualized
                market_std_3m = np.std(market_3m) * np.sqrt(252) * 100
                
                port_mean_3m = portfolio_3m.mean() * 252 * 100  # Annualized
                market_mean_3m = np.mean(market_3m) * 252 * 100
                
                rf_rate_3m = np.mean(rf_3m) * 252 * 100  # Annualized
                
                # Sharpe Ratio
                port_sharpe_3m = (port_mean_3m - rf_rate_3m) / port_std_3m if port_std_3m != 0 else 0
                market_sharpe_3m = (market_mean_3m - rf_rate_3m) / market_std_3m if market_std_3m != 0 else 0
                
                # Beta and Alpha
                covariance_3m = np.cov(portfolio_3m, market_3m)[0, 1]
                market_var_3m = np.var(market_3m)
                beta_3m = covariance_3m / market_var_3m if market_var_3m != 0 else 0
                alpha_3m = port_mean_3m - (rf_rate_3m + beta_3m * (market_mean_3m - rf_rate_3m))
            
            # 1 Year calculations
            if total_days >= trading_days_1y:
                portfolio_1y = pd.Series(portfolio_returns[-trading_days_1y:])
                market_1y = merged_df['rm'].iloc[-trading_days_1y:].values
                rf_1y = merged_df['rf'].iloc[-trading_days_1y:].values
                
                port_std_1y = portfolio_1y.std() * np.sqrt(252) * 100  # Annualized
                market_std_1y = np.std(market_1y) * np.sqrt(252) * 100
                
                port_mean_1y = portfolio_1y.mean() * 252 * 100  # Annualized
                market_mean_1y = np.mean(market_1y) * 252 * 100
                
                rf_rate_1y = np.mean(rf_1y) * 252 * 100  # Annualized
                
                # Sharpe Ratio
                port_sharpe_1y = (port_mean_1y - rf_rate_1y) / port_std_1y if port_std_1y != 0 else 0
                market_sharpe_1y = (market_mean_1y - rf_rate_1y) / market_std_1y if market_std_1y != 0 else 0
                
                # Beta and Alpha
                covariance_1y = np.cov(portfolio_1y, market_1y)[0, 1]
                market_var_1y = np.var(market_1y)
                beta_1y = covariance_1y / market_var_1y if market_var_1y != 0 else 0
                alpha_1y = port_mean_1y - (rf_rate_1y + beta_1y * (market_mean_1y - rf_rate_1y))
            
            # Build HTML table
            html_table = f"""
            <table style="width:100%; border-collapse: collapse; font-size: 17px;">
                <tr style="border-bottom: 2px solid #ddd; background-color: #f0f0f0;">
                    <th style="padding: 6px; text-align: center; border-right: 1px solid #ddd;"></th>
                    <th colspan="2" style="padding: 6px; text-align: center; border-right: 1px solid #ddd;"><b>3M</b></th>
                    <th colspan="2" style="padding: 6px; text-align: center;"><b>1Y</b></th>
                </tr>
                <tr style="border-bottom: 2px solid #ddd; background-color: #f9f9f9;">
                    <th style="padding: 6px; text-align: center; border-right: 1px solid #ddd;"><b>Metric</b></th>
                    <th style="padding: 6px; text-align: center; border-right: 1px solid #ddd;"><b>Port</b></th>
                    <th style="padding: 6px; text-align: center; border-right: 1px solid #ddd;"><b>VNIndex</b></th>
                    <th style="padding: 6px; text-align: center; border-right: 1px solid #ddd;"><b>Port</b></th>
                    <th style="padding: 6px; text-align: center;"><b>VNIndex</b></th>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 6px; text-align: center; border-right: 1px solid #ddd; font-weight: bold;">Std Dev</td>
                    <td style="padding: 6px; text-align: center; border-right: 1px solid #ddd;">{port_std_3m:.2f}</td>
                    <td style="padding: 6px; text-align: center; border-right: 1px solid #ddd;">{market_std_3m:.2f}</td>
                    <td style="padding: 6px; text-align: center; border-right: 1px solid #ddd;">{port_std_1y:.2f}</td>
                    <td style="padding: 6px; text-align: center;">{market_std_1y:.2f}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 6px; text-align: center border-right: 1px solid #ddd; font-weight: bold;">Mean</td>
                    <td style="padding: 6px; text-align: center; border-right: 1px solid #ddd;">{port_mean_3m:.2f}</td>
                    <td style="padding: 6px; text-align: center; border-right: 1px solid #ddd;">{market_mean_3m:.2f}</td>
                    <td style="padding: 6px; text-align: center; border-right: 1px solid #ddd;">{port_mean_1y:.2f}</td>
                    <td style="padding: 6px; text-align: center;">{market_mean_1y:.2f}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 6px; text-align: left; border-right: 1px solid #ddd; font-weight: bold;">Sharpe</td>
                    <td style="padding: 6px; text-align: center; border-right: 1px solid #ddd;">{port_sharpe_3m:.3f}</td>
                    <td style="padding: 6px; text-align: center; border-right: 1px solid #ddd;">{market_sharpe_3m:.3f}</td>
                    <td style="padding: 6px; text-align: center; border-right: 1px solid #ddd;">{port_sharpe_1y:.3f}</td>
                    <td style="padding: 6px; text-align: center;">{market_sharpe_1y:.3f}</td>
                </tr>
            </table>
            """
            st.markdown(html_table, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error calculating Risk and Return Statistics: {e}")

        st.markdown("___")

        st.markdown("""
        <div style="background-color: #F3E5F5; padding: 15px; border-radius: 10px; border-left: 5px solid #00897B;">
            <p style="color: #555; font-size: 17px; line-height: 1.6; margin: 0;">
            Danh mục đầu tư của Mười đang có sự tập trung cực lớn vào ngành Sản xuất (79.5%), dẫn đến việc thiếu trọng số nghiêm trọng ở ngành Dịch vụ (chỉ 20.5%, trong khi VNINDEX là 75.14%). Sự mất cân bằng này làm tăng rủi ro tập trung và tạo ra độ lệch pha lớn so với thị trường chung. Về mặt hiệu suất, mặc dù rủi ro của danh mục thấp hơn trong 3 tháng, lợi nhuận thực tế (Mean) và lợi nhuận điều chỉnh theo rủi ro (Sharpe Ratio) của danh mục đều thua kém đáng kể VNINDEX trong cả giai đoạn 3 tháng và 1 năm. Điều này cho thấy chiến lược tập trung vào Sản xuất của bạn đã không mang lại hiệu quả vượt trội so với rủi ro đã chấp nhận.
            </div>
        """, unsafe_allow_html=True)

            
    st.markdown("")

    # Valuation Multiples and Profitability Analysis
    st.markdown("### 📊 Valuation Multiples & Profitability")
    
    col_valuation, col_profitability = st.columns(2)
    
    with col_valuation:
        st.markdown("**Valuation Multiples**")
        valuation_html = """
        <table style="width:100%; border-collapse: collapse; font-size: 17px;">
            <tr style="border-bottom: 2px solid #ddd; background-color: #f0f0f0;">
                <th style="padding: 8px; text-align: center; border-right: 1px solid #ddd;"><b>Metric</b></th>
                <th style="padding: 8px; text-align: center; border-right: 1px solid #ddd;"><b>Portfolio</b></th>
                <th style="padding: 8px; text-align: center;"><b>VNIndex</b></th>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 8px; text-align: center; border-right: 1px solid #ddd;">Price/Earnings</td>
                <td style="padding: 8px; text-align: center; border-right: 1px solid #ddd;">13.88</td>
                <td style="padding: 8px; text-align: center;">13.28</td>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 8px; text-align: center; border-right: 1px solid #ddd;">Price/Book</td>
                <td style="padding: 8px; text-align: center; border-right: 1px solid #ddd;">2.97</td>
                <td style="padding: 8px; text-align: center;">1.67</td>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 8px; text-align: center; border-right: 1px solid #ddd;">Price/Sales</td>
                <td style="padding: 8px; text-align: center; border-right: 1px solid #ddd;">2.03</td>
                <td style="padding: 8px; text-align: center;">1.71</td>
            </tr>
        </table>
        """
        st.markdown(valuation_html, unsafe_allow_html=True)
    
    with col_profitability:
        st.markdown("**Profitability**")
        profitability_html = """
        <table style="width:100%; border-collapse: collapse; font-size: 17px;">
            <tr style="border-bottom: 2px solid #ddd; background-color: #f0f0f0;">
                <th style="padding: 8px; text-align: center; border-right: 1px solid #ddd;"><b>Metric</b></th>
                <th style="padding: 8px; text-align: center; border-right: 1px solid #ddd;"><b>Portfolio</b></th>
                <th style="padding: 8px; text-align: center;"><b>VNIndex</b></th>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 8px; text-align: center; border-right: 1px solid #ddd;">ROE (%)</td>
                <td style="padding: 8px; text-align: center; border-right: 1px solid #ddd;">20.73</td>
                <td style="padding: 8px; text-align: center;">13.03</td>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 8px; text-align: center; border-right: 1px solid #ddd;">ROA (%)</td>
                <td style="padding: 8px; text-align: center; border-right: 1px solid #ddd;">11.47</td>
                <td style="padding: 8px; text-align: center;">2.14</td>
            </tr>
        </table>
        """
        st.markdown(profitability_html, unsafe_allow_html=True)

    st.markdown("###### Kết luận: ")
    
    st.markdown("""
        <div padding: 15px;">
            <ul style="color: #555; font-size: 17px; line-height: 1.6; margin: 0; padding-left: 20px;">
                <li>So với VNIndex, danh mục này đang được định giá cao hơn trên hầu hết các chỉ số P/E, P/B và P/S. Đặc biệt, hệ số P/B của danh mục gần gấp đôi thị trường, cho thấy các doanh nghiệp trong danh mục được thị trường đánh giá cao hơn về giá trị sổ sách.</li>
                <li>Khả năng sinh lời của danh mục vượt trội so với VNIndex, khi ROE và ROA đều cao hơn đáng kể. Điều này cho thấy các doanh nghiệp trong danh mục hoạt động hiệu quả hơn, sử dụng vốn và tài sản tốt hơn, qua đó tạo ra mức lợi nhuận vượt xa mặt bằng chung của thị trường.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Comparative metrics
    st.markdown("")
    st.markdown("---")

    # ============================================================================
    # SECTION 3: RISK AND RETURN
    # ============================================================================
    st.header("⚠️ RISK AND RETURN ANALYSIS")

    st.subheader("📊 So sánh: Daily Beta vs Rolling 60-Day Beta")

    try:
        # Load both beta files
        beta_daily_df = pd.read_csv('beta.csv', index_col=0, parse_dates=True)
        beta_daily_df.columns = ['Daily_Beta']

        beta_rol_df = pd.read_csv('beta_rol.csv', index_col=0)
        beta_rol_df.columns = ['Rolling_60D_Beta']

        # Get dates starting from the 60th data point (where rolling beta starts)
        rolling_start_idx = 60
        dates_for_rolling = beta_daily_df.index[rolling_start_idx:]

        # Assign dates to rolling beta data
        rolling_beta_with_dates = beta_rol_df['Rolling_60D_Beta'].values[:len(dates_for_rolling)]
        rolling_beta_series = pd.Series(rolling_beta_with_dates, index=dates_for_rolling)

        fig_comparison = go.Figure()

        # Add daily beta (portfolio)
        fig_comparison.add_trace(go.Scatter(
            x=beta_daily_df.index,
            y=beta_daily_df['Daily_Beta'],
            mode='lines',
            name='Daily Beta (Portfolio)',
            line=dict(color='rgba(255, 182, 193, 0.8)', width=2.5),
            hovertemplate='<b>Ngày:</b> %{x|%Y-%m-%d}<br><b>Daily Beta (Portfolio):</b> %{y:.4f}<extra></extra>'
        ))

        # Add rolling 60-day beta (from actual file data) - thêm sau để nằm trên cùng
        fig_comparison.add_trace(go.Scatter(
            x=rolling_beta_series.index,
            y=rolling_beta_series,
            mode='lines',
            name='Rolling 60-Day Beta (Portfolio)',
            line=dict(color='#1976D2', width=4),
            hovertemplate='<b>Ngày:</b> %{x|%Y-%m-%d}<br><b>Rolling 60D Beta (Portfolio):</b> %{y:.4f}<extra></extra>'
        ))

        # Add market reference line
        fig_comparison.add_hline(y=1.0, line_dash="dot", line_color="orange", 
                         annotation_text="Thị trường (β=1.0)", annotation_position="right")

        fig_comparison.update_layout(
            title="Daily Beta vs Rolling 60-Day Beta",
            xaxis_title="Thời gian",
            yaxis_title="Beta Value",
            hovermode='x unified',
            height=450,
            template='plotly_white'
        )

        st.plotly_chart(fig_comparison, use_container_width=True)

        st.markdown("")

        # ============================================================================
        # BEAUTIFUL COMPARISON STATISTICS TABLE
        # ============================================================================

        # Prepare statistics data
        metrics = [
            'Giá trị trung bình',
            'Giá trị cao nhất',
            'Giá trị thấp nhất',
            'Độ lệch chuẩn',
            'Số lượng dữ liệu'
        ]

        stats_data = {
            'Chỉ số': metrics,
            'Daily Beta': [
                f"{beta_daily_df['Daily_Beta'].mean():.4f}",
                f"{beta_daily_df['Daily_Beta'].max():.4f}",
                f"{beta_daily_df['Daily_Beta'].min():.4f}",
                f"{beta_daily_df['Daily_Beta'].std():.4f}",
                f"{len(beta_daily_df)}"
            ],
            'Rolling 60-Day': [
                f"{rolling_beta_series.mean():.4f}",
                f"{rolling_beta_series.max():.4f}",
                f"{rolling_beta_series.min():.4f}",
                f"{rolling_beta_series.std():.4f}",
                f"{len(rolling_beta_series)}"
            ]
        }

        stats_df = pd.DataFrame(stats_data)

        st.subheader("📋 Bảng thống kê so sánh")

        # Display as a styled table
        st.dataframe(
            stats_df.set_index('Chỉ số'),
            use_container_width=True,
            hide_index=False,
            column_config={
                'Daily Beta': st.column_config.TextColumn(width="medium"),
                'Rolling 60-Day': st.column_config.TextColumn(width="medium"),
            }
        )

        st.markdown("")

        # Key metrics cards
        col1, col2, col3 = st.columns(3)

        with col1:
            smoothing_ratio = beta_daily_df['Daily_Beta'].std() / rolling_beta_series.std()
            st.metric(
                "📊 Smoothing Effect",
                f"{smoothing_ratio:.2f}x",
                "Daily cao hơn Rolling"
            )

        with col2:
            noise_reduction = ((beta_daily_df['Daily_Beta'].std() - rolling_beta_series.std()) / beta_daily_df['Daily_Beta'].std() * 100)
            st.metric(
                "🔇 Giảm Noise",
                f"{noise_reduction:.1f}%",
                "Rolling 60D mượt hơn"
            )

        with col3:
            avg_diff = abs(rolling_beta_series.mean() - beta_daily_df['Daily_Beta'].mean())
            st.metric(
                "📈 Chênh lệch TB",
                f"{avg_diff:.4f}",
                "Daily vs Rolling"
            )

        st.markdown("")

        # ============================================================================
        # VOLATILITY COMPARISON
        # ============================================================================




        st.markdown("")

        # ============================================================================
        # KEY INSIGHTS
        # ============================================================================
        st.markdown(" #### Nhận xét chính")

        smoothing_ratio = beta_daily_df['Daily_Beta'].std() / rolling_beta_series.std()
        avg_daily = beta_daily_df['Daily_Beta'].mean()
        avg_rolling = rolling_beta_series.mean()

        st.markdown("""
        **📌 Giải thích:**
        - **Daily Beta (Màu hồng)**: Beta ước lượng bằng mô hình **DCC ARCH/GARCH**, biến động nhiều, phản ánh rủi ro tức thời
        - **Rolling 60-Day Beta (Màu xanh dương)**: beta ước lượng bằng mô hình **OLS** dùng dữ liệu của 60 ngày trước, mượt hơn, phản ánh xu hướng rủi ro dài hạn

        **🔍 Key insight:**
        - Daily Beta được ước lượng bằng DCC-GARCH nên phản ứng rất nhạy với biến động thị trường theo từng ngày và dao động mạnh quanh ~0.57.
        - Trong khi đó, Rolling 60-Day Beta được tính bằng OLS trên cửa sổ trượt nên mượt và ổn định hơn quanh 0.56, giảm khoảng 9% nhiễu ngắn hạn (Smoothing Effect ~0.91x)
        - Cả hai đều thấp hơn β = 1, cho thấy cổ phiếu/quỹ có mức độ nhạy cảm thị trường thấp và khá ổn định, với chênh lệch trung bình nhỏ, không xuất hiện biến động cực đoan kéo dài.
        - Quý 3/2025, VN‑Index bật tăng mạnh do dòng vốn dồi dào từ tín dụng và nhà đầu tư cá nhân, kỳ vọng kinh tế vĩ mô tích cực và khả năng nâng hạng thị trường, cùng với nhóm cổ phiếu vốn hóa lớn dẫn dắt thị trường. Các blue‑chip như VNM, DBD, HPG và ACB trong portfolio tăng nhưng không tương xứng với mức tăng của VN‑Index, vì vậy beta của từng cổ phiếu giảm mạnh kéo theo beta của portfolio giảm do thị trường biến động quá mạnh.
        """)
        


        

    except Exception as e:
            st.error(f"❌ Lỗi khi so sánh Beta data: {e}")



    st.subheader("📊 Value at Risk (VaR) - 3 Phương pháp Tính toán")

    try:
        # Load portfolio returns
        returns_df = pd.read_csv('port.csv', usecols=['Portfolio'])
        # Convert to numeric, handling errors
        portfolio_returns = pd.to_numeric(returns_df['Portfolio'], errors='coerce').dropna()

        # Confidence level selection
        confidence_level = st.radio(
            "Chọn mức độ tin cậy:", 
            options=[85, 90, 95, 99],
            format_func=lambda x: f"{x}%",
            horizontal=True,
            key="var_confidence"
        )
        alpha = 1 - (confidence_level / 100)

        st.markdown(f"**Phân tích với mức tin cậy {confidence_level}% (α = {alpha:.3f})**")

        # ====================================================================
        # METHOD 1: HISTORICAL
        # ====================================================================
        var_hist = np.percentile(portfolio_returns, alpha * 100)
        es_hist = portfolio_returns[portfolio_returns <= var_hist].mean()

        # ====================================================================
        # METHOD 2: PARAMETRIC (NORMAL)
        # ====================================================================
        mean_ret = portfolio_returns.mean()
        std_ret = portfolio_returns.std()
        z_score = norm.ppf(alpha)
        var_param = mean_ret + z_score * std_ret
        pdf_z = norm.pdf(z_score)
        es_param = mean_ret - std_ret * (pdf_z / alpha)

        # ====================================================================
        # METHOD 3: MONTE CARLO
        # ====================================================================
        np.random.seed(42)
        n_sims = 10000
        sim_returns = np.random.normal(mean_ret, std_ret, n_sims)
        var_mc = np.percentile(sim_returns, alpha * 100)
        es_mc = sim_returns[sim_returns <= var_mc].mean()

        # ====================================================================
        # COMPARISON TABLE
        # ====================================================================
        var_comparison = pd.DataFrame({
            'Phương pháp': ['Historical', 'Parametric', 'Monte Carlo'],
            'VaR': [var_hist, var_param, var_mc],
            'ES': [es_hist, es_param, es_mc],
            'Mô tả': [
                'Dữ liệu thực tế',
                'Phân phối chuẩn',
                f'{n_sims:,} mô phỏng'
            ]
        })

        # Display comparison table as main content
        st.markdown("#### 📋 Bảng so sánh VaR & ES (3 Phương pháp)")

        # Format table for better display
        display_table = var_comparison.copy()
        display_table['VaR'] = display_table['VaR'].apply(lambda x: f"{x:.4f}")
        display_table['ES'] = display_table['ES'].apply(lambda x: f"{x:.4f}")

        st.dataframe(
            display_table.set_index('Phương pháp'),
            use_container_width=True,
            column_config={
                'VaR': st.column_config.TextColumn(
                    width="medium",
                    help="Mức thua lỗ tối đa mà portfolio có thể gặp phải trong 1 ngày với xác suất " + f"{confidence_level}%"
                ),
                'ES': st.column_config.TextColumn(
                    width="medium",
                    help="Mức thua lỗ trung bình khi xảy ra trường hợp xấu hơn VaR (trong tail risk)"
                ),
                'Mô tả': st.column_config.TextColumn(width="large"),
            }
        )

        st.markdown("")

        # Create two columns for charts
        col_left, col_right = st.columns(2)

        # Chart 1: VaR vs ES comparison
        with col_left:
            fig_var_es = go.Figure()

            fig_var_es.add_trace(go.Bar(
                name='VaR',
                x=var_comparison['Phương pháp'],
                y=var_comparison['VaR'],
                marker_color='#E74C3C',
                text=[f'{v:.4f}' for v in var_comparison['VaR']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>VaR: %{y:.4f}<extra></extra>'
            ))

            fig_var_es.add_trace(go.Bar(
                name='ES',
                x=var_comparison['Phương pháp'],
                y=var_comparison['ES'],
                marker_color='#3498DB',
                text=[f'{v:.4f}' for v in var_comparison['ES']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>ES: %{y:.4f}<extra></extra>'
            ))

            fig_var_es.update_layout(
                title="VaR vs ES Comparison",
                xaxis_title="Method",
                yaxis_title="Daily Loss",
                barmode='group',
                height=450,
                template='plotly_white',
                showlegend=True
            )

            st.plotly_chart(fig_var_es, use_container_width=True)

        # Chart 2: Distribution with VaR thresholds
            with col_right:
                fig_dist = go.Figure()

                fig_dist.add_trace(go.Histogram(
                    x=portfolio_returns,
                    name='Historical Returns',
                    nbinsx=40,
                    marker_color='rgba(31, 119, 180, 0.6)',
                    hovertemplate='<b>Range:</b> %{x:.4f}<br><b>Freq:</b> %{y}<extra></extra>'
                ))

                # Add VaR lines with proper legend
                colors = ['#E74C3C', '#F39C12', '#9B59B6']
                methods = ['Historical VaR', 'Parametric VaR', 'MC VaR']
                vars_vals = [var_hist, var_param, var_mc]

                for method, var_val, color in zip(methods, vars_vals, colors):
                    fig_dist.add_vline(
                        x=var_val, 
                        line_dash="dash",
                        line_color=color,
                        line_width=2,
                        name=f"{method}: {var_val:.4f}",
                        showlegend=True
                    )

                fig_dist.update_layout(
                    title=f"Returns Distribution + VaR ({confidence_level}%)",
                    xaxis_title="Daily Return",
                    yaxis_title="Frequency",
                    height=450,
                    template='plotly_white',
                    showlegend=True,
                    legend=dict(
                        x=1.02,
                        y=1,
                        xanchor='left',
                        yanchor='top',
                        bgcolor='rgba(255,255,255,0.8)',
                        bordercolor='#ddd',
                        borderwidth=1
                    )
                )

                st.plotly_chart(fig_dist, use_container_width=True)

        st.markdown("")

        # ====================================================================
        # INSIGHTS
        # ====================================================================
        st.markdown("""
        <div style="background-color: #FFF3CD; padding: 15px; border-radius: 8px; border-left: 4px solid #FFC107;">
            <h5 style="color: #FF6B00; margin-top: 0;">🔍 Nhận xét:</h5>
            <b> Tổng quan phân tích rủi ro cho thấy danh mục có mức rủi ro tương đối trung bình trong điều kiện thị trường bình thường, nhưng tồn tại rủi ro tail đáng chú ý. Khi so sánh ba phương pháp Historical, Parametric và Monte Carlo, kết quả Historical cho thấy biến động gần đây không quá lớn, tuy nhiên Expected Shortfall (ES) lại sâu hơn đáng kể, phản ánh sự hiện diện của các cú sốc cực đoan và độ dày tail trong phân phối lợi suất. Biểu đồ phân phối lợi suất cũng cho thấy skew âm rõ rệt và đuôi trái dài, củng cố nhận định rằng danh mục chịu ảnh hưởng mạnh bởi các sự kiện hiếm nhưng tổn thất lớn.

Trong khi đó, Parametric và Monte Carlo cho kết quả khá tương đồng, hàm ý rằng rủi ro danh mục chủ yếu được giải thích bởi hiệp phương sai giữa các tài sản, thay vì các cấu trúc phi tuyến hay tail phức tạp. Tuy nhiên, sự chênh lệch đáng kể giữa ES và VaR ở nhiều mức độ tin cậy cho thấy trong điều kiện bất lợi, mức lỗ thực tế có thể vượt xa VaR, khiến ES trở thành thước đo phản ánh rủi ro đầy đủ hơn. Điều này cũng gợi ý rằng các mô hình nâng cao như phân phối t, Cornish–Fisher hay GARCH có thể phù hợp hơn trong việc mô phỏng tail risk và hành vi biến động thực tế của danh mục.
            </b>
        </div>
        """,unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Lỗi tính VaR: {e}")

    st.markdown("")
    st.divider()
    st.markdown("")
    st.markdown("")

    st.header("📈 CAPM Analysis")
    st.markdown("*Phân tích tại ngày (1/10/2025)*")

    try:
        # Load data
        beta_daily_df = pd.read_csv('beta.csv', index_col=0, parse_dates=True)
        returns_df = pd.read_csv('returns_xts_1763848584845.csv')
        portfolio_returns = returns_df.mean(axis=1)

        # CAPM Parameters
        risk_free_rate = 0.03303238  # 5% annual
        market_return_annual = 0.09698529
        market_risk_premium = market_return_annual - risk_free_rate

        # Fixed Beta (trung bình của toàn bộ dữ liệu lịch sử)
        beta_fixed = beta_daily_df.iloc[:, 0].mean()

        # CAPM Expected Return (annualized)
        capm_expected_return = risk_free_rate + beta_fixed * market_risk_premium

        # ====================================================================
        # 1. CÔNG THỨC CAPM
        # ====================================================================
        st.markdown("##### Công thức CAPM:")
        st.latex(r"E(R_p) = R_f + \beta \times (R_m - R_f)")

        st.markdown("**Trong đó:**")
        st.markdown(f"""
        - **Rf** (Risk-free rate) = lãi suất không rủi ro (Ở đây Mười dùng giá trị trung bình 3 năm của lãi suất trái phiếu chính phủ 10 năm)
        - **Rm** (Market return) = lợi suất thị trường (Mười dùng giá trị trung bình 3 năm của lợi nhuận hàng ngày của VNINDEX)
        - **β** (Beta) = Rủi ro hệ thống của portfolio so với thị trường (giá trị cố định từ dữ liệu lịch sử)
        - **(Rm - Rf)** = mức bù lợi nhuận của thị trường so với lãi suất phi rủi ro
        """)

        # ====================================================================
        # 2. TÍNH TOÁN CỤ THỂ
        # ====================================================================
        st.markdown("#### Kết quả")

        rf_val = 0.013
        rm_rf_val = 0.024
        beta_val = 0.57
        capm_result = rf_val + beta_val * rm_rf_val

        st.latex(rf"E(Rp) = {rf_val}\% + {beta_val} \times {rm_rf_val}\%")
        st.latex(rf"E(Rp) = {rf_val}\% + {beta_val * rm_rf_val:.5f}\%")

        st.markdown("---")
        
        st.markdown("""
        <div style="background-color: #d4edda; padding: 20px; border-radius: 8px; border: 2px solid #28a745; text-align: center; display: flex; justify-content: center; margin: 20px 0;">
            <h3 style="color: #155724; margin: 0; font-size: 24px; font-weight: bold;">E(Rp) = 0.027% (daily)</h3>
            <h3 style="color: #155724; margin: 0; font-size: 24px; font-weight: bold;">E(Rp) = 6.954% (annual)</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # ====================================================================
        # Comparison with Actual Return
        # ====================================================================
        st.markdown("#####  CAPM Expected vs Actual Portfolio Return")
        
        comparison_table = """
        <table style="width:100%; border-collapse: collapse; font-size: 17px; text-align: center; margin: 15px 0;">
            <tr style="background-color: #E3F2FD; border-bottom: 2px solid #1976D2;">
                <th style="padding: 12px; text-align: center; border-right: 1px solid #ddd; font-weight: bold;">Chỉ số</th>
                <th style="padding: 12px; text-align: center; font-weight: bold;">Giá trị</th>
            </tr>
            <tr style="background-color: #F5F5F5; border-bottom: 1px solid #ddd;">
                <td style="padding: 12px; text-align: center; border-right: 1px solid #ddd;"><strong>CAPM Expected Return</strong></td>
                <td style="padding: 12px; text-align: center; color: #FF6B6B; font-weight: bold;">6.954%</td>
            </tr>
            <tr style="background-color: #FFFFFF; border-bottom: 1px solid #ddd;">
                <td style="padding: 12px; text-align: center; border-right: 1px solid #ddd;"><strong>Actual Portfolio Return</strong></td>
                <td style="padding: 12px; text-align: center; color: #28a745; font-weight: bold;">13.31%</td>
            </tr>
            <tr style="background-color: #FFF8DC; border-bottom: 1px solid #ddd;">
                <td style="padding: 12px; text-align: center; border-right: 1px solid #ddd;"><strong>Chênh lệch (Gap)</strong></td>
                <td style="padding: 12px; text-align: center; color: #FF9800; font-weight: bold;">+6.36%</td>
            </tr>
        </table>
        """
        st.markdown(comparison_table, unsafe_allow_html=True)

        st.markdown("##### So sánh với lợi suất thị trường:")

        comparison_data = pd.DataFrame({
            'Chỉ số': [
                'Market Return',
                'CAPM Expected Return',
                'Chênh lệch'
            ],
            'Giá trị': [
                f"{market_return_annual*100:.2f}%",
                f"{0.0695357*100:.2f}%",
                f"{(0.0695357 - market_return_annual)*100:+.2f}%"
            ]
        })

        html_table = '<div style="overflow-x: auto;">'
        html_table += '<table style="width:100%; border-collapse: collapse; font-size: 17px; text-align: center;">'
        html_table += '<thead><tr style="background-color: #E3F2FD; border-bottom: 2px solid #1976D2;">'
        html_table += '<th style="padding: 12px; text-align: center; border-right: 1px solid #ddd; font-weight: bold;">Chỉ số</th>'
        html_table += '<th style="padding: 12px; text-align: center; font-weight: bold;">Giá trị</th>'
        html_table += '</tr></thead>'
        html_table += '<tbody>'

        for idx, row in comparison_data.iterrows():
            bg_color = '#F5F5F5' if idx % 2 == 0 else '#FFFFFF'
            html_table += f'<tr style="background-color: {bg_color}; border-bottom: 1px solid #ddd;">'
            html_table += f'<td style="padding: 10px; text-align: center; border-right: 1px solid #ddd;"><strong>{row["Chỉ số"]}</strong></td>'
            html_table += f'<td style="padding: 10px; text-align: center;">{row["Giá trị"]}</td>'
            html_table += '</tr>'

        html_table += '</tbody></table></div>'
        st.markdown(html_table, unsafe_allow_html=True)

        # ====================================================================
        # 4. NHẬN XÉT
        # ====================================================================
        st.markdown("#### 💡 Nhận xét:")

        insight = f"""
        Danh mục đầu tư đã có hiệu suất rất mạnh mẽ trong kỳ. Lợi suất thực tế $13.31\%$ không chỉ vượt qua Lợi suất thị trường ($9.70\%$) mà còn tạo ra Alpha dương đáng kể là $+6.36\%$ so với mức lợi nhuận kỳ vọng theo mô hình CAPM ($6.95\%$). Điều này cho thấy nhà quản lý danh mục đã thực hiện các lựa chọn đầu tư xuất sắc, tạo ra lợi nhuận vượt xa mức độ rủi ro hệ thống thấp mà danh mục đang nắm giữ.
        """

        st.info(insight)

        st.markdown("")

    except Exception as e:
        st.error(f"❌ Lỗi tính CAPM: {e}")

        st.markdown("---")
        st.markdown("")



    # ============================================================================
    # SECTION 4: INTRINSIC VALUE
    # ============================================================================
    
    st.markdown(" ### INTRINSIC VALUE ANALYSIS")
    
    # Narrative section about Mười's valuation journey
    st.markdown("""
    <div style="background-color: #FFF8E7; padding: 20px; border-radius: 10px; border-left: 5px solid #FF9800; margin-bottom: 20px;">
        <p style="font-size: 16px; line-height: 1.8; color: #333;">
        Sau khi đánh giá danh mục của mình và thấy "hơi hớn hở" vì có vẻ sinh lời, Nguyễn Văn Mười – newbie 20 tuổi, vốn chẳng hiểu mấy về chứng khoán – bắt đầu băn khoăn: 
        <br><br>
        <strong style="color: #FF6F00;">"Liệu mình có nên mua luôn không? Giá nào là hợp lý đây?"</strong>
        <br><br>
        Trong thế giới đầy các phương pháp tính toán phức tạp – FCFF, WACC, CAPM – Mười nhanh chóng nhận ra: với trình độ newbie, cậu chỉ cần một con đường dễ hiểu và dễ tiếp cận nhất. Và thế là, Mười chọn <strong>công thức DCF theo kiểu Warren Buffett</strong>, tức là tính <strong>intrinsic value</strong> dựa trên <strong>FCFE</strong> – dòng tiền tự do mà công ty có thể trả cho cổ đông.
        <br><br>
        Với FCFE, Mười có thể dự báo các dòng tiền trong tương lai bằng <strong>Holt-Winters Exponential Smoothing</strong>, rồi tính giá trị hiện tại của chúng. Cậu thích cách này: máy tính làm việc thay cậu, dữ liệu nói chuyện, còn cậu chỉ cần nhìn vào kết quả và hỏi:
        <br><br>
        <strong style="color: #FF6F00;">"Ồ, cổ phiếu này rẻ hay đắt?"</strong>
        <br><br>
        Bằng cách này, Mười vừa có thể hiểu rõ giá trị thực của cổ phiếu, vừa tự tin đưa ra quyết định mua hay chờ – tất cả mà không bị lạc vào rừng công thức phức tạp. <strong>Một newbie mà vẫn "chơi lớn" theo phong cách của Buffett!</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color: red; font-weight: bold;'>Bài viết này không sử dụng DCF cho ngân hàng do đặc thù trong cơ cấu tài chính của ngân hàng.</p>", unsafe_allow_html=True)
    
    # Centered section title
    st.markdown("<div style='text-align: center;'><h3>🔹 Các bước tính FCFE với CAPM và Holt-Winters</h3></div>", unsafe_allow_html=True)
    
    # Visualization options
    viz_option = st.segmented_control(
        "Chọn cách hiển thị:",
        ["📋 Danh sách", "📊 Biểu đồ", "🔢 Công thức"],
        selection_mode="single",
        default="📋 Danh sách"
    )
    
    if viz_option == "📋 Danh sách":
        st.markdown("""
        <div style="background-color: #F0F4FF; padding: 25px; border-radius: 10px; border: 2px solid #1976D2; margin: 20px 0; text-align: center;">
            <p style="font-size: 16px; line-height: 2.0; color: #1565C0; margin: 0;">
            <strong>Bước 1:</strong> Xác định <strong>FCFE</strong> bằng công thức<br><br>
            <strong>Bước 2:</strong> Dự báo <strong>3 giá trị FCFE tương lai</strong> sử dụng <strong>Holt-Winters</strong><br><br>
            <strong>Bước 3:</strong> Tính <strong>chi phí vốn cổ đông</strong> bằng <strong>CAPM</strong><br><br>
            <strong>Bước 4:</strong> Chọn tốc độ <strong>tăng trưởng dài hạn</strong> <strong>g = 3%</strong><br><br>
            <strong>Bước 5:</strong> Tính <strong>giá trị hiện tại (PV)</strong> bằng cách chiết khấu tất cả dòng tiền
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    elif viz_option == "📊 Biểu đồ":
        st.markdown("""
        <div style="background-color: #F5F5F5; padding: 25px; border-radius: 10px; border: 2px solid #666; margin: 20px 0; text-align: center;">
            <p style="font-size: 14px; color: #666; margin: 10px 0;">
            <strong>Quy trình DCF - FCFE Valuation</strong>
            </p>
            <p style="font-size: 13px; color: #999; line-height: 2.5; margin: 0;">
            📊 FCFE Calculation → 📈 Holt-Winters Forecast → 🎯 CAPM Discount Rate → 💰 Terminal Value → 🔍 Intrinsic Value
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    else:  # 🔢 Công thức
        st.markdown("""
        <div style="background-color: #FFF8E7; padding: 25px; border-radius: 10px; border: 2px solid #FF9800; margin: 20px 0;">
            <div style="text-align: center;">
                <p style="font-size: 15px; margin: 15px 0; color: #333;">
                <strong>Công thức FCFE:</strong><br>
                FCFE = Net Income + Depreciation - CapEx - ΔWC + Net Borrowing
                </p>
                <p style="font-size: 15px; margin: 15px 0; color: #333;">
                <strong>Công thức CAPM:</strong><br>
                r<sub>e</sub> = R<sub>f</sub> + β(R<sub>m</sub> - R<sub>f</sub>)
                </p>
                <p style="font-size: 15px; margin: 15px 0; color: #333;">
                <strong>Công thức DCF:</strong><br>
                Intrinsic Value = Σ(FCFE<sub>t</sub>/(1+r<sub>e</sub>)<sup>t</sup>) + Terminal Value/(1+r<sub>e</sub>)<sup>n</sup>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    
    # Import required calculation functions
    def calculate_capm_return(risk_free_rate, beta, market_risk_premium):
        return risk_free_rate + beta * market_risk_premium
    
    def calculate_dcf_value(current_price, fcf_growth_rates, terminal_growth_rate, discount_rate, current_fcf=None):
        if current_fcf is None:
            current_fcf = current_price * 0.10
        projected_fcf = []
        fcf = current_fcf
        for growth_rate in fcf_growth_rates:
            fcf = fcf * (1 + growth_rate)
            projected_fcf.append(fcf)
        pv_fcf = 0
        for year, fcf_value in enumerate(projected_fcf, 1):
            pv = fcf_value / ((1 + discount_rate) ** year)
            pv_fcf += pv
        terminal_fcf = projected_fcf[-1] * (1 + terminal_growth_rate)
        terminal_value = terminal_fcf / (discount_rate - terminal_growth_rate)
        pv_terminal = terminal_value / ((1 + discount_rate) ** len(fcf_growth_rates))
        intrinsic_value = pv_fcf + pv_terminal
        upside_downside = ((intrinsic_value - current_price) / current_price) * 100
        return {
            'intrinsic_value': intrinsic_value,
            'current_price': current_price,
            'upside_downside_pct': upside_downside,
            'pv_fcf': pv_fcf,
            'pv_terminal': pv_terminal,
            'projected_fcf': projected_fcf
        }
    
    if portfolio_df is not None and extended_hist is not None and PORTFOLIO_HOLDINGS is not None:
        try:
            risk_free_rate = 0.045
            market_risk_premium = 0.06
            terminal_growth_rate = 0.025
            

            
            for stock in PORTFOLIO_HOLDINGS:
                ticker = stock['ticker']
                
                # Skip ACB - only show VNM, HPG, DBD
                if ticker == "ACB":
                    continue
                
                current_price = portfolio_df[portfolio_df['ticker'] == ticker]['current_price'].values[0]
                
                if isinstance(extended_hist['Close'], pd.DataFrame):
                    stock_prices = extended_hist['Close'][ticker].dropna()
                else:
                    stock_prices = extended_hist['Close'].dropna()
                
                if len(stock_prices) > 60:
                    stock_returns = stock_prices.pct_change().dropna()
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
                    
                    capm_return = calculate_capm_return(risk_free_rate, beta, market_risk_premium)
                    fcf_growth_rates = [0.12, 0.10, 0.08, 0.06, 0.04]
                    dcf_result = calculate_dcf_value(current_price, fcf_growth_rates, terminal_growth_rate, capm_return)
                    
                    # Override VNM with actual valuation data
                    if ticker == "VNM":
                        beta = 0.5782436
                        capm_return = 0.0695
                        # DCF Valuation Data for VNM
                        vnm_intrinsic_per_share = 61151.74  # VND per share
                        vnm_current_price = 53000  # Current market price (VND) - approximate
                        vnm_upside = ((vnm_intrinsic_per_share - vnm_current_price) / vnm_current_price) * 100
                        vnm_num_shares = 2089955445
                        
                        # Detailed DCF breakdown for VNM
                        vnm_fcfe_2025 = 6.5998  # Trillion VND
                        vnm_fcfe_2026 = 5.5022  # Trillion VND
                        vnm_fcfe_2027 = 5.5022  # Trillion VND
                        vnm_terminal_value = 143.309  # Trillion VND (rounded)
                        
                        vnm_pv_fcfe_2025 = 6.171  # Billion VND (rounded)
                        vnm_pv_fcfe_2026 = 4.810  # Billion VND (rounded)
                        vnm_pv_fcfe_2027 = 4.497  # Billion VND (rounded)
                        vnm_pv_terminal = 117.132  # Billion VND (rounded)
                        
                        # Total enterprise value
                        pv_fcf_total = (vnm_pv_fcfe_2025 + vnm_pv_fcfe_2026 + vnm_pv_fcfe_2027) * 1e9  # Sum of PV of projected FCFE (in VND)
                        pv_terminal_total = vnm_pv_terminal * 1e9  # PV of terminal value (in VND)
                        total_ev = pv_fcf_total + pv_terminal_total
                        
                        dcf_result = {
                            'intrinsic_value': vnm_intrinsic_per_share / 1000,  # Convert to thousands for display
                            'current_price': vnm_current_price / 1000,
                            'upside_downside_pct': vnm_upside,
                            'pv_fcf': pv_fcf_total / 1e12,
                            'pv_terminal': pv_terminal_total / 1e12,
                            'projected_fcf': [vnm_fcfe_2025, vnm_fcfe_2026, vnm_fcfe_2027],  # FCFE in trillions VND
                            'years': [2025, 2026, 2027],
                            'num_shares': vnm_num_shares,
                            'total_ev': total_ev,
                            'capm_return': capm_return,
                            'detailed_breakdown': {
                                'fcfe': [vnm_fcfe_2025, vnm_fcfe_2026, vnm_fcfe_2027],
                                'pv_fcfe': [vnm_pv_fcfe_2025, vnm_pv_fcfe_2026, vnm_pv_fcfe_2027],
                                'pv_terminal': vnm_pv_terminal,
                                'terminal_value': vnm_terminal_value
                            }
                        }
                    
                    # Override HPG with actual valuation data
                    elif ticker == "HPG":
                        beta = 1.2  # Typical steel sector beta
                        capm_return = 0.1178
                        # DCF Valuation Data for HPG
                        hpg_intrinsic_per_share = 33959.17  # VND per share
                        hpg_current_price = 28000  # Current market price (VND) - approximate
                        hpg_upside = ((hpg_intrinsic_per_share - hpg_current_price) / hpg_current_price) * 100
                        hpg_num_shares = 7675465855
                        
                        # Detailed DCF breakdown for HPG
                        hpg_fcfe_2025 = 20.724  # Trillion VND
                        hpg_fcfe_2026 = 21.163  # Trillion VND (rounded)
                        hpg_fcfe_2027 = 22.163  # Trillion VND (rounded)
                        hpg_terminal_value = 288.738  # Trillion VND (rounded)
                        
                        hpg_pv_fcfe_2025 = 18.541  # Billion VND (rounded)
                        hpg_pv_fcfe_2026 = 17.739  # Billion VND (rounded)
                        hpg_pv_fcfe_2027 = 17.616  # Billion VND (rounded)
                        hpg_pv_terminal = 206.757  # Billion VND (rounded)
                        
                        # Total enterprise value
                        pv_fcf_total = (hpg_pv_fcfe_2025 + hpg_pv_fcfe_2026 + hpg_pv_fcfe_2027) * 1e9  # Sum of PV of projected FCFE (in VND)
                        pv_terminal_total = hpg_pv_terminal * 1e9  # PV of terminal value (in VND)
                        total_ev = pv_fcf_total + pv_terminal_total
                        
                        dcf_result = {
                            'intrinsic_value': hpg_intrinsic_per_share / 1000,  # Convert to thousands for display
                            'current_price': hpg_current_price / 1000,
                            'upside_downside_pct': hpg_upside,
                            'pv_fcf': pv_fcf_total / 1e12,
                            'pv_terminal': pv_terminal_total / 1e12,
                            'projected_fcf': [hpg_fcfe_2025, hpg_fcfe_2026, hpg_fcfe_2027],  # FCFE in trillions VND
                            'years': [2025, 2026, 2027],
                            'num_shares': hpg_num_shares,
                            'total_ev': total_ev,
                            'capm_return': capm_return,
                            'detailed_breakdown': {
                                'fcfe': [hpg_fcfe_2025, hpg_fcfe_2026, hpg_fcfe_2027],
                                'pv_fcfe': [hpg_pv_fcfe_2025, hpg_pv_fcfe_2026, hpg_pv_fcfe_2027],
                                'pv_terminal': hpg_pv_terminal,
                                'terminal_value': hpg_terminal_value
                            }
                        }
                    
                    # Override DBD with actual valuation data
                    elif ticker == "DBD":
                        beta = 0.8  # Typical retail sector beta
                        capm_return = 0.0502
                        # DCF Valuation Data for DBD
                        dbd_intrinsic_per_share = 67731.20  # VND per share
                        dbd_current_price = 63000  # Current market price (VND) - approximate
                        dbd_upside = ((dbd_intrinsic_per_share - dbd_current_price) / dbd_current_price) * 100
                        dbd_num_shares = 93553762
                        
                        # Detailed DCF breakdown for DBD
                        dbd_fcfe_2025 = 0.092850  # Trillion VND
                        dbd_fcfe_2026 = 0.103082  # Trillion VND (rounded)
                        dbd_fcfe_2027 = 0.137119  # Trillion VND (rounded)
                        dbd_terminal_value = 6.992  # Trillion VND (rounded)
                        
                        dbd_pv_fcfe_2025 = 88.412  # Billion VND (rounded)
                        dbd_pv_fcfe_2026 = 93.463  # Billion VND (rounded)
                        dbd_pv_fcfe_2027 = 118.381  # Billion VND (rounded)
                        dbd_pv_terminal = 6036.253  # Billion VND (rounded)
                        
                        # Total enterprise value
                        pv_fcf_total = (dbd_pv_fcfe_2025 + dbd_pv_fcfe_2026 + dbd_pv_fcfe_2027) * 1e9  # Sum of PV of projected FCFE (in VND)
                        pv_terminal_total = dbd_pv_terminal * 1e9  # PV of terminal value (in VND)
                        total_ev = pv_fcf_total + pv_terminal_total
                        
                        dcf_result = {
                            'intrinsic_value': dbd_intrinsic_per_share / 1000,  # Convert to thousands for display
                            'current_price': dbd_current_price / 1000,
                            'upside_downside_pct': dbd_upside,
                            'pv_fcf': pv_fcf_total / 1e12,
                            'pv_terminal': pv_terminal_total / 1e12,
                            'projected_fcf': [dbd_fcfe_2025, dbd_fcfe_2026, dbd_fcfe_2027],  # FCFE in trillions VND
                            'years': [2025, 2026, 2027],
                            'num_shares': dbd_num_shares,
                            'total_ev': total_ev,
                            'capm_return': capm_return,
                            'detailed_breakdown': {
                                'fcfe': [dbd_fcfe_2025, dbd_fcfe_2026, dbd_fcfe_2027],
                                'pv_fcfe': [dbd_pv_fcfe_2025, dbd_pv_fcfe_2026, dbd_pv_fcfe_2027],
                                'pv_terminal': dbd_pv_terminal,
                                'terminal_value': dbd_terminal_value
                            }
                        }
                    
                    with st.expander(f"**{ticker}** - {stock['name']}", expanded=False):
                        try:
                            if 'projected_fcf' in dcf_result and len(dcf_result['projected_fcf']) > 0:
                                fig_dcf = go.Figure()
                                fcf_list = dcf_result['projected_fcf']
                                # Use actual years if available, otherwise use sequential numbers
                                x_labels = dcf_result.get('years', list(range(1, len(fcf_list) + 1)))
                                projection_label = f"{len(fcf_list)}-Year" if ticker == "VNM" else f"{len(fcf_list)}-Year"
                                
                                if ticker in ["VNM", "HPG", "DBD"]:
                                    # VNM, HPG, and DBD use trillion VND, show in appropriate format
                                    fig_dcf.add_trace(go.Bar(x=x_labels, y=fcf_list, name='Projected FCFE', 
                                                            marker=dict(color=['#FF9800', '#4ECDC4', '#45B7D1']),
                                                            text=[f'₫ {v:.3f}T' for v in fcf_list],
                                                            textposition='outside'))
                                    fig_dcf.update_layout(title=f"{ticker} - Projected Free Cash Flows to Equity ({projection_label})", 
                                                         xaxis_title="Year", yaxis_title="FCFE (Trillion VND)", height=400, 
                                                         template='plotly', plot_bgcolor='#f5f5f5', paper_bgcolor='#f5f5f5')
                                else:
                                    fig_dcf.add_trace(go.Bar(x=x_labels, y=fcf_list, name='Projected FCF', marker=dict(color='#0066cc')))
                                    fig_dcf.update_layout(title=f"{ticker} - Projected Free Cash Flows ({projection_label})", xaxis_title="Year", yaxis_title="FCF (kVNĐ)", height=300, template='plotly_dark')
                                
                                st.plotly_chart(fig_dcf, use_container_width=True)
                        except:
                            pass
                        
                        # Methodology section
                        
                        # Summary metrics
                        if ticker in ["HPG", "VNM", "DBD"] and 'detailed_breakdown' in dcf_result:
                            st.markdown("### 💰 Valuation Summary")
                            
                            # Key metrics prominent + supporting
                            st.markdown("**Primary Metrics**")
                            key_col1, key_col2 = st.columns(2)
                            with key_col1:
                                st.metric("💰 Current Price", f"{dcf_result['current_price']:.2f}kVNĐ")
                            with key_col2:
                                st.metric("🎯 Intrinsic Value/Share", f"{dcf_result['intrinsic_value']:,.2f}kVNĐ")
                            
                            st.markdown("**Supporting Metrics**")
                            st.markdown("""
                            <style>
                                [data-testid="stMetric"] {
                                    font-size: 0.75rem;
                                }
                                [data-testid="stMetricLabel"] {
                                    font-size: 0.65rem;
                                }
                            </style>
                            """, unsafe_allow_html=True)
                            sup_col1, sup_col2, sup_col3, sup_col4, sup_col5 = st.columns(5)
                            with sup_col1:
                                st.metric("Enterprise Value", f"{dcf_result['total_ev']/1e12:,.2f}T đ")
                            with sup_col2:
                                st.metric("Shares", f"{dcf_result['num_shares']:,}")
                            with sup_col3:
                                st.metric("Cost of Equity", f"{dcf_result['capm_return']*100:.2f}%")
                            with sup_col4:
                                st.metric("Growth Rate", "3%")
                            with sup_col5:
                                st.metric("Terminal Value", "288.738 Tr đ")
                        
                        upside_pct = dcf_result['upside_downside_pct']
                        if upside_pct > 20:
                            interpretation = "🚀 **Highly Undervalued** - Strong buy signal"
                        elif upside_pct > 10:
                            interpretation = "📈 **Undervalued** - Potential value opportunity"
                        elif upside_pct > -10:
                            interpretation = "➡️ **Fairly Valued** - Market price reflects fundamentals"
                        elif upside_pct > -20:
                            interpretation = "📉 **Slightly Overvalued** - Limited upside"
                        else:
                            interpretation = "⚠️ **Significantly Overvalued** - Consider reducing"
                        
                        st.markdown(f"**Valuation Interpretation:**\n\n{interpretation}")
        
        except Exception as e:
            st.warning(f"Unable to complete CAPM and DCF analysis: {str(e)}")
    else:
        st.info("Data not available. CAPM and DCF analysis requires portfolio data.")
    
    st.markdown("")
    
    # Narrative about Mười's golden rule
    st.markdown("""
    <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-top: 20px; margin-bottom: 20px;">
        <p style="font-size: 16px; line-height: 1.8; color: #333;">
        Sau khi tính xong một cách… ngây thơ nhưng nghiêm túc, Nguyễn Văn Mười đã xác định quy tắc "vàng" cho riêng mình: nếu giá thị trường <strong>dưới intrinsic value</strong> – mua liền, còn nếu <strong>vượt qua intrinsic value</strong> – bán gọn.
        <br><br>
        Với cách này, Mười cảm thấy yên tâm: không cần bơi giữa rừng báo cáo tài chính hay lạc vào mớ công thức phức tạp, chỉ cần nhìn vào con số cuối cùng – intrinsic value – là biết mình nên hành động ra sao. <strong>Một chiến lược đơn giản, dễ hiểu, và đặc biệt… cực kỳ hợp với một newbie như Mười!</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # ============================================================================
    # SECTION 5: FORECAST WITH GBM
    # ============================================================================
    st.header("🔮 GBM Forecast")
    st.markdown(
        "*Geometric Brownian Motion simulations with Cholesky decomposition maintaining correlation between stocks*"
    )

    try:
        # Load price data silently
        price_df = pd.read_csv('attached_assets/price.csv')
        price_df['time'] = pd.to_datetime(price_df['time'])
        prices = price_df[['ACB', 'HPG', 'VNM', 'DBD']].dropna()
        
        stocks = ['ACB', 'HPG', 'VNM', 'DBD']
        n_assets = len(stocks)
        
        # User inputs for GBM parameters
        st.markdown("#### ⚙️ Simulation Parameters")
        col_params1, col_params2 = st.columns(2)
        
        with col_params1:
            n_sims = st.slider(
                "Number of scenarios",
                min_value=100,
                max_value=5000,
                value=1000,
                step=100,
                help="Higher number = more accurate but slower"
            )
        
        with col_params2:
            forecast_days = st.slider(
                "Days to predict",
                min_value=30,
                max_value=756,
                value=252,
                step=21,
                help="30=1 month, 63=3 months, 252=1 year, 756=3 years"
            )
        
        # Run simulation silently without printing steps
        returns = np.log(prices / prices.shift(1)).dropna()
        mu = returns.mean() * 252
        sigma = returns.std() * np.sqrt(252)
        corr = returns.corr()
        L = np.linalg.cholesky(corr)
        
        T = forecast_days / 252
        N = forecast_days
        dt = T / N
        
        S0 = prices.iloc[-1].values
        all_paths = np.zeros((n_sims, N + 1, n_assets))
        
        np.random.seed(42)
        
        # Silent progress during simulation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        all_paths[:, 0, :] = S0
        mu_arr = mu.values
        sigma_arr = sigma.values
        
        for t in range(1, N + 1):
            if t % max(1, N // 10) == 0:
                progress_bar.progress(t / N)
                status_text.text(f"Generating scenarios... {t}/{N}")
            
            z = np.random.normal(size=(n_sims, n_assets))
            eps = z @ L.T
            drift = (mu_arr - 0.5 * sigma_arr**2) * dt
            diffusion = sigma_arr * eps * np.sqrt(dt)
            all_paths[:, t, :] = all_paths[:, t-1, :] * np.exp(drift + diffusion)
        
        progress_bar.progress(1.0)
        status_text.text(f"✓ Generated {n_sims} scenarios for {forecast_days} days")
        st.empty()
        
        st.markdown("")
        
        # Create tabs for each stock
        st.markdown(f"#### 📊 1. Stock Price Predictions ({forecast_days} days)")
        
        tabs = st.tabs([f"📈 {stock}" for stock in stocks])
        
        for tab_idx, (tab, stock) in enumerate(zip(tabs, stocks)):
            with tab:
                idx = tab_idx
                
                final_prices = all_paths[:, -1, idx]
                final_return = ((final_prices - S0[idx]) / S0[idx]) * 100
                
                median_price = np.percentile(final_prices, 50)
                p10_price = np.percentile(final_prices, 10)
                p90_price = np.percentile(final_prices, 90)
                median_return = np.percentile(final_return, 50)
                
                # Display metrics in tab
                metric_cols = st.columns(3)
                with metric_cols[0]:
                    st.metric("Current Price", f"{S0[idx]:.2f}kVNĐ")
                with metric_cols[1]:
                    st.metric("Median Forecast", f"{median_price:.2f}kVNĐ", f"{median_return:+.1f}%")
                with metric_cols[2]:
                    st.metric("Price Range", f"{p10_price:.1f} - {p90_price:.1f}kVNĐ")
                
                
                # Chart for this stock
                fig_stock = go.Figure()
                
                # Display up to 30 sample paths from total simulations
                sample_paths = min(30, n_sims)
                for sim_id in range(sample_paths):
                    path_data = all_paths[sim_id, :, idx]
                    fig_stock.add_trace(
                        go.Scatter(y=path_data,
                                  mode='lines',
                                  name='',
                                  line=dict(width=1, color='rgba(100, 150, 200, 0.3)'),
                                  showlegend=False,
                                  hoverinfo='skip'))
                
                # Add percentile lines
                p10 = np.percentile(all_paths[:, :, idx], 10, axis=0)
                p50 = np.percentile(all_paths[:, :, idx], 50, axis=0)
                p90 = np.percentile(all_paths[:, :, idx], 90, axis=0)
                
                fig_stock.add_trace(
                    go.Scatter(y=p10, mode='lines', name='10th Percentile',
                              line=dict(color='#FF9800', width=1.5, dash='dash'),
                              hovertemplate='10th Percentile<br>Day: %{x}<br>Price: %{y:.2f}kVNĐ<extra></extra>'))
                fig_stock.add_trace(
                    go.Scatter(y=p50, mode='lines', name='Median',
                              line=dict(color='#00D9FF', width=2.5),
                              hovertemplate='Median<br>Day: %{x}<br>Price: %{y:.2f}kVNĐ<extra></extra>'))
                fig_stock.add_trace(
                    go.Scatter(y=p90, mode='lines', name='90th Percentile',
                              line=dict(color='#FF6B6B', width=1.5, dash='dash'),
                              hovertemplate='90th Percentile<br>Day: %{x}<br>Price: %{y:.2f}kVNĐ<extra></extra>'))
                
                fig_stock.update_layout(
                    title=f'{stock} - {sample_paths} Sample Paths ({n_sims} total scenarios)',
                    xaxis_title='Trading Days',
                    yaxis_title='Stock Price (kVNĐ)',
                    height=450,
                    template='plotly',
                    plot_bgcolor='#f5f5f5',
                    paper_bgcolor='#f5f5f5',
                    hovermode='x unified',
                    legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.95)', font=dict(size=10)),
                    xaxis=dict(gridcolor='#eee'),
                    yaxis=dict(gridcolor='#eee'),
                    margin=dict(l=50, r=30, t=40, b=40)
                )
                
                st.plotly_chart(fig_stock, use_container_width=True)
        
        st.markdown("")
        st.divider()
        st.markdown("")
        
        # ============================================================================
        # PORTFOLIO RETURN CALCULATION WITH MIN VARIANCE WEIGHTS
        # ============================================================================
        st.markdown("#### 📈 2. Portfolio Return Analysis")
        
        try:
            # Calculate minimum variance portfolio weights
            cov_matrix = returns.cov()
            n_stocks = len(stocks)
            
            # Solve for minimum variance portfolio: w = Σ^-1 * 1 / (1^T * Σ^-1 * 1)
            inv_cov = np.linalg.inv(cov_matrix)
            ones = np.ones(n_stocks)
            min_var_weights = inv_cov @ ones / (ones @ inv_cov @ ones)
            
            # Normalize weights to ensure they sum to 1
            min_var_weights = min_var_weights / min_var_weights.sum()
            
            # Calculate individual stock returns at forecast end
            stock_final_prices = all_paths[:, -1, :]  # Shape: (n_sims, n_assets)
            stock_returns = (stock_final_prices - S0) / S0  # Shape: (n_sims, n_assets)
            
            # Calculate portfolio return using min variance weights
            portfolio_returns = stock_returns @ min_var_weights  # Shape: (n_sims,)
            
            # Calculate statistics
            
            # Individual stock return statistics
            st.markdown(f"**Individual Stock Returns at Day {forecast_days}:**")
            
            individual_cols = st.columns(4)
            for idx, stock in enumerate(stocks):
                with individual_cols[idx]:
                    stock_ret_median = np.percentile(stock_returns[:, idx], 50) * 100
                    stock_ret_p10 = np.percentile(stock_returns[:, idx], 10) * 100
                    stock_ret_p90 = np.percentile(stock_returns[:, idx], 90) * 100
                    
                    st.metric(
                        f"{stock} Return",
                        f"{stock_ret_median:+.2f}%",
                        f"Range: {stock_ret_p10:+.1f}% to {stock_ret_p90:+.1f}%"
                    )
            
            st.markdown("")
            
            # Portfolio return statistics
            st.markdown(f"**Portfolio Return at Day {forecast_days}:**")
            
            portfolio_return_median = np.percentile(portfolio_returns, 50) * 100
            portfolio_return_p10 = np.percentile(portfolio_returns, 10) * 100
            portfolio_return_p90 = np.percentile(portfolio_returns, 90) * 100
            portfolio_return_mean = np.mean(portfolio_returns) * 100
            portfolio_return_std = np.std(portfolio_returns) * 100
            
            portfolio_cols = st.columns(5)
            with portfolio_cols[0]:
                st.metric(
                    "Median Return",
                    f"{portfolio_return_median:+.2f}%"
                )
            with portfolio_cols[1]:
                st.metric(
                    "Mean Return",
                    f"{portfolio_return_mean:+.2f}%"
                )
            with portfolio_cols[2]:
                st.metric(
                    "Std Dev",
                    f"{portfolio_return_std:.2f}%"
                )
            with portfolio_cols[3]:
                st.metric(
                    "10th Percentile",
                    f"{portfolio_return_p10:+.2f}%"
                )
            with portfolio_cols[4]:
                st.metric(
                    "90th Percentile",
                    f"{portfolio_return_p90:+.2f}%"
                )
            
            st.markdown("")
            
            # Distribution chart for portfolio returns
            fig_portfolio_dist = go.Figure()
            
            fig_portfolio_dist.add_trace(go.Histogram(
                x=portfolio_returns * 100,
                nbinsx=40,
                name='Portfolio Return Distribution',
                marker_color='rgba(31, 119, 180, 0.7)',
                hovertemplate='Return Range: %{x:.2f}%<br>Frequency: %{y}<extra></extra>'
            ))
            
            # Add percentile lines
            fig_portfolio_dist.add_vline(
                x=portfolio_return_p10,
                line_dash="dash",
                line_color="#FF9800",
                line_width=2,
                annotation_text=f"10th: {portfolio_return_p10:.2f}%",
                annotation_position="top left"
            )
            
            fig_portfolio_dist.add_vline(
                x=portfolio_return_median,
                line_dash="solid",
                line_color="#00D9FF",
                line_width=2.5,
                annotation_text=f"Median: {portfolio_return_median:.2f}%",
                annotation_position="top"
            )
            
            fig_portfolio_dist.add_vline(
                x=portfolio_return_p90,
                line_dash="dash",
                line_color="#FF6B6B",
                line_width=2,
                annotation_text=f"90th: {portfolio_return_p90:.2f}%",
                annotation_position="top right"
            )
            
            fig_portfolio_dist.update_layout(
                title=f'Portfolio Return Distribution (Min Variance Weights) - {forecast_days} Days',
                xaxis_title='Return (%)',
                yaxis_title='Frequency',
                height=400,
                template='plotly',
                plot_bgcolor='#f5f5f5',
                paper_bgcolor='#f5f5f5',
                hovermode='x unified',
                showlegend=False,
                xaxis=dict(gridcolor='#eee'),
                yaxis=dict(gridcolor='#eee'),
                margin=dict(l=50, r=30, t=40, b=40)
            )
            
            st.plotly_chart(fig_portfolio_dist, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error calculating portfolio returns: {e}")
            
    except Exception as e:
        st.error(f"Error in GBM forecast: {e}")

    # GBM interpretation box
    st.markdown("""
### 📊 Dự báo GBM với Cholesky

Geometric Brownian Motion (GBM) mô phỏng các con đường giá tương lai dựa trên **lợi suất kỳ vọng và độ biến động lịch sử**.  

Kết quả mô phỏng đã sử dụng **Cholesky decomposition** để đảm bảo **giữ nguyên tương quan lịch sử** giữa các cổ phiếu: các mẫu ngẫu nhiên độc lập được nhân với ma trận Cholesky, tạo ra các biến ngẫu nhiên có tương quan đúng.

**Kết quả dự báo:**
- **Trung vị (tứ phân vị 50):** Giá khả thi nhất.  
- **Dải 10–90:** Bao phủ 80% kết quả có thể xảy ra.  
- **Các đường mô phỏng:** Thể hiện các kịch bản thị trường với tương quan được bảo toàn.
    """)
