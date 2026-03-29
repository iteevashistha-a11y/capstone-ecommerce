"""
Trovia — Shopping Cart Page
"""

import streamlit as st
import sys
import os
import sqlite3
from datetime import datetime
import random
import string

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.products import PRODUCTS, COUPON_CODES, get_product_by_id

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shopiq.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_cart_items(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT product_id, quantity FROM cart WHERE user_id = ? ORDER BY added_at DESC",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()
    items = []
    for row in rows:
        product = get_product_by_id(row["product_id"])
        if product:
            items.append({
                "product": product,
                "quantity": row["quantity"]
            })
    return items


def update_cart_quantity(user_id, product_id, delta):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?",
        (user_id, product_id)
    )
    row = c.fetchone()
    if row:
        new_qty = row["quantity"] + delta
        if new_qty <= 0:
            c.execute(
                "DELETE FROM cart WHERE user_id = ? AND product_id = ?",
                (user_id, product_id)
            )
        else:
            c.execute(
                "UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?",
                (new_qty, user_id, product_id)
            )
    conn.commit()
    # Update cart count
    c.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM cart WHERE user_id = ?",
        (user_id,)
    )
    count = c.fetchone()[0]
    conn.close()
    return count


def remove_from_cart(user_id, product_id):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "DELETE FROM cart WHERE user_id = ? AND product_id = ?",
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


