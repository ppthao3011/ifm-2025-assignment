import streamlit as st

def create_pill_navigation():
    """Option 8: Rounded Pill Buttons sidebar - All buttons styled consistently"""
    st.sidebar.markdown("### 📖 Navigation")
    st.sidebar.markdown("---")
    
    pages = [
        {"id": "📋 Cover Page", "label": "📋 Cover Page"},
        {"id": "📚 Theory Framework", "label": "📚 Theory Framework"},
        {"id": "📖 Main Story", "label": "📖 Main Story"},
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
    # THEME SELECTOR
    # ============================================================================
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Custom Theme")
    
    theme_option = st.sidebar.radio(
        "Select Theme:",
        ["Light", "Dark", "Custom Color"],
        key="theme_radio"
    )
    
    if theme_option == "Light":
        st.markdown("""
        <style>
        :root {
            --primary-color: #1E88E5;
            --bg-color: #F5F5F5;
            --sidebar-color: #EEEEEE;
            --text-color: #212121;
        }
        </style>
        """, unsafe_allow_html=True)
    
    elif theme_option == "Dark":
        st.markdown("""
        <style>
        :root {
            --primary-color: #BB86FC;
            --bg-color: #121212;
            --sidebar-color: #1E1E1E;
            --text-color: #FFFFFF;
        }
        </style>
        """, unsafe_allow_html=True)
    
    elif theme_option == "Custom Color":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            primary_color = st.sidebar.color_picker("Primary", value="#4A90E2")
        with col2:
            bg_color = st.sidebar.color_picker("Background", value="#E8F4F8")
        
        st.markdown(f"""
        <style>
        :root {{
            --primary-color: {primary_color};
            --bg-color: {bg_color};
        }}
        </style>
        """, unsafe_allow_html=True)
    
