import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import base64
import yfinance as yf
from scipy.stats import norm
from theme_config import get_current_theme, get_theme_name

def show_draft_2_page(portfolio_df=None, extended_hist=None, PORTFOLIO_HOLDINGS=None):
    """
    Draft 2 - Enhanced layout version of the Draft Story page.
    Same content with improved design, better organization, and theme integration.
    """
    
    theme = get_current_theme()
    
    with st.sidebar:
        st.markdown("### 📚 Sections")
        st.markdown("---")
        
        sections = [
            ("Introduction", "#introduction"),
            ("Why Stocks?", "#why-stocks"),
            ("Investment Strategy", "#investment-strategy"),
            ("Stock Selection", "#stock-selection"),
            ("Filtering Process", "#filtering-process"),
            ("Efficient Frontier", "#efficient-frontier"),
            ("Portfolio Summary", "#portfolio-summary"),
            ("Stock Prices", "#stock-prices"),
            ("Risk Analysis", "#risk-analysis"),
            ("CAPM & Forecast", "#capm-forecast"),
        ]
        
        for label, anchor in sections:
            st.markdown(f"[{label}]({anchor})")
        
        st.markdown("---")

    st.markdown(f"""
    <style>
    .draft2-header {{
        background: linear-gradient(135deg, {theme['primary_color']} 0%, {theme['secondary_color']} 100%);
        padding: 40px 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }}
    .draft2-header h1 {{
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
    }}
    .draft2-header p {{
        margin: 15px 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }}
    .section-card {{
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid {theme['primary_color']};
    }}
    .info-card {{
        background: {theme['section_colors']['box1']};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 4px solid {theme['card_border']};
    }}
    .highlight-box {{
        background: linear-gradient(135deg, {theme['primary_color']}15 0%, {theme['secondary_color']}15 100%);
        border-radius: 10px;
        padding: 20px;
        border: 1px solid {theme['primary_color']}30;
    }}
    .metric-card {{
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-top: 4px solid {theme['primary_color']};
    }}
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin: 20px 0;
    }}
    .feature-item {{
        padding: 20px;
        border-radius: 12px;
        min-height: 180px;
    }}
    .feature-item h4 {{
        margin: 0 0 12px 0;
        font-size: 1.1rem;
    }}
    .feature-item p {{
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="draft2-header">
        <h1>Cau chuyen dau tu cua Nguyen Van Muoi</h1>
        <p>Lay cam hung tu cuon sach noi tieng Ke toan via he</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        with open("meo.png", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <div style="width:100%; height:150px; position:relative; background:transparent; overflow:hidden; margin-bottom:20px;">
            <img src="data:image/png;base64,{b64}" style="
                position:absolute;
                width:150px;
                top:20px;
                left:50%;
                animation: run 6s linear infinite;">
        </div>
        <style>
        @keyframes run {{
          0% {{ left: 100%; }}
          100% {{ left: -200px; }}
        }}
        </style>
        """, unsafe_allow_html=True)
    except:
        pass

    st.markdown('<a name="introduction"></a>', unsafe_allow_html=True)
    
    intro_col1, intro_col2 = st.columns([2, 1])
    
    with intro_col1:
        st.markdown(f"""
        <div class="section-card">
            <h3 style="color: {theme['primary_color']}; margin-top:0;">📌 Begin of the story...</h3>
            <p style="font-size: 16px; line-height: 1.8; color: #333;">
            Day la Nguyen Van Muoi — cau be vua buoc sang tuoi 20 va bat dau cam thay 
            <span title="Fear of Missing Out" style="border-bottom: 1px dotted {theme['primary_color']}; cursor: help; font-weight: bold;">FOMO</span> 
            khi ban be quanh minh ai cung co ke hoach quan ly tien bac va dau tu ro rang. 
            Muon bat kip nhip chung, Muoi tim hieu cac kenh dau tu pho bien cua small investors o Viet Nam 
            va quyet dinh thu suc voi thi truong chung khoan nhu buoc khoi dau cho hanh trinh tai chinh cua minh.
            </p>
            <div style="background: {theme['section_colors']['box2']}; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <p style="margin: 0; font-style: italic;">
                <strong>Warren Buffett</strong> tung noi: "I started investing at the age of 11, but I still regret starting late."
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with intro_col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <img src="https://i.pinimg.com/736x/2c/b5/d6/2cb5d6ebe6fbc60da58b140f8f50c6ff.jpg" 
                 width="100%" style="border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<a name="why-stocks"></a>', unsafe_allow_html=True)
    st.markdown(f"### 💹 Tai sao chon co phieu?")

    feature_colors = [
        (theme['section_colors']['box1'], theme['primary_color']),
        (theme['section_colors']['box2'], theme['secondary_color']),
        (theme['section_colors']['box3'], theme['success_color']),
        (theme['section_colors']['box4'], theme['warning_color'])
    ]
    
    features = [
        ("Faster Money Growth", "So voi gui tiet kiem hay trai phieu, co phieu co tiem nang giup tien cua ban sinh loi nhanh hon theo thoi gian. Du lieu lich su cho thay co phieu mang lai loi suat trung binh hang nam khoang 10% hoac hon trong dai han."),
        ("Time on Your Side", "La mot nha dau tu tre, Muoi co the chiu duoc nhung bien dong cua gia co phieu vi cau co nhieu nam de phuc hoi sau cac dot suy giam cua thi truong."),
        ("Easy to Access", "Co phieu rat de mua va ban, thong tin va nghien cuu ve co phieu co san mien phi, giup viec hoc va dau tu tro nen don gian."),
        ("Low Starting Capital", "Ban khong can so tien lon de bat dau dau tu co phieu tai Viet Nam. Nhieu cong ty chung khoan cho phep mo tai khoan chi tu vai tram nghin dong.")
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, (title, desc) in enumerate(features):
        bg_color, border_color = feature_colors[idx]
        with (col1 if idx % 2 == 0 else col2):
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 20px; border-radius: 12px; border-left: 4px solid {border_color}; margin-bottom: 15px; min-height: 150px;">
                <h4 style="color: #333; margin: 0 0 10px 0;">{title}</h4>
                <p style="color: #555; font-size: 15px; line-height: 1.6; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<a name="investment-strategy"></a>', unsafe_allow_html=True)
    st.markdown(f"### 🎯 Chien luoc dau tu")

    strategy_data = [
        ("Horizon", "Long-term", "Nhan duoc su tang truong theo lai kep, Overcome nhung bien dong gia ngan han", theme['section_colors']['box1']),
        ("Risk Tolerance", "Safe", "Uu tien bao ve von goc va han che thua lo", theme['section_colors']['box2']),
        ("Required Return", "13% / year", "Vuot qua lam phat, Sinh loi so voi lai suat tiet kiem", theme['section_colors']['box3']),
        ("VNIndex", "Intrinsic Value", "Tap trung vao phan tich co ban va actual economic value", theme['section_colors']['box4'])
    ]
    
    cols = st.columns(4)
    for idx, (param, value, desc, bg_color) in enumerate(strategy_data):
        with cols[idx]:
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 20px; border-radius: 12px; text-align: center; min-height: 200px;">
                <h4 style="color: {theme['primary_color']}; margin: 0 0 10px 0; font-size: 14px;">{param}</h4>
                <p style="font-size: 18px; font-weight: bold; color: {theme['secondary_color']}; margin: 0 0 10px 0;">{value}</p>
                <p style="font-size: 13px; color: #666; margin: 0; line-height: 1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<a name="stock-selection"></a>', unsafe_allow_html=True)
    st.markdown(f"### 📊 Tieu chi chon co phieu")

    criteria_tabs = st.tabs(["🏢 Thuong hieu", "📈 Performance", "💰 Dinh gia"])
    
    with criteria_tabs[0]:
        st.markdown(f"""
        <div class="info-card">
            <h4 style="margin-top:0; color: {theme['primary_color']};">Thuong hieu & Su hien dien tren thi truong</h4>
            <ul style="margin: 0; padding-left: 20px;">
                <li><strong>San giao dich:</strong> Uu tien HOSE hoac HNX vi muc do minh bach va uy tin cao hon.</li>
                <li><strong>Do pho bien trong cac quy:</strong> Duoc nhieu to chuc nam giu la tin hieu tich cuc ve chat luong.</li>
                <li><strong>Chat luong du lieu:</strong> It missing value cho thay muc do minh bach va thanh khoan tot.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with criteria_tabs[1]:
        st.markdown(f"""
        <div class="info-card">
            <h4 style="margin-top:0; color: {theme['primary_color']};">Performance & Trien vong</h4>
            <ul style="margin: 0; padding-left: 20px;">
                <li><strong>EPS (Earnings per Share):</strong> Thu nhap tren moi co phieu.</li>
                <li><strong>ROE (Return on Equity):</strong> Hieu qua su dung von chu so huu.</li>
                <li><strong>F-score (Piotroski):</strong> Danh gia chat luong tai chinh tong the.</li>
                <li><strong>M-score:</strong> Giup phat hien nguy co gian lan loi nhuan.</li>
                <li><strong>Z-score (Altman):</strong> Do luong rui ro pha san.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with criteria_tabs[2]:
        st.markdown(f"""
        <div class="info-card">
            <h4 style="margin-top:0; color: {theme['primary_color']};">Reasonably Priced (Gia hop ly)</h4>
            <ul style="margin: 0; padding-left: 20px;">
                <li><strong>P/E Ratio:</strong> Dinh gia tuong doi, can so sanh nganh</li>
                <li><strong>Intrinsic Value:</strong> Uoc tinh gia tri noi tai (Buffett principle)</li>
                <li><strong>Margin of Safety:</strong> Luon tim mua duoi gia tri noi tai</li>
                <li><strong>Long-term Focus:</strong> Tap trung vao gia tri thuc chu khong gia tam thoi</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<a name="filtering-process"></a>', unsafe_allow_html=True)
    st.markdown(f"### 🔽 Quy trinh loc co phieu")

    funnel_stages = [
        ('Toan bo thi truong', 1025, '#1976D2'),
        ('EPS > 1,500', 495, '#1E88E5'),
        ('ROE > 12%', 282, '#42A5F5'),
        ('HSX & HNX', 264, '#64B5F6'),
        ('IPO > 10 nam', 143, '#90CAF9'),
        ('Z-score > 3', 58, '#BBDEFB'),
        ('M-score OK', 25, '#E3F2FD'),
        ('Portfolio (4)', 4, '#4CAF50')
    ]
    
    fig_funnel = go.Figure(go.Funnel(
        y=[stage[0] for stage in funnel_stages],
        x=[stage[1] for stage in funnel_stages],
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=[stage[2] for stage in funnel_stages]),
        connector=dict(line=dict(color="royalblue", width=2))
    ))
    
    fig_funnel.update_layout(
        title="Stock Filtering Funnel",
        height=500,
        template='plotly_white',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig_funnel, use_container_width=True)

    st.markdown("---")
    st.markdown('<a name="efficient-frontier"></a>', unsafe_allow_html=True)
    st.markdown(f"### 📈 Efficient Frontier Analysis")

    try:
        frontier_data = pd.read_csv('attached_assets/result_output_1763851487710.csv', index_col=0)
        
        fig_ef = go.Figure()
        
        fig_ef.add_trace(go.Scatter(
            x=frontier_data['StdDev'] * 100,
            y=frontier_data['mean'] * 100,
            mode='lines+markers',
            name='Efficient Frontier',
            line=dict(color=theme['primary_color'], width=3),
            marker=dict(size=8),
            hovertemplate='<b>Risk:</b> %{x:.3f}%<br><b>Return:</b> %{y:.4f}%<extra></extra>'
        ))
        
        min_risk_idx = frontier_data['StdDev'].idxmin()
        min_risk_row = frontier_data.loc[min_risk_idx]
        
        fig_ef.add_trace(go.Scatter(
            x=[min_risk_row['StdDev'] * 100],
            y=[min_risk_row['mean'] * 100],
            mode='markers',
            name='Min Variance Portfolio',
            marker=dict(size=15, color=theme['success_color'], symbol='star'),
            hovertemplate='<b>Min Variance</b><br>Risk: %{x:.3f}%<br>Return: %{y:.4f}%<extra></extra>'
        ))
        
        fig_ef.update_layout(
            title='Efficient Frontier - Portfolio Optimization',
            xaxis_title='Daily Risk (Standard Deviation %)',
            yaxis_title='Daily Expected Return (%)',
            height=450,
            template='plotly_white',
            legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.9)')
        )
        
        st.plotly_chart(fig_ef, use_container_width=True)
        
        st.markdown(f"""
        <div style="background: {theme['section_colors']['box3']}; padding: 20px; border-radius: 10px; text-align: center; margin-top: 20px;">
            <p style="color: #333; margin: 0; font-size: 16px;">
            <strong>Portfolio cuoi cung:</strong>
            </p>
            <p style="color: {theme['primary_color']}; margin: 12px 0 0 0; font-size: 20px; font-weight: bold;">
            ACB (20.5%) • HPG (3.1%) • VNM (39.5%) • DBD (36.9%)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.warning(f"Could not load efficient frontier data: {e}")

    st.markdown("---")
    st.markdown('<a name="portfolio-summary"></a>', unsafe_allow_html=True)
    st.markdown(f"### 📋 Portfolio Summary")

    chosen_stocks = pd.DataFrame({
        'Stock': ['ACB', 'HPG', 'VNM', 'DBD'],
        'Allocation': [20.5, 3.1, 39.5, 36.9],
        'Sector': ['Banking', 'Materials', 'Consumer Staples', 'Pharmaceuticals'],
        'Risk': ['Medium', 'High', 'Low', 'Medium']
    })

    summary_col1, summary_col2 = st.columns([1, 1])
    
    with summary_col1:
        pastel_colors = ['#A8D8EA', '#AA96DA', '#FCBAD3', '#FFFFD2']
        
        fig_allocation = go.Figure(data=[
            go.Pie(
                labels=chosen_stocks['Stock'],
                values=chosen_stocks['Allocation'],
                marker=dict(colors=pastel_colors, line=dict(color='#fff', width=2)),
                textposition='inside',
                textinfo='label+percent',
                hole=0.45,
                hovertemplate='<b>%{label}</b><br>Allocation: %{value}%<extra></extra>'
            )
        ])
        
        fig_allocation.update_layout(
            title='Portfolio Allocation',
            height=400,
            template='plotly_white',
            showlegend=True,
            legend=dict(x=1, y=0.5)
        )
        
        st.plotly_chart(fig_allocation, use_container_width=True)
    
    with summary_col2:
        st.markdown("#### Key Metrics")
        
        metrics = [
            ("Daily Return", "0.0481%"),
            ("Annual Return", "12.88%"),
            ("Daily Volatility", "1.106%"),
            ("Annual Volatility", "17.55%"),
            ("Sharpe Ratio", "0.551"),
            ("Beta", "0.571")
        ]
        
        for i in range(0, len(metrics), 2):
            metric_cols = st.columns(2)
            for j, col in enumerate(metric_cols):
                if i + j < len(metrics):
                    name, value = metrics[i + j]
                    col.metric(name, value)

    st.markdown("---")
    st.markdown('<a name="stock-prices"></a>', unsafe_allow_html=True)
    st.markdown(f"### 📈 Stock Prices Analysis")

    try:
        price_df = pd.read_csv('attached_assets/price.csv')
        price_df['time'] = pd.to_datetime(price_df['time'], format='%m/%d/%Y')
        
        start_date = pd.to_datetime('2022-06-01')
        price_df = price_df[price_df['time'] >= start_date]
        price_df = price_df.set_index('time').sort_index()
        
        stocks_needed = ['ACB', 'HPG', 'VNM', 'DBD']
        price_data = price_df[stocks_needed].copy()
        
        colors_line = {
            'ACB': theme['primary_color'],
            'HPG': '#00D9FF',
            'VNM': theme['warning_color'],
            'DBD': theme['secondary_color']
        }
        
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
            title='Daily Closing Prices',
            xaxis_title='Date',
            yaxis_title='Price (VND)',
            height=450,
            template='plotly_white',
            hovermode='x unified',
            legend=dict(x=0.02, y=0.98, bgcolor='rgba(255, 255, 255, 0.9)')
        )
        
        st.plotly_chart(fig_price, use_container_width=True)
        
        st.markdown(f"""
        <div class="info-card">
            <h5 style="color: {theme['primary_color']}; margin-top: 0;">📊 Price Trends Analysis</h5>
            <ul style="color: #555; font-size: 15px; line-height: 1.7; margin: 0; padding-left: 20px;">
                <li><strong>ACB va HPG:</strong> Co su dong pha ro ret, dao dong sat nhau. Duy tri xu huong tang truong ben vung va on dinh.</li>
                <li><strong>VNM:</strong> Xu huong dai han la di xuong. Co phieu tung xuat hien "bong bong" gia vao cuoi nam 2022.</li>
                <li><strong>DBD:</strong> Nguoc lai voi VNM, gia tang dan tu 30.000 len 60.000 VND.</li>
                <li><strong>Nhan xet:</strong> Cac chung khoan trong portfolio co phan khuc gia khac nhau va xu huong khac nhau, giup diversify rui ro.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.warning(f"Could not load price data: {e}")

    st.markdown("---")
    st.markdown('<a name="risk-analysis"></a>', unsafe_allow_html=True)
    st.markdown(f"### ⚠️ Risk Analysis")

    risk_tabs = st.tabs(["📊 Beta Analysis", "📉 VaR & ES", "📈 Performance Metrics"])
    
    with risk_tabs[0]:
        try:
            beta_daily_df = pd.read_csv('beta.csv', index_col=0, parse_dates=True)
            beta_daily_df.columns = ['Daily_Beta']
            
            beta_rol_df = pd.read_csv('beta_rol.csv', index_col=0)
            beta_rol_df.columns = ['Rolling_60D_Beta']
            
            rolling_start_idx = 60
            dates_for_rolling = beta_daily_df.index[rolling_start_idx:]
            rolling_beta_with_dates = beta_rol_df['Rolling_60D_Beta'].values[:len(dates_for_rolling)]
            rolling_beta_series = pd.Series(rolling_beta_with_dates, index=dates_for_rolling)
            
            fig_beta = go.Figure()
            
            fig_beta.add_trace(go.Scatter(
                x=beta_daily_df.index,
                y=beta_daily_df['Daily_Beta'],
                mode='lines',
                name='Daily Beta (DCC-GARCH)',
                line=dict(color='rgba(255, 182, 193, 0.8)', width=2)
            ))
            
            fig_beta.add_trace(go.Scatter(
                x=rolling_beta_series.index,
                y=rolling_beta_series,
                mode='lines',
                name='Rolling 60-Day Beta (OLS)',
                line=dict(color=theme['primary_color'], width=3)
            ))
            
            fig_beta.add_hline(y=1.0, line_dash="dot", line_color="orange", 
                             annotation_text="Market (beta=1.0)", annotation_position="right")
            
            fig_beta.update_layout(
                title="Daily Beta vs Rolling 60-Day Beta",
                xaxis_title="Date",
                yaxis_title="Beta Value",
                hovermode='x unified',
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_beta, use_container_width=True)
            
            beta_cols = st.columns(3)
            with beta_cols[0]:
                st.metric("Average Daily Beta", f"{beta_daily_df['Daily_Beta'].mean():.4f}")
            with beta_cols[1]:
                st.metric("Average Rolling Beta", f"{rolling_beta_series.mean():.4f}")
            with beta_cols[2]:
                noise_reduction = ((beta_daily_df['Daily_Beta'].std() - rolling_beta_series.std()) / beta_daily_df['Daily_Beta'].std() * 100)
                st.metric("Noise Reduction", f"{noise_reduction:.1f}%")
                
        except Exception as e:
            st.warning(f"Could not load beta data: {e}")
    
    with risk_tabs[1]:
        try:
            returns_df = pd.read_csv('port.csv', usecols=['Portfolio'])
            portfolio_returns = pd.to_numeric(returns_df['Portfolio'], errors='coerce').dropna()
            
            confidence_level = st.radio(
                "Select confidence level:", 
                options=[85, 90, 95, 99],
                format_func=lambda x: f"{x}%",
                horizontal=True,
                key="var_confidence_draft2"
            )
            alpha = 1 - (confidence_level / 100)
            
            var_hist = np.percentile(portfolio_returns, alpha * 100)
            es_hist = portfolio_returns[portfolio_returns <= var_hist].mean()
            
            mean_ret = portfolio_returns.mean()
            std_ret = portfolio_returns.std()
            z_score = norm.ppf(alpha)
            var_param = mean_ret + z_score * std_ret
            pdf_z = norm.pdf(z_score)
            es_param = mean_ret - std_ret * (pdf_z / alpha)
            
            np.random.seed(42)
            n_sims = 10000
            sim_returns = np.random.normal(mean_ret, std_ret, n_sims)
            var_mc = np.percentile(sim_returns, alpha * 100)
            es_mc = sim_returns[sim_returns <= var_mc].mean()
            
            var_cols = st.columns(3)
            
            methods = ['Historical', 'Parametric', 'Monte Carlo']
            vars_vals = [var_hist, var_param, var_mc]
            es_vals = [es_hist, es_param, es_mc]
            
            for col, method, var_val, es_val in zip(var_cols, methods, vars_vals, es_vals):
                with col:
                    st.markdown(f"""
                    <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-top: 4px solid {theme['primary_color']};">
                        <h5 style="color: {theme['primary_color']}; margin: 0 0 15px 0;">{method}</h5>
                        <p style="margin: 0; font-size: 14px; color: #666;">VaR ({confidence_level}%)</p>
                        <p style="margin: 5px 0 15px 0; font-size: 20px; font-weight: bold; color: #E74C3C;">{var_val:.4f}</p>
                        <p style="margin: 0; font-size: 14px; color: #666;">Expected Shortfall</p>
                        <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: bold; color: #3498DB;">{es_val:.4f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
        except Exception as e:
            st.warning(f"Could not calculate VaR: {e}")
    
    with risk_tabs[2]:
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            st.markdown("**Valuation Multiples**")
            valuation_data = pd.DataFrame({
                'Metric': ['P/E', 'P/B', 'P/S'],
                'Portfolio': [13.88, 2.97, 2.03],
                'VNIndex': [13.28, 1.67, 1.71]
            })
            st.dataframe(valuation_data.set_index('Metric'), use_container_width=True)
        
        with metrics_col2:
            st.markdown("**Profitability**")
            profit_data = pd.DataFrame({
                'Metric': ['ROE (%)', 'ROA (%)'],
                'Portfolio': [20.73, 11.47],
                'VNIndex': [13.03, 2.14]
            })
            st.dataframe(profit_data.set_index('Metric'), use_container_width=True)

    st.markdown("---")
    st.markdown('<a name="capm-forecast"></a>', unsafe_allow_html=True)
    st.markdown(f"### 📈 CAPM & Forecast")

    capm_col1, capm_col2 = st.columns(2)
    
    with capm_col1:
        st.markdown("#### CAPM Formula")
        st.latex(r"E(R_p) = R_f + \beta \times (R_m - R_f)")
        
        st.markdown(f"""
        <div class="info-card">
            <p><strong>Parameters:</strong></p>
            <ul style="margin: 0; padding-left: 20px;">
                <li><strong>Rf</strong> (Risk-free rate) = 3.30%</li>
                <li><strong>Rm</strong> (Market return) = 9.70%</li>
                <li><strong>Beta</strong> = 0.571</li>
                <li><strong>Expected Return</strong> = 6.95%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with capm_col2:
        st.markdown("#### Portfolio Interpretation")
        st.markdown(f"""
        <div class="info-card">
            <p style="line-height: 1.8;">
            Portfolio nay duoc thiet ke de mang lai loi nhuan on dinh, voi loi suat hang nam khoang 13.3% 
            trong khi kiem soat rui ro o muc hop ly. Nho Beta khoang 0.57, portfolio dao dong it hon thi truong, 
            giup bao ve von trong cac giai doan bien dong manh.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, {theme['primary_color']}10 0%, {theme['secondary_color']}10 100%); border-radius: 12px;">
        <p style="color: {theme['primary_color']}; font-size: 14px; margin: 0;">
        📚 Draft 2 - Enhanced Layout Version | Theme: {get_theme_name()}
        </p>
    </div>
    """, unsafe_allow_html=True)