def clear_cart(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def place_order(user_id, items, total_amount, coupon_code, discount_amount):
    conn = get_db()
    c = conn.cursor()

    # Determine status
    statuses = ["Processing", "Shipped", "Delivered"]
    status = "Processing"

    c.execute(
        "INSERT INTO orders (user_id, total_amount, status, coupon_code, discount_amount) VALUES (?, ?, ?, ?, ?)",
        (user_id, total_amount, status, coupon_code, discount_amount)
    )
    order_id = c.lastrowid

    for item in items:
        product = item["product"]
        c.execute(
            "INSERT INTO order_items (order_id, product_id, product_name, product_emoji, quantity, unit_price) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (order_id, product["id"], product["name"], product["emoji"], item["quantity"], product["price"])
        )

    conn.commit()
    conn.close()
    return order_id


def generate_order_id():
    return "SIQ" + "".join(random.choices(string.digits, k=8))


def show_cart():
    if not st.session_state.get("user"):
        st.warning("Please login to view your cart.")
        return

    user_id = st.session_state.user["id"]

    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0 0.5rem 0;">
        <h1 style="font-size: 2.5rem; font-weight: 900;
             background: linear-gradient(135deg, #a78bfa, #f0abfc);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             background-clip: text;">
            🛒 Shopping Cart
        </h1>
    </div>
    """, unsafe_allow_html=True)

    cart_items = get_cart_items(user_id)

    if not cart_items:
        # Empty cart state
        st.markdown("""
        <div style="text-align: center; padding: 5rem 2rem;
             background: linear-gradient(135deg, rgba(108,59,255,0.08), rgba(168,85,247,0.05));
             border: 2px dashed rgba(130,80,255,0.25); border-radius: 30px;
             margin: 2rem 0;">
            <div style="font-size: 6rem; margin-bottom: 1.5rem;">🛒</div>
            <h2 style="color: #c4b5fd; font-weight: 800; margin-bottom: 1rem;">
                Your cart is empty!
            </h2>
            <p style="color: rgba(196,181,253,0.6); font-size: 1.1rem; margin-bottom: 2rem;">
                Looks like you haven't added anything yet.<br>
                Discover amazing products and fill your cart!
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🛍️ Start Shopping", use_container_width=True, type="primary"):
                st.session_state.page = "Products"
                st.rerun()
        return

    # ── Cart Items ─────────────────────────────────────────────────────────────
    cart_col, summary_col = st.columns([3, 2])

    with cart_col:
        st.markdown("""
        <h3 style="color: #e8e0ff; font-weight: 800; margin-bottom: 1rem;">
            🛍️ Items in Your Cart
        </h3>
        """, unsafe_allow_html=True)

        for item in cart_items:
            product = item["product"]
            quantity = item["quantity"]
            subtotal = product["price"] * quantity

            with st.container():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(13,13,43,0.9), rgba(20,10,45,0.9));
                     border: 1px solid rgba(130,80,255,0.2); border-radius: 20px;
                     padding: 1.2rem; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
                        <div style="font-size: 3rem;">{product['emoji']}</div>
                        <div style="flex: 1; min-width: 150px;">
                            <div style="font-size: 1.1rem; font-weight: 800; color: #e8e0ff;">
                                {product['name']}
                            </div>
                            <div style="color: rgba(196,181,253,0.6); font-size: 0.85rem;">
                                {product['category']}
                            </div>
                            <div style="font-size: 1.1rem; font-weight: 700; color: #a78bfa;">
                                &#8377;{product['price']:,} each
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.3rem; font-weight: 900;
                                 background: linear-gradient(135deg, #a78bfa, #f0abfc);
                                 -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                                 background-clip: text;">
                                &#8377;{subtotal:,}
                            </div>
                            <div style="color: rgba(196,181,253,0.5); font-size: 0.8rem;">
                                Subtotal
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Quantity controls + Remove
                qty_col1, qty_col2, qty_col3, qty_col4, qty_col5 = st.columns([1, 1, 1, 1, 2])

                with qty_col1:
                    if st.button(
                        "➖",
                        key=f"minus_{product['id']}",
                        use_container_width=True,
                        help="Decrease quantity"
                    ):
                        count = update_cart_quantity(user_id, product["id"], -1)
                        st.session_state.cart_count = count
                        st.rerun()

                with qty_col2:
                    st.markdown(
                        f"<div style='text-align:center; padding: 0.5rem; font-weight:900; "
                        f"font-size:1.2rem; color:#e8e0ff;'>{quantity}</div>",
                        unsafe_allow_html=True
                    )

                with qty_col3:
                    if st.button(
                        "➕",
                        key=f"plus_{product['id']}",
                        use_container_width=True,
                        help="Increase quantity"
                    ):
                        count = update_cart_quantity(user_id, product["id"], 1)
                        st.session_state.cart_count = count
                        st.rerun()

                with qty_col5:
                    if st.button(
                        "🗑️ Remove",
                        key=f"remove_{product['id']}",
                        use_container_width=True
                    ):
                        count = remove_from_cart(user_id, product["id"])
                        st.session_state.cart_count = count
                        st.rerun()

        st.markdown("---")
        if st.button("🗑️ Clear Entire Cart", use_container_width=True):
            clear_cart(user_id)
            st.session_state.cart_count = 0
            st.rerun()

    # ── Order Summary ──────────────────────────────────────────────────────────
    with summary_col:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(108,59,255,0.15), rgba(168,85,247,0.1));
             border: 1px solid rgba(130,80,255,0.25); border-radius: 25px; padding: 1.5rem;
             position: sticky; top: 1rem;">
            <h3 style="color: #e8e0ff; font-weight: 800; margin-bottom: 1.5rem; text-align: center;">
                📋 Order Summary
            </h3>
        """, unsafe_allow_html=True)

        subtotal = sum(item["product"]["price"] * item["quantity"] for item in cart_items)
        delivery_charge = 0 if subtotal >= 499 else 49
        gst_rate = 0.18
        gst = round(subtotal * gst_rate, 2)

        # Coupon
        coupon_discount = 0
        applied_coupon = None

        if "applied_coupon" not in st.session_state:
            st.session_state.applied_coupon = None
        if "coupon_discount" not in st.session_state:
            st.session_state.coupon_discount = 0

        coupon_input = st.text_input(
            "🎟️ Coupon Code",
            placeholder="Enter coupon code (SAVE10, FIRST50, TROVIA20)",
            key="coupon_input"
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Apply Coupon", use_container_width=True, key="apply_coupon"):
                if coupon_input.strip().upper() in COUPON_CODES:
                    code = coupon_input.strip().upper()
                    coupon_data = COUPON_CODES[code]
                    st.session_state.applied_coupon = code

                    if coupon_data["type"] == "percent":
                        discount = round(subtotal * coupon_data["value"] / 100, 2)
                    else:
                        discount = coupon_data["value"]

                    st.session_state.coupon_discount = min(discount, subtotal)
                    st.success(f"Coupon applied! {coupon_data['description']}")
                    st.rerun()
                elif coupon_input.strip():
                    st.error("Invalid coupon code.")

        with c2:
            if st.session_state.applied_coupon:
                if st.button("Remove", use_container_width=True, key="remove_coupon"):
                    st.session_state.applied_coupon = None
                    st.session_state.coupon_discount = 0
                    st.rerun()

        if st.session_state.applied_coupon:
            coupon_discount = st.session_state.coupon_discount
            applied_coupon = st.session_state.applied_coupon
            st.markdown(
                f"<div style='background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3); "
                f"border-radius: 10px; padding: 0.5rem 1rem; margin-bottom: 0.5rem;'>"
                f"<p style='color: #10b981; margin: 0; font-size: 0.9rem; font-weight: 700;'>"
                f"✅ {applied_coupon} applied — -&#8377;{coupon_discount:,.2f}</p></div>",
                unsafe_allow_html=True
            )

        total = subtotal + delivery_charge + gst - coupon_discount
        total = max(0, total)

        # Summary lines
        def summary_row(label, value, highlight=False, negative=False):
            color = "#ef4444" if negative else ("#a78bfa" if highlight else "rgba(196,181,253,0.8)")
            size = "1.3rem" if highlight else "1rem"
            weight = "900" if highlight else "600"
            sign = "-" if negative else ""
            return (
                f"<div style='display:flex; justify-content:space-between; "
                f"padding: 0.5rem 0; border-bottom: 1px solid rgba(130,80,255,0.1);'>"
                f"<span style='color: rgba(196,181,253,0.7); font-size: {size};'>{label}</span>"
                f"<span style='color: {color}; font-weight: {weight}; font-size: {size};'>"
                f"{sign}&#8377;{value:,.2f}</span></div>"
            )

        delivery_label = "🚚 Delivery (Free above ₹499)" if subtotal >= 499 else "🚚 Delivery"
        delivery_display = 0.00 if delivery_charge == 0 else float(delivery_charge)
        delivery_free = subtotal >= 499

        summary_html = (
            summary_row(f"📦 Subtotal ({len(cart_items)} items)", float(subtotal)) +
            (summary_row(delivery_label, 0.00) if delivery_free else summary_row(delivery_label, float(delivery_charge))) +
            summary_row("📊 GST (18%)", gst) +
            (summary_row("🎟️ Coupon Discount", coupon_discount, negative=True) if coupon_discount > 0 else "") +
            f"<div style='display:flex; justify-content:space-between; padding: 1rem 0 0.5rem 0;'>"
            f"<span style='color: #e8e0ff; font-size: 1.3rem; font-weight: 800;'>💰 Total</span>"
            f"<span style='font-size: 1.5rem; font-weight: 900; "
            f"background: linear-gradient(135deg, #a78bfa, #f0abfc); "
            f"-webkit-background-clip: text; -webkit-text-fill-color: transparent; "
            f"background-clip: text;'>&#8377;{total:,.2f}</span></div>"
        )

        st.markdown(summary_html, unsafe_allow_html=True)

        if delivery_charge == 0:
            st.markdown(
                "<p style='color: #10b981; font-size: 0.85rem; font-weight: 600; text-align: center;'>"
                "🎉 You got FREE delivery!</p>",
                unsafe_allow_html=True
            )
        else:
            needed = 499 - subtotal
            st.markdown(
                f"<p style='color: #fbbf24; font-size: 0.85rem; font-weight: 600; text-align: center;'>"
                f"Add &#8377;{needed:,.0f} more for FREE delivery!</p>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Place Order Button ─────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "🚀 Place Order",
            use_container_width=True,
            type="primary",
            key="place_order_btn"
        ):
            if not cart_items:
                st.warning("Your cart is empty!")
            else:
                with st.spinner("Processing your order..."):
                    order_id = place_order(
                        user_id,
                        cart_items,
                        total,
                        applied_coupon or "",
                        coupon_discount
                    )
                    clear_cart(user_id)
                    st.session_state.cart_count = 0
                    st.session_state.applied_coupon = None
                    st.session_state.coupon_discount = 0

                st.balloons()
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(5,150,105,0.1));
                     border: 1px solid rgba(16,185,129,0.4); border-radius: 20px; padding: 1.5rem;
                     text-align: center; margin: 1rem 0;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎉</div>
                    <h3 style="color: #10b981; font-weight: 800; margin-bottom: 0.5rem;">
                        Order Placed Successfully!
                    </h3>
                    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 0.8rem;
                         margin: 0.8rem 0;">
                        <span style="color: rgba(196,181,253,0.7); font-size: 0.85rem;">Order ID</span><br>
                        <span style="color: #a78bfa; font-size: 1.3rem; font-weight: 900;">#{order_id}</span>
                    </div>
                    <p style="color: rgba(196,181,253,0.8); font-size: 0.9rem;">
                        Total paid: <strong style="color: #e8e0ff;">&#8377;{total:,.2f}</strong><br>
                        Estimated delivery: 3-5 business days
                    </p>
                </div>
                """, unsafe_allow_html=True)

                view_col1, view_col2 = st.columns(2)
                with view_col1:
                    if st.button("📋 View Orders", use_container_width=True):
                        st.session_state.page = "Orders"
                        st.rerun()
                with view_col2:
                    if st.button("🛍️ Continue Shopping", use_container_width=True):
                        st.session_state.page = "Products"
                        st.rerun()

        # Available coupons hint
        st.markdown("""
        <div style="background: rgba(108,59,255,0.08); border: 1px solid rgba(130,80,255,0.15);
             border-radius: 15px; padding: 1rem; margin-top: 1rem;">
            <p style="color: #c4b5fd; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.5rem;">
                🎟️ Available Coupons:
            </p>
            <div style="color: rgba(196,181,253,0.7); font-size: 0.8rem; line-height: 1.8;">
                <strong style="color: #a78bfa;">SAVE10</strong> — 10% off on all orders<br>
                <strong style="color: #a78bfa;">FIRST50</strong> — Flat ₹50 off<br>
                <strong style="color: #a78bfa;">TROVIA20</strong> — 20% off (Trovia special)
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(page_title="Trovia Cart", layout="wide")
    show_cart()
