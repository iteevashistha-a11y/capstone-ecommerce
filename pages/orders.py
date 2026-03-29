"""
Trovia — Orders Page
"""

import streamlit as st
import sys
import os
import sqlite3
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.products import get_product_by_id

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shopiq.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_user_orders(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        """SELECT o.*,
           (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.id) as item_count
           FROM orders o
           WHERE o.user_id = ?
           ORDER BY o.placed_at DESC""",
        (user_id,)
    )
    orders = [dict(row) for row in c.fetchall()]
    conn.close()
    return orders


def get_order_items(order_id):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM order_items WHERE order_id = ?",
        (order_id,)
    )
    items = [dict(row) for row in c.fetchall()]
    conn.close()
    return items


def reorder(user_id, order_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    items = c.fetchall()
    added = 0
    for item in items:
        try:
            c.execute(
                "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?) "
                "ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = quantity + ?",
                (user_id, item["product_id"], item["quantity"], item["quantity"])
            )
            added += 1
        except Exception:
            pass
    conn.commit()
    c.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM cart WHERE user_id = ?",
        (user_id,)
    )
    count = c.fetchone()[0]
    conn.close()
    return added, count


def format_date(date_str):
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return date_str


def get_status_style(status):
    styles = {
        "Delivered": ("status-delivered", "✅"),
        "Processing": ("status-processing", "⏳"),
        "Shipped": ("status-shipped", "🚚"),
        "Cancelled": ("background: #ef4444; color: white; border-radius: 20px; padding: 0.2rem 0.8rem;", "❌"),
    }
    return styles.get(status, ("status-processing", "📦"))


