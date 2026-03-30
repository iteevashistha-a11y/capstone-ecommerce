"""
Trovia — Products Page
"""

import streamlit as st
import sys
import os
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.products import PRODUCTS, CATEGORIES


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shopiq.db")

ITEMS_PER_PAGE = 8


def get_product_image_url(product):
    """Return a relevant product image using image_keywords for loremflickr."""
    keywords = product.get("image_keywords", [product["category"].lower()])
    keyword_str = ",".join(keywords[:2])
    lock = product["id"]  # keeps the same image per product every load
    return f"https://loremflickr.com/400/280/{keyword_str}?lock={lock}"


def get_stars(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty


def add_to_cart(product_id, user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1) "
            "ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = quantity + 1",
            (user_id, product_id)
        )
        conn.commit()
        c.execute(
            "SELECT COALESCE(SUM(quantity), 0) FROM cart WHERE user_id = ?",
            (user_id,)
        )
        count = c.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        conn.close()
        raise e


def get_reviews(product_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """SELECT r.rating, r.comment, r.created_at, u.username
           FROM reviews r JOIN users u ON r.user_id = u.id
           WHERE r.product_id = ?
           ORDER BY r.created_at DESC LIMIT 10""",
        (product_id,)
    )
    rows = c.fetchall()
    conn.close()
    return rows


