"""
Trovia — AI-Powered E-Commerce
GLT × AceAI.Club Capstone Project
Main entry point
"""

import streamlit as st
import sqlite3
import hashlib
import os
from datetime import datetime

# Page config MUST be first
st.set_page_config(
    page_title="Trovia — AI-Powered E-Commerce",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Database Setup ───────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "shopiq.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'customer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            rating REAL,
            emoji TEXT,
            description TEXT,
            in_stock INTEGER DEFAULT 1
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, product_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_amount REAL,
            status TEXT DEFAULT 'Processing',
            coupon_code TEXT,
            discount_amount REAL DEFAULT 0,
            placed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT,
            product_emoji TEXT,
            quantity INTEGER,
            unit_price REAL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username, email, password, role="customer"):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (username, email, hash_password(password), role)
        )
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def verify_user(email, password):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE email = ? AND password_hash = ?",
        (email, hash_password(password))
    )
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None


def get_cart_count(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(quantity), 0) FROM cart WHERE user_id = ?", (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count


# ─── Dark Theme CSS ───────────────────────────────────────────────────────────

def inject_global_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif !important;
        background-color: #f7f9fc !important;
        color: #1f2937 !important;
    }

    .stApp {
        background: linear-gradient(135deg, #f7f9fc 0%, #ffffff 50%, #eef2f8 100%) !important;
        min-height: 100vh;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.5);
        color: #1f2937 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #22d3ee) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 700 !important;
        padding: 0.45rem 1.2rem !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25) !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3) !important;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        color: #1f2937 !important;
        font-family: 'Nunito', sans-serif !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    /* Labels and section headings */
    .stTextInput > label,
    .stTextArea > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4,
    .stMarkdown h5,
    .stMarkdown h6 {
        color: #1e3a8a !important;
        font-weight: 700 !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12) !important;
    }

    /* Cards */
    .product-card,
    .hero-section,
    .category-card,
    .chat-user,
    .chat-bot,
    .stForm {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08) !important;
        border-radius: 16px !important;
        color: #1f2937 !important;
    }

    .product-card:hover,
    .category-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.18) !important;
    }

    .hero-section {
        background: linear-gradient(135deg, #eff6ff, #e0f2fe) !important;
        border: 1px solid #dbeafe !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        text-align: center !important;
        margin-bottom: 1.8rem !important;
    }

    .rainbow-header {
        background: linear-gradient(270deg, #0ea5e9, #38bdf8, #7dd3fc, #60a5fa, #3b82f6);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: rainbow 3.5s ease infinite;
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        margin-bottom: 0.7rem !important;
        text-align: center !important;
    }

    .nav-container {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }

    .nav-btn {
        background: #eff6ff !important;
        border: 1px solid #bae6fd !important;
        color: #1d4ed8 !important;
        border-radius: 999px !important;
        padding: 0.4rem 1.2rem !important;
        font-weight: 700 !important;
    }

    .nav-btn:hover, .nav-btn.active {
        background: linear-gradient(135deg, #38bdf8, #0ea5e9) !important;
        color: #ffffff !important;
        border-color: transparent !important;
    }

    .badge {
        background: linear-gradient(135deg, #22d3ee, #2563eb) !important;
        color: #f8fafc !important;
        border-radius: 999px !important;
        padding: 0.25rem 0.8rem !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
    }

    .chat-user, .chat-bot {
        border: 1px solid #e2e8f0 !important;
        background: #f8fafc !important;
    }

    .chat-user {
        margin-left: 20% !important;
        margin-right: 0 !important;
        background: #dbeafe !important;
    }

    .chat-bot {
        margin-left: 0 !important;
        margin-right: 20% !important;
        background: #e0f2fe !important;
    }

    .stAlert {
        border-radius: 14px !important;
        border: 1px solid #60a5fa !important;
        background: #dbeafe !important;
        color: #1e3a8a !important;
    }

    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}

    @keyframes rainbow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #ffffff;
        border-bottom: 2px solid #e2e8f0;
        padding: 0;
    }

    .stTabs [data-baseweb="tab"] {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 12px 24px !important;
        border-radius: 8px 8px 0 0 !important;
        border-bottom: 3px solid transparent !important;
        margin-right: 8px !important;
    }

    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
        background: #f0f9ff !important;
        border-bottom: 3px solid #2563eb !important;
    }

    .stTabs [aria-selected="true"]::after {
        background-color: transparent !important;
    }

    /* Form Container Styling */
    .stForm {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07) !important;
    }

    .stForm > div {
        display: flex !important;
        flex-direction: column !important;
    }

    .stFormSubmitButton button {
        background: linear-gradient(135deg, #2563eb, #22d3ee) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }

    .stFormSubmitButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 24px rgba(37, 99, 235, 0.4) !important;
    }

    /* Tab Content */
    .stTabs > div:nth-child(2) {
        padding: 20px !important;
    }

    /* Hide password eye icon */
    button[data-testid="stPasswordFieldToggle"],
    [data-testid="stPasswordFieldToggle"],
    .stTextInput button,
    input[type="password"] ~ button,
    div[data-baseweb="input"] button {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


def music_player():
    """Render background music button"""
    music_path = os.path.join(os.path.dirname(__file__), "assets", "music", "learning_bg.mp3")

    if "music_on" not in st.session_state:
        st.session_state.music_on = False

    if os.path.exists(music_path):
        col_spacer, col_music = st.columns([20, 1])
        with col_music:
            if st.button("🎵", key="music_toggle", help="Toggle background music"):
                st.session_state.music_on = not st.session_state.music_on

        if st.session_state.music_on:
            with open(music_path, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3", start_time=0)


# ─── Session State Init ───────────────────────────────────────────────────────

def init_session_state():
    defaults = {
        "logged_in": False,
        "user": None,
        "page": "Home",
        "cart_count": 0,
        "chat_history": [],
        "search_history": [],
        "music_on": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ─── Auth UI ─────────────────────────────────────────────────────────────────

def show_auth_page():
    inject_global_css()

    st.markdown("""
    <div style="text-align:center; padding: 2rem 0;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🛒</div>
        <div class="rainbow-header">Trovia</div>
        <p style="color: #1e3a8a; font-size: 1.2rem; font-weight: 600;">
            AI-Powered E-Commerce • GLT × AceAI.Club
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

        with tab1:
            with st.form("login_form"):
                st.markdown("<h3 style='color:#1e3a8a; text-align:center;'>Welcome Back!</h3>", unsafe_allow_html=True)
                email = st.text_input("Email", placeholder="your@email.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                login_btn = st.form_submit_button("🚀 Login", use_container_width=True)

                if login_btn:
                    if email and password:
                        user = verify_user(email, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            st.session_state.cart_count = get_cart_count(user["id"])
                            st.success("Welcome back! Redirecting...")
                            st.rerun()
                        else:
                            st.error("Invalid email or password.")
                    else:
                        st.warning("Please fill in all fields.")

            st.markdown("""
            <div style="text-align:center; margin-top:1rem; padding:1rem;
                background: #e0f2fe; border-radius:15px;
                border: 1px solid #7dd3fc;">
                <p style="color:#0c4a6e; font-size:0.9rem; margin:0;">
                    <strong>Demo Account:</strong><br>
                    Email: demo@trovia.com | Password: demo123
                </p>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            with st.form("signup_form"):
                st.markdown("<h3 style='color:#c4b5fd; text-align:center;'>Create Account</h3>", unsafe_allow_html=True)
                new_username = st.text_input("Username", placeholder="coolshopper")
                new_email = st.text_input("Email", placeholder="your@email.com")
                new_password = st.text_input("Password", type="password", placeholder="Min 6 characters")
                confirm_pass = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
                role = st.selectbox("Account Type", ["customer", "admin"])
                signup_btn = st.form_submit_button("✨ Create Account", use_container_width=True)

                if signup_btn:
                    if not all([new_username, new_email, new_password, confirm_pass]):
                        st.warning("Please fill all fields.")
                    elif new_password != confirm_pass:
                        st.error("Passwords do not match!")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        user_id = create_user(new_username, new_email, new_password, role)
                        if user_id:
                            user = verify_user(new_email, new_password)
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            st.session_state.cart_count = 0
                            st.success("Account created! Welcome to Trovia!")
                            st.rerun()
                        else:
                            st.error("Username or email already exists. Try another.")


# ─── Navigation ───────────────────────────────────────────────────────────────

def render_navbar():
    user = st.session_state.user
    cart_count = st.session_state.cart_count

    cart_label = "🛒 Cart"
    if cart_count > 0:
        cart_label = f"🛒 Cart ({cart_count})"

    pages = ["🏠 Home", "🔍 Trovia Chat", "📦 Products", "📋 Orders", cart_label, "🤖 AI Agents"]
    page_keys = ["Home", "AI Assistant", "Products", "Orders", "Cart", "Agents"]

    with st.sidebar:
        st.markdown("""
        <div style="padding:1rem; text-align:center;">
            <div style="font-size:2.2rem; font-weight:800;">🔍 Trovia</div>
            <div style="font-size:1rem; color:#475569; margin-top:0.2rem;">All India + Global Marketplace</div>
        </div>
        """, unsafe_allow_html=True)

        # Sync radio to current page so button-driven navigation isn't overridden
        if st.session_state.page in page_keys:
            st.session_state["sidebar_page_select"] = st.session_state.page

        selected_page = st.radio(
            "Navigate",
            options=page_keys,
            key="sidebar_page_select"
        )

        # Set page when user manually clicks sidebar
        if selected_page != st.session_state.page:
            st.session_state.page = selected_page
            st.rerun()

        st.markdown("---")

        # Logout button
        if st.button("🚪 Logout", key="sidebar_logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.cart_count = 0
            st.session_state.chat_history = []
            st.session_state.page = "Home"
            st.rerun()

        if user:
            st.markdown(
                f"<p style='text-align:center; color:#334155; font-size:0.9rem; margin:0;'>"
                f"👤 {user['username']} • {user['role'].title()}</p>",
                unsafe_allow_html=True
            )

    # Top title bar (still visible on main view)
    st.markdown("""
        <div style="background: linear-gradient(90deg, #2563eb, #22d3ee);
             border-radius: 16px; padding: 1rem; margin-bottom: 1rem;
             display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 0.8rem;">
                <div style="width: 42px; height: 42px; border-radius: 12px;
                    background: linear-gradient(135deg, #0f52ba, #22d3ee);
                    display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.35rem;">🛒</span>
                </div>
                <div>
                    <div style="font-size:1.7rem; font-weight:900; color:#ffffff; margin:0;">Trovia</div>
                    <div style="font-size:0.95rem; color:#e0f2fe; font-weight:600; margin-top:0.2rem;">
                        AI Product Description Platform — E-commerce Ready
                    </div>
                </div>
            </div>
            <div style="font-size:0.95rem; color:#e0f2fe; font-weight:700;">
                Unified listings, smart description, cross-platform images
            </div>
        </div>
    """, unsafe_allow_html=True)


# ─── Page Router ─────────────────────────────────────────────────────────────

def route_page():
    page = st.session_state.page

    if page == "Home":
        from pages.home import show_home
        show_home()
    elif page == "Products":
        from pages.products import show_products
        show_products()
    elif page == "Image Search":
        from pages.image_search import show_image_search
        show_image_search()
    elif page == "Cart":
        from pages.cart import show_cart
        show_cart()
    elif page == "Orders":
        from pages.orders import show_orders
        show_orders()
    elif page == "AI Assistant":
        from pages.ai_assistant import show_ai_assistant
        show_ai_assistant()
    elif page == "Agents":
        from pages.agents_dashboard import show_agents_dashboard
        show_agents_dashboard()


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    init_db()
    init_session_state()
    inject_global_css()

    # Create demo user if not exists (update email if username already exists)
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = 'demo_user'")
    existing = c.fetchone()
    if existing:
        c.execute("UPDATE users SET email = 'demo@trovia.com' WHERE username = 'demo_user'")
    else:
        c.execute(
            "INSERT OR IGNORE INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ("demo_user", "demo@trovia.com", hash_password("demo123"), "customer")
        )
    conn.commit()
    conn.close()

    if not st.session_state.logged_in:
        show_auth_page()
    else:
        # Update cart count
        if st.session_state.user:
            st.session_state.cart_count = get_cart_count(st.session_state.user["id"])

        render_navbar()
        route_page()
        music_player()


if __name__ == "__main__":
    main()
