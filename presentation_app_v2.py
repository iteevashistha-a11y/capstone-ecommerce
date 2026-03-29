"""
🚀 E-Commerce Product Description Solution - CREATIVE EDITION
Next-Gen Interactive Presentation with Modern UI/UX
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu
import sys
from pathlib import Path
import time

# Add agents to path
sys.path.insert(0, str(Path(__file__).parent))

from agents import (
    market_agent,
    financial_agent,
    technical_agent,
    usecase_agent,
    strategy_agent
)
from utils import visualizations, data_processor

# Page configuration
st.set_page_config(
    page_title="AI Product Description Solution",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = []

def check_login(username, password):
    """Verify credentials"""
    demo_users = {
        "demo": "demo123",
        "admin": "admin@123",
        "user": "user@123",
        "seller": "seller@2026",
        "test": "test123"
    }
    return username in demo_users and demo_users[username] == password

# 🎨 MODERN CREATIVE CSS STYLING
st.markdown("""
    <style>
    /* Root Variables */
    :root {
        --primary: #1e5a96;
        --secondary: #512da8;
        --accent: #e65100;
        --success: #2e7d32;
        --warning: #f57f17;
        --dark-bg: #0f1419;
        --light-bg: #f5f7fa;
    }
    
    /* Global Styles */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
        padding-top: 2rem;
    }
    
    /* Modern Card Styles */
    .modern-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(30, 90, 150, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .modern-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(30, 90, 150, 0.2);
        border-color: rgba(30, 90, 150, 0.3);
    }
    
    /* Gradient Cards */
    .gradient-card-primary {
        background: linear-gradient(135deg, #1e5a96 0%, #2575ba 100%);
        color: white;
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 8px 32px rgba(30, 90, 150, 0.3);
    }
    
    .gradient-card-secondary {
        background: linear-gradient(135deg, #512da8 0%, #7e57c2 100%);
        color: white;
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 8px 32px rgba(81, 45, 168, 0.3);
    }
    
    .gradient-card-accent {
        background: linear-gradient(135deg, #e65100 0%, #ef6c00 100%);
        color: white;
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 8px 32px rgba(230, 81, 0, 0.3);
    }
    
    /* KPI Container */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }
    
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border-left: 4px solid #1e5a96;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: scale(1.05);
        border-left-color: #e65100;
        box-shadow: 0 8px 24px rgba(230, 81, 0, 0.15);
    }
    
    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #1e5a96;
        margin: 8px 0;
    }
    
    .kpi-label {
        font-size: 13px;
        color: #666;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    /* Section Header */
    .section-header {
        background: linear-gradient(90deg, #1e5a96 0%, #512da8 100%);
        color: white;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(30, 90, 150, 0.2);
    }
    
    .section-header h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 800;
    }
    
    .section-header p {
        margin: 8px 0 0 0;
        font-size: 14px;
        opacity: 0.9;
    }
    
    /* Feature Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .feature-item {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #e65100;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .feature-item:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 24px rgba(230, 81, 0, 0.15);
        border-left-color: #512da8;
    }
    
    .feature-icon {
        font-size: 32px;
        margin-bottom: 12px;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-success {
        background: #e8f5e9;
        color: #2e7d32;
    }
    
    .badge-warning {
        background: #fff8e1;
        color: #f57f17;
    }
    
    .badge-info {
        background: #e3f2fd;
        color: #1565c0;
    }
    
    /* Progress Bar */
    .progress-bar {
        background: #e0e0e0;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin: 12px 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #1e5a96 0%, #512da8 100%);
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    /* Sidebar Styles */
    .sidebar-header {
        background: linear-gradient(135deg, #1e5a96 0%, #512da8 100%);
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 16px;
        text-align: center;
    }
    
    .login-container {
        background: white;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 2px solid #e65100;
    }
    
    /* Animation */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated {
        animation: slideIn 0.5s ease;
    }
    
    /* Title */
    h1 {
        color: #1e5a96;
        font-weight: 800;
        font-size: 40px;
        margin-top: 0;
    }
    
    h2 {
        color: #1e5a96;
        font-weight: 700;
        font-size: 28px;
        margin-top: 24px;
    }
    
    h3 {
        color: #512da8;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR NAVIGATION ====================
with st.sidebar:
    # Creative header
    st.markdown("""
        <div class="sidebar-header">
            <h2 style="margin: 0; font-size: 24px;">🚀 AI PRODUCT DESCRIPTIONS</h2>
            <p style="margin: 8px 0 0 0; font-size: 12px; opacity: 0.9;">Next Gen Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Authentication
    if not st.session_state.authenticated:
        st.markdown("""
            <div class="login-container">
                <h3 style="margin-top: 0; color: #e65100;">🔐 Unlock Access</h3>
            </div>
        """, unsafe_allow_html=True)
        
        login_username = st.text_input("👤 Username", key="login_username", placeholder="Enter username")
        login_password = st.text_input("🔑 Password", type="password", key="login_password", placeholder="Enter password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔓 Login", use_container_width=True, key="login_btn"):
                if login_username and login_password:
                    if check_login(login_username, login_password):
                        st.session_state.authenticated = True
                        st.session_state.username = login_username
                        st.success(f"✅ Welcome {login_username}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.warning("⚠️ Enter credentials")
        
        with col2:
            if st.button("ℹ️ Demo", use_container_width=True, key="demo_btn"):
                st.info("""
                **Demo Credentials:**
                - demo / demo123
                - admin / admin@123
                - seller / seller@2026
                """)
    else:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2e7d32 0%, #388e3c 100%); color: white; 
            padding: 16px; border-radius: 12px; text-align: center; margin-bottom: 12px;">
                <h3 style="margin: 0; color: white; font-size: 18px;">✅ {st.session_state.username.upper()}</h3>
                <p style="margin: 4px 0 0 0; font-size: 12px; opacity: 0.9;">Logged In</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔓 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.success("✅ Logged out!")
            time.sleep(1)
            st.rerun()
    
    st.divider()
    
    # Navigation menu
    selected = option_menu(
        menu_title="📋 MENU",
        options=[
            "🏠 Home",
            "📊 Market 360",
            "🇮🇳 India Focus",
            "🌍 Global View",
            "📈 Growth Analytics",
            "💼 Financial Model",
            "⚙️ Tech Stack",
            "💡 Use Cases",
            "🎯 Strategy",
            "🏆 Competitive Edge",
            "📍 Roadmap",
            "🛒 Cart",
            "⚙️ Settings"
        ],
        icons=[
            "house", "graph-up", "pin-map", "globe", "bar-chart",
            "cash-coin", "gear", "lightbulb", "target", "trophy", "map", "cart", "sliders"
        ],
        menu_icon="menu-button-wide",
        default_index=0,
        styles={
            "container": {"padding": "0.5rem"},
            "nav-link": {
                "font-size": "14px",
                "margin": "0.5rem 0",
                "border-radius": "10px",
                "padding": "10px 12px"
            },
            "nav-link-selected": {
                "background-color": "#e65100",
                "color": "white",
                "font-weight": "bold"
            }
        }
    )

# ==================== MAIN CONTENT ====================

if selected == "🏠 Home":
    # Hero Section
    st.markdown("""
        <div class="section-header">
            <h1>🚀 AI-Powered Product Descriptions</h1>
            <p>Transform E-Commerce with Intelligent Content Generation | India & Global Ready</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="kpi-card">
                <div style="font-size: 28px;">💰</div>
                <div class="kpi-value">$3.5B</div>
                <div class="kpi-label">Market TAM</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 85%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="kpi-card">
                <div style="font-size: 28px;">📈</div>
                <div class="kpi-value">25%</div>
                <div class="kpi-label">India CAGR</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 90%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="kpi-card">
                <div style="font-size: 28px;">🌍</div>
                <div class="kpi-value">50M+</div>
                <div class="kpi-label">Global Sellers</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 75%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="kpi-card">
                <div style="font-size: 28px;">⚡</div>
                <div class="kpi-value">50x</div>
                <div class="kpi-label">ROI Potential</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 95%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Problem vs Solution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="gradient-card-accent">
                <h3 style="color: white; margin-top: 0;">❌ The Problem</h3>
                <ul style="color: white; line-height: 1.8;">
                    <li><strong>$2.5B</strong> wasted on manual descriptions yearly</li>
                    <li><strong>15-30 min</strong> per product (slow!)</li>
                    <li><strong>$2-5</strong> cost per description</li>
                    <li>⚠️ <strong>Inconsistent quality</strong></li>
                    <li>🔍 <strong>Poor SEO optimization</strong></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="gradient-card-primary">
                <h3 style="color: white; margin-top: 0;">✅ Our Solution</h3>
                <ul style="color: white; line-height: 1.8;">
                    <li><strong>&lt;5 seconds</strong> per image (blazing fast!)</li>
                    <li><strong>$0.01-0.50</strong> per description (99% cheaper!)</li>
                    <li>✨ <strong>90-95% accuracy</strong> with AI</li>
                    <li>📱 <strong>Multi-platform ready</strong> (Shopify, WooCommerce)</li>
                    <li>🎯 <strong>Built-in SEO optimization</strong></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Features Grid
    st.subheader("🎯 Key Features & Benefits")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-item">
                <div class="feature-icon">🖼️</div>
                <h4 style="margin-top: 0;">Image Recognition</h4>
                <p>Advanced AI detects every detail in product images for accurate descriptions.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-item">
                <div class="feature-icon">🌐</div>
                <h4 style="margin-top: 0;">Multi-Language</h4>
                <p>Generate descriptions in 50+ languages for global reach.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-item">
                <div class="feature-icon">📊</div>
                <h4 style="margin-top: 0;">Analytics Ready</h4>
                <p>Built-in analytics track performance and optimize conversion.</p>
            </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-item">
                <div class="feature-icon">🔌</div>
                <h4 style="margin-top: 0;">API Integration</h4>
                <p>Seamless integration with Shopify, Amazon, Myntra, WooCommerce.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-item">
                <div class="feature-icon">⚙️</div>
                <h4 style="margin-top: 0;">Custom AI Models</h4>
                <p>Train models on your brand guidelines and tone.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-item">
                <div class="feature-icon">🎨</div>
                <h4 style="margin-top: 0;">A/B Testing</h4>
                <p>Generate multiple variations and test for best conversion.</p>
            </div>
        """, unsafe_allow_html=True)

elif selected == "📊 Market 360":
    st.markdown("""
        <div class="section-header">
            <h1>📊 Comprehensive Market Analysis</h1>
            <p>Global E-Commerce Product Description Market Deep Dive</p>
        </div>
    """, unsafe_allow_html=True)
    
    market_data = market_agent.get_market_analysis()
    
    # TAM/SAM/SOM Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="modern-card">
                <h4 style="color: #1e5a96; margin-top: 0;">📊 TAM (Total)</h4>
                <div style="font-size: 32px; font-weight: 800; color: #1e5a96;">$3.5B</div>
                <p style="color: #666; margin: 8px 0;">Total Addressable Market</p>
                <div style="background: #e3f2fd; padding: 8px; border-radius: 8px; font-size: 12px; color: #1565c0;">
                    All e-commerce product descriptions needed
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="modern-card">
                <h4 style="color: #512da8; margin-top: 0;">🎯 SAM (Serviceable)</h4>
                <div style="font-size: 32px; font-weight: 800; color: #512da8;">$1.2B</div>
                <p style="color: #666; margin: 8px 0;">Serviceable Addressable Market</p>
                <div style="background: #f3e5f5; padding: 8px; border-radius: 8px; font-size: 12px; color: #512da8;">
                    Our target market segments
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="modern-card">
                <h4 style="color: #e65100; margin-top: 0;">🎁 SOM (Obtainable)</h4>
                <div style="font-size: 32px; font-weight: 800; color: #e65100;">$150M</div>
                <p style="color: #666; margin: 8px 0;">Year 5 Conservative</p>
                <div style="background: #fff3e0; padding: 8px; border-radius: 8px; font-size: 12px; color: #e65100;">
                    Realistic market capture
                </div>
            </div>
        """, unsafe_before_html=True)
    
    st.divider()
    
    # Market Growth Chart
    st.subheader("📈 Market Growth Projection (5 Years)")
    
    years_data = {
        'Year': ['2024', '2025', '2026', '2027', '2028'],
        'TAM ($B)': [3.5, 3.9, 4.5, 5.2, 6.0],
        'Seller Base (M)': [50, 58, 68, 82, 100]
    }
    
    df = pd.DataFrame(years_data)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df['TAM ($B)'],
        mode='lines+markers',
        name='TAM Growth ($B)',
        line=dict(color='#1e5a96', width=4),
        marker=dict(size=12, symbol='diamond'),
        fill='tozeroy',
        fillcolor='rgba(30, 90, 150, 0.1)'
    ))
    
    fig.update_layout(
        title="Market Total Addressable Market Expansion",
        xaxis_title="Timeline",
        yaxis_title="TAM ($B)",
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Market Segments
    st.subheader("🎯 Market Segmentation Strategy")
    
    segments_data = {
        'Segment': ['Enterprise Platforms', 'Mid-Size Marketplaces', 'SMB Sellers', 'Brands', 'D2C'],
        'TAM ($M)': [750, 400, 800, 350, 200],
        'Difficulty': ['Hard', 'Medium', 'Easy', 'Medium', 'Easy'],
        'Growth Rate': ['8%', '15%', '28%', '18%', '35%']
    }
    
    seg_df = pd.DataFrame(segments_data)
    
    fig2 = px.bar(
        seg_df,
        x='Segment',
        y='TAM ($M)',
        color='Growth Rate',
        title='Market Segments by TAM and Growth',
        color_discrete_sequence=['#e65100', '#ef6c00', '#f57c00', '#fb8c00', '#ff6f00'],
        labels={'TAM ($M)': 'Market Size ($M)', 'Growth Rate': 'Growth Rate'}
    )
    
    fig2.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig2, use_container_width=True)

elif selected == "🇮🇳 India Focus":
    st.markdown("""
        <div class="section-header" style="background: linear-gradient(135deg, #e65100 0%, #ef6c00 100%);">
            <h1>🇮🇳 India Market - Fastest Growing</h1>
            <p>5.2M Sellers | 25% CAGR | $850M TAM</p>
        </div>
    """, unsafe_allow_html=True)
    
    marker_data = market_agent.get_market_analysis()
    india_data = marker_data['india']
    
    # India KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid #e65100;">
                <div style="font-size: 28px;">📊</div>
                <div class="kpi-value" style="color: #e65100;">${india_data['tam']['value']}B</div>
                <div class="kpi-label">Market TAM</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="kpi-card" style="border-left: 4px solid #e65100;">
                <div style="font-size: 28px;">👥</div>
                <div class="kpi-value" style="color: #e65100;">5.2M</div>
                <div class="kpi-label">Active Sellers</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="kpi-card" style="border-left: 4px solid #e65100;">
                <div style="font-size: 28px;">📈</div>
                <div class="kpi-value" style="color: #e65100;">40%</div>
                <div class="kpi-label">YoY Growth</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # India Growth Projection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        india_years = ['2024', '2025', '2026', '2027', '2028']
        india_tam_vals = [0.85, 0.95, 1.15, 1.42, 1.70]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=india_years,
            y=india_tam_vals,
            mode='lines+markers',
            name='India TAM',
            line=dict(color='#e65100', width=4),
            marker=dict(size=12)
        ))
        
        fig.update_layout(
            title="India Market TAM Growth (2024-2028)",
            xaxis_title="Year",
            yaxis_title="TAM ($B)",
            height=350,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
            <div class="gradient-card-accent">
                <h4 style="color: white; margin-top: 0;">🚀 India Highlights</h4>
                <ul style="color: white; font-size: 13px; line-height: 1.8;">
                    <li><strong>112%</strong> 5-year growth</li>
                    <li><strong>25%</strong> annual CAGR</li>
                    <li><strong>180M</strong> products/year</li>
                    <li><strong>Tier-2/3</strong> cities growing fastest</li>
                    <li><strong>Mobile</strong>-first (85%)</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # India Market Insights
    st.subheader("💡 India Market Opportunities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="modern-card">
                <h4 style="color: #e65100;">📱 Mobile-First Market</h4>
                <p><strong>85%</strong> of traffic from mobile. Our solution is optimized for mobile sellers and buyers.</p>
                <div style="background: #fff3e0; padding: 12px; border-radius: 8px; margin-top: 12px;">
                    <strong>Opportunity:</strong> Mobile-first UI, offline-first sync, lightweight processing
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="modern-card">
                <h4 style="color: #e65100;">🌐 Multi-Language Support</h4>
                <p>12+ regional languages needed. Sellers want local language descriptions.</p>
                <div style="background: #fff3e0; padding: 12px; border-radius: 8px; margin-top: 12px;">
                    <strong>Opportunity:</strong> Regional language models, local cultural adaptation
                </div>
            </div>
        """, unsafe_allow_html=True)

elif selected == "🌍 Global View":
    st.markdown("""
        <div class="section-header" style="background: linear-gradient(135deg, #512da8 0%, #7e57c2 100%);">
            <h1>🌍 International Markets</h1>
            <p>45M Sellers | 16% CAGR | $4.35B TAM</p>
        </div>
    """, unsafe_allow_html=True)
    
    market_data = market_agent.get_market_analysis()
    intl_data = market_data['international']
    
    # International KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid #512da8;">
                <div style="font-size: 28px;">📊</div>
                <div class="kpi-value" style="color: #512da8;">${intl_data['tam']['value']}B</div>
                <div class="kpi-label">Market TAM</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="kpi-card" style="border-left: 4px solid #512da8;">
                <div style="font-size: 28px;">🌐</div>
                <div class="kpi-value" style="color: #512da8;">45M</div>
                <div class="kpi-label">Global Sellers</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="kpi-card" style="border-left: 4px solid #512da8;">
                <div style="font-size: 28px;">📈</div>
                <div class="kpi-value" style="color: #512da8;">16%</div>
                <div class="kpi-label">Annual CAGR</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Regional Breakdown
    st.subheader("🗺️ Regional Market Breakdown")
    
    regions = {
        'Region': ['North America', 'Europe', 'Asia-Pacific', 'LATAM', 'Middle East'],
        'TAM ($B)': [1.2, 0.8, 1.5, 0.3, 0.25],
        'Growth %': [8, 10, 22, 20, 18]
    }
    
    reg_df = pd.DataFrame(regions)
    
    fig = px.sunburst(
        reg_df,
        labels=['Region', 'TAM'],
        parents=['', 'North America', 'Europe', 'Asia-Pacific', 'LATAM', 'Middle East'],
        values=[4.05, 1.2, 0.8, 1.5, 0.3, 0.25],
        color=['Region', 'Growth %'],
        color_discrete_sequence=px.colors.sequential.Purples
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif selected == "🛒 Cart":
    if not st.session_state.authenticated:
        st.error("❌ Please Login First")
        st.markdown("""
            <div class="modern-card">
                <h3 style="color: #e65100;">🔐 Cart Access Restricted</h3>
                <p>You need to log in to access the shopping cart.</p>
                <div style="background: #fff3e0; padding: 16px; border-radius: 12px; margin-top: 16px;">
                    <strong>Demo Credentials:</strong><br>
                    demo / demo123 or admin / admin@123
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="section-header" style="background: linear-gradient(135deg, #2e7d32 0%, #388e3c 100%);">
                <h1>🛒 Shopping Cart</h1>
                <p>Welcome back, {st.session_state.username.title()}!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Cart Stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="kpi-card" style="border-left: 4px solid #2e7d32;">
                    <div style="font-size: 28px;">📦</div>
                    <div class="kpi-value" style="color: #2e7d32;">{len(st.session_state.cart_items)}</div>
                    <div class="kpi-label">Items in Cart</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total = sum([item.get('total', 0) for item in st.session_state.cart_items])
            st.markdown(f"""
                <div class="kpi-card" style="border-left: 4px solid #2e7d32;">
                    <div style="font-size: 28px;">💰</div>
                    <div class="kpi-value" style="color: #2e7d32;">${total:.2f}</div>
                    <div class="kpi-label">Total Amount</div>
                </div>
            """, unsafe_after_html=True)
        
        with col3:
            st.markdown("""
                <div class="kpi-card" style="border-left: 4px solid #2e7d32;">
                    <div style="font-size: 28px;">🎁</div>
                    <div class="kpi-value" style="color: #2e7d32;">FREE</div>
                    <div class="kpi-label">Shipping</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Add to Cart
        st.subheader("➕ Add Product to Cart")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            product_name = st.text_input("🏷️ Product Name", placeholder="e.g., Laptop")
        with col2:
            price = st.number_input("💵 Price ($)", min_value=0.01, value=99.99)
        with col3:
            quantity = st.number_input("📦 Quantity", min_value=1, max_value=100, value=1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("➕ Add to Cart", use_container_width=True):
                if product_name:
                    st.session_state.cart_items.append({
                        'name': product_name,
                        'price': price,
                        'quantity': quantity,
                        'total': price * quantity
                    })
                    st.success(f"✅ {product_name} added!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Enter product name")
        
        with col2:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        st.divider()
        
        # Cart Items
        if st.session_state.cart_items:
            st.subheader("📋 Your Items")
            
            cart_df = pd.DataFrame(st.session_state.cart_items)
            st.dataframe(cart_df, use_container_width=True, hide_index=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🗑️ Clear Cart", use_container_width=True):
                    st.session_state.cart_items = []
                    st.success("Cart cleared!")
                    time.sleep(1)
                    st.rerun()
            
            with col2:
                if st.button("💳 Checkout", use_container_width=True):
                    st.success("✅ Order Confirmed!")
                    st.balloons()
                    total = sum([item.get('total', 0) for item in st.session_state.cart_items])
                    st.markdown(f"""
                        <div class="gradient-card-primary">
                            <h3 style="color: white; margin-top: 0;">✅ Order Summary</h3>
                            <p style="color: white;"><strong>Total:</strong> ${total:.2f}</p>
                            <p style="color: white;"><strong>Items:</strong> {len(st.session_state.cart_items)}</p>
                            <p style="color: white;"><strong>User:</strong> {st.session_state.username.title()}</p>
                            <hr style="border-color: rgba(255,255,255,0.3);">
                            <p style="color: white;">🎉 Thank you for your purchase!</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("🛒 Your cart is empty. Add items to get started!")

else:
    st.markdown("""
        <div class="section-header">
            <h1>🚀 Coming Soon</h1>
            <p>Feature will be available soon! Stay tuned.</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; padding: 24px; color: #666;">
        <p style="margin: 0;"><strong>AI Product Description Solution</strong> | Next-Gen E-Commerce Platform</p>
        <p style="margin: 4px 0; font-size: 12px;">India & Global Market Leader | March 2026</p>
    </div>
""", unsafe_allow_html=True)
