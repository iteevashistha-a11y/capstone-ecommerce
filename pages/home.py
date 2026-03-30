"""
Trovia — Home Page
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.products import PRODUCTS, CATEGORIES, get_featured_products, get_trending_products


def get_stars(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + "½" * half + "☆" * empty


def get_product_image_url(product):
    keywords = product.get("image_keywords", [product["category"].lower()])
    keyword_str = ",".join(keywords[:2])
    return f"https://loremflickr.com/400/260/{keyword_str}?lock={product['id']}"


def render_product_card(product, col_key=""):
    stars = get_stars(product["rating"])
    img_url = get_product_image_url(product)
    in_stock = product.get("in_stock", True)

    try:
        st.image(img_url, use_container_width=True)
    except Exception:
        st.markdown(f"<div style='text-align:center;font-size:4rem;padding:1rem;'>{product['emoji']}</div>",
                    unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:0 0 14px 14px;
         padding:0.9rem; margin-bottom:0.5rem; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
        <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase;
             letter-spacing:1px; margin-bottom:0.2rem;">{product['category']}</div>
        <div style="font-size:1rem; font-weight:800; color:#1e3a8a;
             margin-bottom:0.3rem;">{product['name']}</div>
        <div style="color:#f59e0b; margin-bottom:0.3rem; font-size:0.9rem;">{stars}
            <span style="color:#374151; font-weight:600;"> {product['rating']}</span></div>
        <div style="font-size:1.15rem; font-weight:900; color:#2563eb;
             margin-bottom:0.5rem;">₹{product['price']:,}</div>
        <div style="font-size:0.82rem; color:#374151; line-height:1.5;
             margin-bottom:0.5rem;">{product['description'][:100]}...</div>
        {'<span style="color:#10b981; font-size:0.8rem; font-weight:700;">✅ In Stock</span>' if in_stock else '<span style="color:#ef4444; font-size:0.8rem; font-weight:700;">❌ Out of Stock</span>'}
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        f"🛒 Add to Cart",
        key=f"home_cart_{product['id']}_{col_key}",
        use_container_width=True,
        disabled=not in_stock
    ):
        add_to_cart_action(product)


def add_to_cart_action(product):
    if "user" not in st.session_state or not st.session_state.user:
        st.warning("Please login to add items to cart.")
        return

    import sqlite3
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shopiq.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1) "
            "ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = quantity + 1",
            (st.session_state.user["id"], product["id"])
        )
        conn.commit()
        c.execute(
            "SELECT COALESCE(SUM(quantity), 0) FROM cart WHERE user_id = ?",
            (st.session_state.user["id"],)
        )
        st.session_state.cart_count = c.fetchone()[0]
        st.success(f"Added {product['emoji']} {product['name']} to cart!")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()


def show_home():
    # ── Hero Banner ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🛒✨</div>
        <div class="rainbow-header">Find exactly what you want with AI 🤖</div>
        <p style="color: #1e3a8a; font-size: 1.2rem; font-weight: 600; margin: 1rem 0 2rem 0;">
            Trovia uses cutting-edge AI to help you discover products, compare prices,
            and shop smarter than ever before.
        </p>
    </div>
    """, unsafe_allow_html=True)

    hero_c1, hero_c2, hero_c3, hero_c4 = st.columns(4)
    with hero_c1:
        if st.button("🔍 Visual Search", use_container_width=True, key="hero_visual"):
            st.session_state.page = "Image Search"
            st.session_state["sidebar_page_select"] = "Image Search"
            st.rerun()
    with hero_c2:
        if st.button("🤖 AI Recommendations", use_container_width=True, key="hero_rec"):
            st.session_state.page = "Agents"
            st.session_state["sidebar_page_select"] = "Agents"
            st.rerun()
    with hero_c3:
        if st.button("💰 Smart Deals", use_container_width=True, key="hero_deals"):
            st.session_state.page = "Products"
            st.session_state["sidebar_page_select"] = "Products"
            st.rerun()
    with hero_c4:
        if st.button("🛒 Go to Cart", use_container_width=True, key="hero_cart"):
            st.session_state.page = "Cart"
            st.session_state["sidebar_page_select"] = "Cart"
            st.rerun()

    # ── Quick Search Bar ──────────────────────────────────────────────────────
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input(
            "",
            placeholder="🔍 Search for products, brands, categories...",
            key="hero_search",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("Search 🚀", key="hero_search_btn", use_container_width=True):
            if search_query:
                st.session_state.page = "Products"
                st.session_state["sidebar_page_select"] = "Products"
                st.session_state["product_search_query"] = search_query
                st.rerun()

    st.markdown("---")

    # ── Categories Row ────────────────────────────────────────────────────────
    st.markdown("""
    <h2 style="color: #1e3a8a; font-weight: 800; text-align: center; margin-bottom: 1.5rem;">
        🏪 Shop by Category
    </h2>
    """, unsafe_allow_html=True)

    cat_cols = st.columns(len(CATEGORIES))
    for i, cat in enumerate(CATEGORIES):
        with cat_cols[i]:
            st.markdown(f"""
            <div class="category-card">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{cat['emoji']}</div>
                <div style="font-weight: 800; color: #1e3a8a; font-size: 0.95rem;">{cat['name']}</div>
                <div style="color: rgba(196,181,253,0.6); font-size: 0.75rem; margin-top: 0.3rem;">
                    {cat['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(
                f"Explore {cat['name']}",
                key=f"cat_{cat['name']}",
                use_container_width=True
            ):
                st.session_state.page = "Products"
                st.session_state["sidebar_page_select"] = "Products"
                st.session_state["selected_category"] = cat["name"]
                st.rerun()

    st.markdown("---")

    # ── India vs International Market Highlight ─────────────────────────────────
    st.markdown("""
    <div style="display:flex; gap:1rem; flex-wrap:wrap;">
        <div style="flex:1; min-width:260px; background:#ffffff; border:1px solid #cbd5e1; border-radius:16px;
                    padding:1rem; box-shadow:0 4px 12px rgba(15,23,42,0.08);">
            <h3 style="margin-top:0; color:#1e3a8a;">🇮🇳 India Market</h3>
            <p style="color:#334155; margin:0.5rem 0;">High-growth + high-impact. 25% CAGR in AI commerce, 5.2M active sellers, value-focused buyers.</p>
            <ul style="margin:0 0 0.5rem 1rem; color:#334155;">
                <li>TAM: ₹850cr → ₹1950cr (2029)</li>
                <li>Focus: Regional deals, vernacular UX, affordability</li>
                <li>Strategy: Marketplace + partner onboarding</li>
            </ul>
        </div>
        <div style="flex:1; min-width:260px; background:#ffffff; border:1px solid #cbd5e1; border-radius:16px;
                    padding:1rem; box-shadow:0 4px 12px rgba(15,23,42,0.08);">
            <h3 style="margin-top:0; color:#1e3a8a;">🌍 International Market</h3>
            <p style="color:#334155; margin:0.5rem 0;">Mature segments with steady 16% CAGR, 45M sellers, premium price acceptance and scale.</p>
            <ul style="margin:0 0 0.5rem 1rem; color:#334155;">
                <li>TAM: ₹4350cr → ₹7850cr (2029)</li>
                <li>Focus: Advanced AI personalization, cross-border logistics</li>
                <li>Strategy: Enterprise deployment + multilang Genie</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Ruflo Swarm Banner ────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e3a8a,#0ea5e9); border-radius:16px;
         padding:1.2rem 1.5rem; margin-bottom:1.5rem; display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
        <div style="font-size:2rem;">🤖</div>
        <div>
            <div style="color:#ffffff; font-size:1.1rem; font-weight:900;">Ruflo Swarm — 3 Agents Active</div>
            <div style="color:#bae6fd; font-size:0.85rem;">
                ProductSearchAgent · RecommendationAgent · PriceOptimizerAgent running in parallel
            </div>
        </div>
        <div style="margin-left:auto; display:flex; gap:0.5rem; flex-wrap:wrap;">
            <span style="background:rgba(255,255,255,0.2); color:#fff; border-radius:20px;
                 padding:0.3rem 0.8rem; font-size:0.78rem; font-weight:700;">🔍 Semantic Search</span>
            <span style="background:rgba(255,255,255,0.2); color:#fff; border-radius:20px;
                 padding:0.3rem 0.8rem; font-size:0.78rem; font-weight:700;">💡 Personalised Recs</span>
            <span style="background:rgba(255,255,255,0.2); color:#fff; border-radius:20px;
                 padding:0.3rem 0.8rem; font-size:0.78rem; font-weight:700;">💰 Price Optimiser</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Featured Products ─────────────────────────────────────────────────────
    st.markdown("""
    <h2 style="color: #1e3a8a; font-weight: 800; text-align: center; margin-bottom: 1.5rem;">
        ⭐ Featured Products
    </h2>
    """, unsafe_allow_html=True)

    featured = get_featured_products(6)
    cols = st.columns(3)
    for i, product in enumerate(featured):
        with cols[i % 3]:
            render_product_card(product, f"featured_{i}")

    st.markdown("---")

    # ── How AI Helps You Shop ─────────────────────────────────────────────────
    st.markdown("""
    <h2 style="color: #1e3a8a; font-weight: 800; text-align: center; margin-bottom: 1.5rem;">
        🧠 How AI Helps You Shop
    </h2>
    """, unsafe_allow_html=True)

    ai_col1, ai_col2, ai_col3 = st.columns(3)

    with ai_col1:
        st.markdown("""
        <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:16px;
             padding:1.5rem; text-align:left; height:100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: #1e3a8a; margin-bottom: 0.8rem;">
                Visual Search
            </div>
            <div style="color:#374151; font-size: 0.92rem; line-height: 1.6;">
                Upload any image — a photo you saw online, from a magazine, or in real life —
                and our AI will identify the product and find the best matches instantly.
            </div>
            <div style="margin-top:1rem; background:#2563eb; color:white; border-radius:20px;
                 padding:0.3rem 0.9rem; display:inline-block; font-size:0.8rem; font-weight:700;">
                GPT-4o Vision
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ai_col2:
        st.markdown("""
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:16px;
             padding:1.5rem; text-align:left; height:100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💡</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: #1e3a8a; margin-bottom: 0.8rem;">
                Smart Recommendations
            </div>
            <div style="color:#374151; font-size: 0.92rem; line-height: 1.6;">
                Our Ruflo swarm agents analyse your cart, preferences and budget
                to recommend products you'll actually love — instantly.
            </div>
            <div style="margin-top:1rem; background:#10b981; color:white; border-radius:20px;
                 padding:0.3rem 0.9rem; display:inline-block; font-size:0.8rem; font-weight:700;">
                Ruflo Swarm Agent
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ai_col3:
        st.markdown("""
        <div style="background:#fff7ed; border:1px solid #fed7aa; border-radius:16px;
             padding:1.5rem; text-align:left; height:100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💰</div>
            <div style="font-size: 1.1rem; font-weight: 800; color: #1e3a8a; margin-bottom: 0.8rem;">
                Price Optimizer
            </div>
            <div style="color:#374151; font-size: 0.92rem; line-height: 1.6;">
                PriceOptimizerAgent scans your cart, finds best coupons,
                checks your budget and scores every item's value in real-time.
            </div>
            <div style="margin-top:1rem; background:#f97316; color:white; border-radius:20px;
                 padding:0.3rem 0.9rem; display:inline-block; font-size:0.8rem; font-weight:700;">
                PriceOptimizerAgent
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Trending Now ──────────────────────────────────────────────────────────
    st.markdown("""
    <h2 style="color: #1e3a8a; font-weight: 800; text-align: center; margin-bottom: 1.5rem;">
        🔥 Trending Now
    </h2>
    """, unsafe_allow_html=True)

    trending = get_trending_products(4)
    trend_cols = st.columns(4)
    for i, product in enumerate(trending):
        with trend_cols[i]:
            stars = get_stars(product["rating"])
            img_url = get_product_image_url(product)
            try:
                st.image(img_url, use_container_width=True)
            except Exception:
                st.markdown(f"<div style='text-align:center;font-size:3rem;'>{product['emoji']}</div>",
                            unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:0 0 12px 12px;
                 padding:0.8rem; margin-bottom:0.5rem;">
                <div style="font-size:0.72rem; font-weight:700; color:#ef4444;
                     text-transform:uppercase; margin-bottom:0.3rem;">🔥 Trending</div>
                <div style="font-weight:800; color:#1e3a8a; font-size:0.95rem;">{product['name']}</div>
                <div style="color:#f59e0b; font-size:0.85rem;">{stars}</div>
                <div style="font-weight:900; color:#2563eb; font-size:1.1rem;">₹{product['price']:,}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(
                "🛒 Add to Cart",
                key=f"trend_cart_{product['id']}",
                use_container_width=True
            ):
                add_to_cart_action(product)

    st.markdown("---")

    # ── Stats Banner ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(108,59,255,0.15), rgba(168,85,247,0.1));
         border: 1px solid rgba(130,80,255,0.2); border-radius: 25px; padding: 2rem;">
        <h3 style="text-align: center; color: #1e3a8a; font-weight: 800; margin-bottom: 1.5rem;">
            Why Shoppers Love Trovia
        </h3>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 900;
                     background: linear-gradient(135deg, #a78bfa, #f0abfc);
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                     background-clip: text;">10K+</div>
                <div style="color: #c4b5fd; font-weight: 600;">Happy Shoppers</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 900;
                     background: linear-gradient(135deg, #a78bfa, #f0abfc);
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                     background-clip: text;">500+</div>
                <div style="color: #c4b5fd; font-weight: 600;">Products</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 900;
                     background: linear-gradient(135deg, #a78bfa, #f0abfc);
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                     background-clip: text;">98%</div>
                <div style="color: #c4b5fd; font-weight: 600;">Satisfaction Rate</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 900;
                     background: linear-gradient(135deg, #a78bfa, #f0abfc);
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                     background-clip: text;">24/7</div>
                <div style="color: #c4b5fd; font-weight: 600;">AI Support</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    import streamlit as st
    st.set_page_config(page_title="Trovia Home", layout="wide")
    show_home()
