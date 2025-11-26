import streamlit as st

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
    },
    "Ocean Teal": {
        "primary_color": "#00796B",
        "secondary_color": "#004D40",
        "accent_color": "#80CBC4",
        "background_gradient": "linear-gradient(135deg, #E0F2F1 0%, #B2DFDB 50%, #80CBC4 100%)",
        "card_bg": "#E0F2F1",
        "card_border": "#00796B",
        "text_color": "#263238",
        "highlight_color": "#00897B",
        "success_color": "#26A69A",
        "warning_color": "#FFB300",
        "info_box_bg": "#E0F7FA",
        "section_colors": {
            "box1": "#E0F2F1",
            "box2": "#B2EBF2",
            "box3": "#C8E6C9",
            "box4": "#DCEDC8"
        }
    },
    "Sunset Orange": {
        "primary_color": "#E65100",
        "secondary_color": "#BF360C",
        "accent_color": "#FFAB91",
        "background_gradient": "linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 50%, #FFCC80 100%)",
        "card_bg": "#FFF3E0",
        "card_border": "#E65100",
        "text_color": "#3E2723",
        "highlight_color": "#FF6D00",
        "success_color": "#7CB342",
        "warning_color": "#F57C00",
        "info_box_bg": "#FBE9E7",
        "section_colors": {
            "box1": "#FFF3E0",
            "box2": "#FCE4EC",
            "box3": "#FFEBEE",
            "box4": "#FBE9E7"
        }
    },
    "Royal Purple": {
        "primary_color": "#7B1FA2",
        "secondary_color": "#4A148C",
        "accent_color": "#CE93D8",
        "background_gradient": "linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 50%, #CE93D8 100%)",
        "card_bg": "#F3E5F5",
        "card_border": "#7B1FA2",
        "text_color": "#311B92",
        "highlight_color": "#9C27B0",
        "success_color": "#66BB6A",
        "warning_color": "#FFA726",
        "info_box_bg": "#EDE7F6",
        "section_colors": {
            "box1": "#F3E5F5",
            "box2": "#E8EAF6",
            "box3": "#FCE4EC",
            "box4": "#EDE7F6"
        }
    },
    "Forest Green": {
        "primary_color": "#2E7D32",
        "secondary_color": "#1B5E20",
        "accent_color": "#A5D6A7",
        "background_gradient": "linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 50%, #A5D6A7 100%)",
        "card_bg": "#E8F5E9",
        "card_border": "#2E7D32",
        "text_color": "#1B5E20",
        "highlight_color": "#43A047",
        "success_color": "#66BB6A",
        "warning_color": "#FFB300",
        "info_box_bg": "#DCEDC8",
        "section_colors": {
            "box1": "#E8F5E9",
            "box2": "#F1F8E9",
            "box3": "#C8E6C9",
            "box4": "#DCEDC8"
        }
    }
}

def get_current_theme():
    """Get the current theme from session state or return default"""
    if "current_theme" not in st.session_state:
        st.session_state.current_theme = "Default Blue"
    return THEMES[st.session_state.current_theme]

def get_theme_name():
    """Get the current theme name"""
    if "current_theme" not in st.session_state:
        st.session_state.current_theme = "Default Blue"
    return st.session_state.current_theme

def create_theme_selector():
    """Create theme selector in sidebar"""
    st.sidebar.markdown("### 🎨 Theme")
    
    theme_options = list(THEMES.keys())
    current_idx = theme_options.index(st.session_state.get("current_theme", "Default Blue"))
    
    selected_theme = st.sidebar.selectbox(
        "Choose Theme",
        options=theme_options,
        index=current_idx,
        key="theme_selector"
    )
    
    if selected_theme != st.session_state.get("current_theme", "Default Blue"):
        st.session_state.current_theme = selected_theme
        st.rerun()

def apply_theme_css():
    """Apply theme CSS to the page"""
    theme = get_current_theme()
    
    st.markdown(f"""
    <style>
    .main {{
        background: {theme['background_gradient']};
    }}
    
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {theme['primary_color']} 0%, {theme['secondary_color']} 100%) !important;
        border-color: {theme['primary_color']} !important;
    }}
    
    .stButton > button[kind="primary"]:hover {{
        background: linear-gradient(135deg, {theme['secondary_color']} 0%, {theme['primary_color']} 100%) !important;
    }}
    
    h1, h2, h3 {{
        color: {theme['primary_color']} !important;
    }}
    
    .themed-card {{
        background-color: {theme['card_bg']};
        border-left: 5px solid {theme['card_border']};
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }}
    
    .themed-info-box {{
        background-color: {theme['info_box_bg']};
        border-left: 5px solid {theme['card_border']};
        padding: 20px;
        border-radius: 10px;
    }}
    
    .themed-header {{
        background: linear-gradient(135deg, {theme['primary_color']} 0%, {theme['secondary_color']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    </style>
    """, unsafe_allow_html=True)
