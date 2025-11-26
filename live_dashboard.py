import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def show_live_dashboard():
    """Live Portfolio Dashboard with real-time monitoring (beta version)"""
    
    st.title("💹 LIVE Portfolio Dashboard (beta)")
    st.markdown("---")
    
    st.markdown(
        "<p style='color: #666; font-size: 14px;'><i>⚠️ Beta version: This dashboard is currently under development and may have limited functionality.</i></p>",
        unsafe_allow_html=True
    )
    
    st.markdown("")
    
    # Key Metrics Section
    st.subheader("📊 Portfolio Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Portfolio Value",
            value="$138,780",
            delta="+$5,780 (+4.35%)",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Daily Change",
            value="+$245",
            delta="+0.18%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="YTD Return",
            value="+8.92%",
            delta="vs VNINDEX +5.12%",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Portfolio Beta",
            value="0.92",
            delta="Less volatile than market",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Holdings Section
    st.subheader("📈 Stock Holdings")
    
    holdings_data = {
        'Ticker': ['ACB', 'HPG', 'VNM', 'DBD'],
        'Company': ['Asia Commercial Bank', 'Hoa Phat Group', 'Vietnam Beverage', 'Diamond Brightest'],
        'Shares': [100, 100, 100, 100],
        'Current Price': ['$25.80', '$28.30', '$59.32', '$25.65'],
        'Position Value': ['$2,580', '$2,830', '$5,932', '$2,565'],
        'Gain/Loss': ['+$80 (+3.2%)', '-$170 (-5.7%)', '+$620 (+11.7%)', '+$115 (+4.7%)'],
        'Weight': ['18.6%', '20.4%', '42.8%', '18.5%']
    }
    
    holdings_df = pd.DataFrame(holdings_data)
    st.dataframe(holdings_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Performance Chart Section
    st.subheader("📉 Performance Tracking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Portfolio Performance (1M)**")
        
        # Sample performance data
        dates = pd.date_range(start='2024-10-25', end='2024-11-25', freq='D')
        portfolio_values = [133000 + i * 230 + (i % 5) * 50 for i in range(len(dates))]
        
        fig_perf = go.Figure()
        fig_perf.add_trace(go.Scatter(
            x=dates,
            y=portfolio_values,
            mode='lines+markers',
            name='Portfolio Value',
            line=dict(color='#1E40AF', width=2),
            fill='tozeroy',
            fillcolor='rgba(30, 64, 175, 0.1)'
        ))
        
        fig_perf.update_layout(
            height=350,
            template='plotly',
            plot_bgcolor='#f5f5f5',
            paper_bgcolor='#f5f5f5',
            hovermode='x unified',
            xaxis_title='Date',
            yaxis_title='Portfolio Value ($)',
            margin=dict(l=50, r=30, t=30, b=40)
        )
        
        st.plotly_chart(fig_perf, use_container_width=True)
    
    with col2:
        st.markdown("**Stock Performance Comparison**")
        
        stocks = ['ACB', 'HPG', 'VNM', 'DBD']
        performance = [3.2, -5.7, 11.7, 4.7]
        colors = ['#4CAF50' if x > 0 else '#F44336' for x in performance]
        
        fig_stocks = go.Figure()
        fig_stocks.add_trace(go.Bar(
            x=stocks,
            y=performance,
            marker=dict(color=colors),
            text=[f'{x:.1f}%' for x in performance],
            textposition='outside',
            name='Return %'
        ))
        
        fig_stocks.update_layout(
            height=350,
            template='plotly',
            plot_bgcolor='#f5f5f5',
            paper_bgcolor='#f5f5f5',
            hovermode='x unified',
            xaxis_title='Stock',
            yaxis_title='Return (%)',
            margin=dict(l=50, r=30, t=30, b=40),
            showlegend=False
        )
        
        st.plotly_chart(fig_stocks, use_container_width=True)
    
    st.markdown("---")
    
    # Sector Allocation
    st.subheader("🎯 Sector Allocation")
    
    sector_data = {
        'Sector': ['Beverage', 'Banking', 'Steel', 'Retail'],
        'Allocation': [42.8, 18.6, 20.4, 18.5]
    }
    
    fig_sectors = go.Figure(data=[go.Pie(
        labels=sector_data['Sector'],
        values=sector_data['Allocation'],
        marker=dict(colors=['#FF6B9D', '#4A90E2', '#7B68EE', '#FFA500'])
    )])
    
    fig_sectors.update_layout(
        height=400,
        template='plotly',
        paper_bgcolor='#f5f5f5',
        margin=dict(l=30, r=30, t=30, b=30)
    )
    
    st.plotly_chart(fig_sectors, use_container_width=True)
    
    st.markdown("---")
    
    # Alert Section
    st.subheader("🚨 Alerts & Notifications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📌 VNM reached 52-week high. Consider profit-taking at $61.50")
    
    with col2:
        st.warning("⚠️ HPG below 50-day moving average. Monitor closely.")
    
    st.markdown("---")
    
    # Footer with last update time
    st.markdown(
        f"<p style='text-align: center; font-size: 12px; color: gray;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>",
        unsafe_allow_html=True
    )