def submit_review(product_id, user_id, rating, comment):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO reviews (product_id, user_id, rating, comment) VALUES (?, ?, ?, ?)",
            (product_id, user_id, rating, comment)
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def show_products():
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0;">
        <h1 style="font-size: 2.5rem; font-weight: 900;
             background: linear-gradient(135deg, #a78bfa, #f0abfc);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             background-clip: text;">
            📦 All Products
        </h1>
        <p style="color: #c4b5fd; font-size: 1rem;">
            Discover {count} amazing products across {cats} categories
        </p>
    </div>
    """.format(count=len(PRODUCTS), cats=len(CATEGORIES)), unsafe_allow_html=True)

    # ── Sidebar Filters ────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #6c3bff, #a855f7);
             border-radius: 15px; padding: 1rem; text-align: center; margin-bottom: 1rem;">
            <h3 style="color: white; margin: 0; font-weight: 800;">🎛️ Filters</h3>
        </div>
        """, unsafe_allow_html=True)

        # Search
        search_default = st.session_state.get("product_search_query", "")
        search_query = st.text_input(
            "🔍 Search Products",
            value=search_default,
            placeholder="Type to search..."
        )
        if "product_search_query" in st.session_state:
            del st.session_state["product_search_query"]

        # Category filter
        cat_options = ["All Categories"] + [c["name"] for c in CATEGORIES]
        default_cat = st.session_state.get("selected_category", "All Categories")
        if default_cat not in cat_options:
            default_cat = "All Categories"
        default_cat_idx = cat_options.index(default_cat)

        selected_category = st.selectbox(
            "📂 Category",
            cat_options,
            index=default_cat_idx
        )
        if "selected_category" in st.session_state:
            del st.session_state["selected_category"]

        # Price range
        st.markdown("<p style='color: #c4b5fd; font-weight: 700; margin-bottom: 0;'>💰 Price Range</p>",
                    unsafe_allow_html=True)
        price_range = st.slider(
            "Price Range",
            min_value=0,
            max_value=150000,
            value=(0, 150000),
            step=500,
            format="₹%d",
            label_visibility="collapsed"
        )

        # Rating filter
        min_rating = st.select_slider(
            "⭐ Minimum Rating",
            options=[0.0, 1.0, 2.0, 3.0, 3.5, 4.0, 4.5],
            value=0.0
        )

        # Sort by
        sort_by = st.selectbox(
            "📊 Sort By",
            ["Default", "Price: Low to High", "Price: High to Low",
             "Rating: High to Low", "Name: A to Z"]
        )

        # In stock only
        in_stock_only = st.checkbox("✅ In Stock Only", value=False)

        st.markdown("---")
        if st.button("🔄 Reset Filters", use_container_width=True):
            st.rerun()

    # ── Filter Products via ProductSearchAgent (Ruflo swarm) ──────────────────
    agent_result = None
    if search_query:
        from agents.trovia_agents import ProductSearchAgent
        agent = ProductSearchAgent()
        filters = {}
        if price_range != (0, 150000):
            filters["max_price"] = price_range[1]
            filters["min_price"] = price_range[0]
        if selected_category != "All Categories":
            filters["category"] = selected_category
        if min_rating > 0:
            filters["min_rating"] = min_rating
        if in_stock_only:
            filters["in_stock"] = True
        agent_result = agent.run(search_query, filters)
        filtered = agent_result.data if agent_result.status == "success" else []
    else:
        filtered = list(PRODUCTS)
        if selected_category != "All Categories":
            filtered = [p for p in filtered if p["category"] == selected_category]
        filtered = [p for p in filtered if price_range[0] <= p["price"] <= price_range[1]]
        filtered = [p for p in filtered if p["rating"] >= min_rating]
        if in_stock_only:
            filtered = [p for p in filtered if p["in_stock"]]

    # Sort (only when not using agent — agent returns by relevance score)
    if not search_query:
        if sort_by == "Price: Low to High":
            filtered.sort(key=lambda x: x["price"])
        elif sort_by == "Price: High to Low":
            filtered.sort(key=lambda x: x["price"], reverse=True)
        elif sort_by == "Rating: High to Low":
            filtered.sort(key=lambda x: x["rating"], reverse=True)
        elif sort_by == "Name: A to Z":
            filtered.sort(key=lambda x: x["name"])

    # ── Agent Activity Banner ──────────────────────────────────────────────────
    if search_query and agent_result:
        latency = f"{agent_result.latency_ms:.1f}ms"
        status_color = "#10b981" if filtered else "#ef4444"
        status_label = f"✅ {len(filtered)} results" if filtered else "⚠️ No matches"
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#dbeafe,#eff6ff); border:1px solid #93c5fd;
             border-radius:12px; padding:0.8rem 1.2rem; margin-bottom:1rem;">
            <div style="display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                <span style="font-size:1.2rem;">🤖</span>
                <strong style="color:#1e3a8a;">ProductSearchAgent</strong>
                <span style="color:#475569; font-size:0.9rem;">— Ruflo swarm · {len(PRODUCTS)} products scanned · {latency}</span>
                <span style="margin-left:auto; background:{status_color}; color:white; border-radius:20px;
                     padding:0.2rem 0.9rem; font-size:0.78rem; font-weight:700;">{status_label}</span>
            </div>
            <div style="color:#64748b; font-size:0.82rem; margin-top:0.3rem;">
                Scoring by: name · tags · category · brand · description
            </div>
        </div>
        """, unsafe_allow_html=True)
        if not filtered:
            st.info(f"🤖 No products matched **\"{search_query}\"**. Try: *phone*, *shoes*, *books*, *laptop*")

    # ── Results Summary ────────────────────────────────────────────────────────
    col_info, _ = st.columns([3, 1])
    with col_info:
        st.markdown(
            f"<p style='color: #475569; font-weight: 600;'>"
            f"Showing <strong style='color:#2563eb'>{len(filtered)}</strong> products</p>",
            unsafe_allow_html=True
        )

    # ── Pagination ─────────────────────────────────────────────────────────────
    total_pages = max(1, (len(filtered) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

    if "products_page" not in st.session_state:
        st.session_state.products_page = 1

    if st.session_state.products_page > total_pages:
        st.session_state.products_page = 1

    current_page = st.session_state.products_page
    start_idx = (current_page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_products = filtered[start_idx:end_idx]

    # ── Product Grid ──────────────────────────────────────────────────────────
    if not page_products:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;
             background: #f8fafc; border-radius: 25px;
             border: 1px dashed #cbd5e1;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">😕</div>
            <h3 style="color: #1e3a8a;">No products found</h3>
            <p style="color: #475569;">Try adjusting your filters or search query</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for i, product in enumerate(page_products):
            with cols[i % 3]:
                stars = get_stars(product["rating"])
                in_stock = product["in_stock"]
                img_url = get_product_image_url(product)

                # Product image
                try:
                    st.image(img_url, use_container_width=True)
                except Exception:
                    st.markdown(f"<div style='text-align:center;font-size:4rem;'>{product['emoji']}</div>",
                                unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px;
                     padding:1rem; margin-bottom:0.5rem;">
                    <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase;
                         letter-spacing:1px; margin-bottom:0.3rem;">{product['category']}</div>
                    <div style="font-size:1rem; font-weight:800; color:#1e3a8a;
                         margin-bottom:0.4rem;">{product['name']}</div>
                    <div style="color:#f59e0b; margin-bottom:0.3rem;">{stars}
                        <span style="color:#64748b; font-size:0.85rem;"> {product['rating']}</span></div>
                    <div style="font-size:1.2rem; font-weight:900; color:#2563eb;
                         margin-bottom:0.6rem;">₹{product['price']:,}</div>
                    <div style="font-size:0.85rem; color:#475569; line-height:1.5;
                         margin-bottom:0.6rem;">{product['description']}</div>
                    <div style="font-size:0.8rem; font-weight:700;">
                        {'<span style="color:#10b981;">✅ In Stock</span>' if in_stock else '<span style="color:#ef4444;">❌ Out of Stock</span>'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(
                        "🛒 Add to Cart",
                        key=f"prod_cart_{product['id']}_{i}",
                        use_container_width=True,
                        disabled=not in_stock
                    ):
                        if st.session_state.get("user"):
                            try:
                                count = add_to_cart(product["id"], st.session_state.user["id"])
                                st.session_state.cart_count = count
                                st.success(f"✅ Added {product['name']} to cart!")
                            except Exception as e:
                                st.error(f"Error: {e}")
                        else:
                            st.warning("Please login first.")

                with btn_col2:
                    if st.button("🚀 Buy Now", key=f"buy_{product['id']}_{i}",
                                 use_container_width=True, disabled=not in_stock):
                        if st.session_state.get("user"):
                            try:
                                count = add_to_cart(product["id"], st.session_state.user["id"])
                                st.session_state.cart_count = count
                                st.session_state.page = "Cart"
                                st.session_state["sidebar_page_select"] = "Cart"
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
                        else:
                            st.warning("Please login first.")

                with st.expander("📋 Specs & Reviews"):
                    with st.container():
                        st.markdown(f"""
                        <div>
                            <h4 style="color:#1e3a8a; margin-bottom:0.8rem;">📐 Specifications</h4>
                        </div>
                        """, unsafe_allow_html=True)

                        if "specs" in product:
                            for spec_key, spec_val in product["specs"].items():
                                st.markdown(
                                    f"<div style='display:flex; justify-content:space-between; "
                                    f"padding:0.4rem 0; border-bottom:1px solid #e2e8f0;'>"
                                    f"<span style='color:#374151; font-weight:700;'>{spec_key}</span>"
                                    f"<span style='color:#1e3a8a; font-weight:600;'>{spec_val}</span></div>",
                                    unsafe_allow_html=True
                                )

                        st.markdown(
                            "<h4 style='color:#1e3a8a; margin:1rem 0 0.8rem 0;'>💬 Reviews</h4>",
                            unsafe_allow_html=True
                        )
                        reviews = get_reviews(product["id"])
                        if reviews:
                            for rev in reviews:
                                rev_stars = get_stars(rev[0])
                                st.markdown(
                                    f"<div style='background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; "
                                    f"padding:0.8rem; margin-bottom:0.5rem;'>"
                                    f"<div style='color:#f59e0b;'>{rev_stars}</div>"
                                    f"<div style='color:#1f2937; font-size:0.9rem;'>{rev[1]}</div>"
                                    f"<div style='color:#64748b; font-size:0.75rem;'>"
                                    f"— {rev[3]}</div></div>",
                                    unsafe_allow_html=True
                                )
                        else:
                            st.markdown(
                                "<p style='color:#64748b; font-size:0.85rem;'>"
                                "No reviews yet. Be the first!</p>",
                                unsafe_allow_html=True
                            )

                        if st.session_state.get("user"):
                            with st.form(f"review_form_{product['id']}"):
                                rev_rating = st.select_slider(
                                    "Your Rating",
                                    options=[1, 2, 3, 4, 5],
                                    value=5
                                )
                                rev_comment = st.text_area(
                                    "Your Review",
                                    placeholder="Share your experience...",
                                    height=80
                                )
                                if st.form_submit_button("Submit Review", use_container_width=True):
                                    if rev_comment.strip():
                                        submit_review(
                                            product["id"],
                                            st.session_state.user["id"],
                                            rev_rating,
                                            rev_comment
                                        )
                                        st.success("Review submitted!")
                                        st.rerun()

    # ── Pagination Controls ────────────────────────────────────────────────────
    if total_pages > 1:
        st.markdown("---")
        pcols = st.columns([1, 3, 1])
        with pcols[0]:
            if current_page > 1:
                if st.button("← Previous", use_container_width=True):
                    st.session_state.products_page -= 1
                    st.rerun()
        with pcols[1]:
            page_buttons = st.columns(min(total_pages, 7))
            start_page = max(1, current_page - 3)
            end_page = min(total_pages + 1, start_page + 7)
            for j, pg in enumerate(range(start_page, end_page)):
                with page_buttons[j]:
                    btn_type = "primary" if pg == current_page else "secondary"
                    if st.button(str(pg), key=f"page_{pg}", use_container_width=True, type=btn_type):
                        st.session_state.products_page = pg
                        st.rerun()
        with pcols[2]:
            if current_page < total_pages:
                if st.button("Next →", use_container_width=True):
                    st.session_state.products_page += 1
                    st.rerun()

        st.markdown(
            f"<p style='text-align:center; color:rgba(196,181,253,0.6); font-size:0.85rem;'>"
            f"Page {current_page} of {total_pages}</p>",
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    st.set_page_config(page_title="Trovia Products", layout="wide")
    show_products()
