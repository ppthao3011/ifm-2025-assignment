import streamlit as st

def show_theory_page():
    # ============================================================================
    # SIDEBAR SECTION NAVIGATION
    # ============================================================================
    with st.sidebar:
        st.markdown("### 📚 Sections")
        st.markdown("---")
        
        sections = [
            ("VaR & ES", "#i-va-r-value-at-risk-and-es-expected-shortfall"),
            ("F-score", "#ii-f-score-piotroski-f-score"),
            ("Z-score", "#iii-z-score-altman-z-score"),
            ("M-score", "#iv-m-score-beneish-m-score"),
            ("CAPM", "#v-capm-capital-asset-pricing-model"),
            ("GBM", "#vi-gbm-geometric-brownian-motion"),
            ("ARCH/GARCH & DCC", "#vii-archgarch-dcc-dynamic-conditional-correlation"),
            ("Holt-Winters", "#viii-holt-winters-exponential-smoothing"),
            ("FCFE", "#ix-fcfe-free-cash-flow-to-equity"),
        ]
        
        for label, anchor in sections:
            st.markdown(f"[{label}]({anchor})")
        
        st.markdown("---")
    
    # ============================================================================
    # TITLE
    # ============================================================================
    st.title("📚 Portfolio Theory Framework")
    st.markdown("---")
    
    # VaR and ES Section
    st.header("I. VaR (Value at Risk) & ES (Expected Shortfall)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Định nghĩa")
        st.markdown("""
        **Value at Risk (VaR):** Mức tổn thất tối đa có thể xảy ra trong một khoảng thời gian nhất định với mức độ tin cậy α cho trước.
        
        **Expected Shortfall (ES):** Giá trị kỳ vọng của tổn thất khi vượt quá mức VaR. Nói cách khác, ES là mức tổn thất trung bình trong những tình huống xấu nhất.
        """)
    
    with col2:
        st.subheader("💡 Ý nghĩa")
        st.markdown("""
        - VaR cho biết "tệ nhất có thể xảy ra là mất bao nhiêu"
        - ES đi sâu hơn: "khi mất nhiều hơn VaR, tôi sẽ mất trung bình bao nhiêu"
        - Hai chỉ số này giúp quản lý rủi ro hiệu quả
        """)
    
    st.subheader("📈 Ba phương pháp tính VaR & ES:")
    
    st.markdown("##### a) **Phương pháp Lịch sử (Historical Simulation)**")
    st.markdown("""
    - Dựa trên dữ liệu lịch sử thực tế để ước lượng tổn thất tiềm ẩn
    - Quy trình: Thu thập dữ liệu lịch sử → Áp dụng lên danh mục hiện tại → Phân tích phân phối kết quả
    - **Ưu điểm:** Không cần giả định về phân phối, sử dụng dữ liệu thực tế
    - **Nhược điểm:** Dễ bỏ sót các sự kiện chưa từng xảy ra, có thể không đại diện cho tương lai
    """)
    
    st.markdown("##### b) **Phương pháp Tham số hóa (Parametric / Variance-Covariance)**")
    st.markdown("""
    - Giả định lợi suất tuân theo phân phối chuẩn
    - Công thức: VaR = μ - σ × Z(α), trong đó:
      - μ = trung bình lợi suất
      - σ = độ lệch chuẩn
      - Z(α) = giá trị từ bảng phân phối chuẩn ứng với mức tin cậy α
    - **Ưu điểm:** Tính toán nhanh, phù hợp với danh mục lớn
    - **Nhược điểm:** Giả định chuẩn không chính xác với tài chính thực tế (có fat tails), có thể đánh giá thấp rủi ro cực trị
    """)
    
    st.markdown("##### c) **Phương pháp Mô phỏng Monte Carlo**")
    st.markdown("""
    - Tạo ra hàng ngàn kịch bản tương lai dựa trên các thông số thống kê
    - Quy trình: Định nghĩa phân phối & tương quan → Tạo ngẫu nhiên các con đường giá → Phân tích kết quả
    - **Ưu điểm:** Có thể mô hình hóa các danh mục phức tạp, không tuyến tính
    - **Nhược điểm:** Yêu cầu tính toán cao, kết quả phụ thuộc vào giả định ban đầu
    """)
    
    st.markdown("---")
    
    # F-score Section
    st.header("II. F-score (Piotroski F-Score)")
    
    st.markdown("""
    **Định nghĩa:** Chỉ số đánh giá sức khỏe tài chính của doanh nghiệp thông qua 9 tiêu chí nhị phân (có/không).
    
    **Công thức:** F-Score = Tổng điểm từ 9 tiêu chí (0-9 điểm)
    """)
    
    st.markdown("##### 📋 Cấu thành 9 tiêu chí:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Khả năng sinh lợi (4 điểm):**
        1. Lợi nhuận ròng dương (1 điểm)
        2. ROA dương (1 điểm)
        3. OCF dương (1 điểm)
        4. OCF > Lợi nhuận ròng (1 điểm)
        """)
    
        with col2:
            st.markdown("""
        **Tài chính & Thanh khoản (3 điểm):**<br>
                                   <br>
        5. Nợ dài hạn giảm (1 điểm)<br>
        6. Current ratio tăng (1 điểm)<br>
        7. Không phát hành cổ phiếu mới (1 điểm)
        """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
        **Hiệu quả hoạt động (2 điểm):**<br>
                                        <br>
        8. Lợi nhuận gộp tăng (1 điểm)<br>
        9. Vòng quay tài sản tăng (1 điểm)
        """, unsafe_allow_html=True)
    
    st.markdown("""
    **Diễn giải kết quả:**
    - F-Score **7-9:**  Doanh nghiệp tài chính lành mạnh, đáng để cân nhắc đầu tư dài hạn.
    - F-Score **4-6:** Công ty trung bình, cần phân tích thêm trước khi đầu tư.
    - F-Score **0-3:** Công ty rất yếu, rủi ro cao
    """)
    
    st.markdown("---")
    
    # Z-score Section
    st.header("III. Z-score (Altman Z-Score)")
    
    st.markdown("""
    **Định nghĩa:** Mô hình dự báo xác suất phá sản của doanh nghiệp trong vòng 2 năm tới.
    """)
    
    st.markdown("##### 📐 Công thức Z-score:")
    st.latex(r"Z = 1.2X_1 + 1.4X_2 + 3.3X_3 + 0.6X_4 + 1.0X_5")
    
    st.markdown("""
    **Trong đó:**
    - X₁ = Vốn lưu động / Tổng tài sản
    - X₂ = Lợi nhuận giữ lại / Tổng tài sản  
    - X₃ = EBIT / Tổng tài sản
    - X₄ = Giá trị thị trường vốn chủ / Tổng nợ
    - X₅ = Doanh thu / Tổng tài sản
    """)
    
    st.markdown("##### 🎯 Phân vùng (Zone of Discrimination):")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🟢 Safe Zone", "Z > 2.99", "An toàn")
    with col2:
        st.metric("🟡 Grey Zone", "1.81 < Z < 2.99", "Cảnh báo")
    with col3:
        st.metric("🔴 Distress Zone", "Z < 1.81", "Nguy hiểm")
    
    st.markdown("---")
    
    # M-score Section
    st.header("IV. M-score (Beneish M-Score)")
    
    st.markdown("""
    **Định nghĩa:** Mô hình phát hiện xem công ty có thao túng báo cáo lợi nhuận hay không.
    
    **Ngưỡng:** M-Score = **-1.78**
    - **M-Score < -1.78:** Công ty không thao túng
    - **M-Score > -1.78:** Công ty có khả năng thao túng (cảnh báo)
    """)
    st.markdown("##### 📐 Công thức M-score:")
    st.latex(r"""
    \text{M-Score} = -4.84 + 0.92 \cdot \text{DSRI} + 0.528 \cdot \text{GMI} 
    + 0.404 \cdot \text{AQI} + 0.892 \cdot \text{SGI} + 0.115 \cdot \text{DEPI} 
    - 0.172 \cdot \text{SGAI} + 4.679 \cdot \text{TATA} - 0.327 \cdot \text{LVGI}
    """)
    st.markdown("Trong đó:")
    
    indicators = {
        "DSRI (Days' sales in a receivable index)": r"\text{DSRI} = \frac{AR_t / Sales_t}{AR_{t-1} / Sales_{t-1}}",
        "GMI ( Gross margin index)": r"\text{GMI} = \frac{GM_{t-1}}{GM_t}",
        "AQI (Asset quality index)": r"\text{AQI} = \frac{1 - \frac{CA + PPE}{TA}}{1 - \frac{CA_{t-1} + PPE_{t-1}}{TA_{t-1}}}",
        "SGI ( Sales growth index)": r"\text{SGI} = \frac{Sales_t}{Sales_{t-1}}",
        "DEPI (Depreciation index)": r"\text{DEPI} = \frac{Dep_{t-1} / (PPE_{t-1} + Dep_{t-1})}{Dep_t / (PPE_t + Dep_t)}",
        "SGAI (Sales and general and administrative expenses index )": r"\text{SGAI} = \frac{SGA_t / Sales_t}{SGA_{t-1} / Sales_{t-1}}",
        "LVGI (Leverage index)": r"\text{LVGI} = \frac{(CL + LTD)_t / TA_t}{(CL + LTD)_{t-1} / TA_{t-1}}",
        "TATA (Total accruals to total assets)": r"\text{TATA} = \frac{NI - OCF}{TA}"
    }

    for idx, (name, formula) in enumerate(indicators.items(), 1):
        st.markdown(f"**{idx}. {name}**")
        st.latex(formula)
    st.markdown("---")
    
    # CAPM Section
    st.header("V. CAPM (Capital Asset Pricing Model)")
    
    st.markdown("""
    **Định nghĩa:** Mô hình tính toán lợi suất kỳ vọng của một tài sản dựa trên rủi ro hệ thống.
    """)
    
    st.markdown("##### 📐 Công thức CAPM:")
    st.latex(r"E(R_i) = R_f + \beta_i(R_m - R_f)")
    
    st.markdown("""
    **Các thành phần:**
    - **E(Rᵢ):** Lợi suất kỳ vọng của tài sản
    - **Rf:** Lãi suất phi rủi ro (thường là lợi suất trái phiếu chính phủ)
    - **βᵢ:** Beta - độ nhạy cảm so với thị trường
    - **Rm:** Lợi suất kỳ vọng của thị trường
    - **(Rm - Rf):** Phần bù rủi ro thị trường (Market Risk Premium)
    """)
    
    st.markdown("##### 💡 Ý nghĩa:")
    st.markdown("""
    - **Beta = 1:** Tài sản biến động cùng thị trường
    - **Beta > 1:** Tài sản biến động mạnh hơn thị trường (rủi ro cao hơn)
    - **Beta < 1:** Tài sản ít biến động hơn (rủi ro thấp hơn)
    - Lợi suất kỳ vọng càng cao khi rủi ro (beta) càng lớn
    """)
    
    st.markdown("---")
    
    # GBM Section
    st.header("VI. GBM (Geometric Brownian Motion)")
    
    st.markdown("""
    **Định nghĩa:** Mô hình toán học mô tả sự thay đổi giá tài sản theo thời gian thực, được sử dụng để dự báo giá cổ phiếu.
    """)
    
    st.markdown("##### 📐 Phương trình vi phân ngẫu nhiên:")
    st.latex(r"dS_t = \mu S_t dt + \sigma S_t dW_t")
    
    st.markdown("""
    **Các thành phần:**
    - **St:** Giá tài sản tại thời điểm t
    - **μ:** Drift (kỳ vọng lợi suất)
    - **σ:** Volatility (độ biến động)
    - **dWt:** Wiener process (chuyển động ngẫu nhiên)
    """)
    
    st.markdown("##### 📊 Lời giải của phương trình:")
    st.latex(r"S_t = S_0 \exp\left[\left(\mu - \frac{\sigma^2}{2}\right)t + \sigma W_t\right]")
    
    st.markdown("""
    **Ứng dụng:**
    - Mô phỏng Monte Carlo để dự báo giá cổ phiếu
    - Tính toán xác suất các kịch bản tương lai
    - Định giá các sản phẩm phái sinh
    """)
    
    st.markdown("---")
    
    # DCC ARCH/GARCH Section
    st.header("VII. ARCH/GARCH & DCC (Dynamic Conditional Correlation)")
    
    st.markdown("""
    **Định nghĩa:** ARCH (AutoRegressive Conditional Heteroskedasticity) và GARCH (Generalized ARCH) là các mô hình để mô hình hóa độ biến động thay đổi theo thời gian (time-varying volatility). DCC là phần mở rộng để mô hình hóa tương quan động giữa các tài sản.
    """)
    
    st.markdown("##### 📊 ARCH Model (Autoregressive Conditional Heteroskedasticity)")
    st.markdown("""
    **Ý tưởng cốt lõi:** Độ biến động hiện tại phụ thuộc vào sai số quá khứ.
    
    **Công thức ARCH(q):**
    """)
    st.latex(r"\sigma_t^2 = \omega + \sum_{i=1}^{q} \alpha_i \epsilon_{t-i}^2")
    
    st.markdown("""
    - **σₜ²:** Phương sai (độ biến động bình phương) tại thời điểm t
    - **ω:** Hằng số
    - **αᵢ:** Hệ số tác động của sai số quá khứ
    - **εₜ₋ᵢ:** Sai số (innovation) ở thời điểm quá khứ
    """)
    
    st.markdown("##### 📈 GARCH Model (Generalized ARCH)")
    st.markdown("""
    **Cải tiến:** Thêm phần phụ thuộc vào phương sai quá khứ, giúp mô hình gọn hơn.
    
    **Công thức GARCH(p,q):**
    """)
    st.latex(r"\sigma_t^2 = \omega + \sum_{i=1}^{q} \alpha_i \epsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_j \sigma_{t-j}^2")
    
    st.markdown("""
    - **αᵢ:** Hệ số tác động từ sai số quá khứ (ARCH effect)
    - **βⱼ:** Hệ số tác động từ phương sai quá khứ (GARCH effect)
    - **GARCH(1,1)** là mô hình phổ biến nhất, cân bằng giữa sự nhạy cảm với tin tức gần đây và độ trơn.
    """)
    
    st.markdown("##### 🔗 DCC Model (Dynamic Conditional Correlation)")
    st.markdown("""
    **Ý tưởng:** Khi thị trường biến động mạnh, tương quan giữa các tài sản thường tăng lên (không phải hằng số).
    
    **DCC GARCH gồm 2 bước:**
    
    1. **Bước 1:** Ước lượng GARCH univariate cho từng tài sản riêng lẻ
    2. **Bước 2:** Ước lượng tương quan động dựa trên các residual chuẩn hóa
    
    **Phương trình tương quan động:**
    """)
    st.latex(r"Q_t = \bar{Q} + \alpha(z_{t-1}z_{t-1}' - \bar{Q}) + \beta(Q_{t-1} - \bar{Q})")
    
    st.markdown("""
    - **Qₜ:** Ma trận tương quan tại thời điểm t
    - **Q̄:** Tương quan trung bình (dài hạn)
    - **α, β:** Tham số điều chỉnh tốc độ thay đổi tương quan
    - **zₜ:** Residual chuẩn hóa
    """)
    
    st.markdown("##### 💡 Ý nghĩa thực tế:")
    st.markdown("""
    - **Trong thời bình:** Tương quan có thể thấp, danh mục được đa dạng hóa tốt
    - **Trong thời kỳ khủng hoảng:** Tương quan tăng cao, các tài sản giảm giá cùng lúc (systemic risk)
    - Giúp quản lý rủi ro danh mục động và chính xác hơn
    - Quan trọng để ước lượng VaR và ES của danh mục chính xác
    """)
    
    st.markdown("##### 📌 Ứng dụng trong phân tích danh mục:")
    st.markdown("""
    - Ước lượng phương sai-hiệp phương sai ma trận thay đổi theo thời gian
    - Dự báo độ biến động và tương quan trong các kịch bản thị trường khác nhau
    - Tối ưu hóa trọng số danh mục dựa trên thông tin mới nhất
    - Tính toán rủi ro danh mục (VaR, ES) với tương quan động
    - Phát hiện thời kỳ systemic risk khi tương quan tất cả các tài sản tăng đột ngột
    """)
    
    st.markdown("---")
    
    # Holt-Winters Section
    st.header("VIII. Holt-Winters (Exponential Smoothing)")
    
    st.markdown("""
    **Định nghĩa:** Phương pháp dự báo chuỗi thời gian sử dụng trọng số mũ, phù hợp cho dữ liệu có xu hướng (trend) và tính mùa vụ (seasonality).
    """)
    
    st.markdown("##### 📊 Ba thành phần chính:")
    st.markdown("""
    1. **Level (Mức):** Giá trị trung bình hiệu chỉnh
    2. **Trend (Xu hướng):** Hướng biến động của dữ liệu
    3. **Seasonal (Mùa vụ):** Mô hình lặp lại theo chu kỳ
    """)
    
    st.markdown("##### 📈 Công thức Holt-Winters:")
    
    st.markdown("**a) Simple Exponential Smoothing (SES) - Dữ liệu không có xu hướng:**")
    st.latex(r"L_t = \alpha Y_t + (1-\alpha) L_{t-1}")
    st.markdown("- **Lₜ:** Level tại thời điểm t")
    st.markdown("- **α:** Tham số smoothing (0 < α < 1)")
    st.markdown("- **Yₜ:** Giá trị quan sát")
    
    st.markdown("**b) Holt's Linear Trend (HLT) - Dữ liệu có xu hướng tuyến tính:**")
    st.latex(r"L_t = \alpha Y_t + (1-\alpha)(L_{t-1} + T_{t-1})")
    st.latex(r"T_t = \beta(L_t - L_{t-1}) + (1-\beta)T_{t-1}")
    st.markdown("- **Tₜ:** Trend (độ dốc)")
    st.markdown("- **β:** Tham số smoothing cho trend")
    
    st.markdown("**c) Holt-Winters Additive - Dữ liệu có mùa vụ:**")
    st.latex(r"L_t = \alpha(Y_t - S_{t-m}) + (1-\alpha)(L_{t-1} + T_{t-1})")
    st.latex(r"T_t = \beta(L_t - L_{t-1}) + (1-\beta)T_{t-1}")
    st.latex(r"S_t = \gamma(Y_t - L_t) + (1-\gamma)S_{t-m}")
    st.markdown("- **Sₜ:** Yếu tố mùa vụ")
    st.markdown("- **m:** Độ dài chu kỳ mùa vụ")
    st.markdown("- **γ:** Tham số smoothing cho mùa vụ")
    
    st.markdown("##### 💡 Ứng dụng trong phân tích tài chính:")
    st.markdown("""
    - Dự báo giá cổ phiếu trong ngắn hạn
    - Dự báo doanh số bán hàng theo mùa
    - Dự báo lãi suất và tỷ giá hối đoái
    - Cộng hưởng với xu hướng thị trường và biến động mùa vụ
    - Phù hợp cho dữ liệu không yêu cầu độ phức tạp cao như ARIMA
    """)
    
    st.markdown("---")
    
    # FCFE Section
    st.header("IX. FCFE (Free Cash Flow to Equity)")
    
    st.markdown("""
    **Định nghĩa:** Dòng tiền tự do có sẵn cho các cổ đông sau khi công ty đã thanh toán chi phí hoạt động, thuế, nợ, và tái đầu tư cần thiết.
    
    **Ý nghĩa:** FCFE thể hiện khả năng của công ty trong việc trả cổ tức hay mua lại cổ phiếu cho cổ đông.
    """)
    
    st.markdown("##### 📐 Công thức FCFE:")
    st.latex(r"FCFE = NI + Depreciation - CapEx - \Delta WC + Net\_Borrowing")
    
    st.markdown("""
    **Trong đó:**
    - **NI:** Lợi nhuận ròng (Net Income)
    - **Depreciation:** Khấu hao (hạch toán không liên quan đến tiền)
    - **CapEx:** Chi phí tái đầu tư (Capital Expenditure)
    - **ΔWC:** Thay đổi vốn lưu động (Change in Working Capital)
    - **Net Borrowing:** Khoản vay ròng (Vay mới - Trả nợ)
    """)
    
    st.markdown("##### 📊 Phiên bản đơn giản hơn:")
    st.latex(r"FCFE = Operating\ Cash\ Flow - CapEx + Net\_Borrowing")
    
    st.markdown("##### 💡 Cách diễn giải FCFE:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **FCFE dương:**
        - Công ty có tiền thặng dư cho cổ đông
        - Có thể trả cổ tức hoặc mua lại cổ phiếu
        - Dấu hiệu sức khỏe tài chính tốt
        """)
    with col2:
        st.markdown("""
        **FCFE âm:**
        - Công ty cần đầu tư nhiều hoặc có nợ cao
        - Không có tiền cho cổ đông
        - Cần giám sát tình hình tài chính
        """)
    
    st.markdown("##### 📌 Ứng dụng trong định giá:")
    st.markdown("""
    - **Định giá Dividend Discount Model (DDM):** Sử dụng FCFE thay thế cho cổ tức thực tế
    - **Định giá doanh nghiệp:** Chiết khấu FCFE để tính giá trị vốn chủ sở hữu
    - **Phân tích khả năng trả cổ tức:** FCFE cao hơn cổ tức hiện tại = công ty an toàn
    - **So sánh công ty:** FCFE/Equity Market Cap cho thấy mức định giá tương đối
    - **Dự báo tăng trưởng:** Xu hướng FCFE thể hiện mô mentum của công ty
    """)
    
    st.markdown("##### 📈 Ví dụ tính toán FCFE:")
    st.markdown("""
    | Chỉ tiêu | Giá trị (tỷ VND) |
    |---------|-----------------|
    | Lợi nhuận ròng (NI) | 100 |
    | Cộng: Khấu hao | 30 |
    | Trừ: Chi phí tái đầu tư (CapEx) | -50 |
    | Trừ: Thay đổi vốn lưu động (ΔWC) | -10 |
    | Cộng: Khoản vay ròng (Net Borrowing) | 20 |
    | **FCFE** | **90** |
    
    Kết luận: Công ty có 90 tỷ VND dòng tiền tự do để trả cho cổ đông
    """)
    
    st.markdown("---")
    
    st.info("💬 **Ghi chú:** 9 phương pháp trên được áp dụng trong bài báo cáo này để phân tích danh mục đầu tư của Mười một cách toàn diện và khoa học, bao gồm đánh giá rủi ro, sức khỏe tài chính, dự báo xu hướng, và định giá dòng tiền.")

    st.header("X. CHOLESKY DECOMPOSITION")
    st.markdown("""
Cholesky Decomposition

Cho ma trận hiệp phương sai $\\Sigma$ của các biến ngẫu nhiên, Cholesky decomposition phân tách thành ma trận tam giác dưới $L$ sao cho:

$$
\\Sigma = L L^\\top
$$

Khi nhân ma trận $L$ với vector các biến ngẫu nhiên chuẩn độc lập $Z \\sim N(0,1)$, ta thu được vector:

$$
X = L Z
$$

Vector $X$ có **ma trận hiệp phương sai đúng bằng $\\Sigma$**, giữ nguyên mối tương quan giữa các biến.
""")



