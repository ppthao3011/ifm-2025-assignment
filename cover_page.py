import streamlit as st

def show_cover_page():
    

    # Custom CSS with enhanced design
    st.markdown("""
    <style>
    .cover-wrapper {
        max-width: 1300px;
        margin: 0 auto;
        padding: 80px 60px;
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 50%, #e8f1ff 100%);
        border-radius: 20px;
    }

    /* Hero Section */
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

    /* Info Cards */
    .info-cards-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 25px;
        margin-bottom: 60px;
    }

    .info-card {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        padding: 35px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 35px rgba(102, 126, 234, 0.25);
        transition: all 0.3s ease;
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

    /* Sections */
    .content-section {
        background: white;
        padding: 45px;
        border-radius: 15px;
        margin-bottom: 40px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
        border-left: 5px solid;
    }

    .overview-section {
        border-left-color: #667EEA;
    }

    .team-section {
        border-left-color: #764BA2;
    }

    .distribution-section {
        border-left-color: #f093fb;
    }

    .section-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Overview */
    .overview-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }

    .overview-item {
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667EEA;
        font-weight: 600;
        color: #333;
    }

    /* Team Members */
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
        transition: all 0.3s ease;
    }

    .member-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }

    /* Distribution */
    .distribution-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 25px;
        margin-bottom: 30px;
    }

    .dist-card {
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #e0e7ff;
        transition: all 0.3s ease;
    }

    .dist-card:hover {
        border-color: #667EEA;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
    }

    .dist-name {
        font-weight: 800;
        color: #1a1f3a;
        margin-bottom: 15px;
        font-size: 15px;
    }

    .dist-bar-bg {
        width: 100%;
        height: 10px;
        background: #e0e7ff;
        border-radius: 5px;
        overflow: hidden;
        margin-bottom: 12px;
    }

    .dist-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #667EEA 0%, #764BA2 50%, #f093fb 100%);
        width: 33.33%;
        border-radius: 5px;
    }

    .dist-percent {
        font-weight: 800;
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 18px;
    }

    .dist-total {
        text-align: center;
        margin-top: 25px;
        padding-top: 25px;
        border-top: 3px solid #e0e7ff;
        font-weight: 800;
        font-size: 18px;
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Footer */
    .cover-footer {
        text-align: center;
        padding-top: 40px;
        border-top: 2px solid #e0e7ff;
        color: #999;
        font-size: 13px;
        letter-spacing: 1px;
    }

    @media (max-width: 768px) {
        .info-cards-grid {
            grid-template-columns: 1fr;
        }
        .team-grid {
            grid-template-columns: 1fr;
        }
        .distribution-grid {
            grid-template-columns: 1fr;
        }
        .hero-title {
            font-size: 48px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Main Container
    st.markdown('<div class="cover-wrapper">', unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-label">📚 Assignment</div>
        <div class="hero-title">Portfolio Analysis - Góc nhìn của newbie</div>
        <div class="hero-subtitle">Phân tích danh mục đầu tư với các phương pháp định lượng</div>
    </div>
    """, unsafe_allow_html=True)

    # Info Cards (Teacher & University)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <style>
        button[data-testid="stButton"][key="story_nav_col1"] {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("Navigate to Main Story", key="story_nav_col1"):
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

    # Overview Section  
    intro_text = """
    <div class="content-section overview-section">
         <div class="section-title" , cursive;">📖 Giới thiệu bài làm</div>
        <div style="margin-top: 20px; color: #1565C0; line-height: 1.8; font-size: 18px;">
            <p>Bài tập lớn này được nhóm chung em xây dựng dưới góc nhìn của một nhân vật đại diện là Nguyễn Văn Mười, một sinh viên 20 tuổi mới chập chững học về thị trường tài chính. Mười là đại diện những người còn ít trải nghiệm thực tế, đang trong giai đoạn khám phá và tiếp cận các khái niệm đầu tư from scratch.</p>
            <p>Vì vậy, chúng xem mở đầu từ cách chọn Portfolio thật thận trọng, những danh mục ưu tiên an toàn và một số cách đánh giá còn đơn giản, phản ánh đúng mức độ hiểu biết của một nhà đầu tư mới. Mặc dù các phương pháp phân tích chưa thể toàn diện như giới đầu tư chuyên nghiệp, bài báo cáo hướng tới mục tiêu trình bày lại quá trình tiếp cận thị trường theo cách dễ hiểu của một newbie.</p>
            <p>Thông qua hành trình đầu tư của Mười, chúng em mong muốn người đọc – đặc biệt – có thể hiểu hơn phần nào về cách tiếp cận thị trường chứng khoán ở giai đoạn đầu: từ việc lựa chọn cổ phiếu, xem xét chỉ số đến xây dựng danh mục. Bài báo cáo không chỉ mô phỏng trải nghiệm thực tế của một nhà đầu tư trẻ mà còn hướng đến việc truyền tải kiến thức theo cách nhẹ nhàng, gần gũi và dễ tiếp cận.</p>
            <p>Chúng em ý thức rằng bài phân tích vẫn còn nhiều thiếu sót do hạn chế về học thuật kết hợp với kiến thức kinh tế tài chính vĩ mô, và mong cô thông cảm. Tuy nhiên, trong quá trình làm bài, chúng em thấy rất vui và hào hứng trong cả quá trình từ lên ý tưởng, nghiên cứu, thực hiện và cuối cùng là trình bày.</p>
            <p>Chúng em rất cảm ơn cô rất nhiều vì đã cho chúng em cơ hội được freestyle làm một bài tập lớn thật tuyệt như này ạ 💕 Chúc cô luôn vui vẻ, đạt nhiều thành công trong cuộc sống và tạo càng nhiều những cơ hội tuyệt vời như thế này với các bạn sinh viên của mình 💐</p>
        </div>
    </div>
    """
    st.markdown(intro_text, unsafe_allow_html=True)

    # Team Section
    team_text = """
    <div class="content-section team-section" id="team-section">
        <div class="section-title">👥 Thành viên nhóm</div>
        <div class="team-grid">
            <div class="member-card">
                <span style="font-size: 20px; font-weight: bold;">Nguyễn Ngọc Bảo Anh</span><br>
                <span style="font-size: 16px; opacity: 0.85;">MSSV: 11230419<br>Lớp: Actuary 65B</span>
            </div>
            <div class="member-card">
                <span style="font-size: 20px; font-weight: bold;">Nguyễn Bảo Ngọc</span><br>
                <span style="font-size: 16px; opacity: 0.85;">MSSV: 11230473<br>Lớp: Actuary 65B</span>
            </div>
            <div class="member-card">
                <span style="font-size: 20px; font-weight: bold;">Phạm Phương Thảo</span><br>
                <span style="font-size: 16px; opacity: 0.85;">MSSV: 11230493<br>Lớp: Actuary 65B</span>
            </div>
        </div>
    </div>
    """
    st.markdown(team_text, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="cover-footer">
        © 2025 • Khoa Toán kinh tế • Đại học Kinh tế Quốc dân
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