def show_orders():
    if not st.session_state.get("user"):
        st.warning("Please login to view your orders.")
        return

    user_id = st.session_state.user["id"]

    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0 0.5rem 0;">
        <h1 style="font-size: 2.5rem; font-weight: 900;
             background: linear-gradient(135deg, #a78bfa, #f0abfc);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             background-clip: text;">
            📋 My Orders
        </h1>
        <p style="color: #c4b5fd; font-size: 1rem;">Track and manage your orders</p>
    </div>
    """, unsafe_allow_html=True)

    orders = get_user_orders(user_id)

    if not orders:
        st.markdown("""
        <div style="text-align: center; padding: 5rem 2rem;
             background: linear-gradient(135deg, rgba(108,59,255,0.08), rgba(168,85,247,0.05));
             border: 2px dashed rgba(130,80,255,0.25); border-radius: 30px; margin: 2rem 0;">
            <div style="font-size: 5rem; margin-bottom: 1.5rem;">📦</div>
            <h2 style="color: #c4b5fd; font-weight: 800; margin-bottom: 1rem;">
                No orders yet!
            </h2>
            <p style="color: rgba(196,181,253,0.6); font-size: 1.1rem; margin-bottom: 2rem;">
                You haven't placed any orders yet.<br>
                Start shopping and your orders will appear here.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🛍️ Start Shopping", use_container_width=True, type="primary"):
                st.session_state.page = "Products"
                st.rerun()
        return

    # ── Stats Row ─────────────────────────────────────────────────────────────
    total_orders = len(orders)
    total_spent = sum(o["total_amount"] for o in orders if o["total_amount"])
    delivered = sum(1 for o in orders if o["status"] == "Delivered")
    processing = sum(1 for o in orders if o["status"] in ["Processing", "Shipped"])

    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        (m1, "📦 Total Orders", str(total_orders)),
        (m2, "💰 Total Spent", f"₹{total_spent:,.0f}"),
        (m3, "✅ Delivered", str(delivered)),
        (m4, "⏳ In Progress", str(processing)),
    ]
    for col, label, value in metrics:
        with col:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(108,59,255,0.15), rgba(168,85,247,0.1));
                 border: 1px solid rgba(130,80,255,0.2); border-radius: 20px; padding: 1.2rem;
                 text-align: center; margin-bottom: 1rem;">
                <div style="color: rgba(196,181,253,0.6); font-size: 0.85rem; font-weight: 700;">
                    {label}
                </div>
                <div style="font-size: 1.8rem; font-weight: 900;
                     background: linear-gradient(135deg, #a78bfa, #f0abfc);
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                     background-clip: text; margin-top: 0.3rem;">
                    {value}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Orders List ────────────────────────────────────────────────────────────
    st.markdown("""
    <h3 style="color: #e8e0ff; font-weight: 800; margin-bottom: 1rem;">
        🗂️ Order History
    </h3>
    """, unsafe_allow_html=True)

    for order in orders:
        order_id = order["id"]
        status = order["status"]
        status_style, status_icon = get_status_style(status)
        placed_at = format_date(order["placed_at"])
        total = order["total_amount"] or 0
        item_count = order["item_count"]

        # Order header
        with st.expander(
            f"Order #{order_id} — ₹{total:,.2f} — {status_icon} {status} — {placed_at}",
            expanded=False
        ):
            # Order metadata
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 0.8rem;
                     background: rgba(108,59,255,0.1); border-radius: 12px;">
                    <div style="color: rgba(196,181,253,0.6); font-size: 0.75rem; font-weight: 700;">ORDER ID</div>
                    <div style="color: #a78bfa; font-weight: 900; font-size: 1rem;">#{order_id}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 0.8rem;
                     background: rgba(108,59,255,0.1); border-radius: 12px;">
                    <div style="color: rgba(196,181,253,0.6); font-size: 0.75rem; font-weight: 700;">PLACED ON</div>
                    <div style="color: #e8e0ff; font-weight: 700; font-size: 0.9rem;">{placed_at}</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div style="text-align: center; padding: 0.8rem;
                     background: rgba(108,59,255,0.1); border-radius: 12px;">
                    <div style="color: rgba(196,181,253,0.6); font-size: 0.75rem; font-weight: 700;">ITEMS</div>
                    <div style="color: #e8e0ff; font-weight: 900; font-size: 1rem;">{item_count}</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div style="text-align: center; padding: 0.8rem;
                     background: rgba(108,59,255,0.1); border-radius: 12px;">
                    <div style="color: rgba(196,181,253,0.6); font-size: 0.75rem; font-weight: 700;">TOTAL</div>
                    <div style="color: #a78bfa; font-weight: 900; font-size: 1rem;">&#8377;{total:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)

            # Status badge + timeline
            st.markdown("<br>", unsafe_allow_html=True)

            status_colors = {
                "Processing": ("#f59e0b", "Your order is being prepared"),
                "Shipped": ("#3b82f6", "Your order is on its way!"),
                "Delivered": ("#10b981", "Order delivered successfully!"),
            }
            s_color, s_msg = status_colors.get(status, ("#c4b5fd", "Order received"))

            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.2); border: 1px solid {s_color}40;
                 border-radius: 15px; padding: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
                    <span style="background: {s_color}; color: white; border-radius: 20px;
                         padding: 0.3rem 1rem; font-weight: 800; font-size: 0.9rem;">
                        {status_icon} {status}
                    </span>
                    <span style="color: rgba(196,181,253,0.8); font-size: 0.9rem;">{s_msg}</span>
                </div>
                <div style="display: flex; gap: 0.5rem; margin-top: 1rem; align-items: center;">
                    {"".join(
                        f'<div style="flex: 1; height: 4px; border-radius: 2px; background: {s_color if i <= ["Processing","Shipped","Delivered"].index(status) else "rgba(130,80,255,0.2)"};"></div>'
                        + (f'<div style="font-size: 0.65rem; color: {s_color if i <= ["Processing","Shipped","Delivered"].index(status) else "rgba(196,181,253,0.3)"}; white-space: nowrap;">{lbl}</div>' if i < 2 else "")
                        for i, lbl in enumerate(["Processing", "Shipped", "Delivered"])
                        if True
                    )}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Order Items
            order_items = get_order_items(order_id)
            if order_items:
                st.markdown("""
                <h4 style="color: #e8e0ff; font-weight: 800; margin-bottom: 0.8rem;">
                    📦 Items in this Order
                </h4>
                """, unsafe_allow_html=True)

                items_html = ""
                for oi in order_items:
                    item_total = (oi["unit_price"] or 0) * (oi["quantity"] or 1)
                    items_html += (
                        f"<div style='display:flex; align-items:center; gap:1rem; "
                        f"padding:0.8rem; border-bottom: 1px solid rgba(130,80,255,0.1);'>"
                        f"<div style='font-size:2rem;'>{oi['product_emoji'] or '📦'}</div>"
                        f"<div style='flex:1;'>"
                        f"<div style='color:#e8e0ff; font-weight:700;'>{oi['product_name']}</div>"
                        f"<div style='color:rgba(196,181,253,0.6); font-size:0.85rem;'>"
                        f"Qty: {oi['quantity']} × &#8377;{oi['unit_price']:,}</div>"
                        f"</div>"
                        f"<div style='color:#a78bfa; font-weight:900;'>&#8377;{item_total:,.0f}</div>"
                        f"</div>"
                    )

                st.markdown(f"""
                <div style="background: rgba(13,13,43,0.7); border: 1px solid rgba(130,80,255,0.15);
                     border-radius: 15px; overflow: hidden; margin-bottom: 1rem;">
                    {items_html}
                </div>
                """, unsafe_allow_html=True)

            # Coupon & total breakdown
            if order.get("coupon_code"):
                st.markdown(
                    f"<p style='color: #10b981; font-size: 0.9rem; font-weight: 700;'>"
                    f"🎟️ Coupon <strong>{order['coupon_code']}</strong> applied — "
                    f"saved &#8377;{order['discount_amount']:,.2f}</p>",
                    unsafe_allow_html=True
                )

            # Action buttons
            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
            with btn_col1:
                if st.button(
                    "🔄 Reorder",
                    key=f"reorder_{order_id}",
                    use_container_width=True
                ):
                    added, count = reorder(user_id, order_id)
                    st.session_state.cart_count = count
                    st.success(f"Added {added} items back to cart!")
                    st.rerun()

            with btn_col2:
                if status == "Delivered":
                    if st.button(
                        "⭐ Rate Order",
                        key=f"rate_{order_id}",
                        use_container_width=True
                    ):
                        st.session_state.page = "Products"
                        st.rerun()

            # Invoice download hint
            with btn_col3:
                st.markdown(
                    f"<p style='color: rgba(196,181,253,0.5); font-size: 0.8rem; padding-top: 0.5rem;'>"
                    f"📧 Invoice sent to your email</p>",
                    unsafe_allow_html=True
                )


if __name__ == "__main__":
    st.set_page_config(page_title="Trovia Orders", layout="wide")
    show_orders()
