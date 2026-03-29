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

    # ── Filter Products ────────────────────────────────────────────────────────
    filtered = list(PRODUCTS)

    if search_query:
        q = search_query.lower()
        filtered = [
            p for p in filtered
            if q in p["name"].lower()
            or q in p["description"].lower()
            or q in p["category"].lower()
            or any(q in tag for tag in p["tags"])
        ]

    if selected_category != "All Categories":
        filtered = [p for p in filtered if p["category"] == selected_category]

    filtered = [p for p in filtered if price_range[0] <= p["price"] <= price_range[1]]
    filtered = [p for p in filtered if p["rating"] >= min_rating]

    if in_stock_only:
        filtered = [p for p in filtered if p["in_stock"]]

    # Sort
    if sort_by == "Price: Low to High":
        filtered.sort(key=lambda x: x["price"])
    elif sort_by == "Price: High to Low":
        filtered.sort(key=lambda x: x["price"], reverse=True)
    elif sort_by == "Rating: High to Low":
        filtered.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "Name: A to Z":
        filtered.sort(key=lambda x: x["name"])

    # ── Results Summary ────────────────────────────────────────────────────────
    col_info, col_view = st.columns([3, 1])
    with col_info:
        st.markdown(
            f"<p style='color: #c4b5fd; font-weight: 600;'>"
            f"Showing <strong style='color:#a78bfa'>{len(filtered)}</strong> products</p>",
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
             background: rgba(108,59,255,0.05); border-radius: 25px;
             border: 1px dashed rgba(130,80,255,0.3);">
            <div style="font-size: 4rem; margin-bottom: 1rem;">😕</div>
            <h3 style="color: #c4b5fd;">No products found</h3>
            <p style="color: rgba(196,181,253,0.6);">Try adjusting your filters or search query</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for i, product in enumerate(page_products):
            with cols[i % 3]:
                stars = get_stars(product["rating"])
                stock_badge = (
                    '<span style="color: #10b981; font-size: 0.8rem; font-weight: 700;">✅ In Stock</span>'
                    if product["in_stock"]
                    else '<span style="color: #ef4444; font-size: 0.8rem; font-weight: 700;">❌ Out of Stock</span>'
                )

                st.markdown(f"""
                <div class="product-card">
                    <span class="product-emoji">{product['emoji']}</span>
                    <div style="font-size: 0.75rem; color: rgba(196,181,253,0.6);
                         text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.3rem;">
                        {product['category']}
                    </div>
                    <div class="product-name">{product['name']}</div>
                    <div class="product-rating">{stars} <span style="color: #c4b5fd;">{product['rating']}</span></div>
                    <div class="product-price">&#8377;{product['price']:,}</div>
                    <div style="color: rgba(196,181,253,0.7); font-size: 0.85rem;
                         margin-bottom: 0.8rem; line-height: 1.4;">
                        {product['description'][:90]}...
                    </div>
                    {stock_badge}
                </div>
                """, unsafe_allow_html=True)

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(
                        "🛒 Cart",
                        key=f"prod_cart_{product['id']}_{i}",
                        use_container_width=True,
                        disabled=not product["in_stock"]
                    ):
                        if st.session_state.get("user"):
                            try:
                                count = add_to_cart(product["id"], st.session_state.user["id"])
                                st.session_state.cart_count = count
                                st.success(f"Added {product['emoji']} to cart!")
                            except Exception as e:
                                st.error(f"Error: {e}")
                        else:
                            st.warning("Please login first.")

                with btn_col2:
                    with st.expander("📋 Details"):
                        st.markdown(f"""
                        <div style="color: #e8e0ff;">
                            <p style="font-size: 0.95rem; line-height: 1.6; color: rgba(196,181,253,0.9);">
                                {product['description']}
                            </p>
                            <hr style="border-color: rgba(130,80,255,0.2);"/>
                            <h4 style="color: #a78bfa; margin-bottom: 0.8rem;">📐 Specifications</h4>
                        </div>
                        """, unsafe_allow_html=True)

                        if "specs" in product:
                            for spec_key, spec_val in product["specs"].items():
                                st.markdown(
                                    f"<div style='display:flex; justify-content:space-between; "
                                    f"padding:0.3rem 0; border-bottom: 1px solid rgba(130,80,255,0.1);'>"
                                    f"<span style='color:#c4b5fd; font-weight:700;'>{spec_key}</span>"
                                    f"<span style='color:#e8e0ff;'>{spec_val}</span></div>",
                                    unsafe_allow_html=True
                                )

                        st.markdown(
                            "<h4 style='color: #a78bfa; margin: 1rem 0 0.8rem 0;'>💬 Reviews</h4>",
                            unsafe_allow_html=True
                        )
                        reviews = get_reviews(product["id"])
                        if reviews:
                            for rev in reviews:
                                rev_stars = get_stars(rev[0])
                                st.markdown(
                                    f"<div style='background: rgba(108,59,255,0.1); border-radius:10px; "
                                    f"padding: 0.8rem; margin-bottom: 0.5rem;'>"
                                    f"<div style='color: #fbbf24;'>{rev_stars}</div>"
                                    f"<div style='color: #e8e0ff; font-size: 0.9rem;'>{rev[1]}</div>"
                                    f"<div style='color: rgba(196,181,253,0.5); font-size: 0.75rem;'>"
                                    f"— {rev[3]}</div></div>",
                                    unsafe_allow_html=True
                                )
                        else:
                            st.markdown(
                                "<p style='color: rgba(196,181,253,0.5); font-size:0.85rem;'>"
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
