"""
Trovia — Search by Image (AI Visual Search)
"""

import streamlit as st
import sys
import os
import base64
import json
from io import BytesIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.products import PRODUCTS


def load_openai_client():
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except Exception:
        return None


def image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")


def analyze_image_with_gpt4o(image_bytes, client):
    """Use GPT-4o vision to analyze an uploaded product image."""
    b64 = image_to_base64(image_bytes)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Analyze this image and identify the product or item shown. "
                                "Respond ONLY with a JSON object (no markdown, no code blocks) with these fields:\n"
                                "- category: one of [Electronics, Fashion, Books, Food, Sports, Beauty, Other]\n"
                                "- product_type: specific type (e.g. smartphone, jeans, book)\n"
                                "- color: main color(s)\n"
                                "- brand_hints: any brand hints visible (or 'unknown')\n"
                                "- keywords: array of 5-8 search keywords\n"
                                "- description: 1-2 sentence description of what you see\n"
                                "- confidence: high/medium/low"
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        raw = response.choices[0].message.content.strip()
        # Clean potential markdown
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {
            "category": "Other",
            "product_type": "product",
            "color": "unknown",
            "brand_hints": "unknown",
            "keywords": ["product"],
            "description": raw if "raw" in dir() else "Could not parse response",
            "confidence": "low"
        }
    except Exception as e:
        return {"error": str(e)}


def analyze_text_query_with_ai(query, client):
    """Use GPT-4o-mini to map a text description to product keywords."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a product search assistant. Given a user's description, "
                        "extract search keywords to find products. "
                        "Respond ONLY with a JSON object with fields: "
                        "category (Electronics/Fashion/Books/Food/Sports/Beauty/Other), "
                        "keywords (array of 5 search terms), "
                        "product_type (specific product type). No markdown."
                    )
                },
                {"role": "user", "content": f"Find products matching: {query}"}
            ],
            max_tokens=200
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception:
        return {
            "category": "Other",
            "keywords": query.lower().split()[:5],
            "product_type": query
        }


def match_products(analysis_result):
    """Match analyzed image/text to products in catalog."""
    if "error" in analysis_result:
        return []

    matches = []
    keywords = [k.lower() for k in analysis_result.get("keywords", [])]
    category = analysis_result.get("category", "").lower()
    product_type = analysis_result.get("product_type", "").lower()

    # Build all searchable terms
    all_search_terms = keywords + [category, product_type]
    all_search_terms = [t.strip() for t in all_search_terms if t.strip()]

    for product in PRODUCTS:
        score = 0

        # Category match (high weight)
        if category and category in product["category"].lower():
            score += 5

        # Product tags match
        for tag in product["tags"]:
            for term in all_search_terms:
                if term in tag or tag in term:
                    score += 2

        # Name match
        for term in all_search_terms:
            if term in product["name"].lower():
                score += 3

        # Image keywords match
        for img_kw in product.get("image_keywords", []):
            for term in all_search_terms:
                if term in img_kw or img_kw in term:
                    score += 2

        # Description match
        for term in all_search_terms:
            if term in product["description"].lower():
                score += 1

        if score > 0:
            matches.append((score, product))

    # Sort by score descending
    matches.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in matches[:6]]


def get_stars(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty


def add_to_cart(product_id, user_id):
    import sqlite3
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shopiq.db")
    conn = sqlite3.connect(db_path)
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


def show_image_search():
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0 0.5rem 0;">
        <h1 style="font-size: 2.5rem; font-weight: 900;
             background: linear-gradient(135deg, #a78bfa, #f0abfc);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             background-clip: text;">
            🔍 Search by Image
        </h1>
        <p style="color: #c4b5fd; font-size: 1rem;">Find Products Visually with AI</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Explanation Banner ────────────────────────────────────────────────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(108,59,255,0.15), rgba(168,85,247,0.1));
         border: 1px solid rgba(130,80,255,0.25); border-radius: 20px; padding: 1.5rem; margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
            <div style="font-size: 3rem;">🤖</div>
            <div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #e8e0ff; margin-bottom: 0.5rem;">
                    Upload any image and our AI finds matching products!
                </div>
                <div style="color: rgba(196,181,253,0.8); font-size: 0.95rem; line-height: 1.5;">
                    Our AI (GPT-4o Vision) analyzes your image to detect the product category, type, color,
                    and brand — then searches our entire catalog for the best matches.
                    Works with photos, screenshots, or any product image!
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
            <span style="background: rgba(108,59,255,0.2); border: 1px solid rgba(130,80,255,0.3);
                color: #c4b5fd; border-radius: 20px; padding: 0.3rem 1rem; font-size: 0.85rem; font-weight: 700;">
                📸 Upload Image
            </span>
            <span style="background: rgba(108,59,255,0.2); border: 1px solid rgba(130,80,255,0.3);
                color: #c4b5fd; border-radius: 20px; padding: 0.3rem 1rem; font-size: 0.85rem; font-weight: 700;">
                🧠 AI Analysis
            </span>
            <span style="background: rgba(108,59,255,0.2); border: 1px solid rgba(130,80,255,0.3);
                color: #c4b5fd; border-radius: 20px; padding: 0.3rem 1rem; font-size: 0.85rem; font-weight: 700;">
                🛒 Find Products
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    client = load_openai_client()
    api_available = client is not None

    if not api_available:
        st.markdown("""
        <div style="background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.4);
             border-radius: 15px; padding: 1rem; margin-bottom: 1rem;">
            <p style="color: #fbbf24; margin: 0; font-weight: 700;">
                ⚠️ OpenAI API key not found. Add OPENAI_API_KEY to your .env file for AI-powered search.
                Keyword-based matching is still available!
            </p>
        </div>
        """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📸 Upload Image", "✍️ Describe What You Want"])

    # ── Tab 1: Image Upload ────────────────────────────────────────────────────
    with tab1:
        col_upload, col_preview = st.columns([1, 1])

        with col_upload:
            st.markdown("""
            <div style="color: #c4b5fd; font-weight: 700; font-size: 1rem; margin-bottom: 0.5rem;">
                📤 Upload a product image
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Upload image",
                type=["jpg", "jpeg", "png", "webp"],
                key="image_uploader",
                label_visibility="collapsed",
                help="Upload a JPG, PNG, or WebP image of a product"
            )

            if uploaded_file:
                st.markdown("""
                <div style="color: #10b981; font-weight: 700; font-size: 0.9rem; margin: 0.5rem 0;">
                    ✅ Image uploaded successfully!
                </div>
                """, unsafe_allow_html=True)

                analyze_btn = st.button(
                    "🔍 Analyze with AI",
                    key="analyze_btn",
                    use_container_width=True,
                    type="primary"
                )

        with col_preview:
            if uploaded_file:
                from PIL import Image
                img = Image.open(uploaded_file)
                st.markdown("""
                <div style="border: 2px solid rgba(130,80,255,0.5); border-radius: 20px;
                     padding: 1rem; background: rgba(13,13,43,0.5); text-align: center;
                     margin-bottom: 1rem;">
                    <p style="color: #c4b5fd; font-size: 0.85rem; margin-bottom: 0.5rem;">
                        📸 Your uploaded image:
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.image(img, caption="Uploaded Image", use_column_width=True)

        # Analysis & Results
        if uploaded_file and "analyze_btn" in dir() and analyze_btn:
            uploaded_file.seek(0)
            image_bytes = uploaded_file.read()

            # Save to history
            if "search_history" not in st.session_state:
                st.session_state.search_history = []

            st.session_state.search_history.insert(0, {
                "type": "image",
                "name": uploaded_file.name,
                "bytes": image_bytes[:5000]  # Store small preview
            })
            st.session_state.search_history = st.session_state.search_history[:5]

            with st.spinner("🤖 AI is analyzing your image..."):
                if api_available:
                    analysis = analyze_image_with_gpt4o(image_bytes, client)
                else:
                    # Fallback: keyword from filename
                    name_kw = uploaded_file.name.replace("_", " ").replace("-", " ")
                    analysis = {
                        "category": "Other",
                        "product_type": name_kw,
                        "color": "unknown",
                        "brand_hints": "unknown",
                        "keywords": name_kw.lower().split()[:5],
                        "description": f"Image: {name_kw}",
                        "confidence": "low"
                    }

            if "error" in analysis:
                st.error(f"AI Analysis Error: {analysis['error']}")
            else:
                # Show AI Analysis Card
                confidence_colors = {"high": "#10b981", "medium": "#f59e0b", "low": "#ef4444"}
                conf_color = confidence_colors.get(analysis.get("confidence", "low"), "#c4b5fd")

                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(108,59,255,0.2), rgba(168,85,247,0.1));
                     border: 1px solid rgba(130,80,255,0.3); border-radius: 20px;
                     padding: 1.5rem; margin: 1.5rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;
                         margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
                        <h3 style="color: #e8e0ff; font-weight: 800; margin: 0;">
                            🧠 AI Analysis Result
                        </h3>
                        <span style="background: {conf_color}; color: white; border-radius: 15px;
                             padding: 0.2rem 0.8rem; font-size: 0.85rem; font-weight: 700;">
                            {analysis.get('confidence', 'low').title()} Confidence
                        </span>
                    </div>
                    <p style="color: rgba(196,181,253,0.9); margin-bottom: 1rem; line-height: 1.6;">
                        {analysis.get('description', 'Product detected')}
                    </p>
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                        <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 0.8rem 1.2rem;">
                            <div style="color: rgba(196,181,253,0.6); font-size: 0.75rem; font-weight: 700;">
                                CATEGORY
                            </div>
                            <div style="color: #e8e0ff; font-weight: 800; font-size: 1rem;">
                                {analysis.get('category', 'Unknown')}
                            </div>
                        </div>
                        <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 0.8rem 1.2rem;">
                            <div style="color: rgba(196,181,253,0.6); font-size: 0.75rem; font-weight: 700;">
                                TYPE
                            </div>
                            <div style="color: #e8e0ff; font-weight: 800; font-size: 1rem;">
                                {analysis.get('product_type', 'Unknown')}
                            </div>
                        </div>
                        <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 0.8rem 1.2rem;">
                            <div style="color: rgba(196,181,253,0.6); font-size: 0.75rem; font-weight: 700;">
                                COLOR
                            </div>
                            <div style="color: #e8e0ff; font-weight: 800; font-size: 1rem;">
                                {analysis.get('color', 'Unknown')}
                            </div>
                        </div>
                        <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 0.8rem 1.2rem;">
                            <div style="color: rgba(196,181,253,0.6); font-size: 0.75rem; font-weight: 700;">
                                BRAND HINT
                            </div>
                            <div style="color: #e8e0ff; font-weight: 800; font-size: 1rem;">
                                {analysis.get('brand_hints', 'Unknown')}
                            </div>
                        </div>
                    </div>
                    <div style="margin-top: 1rem;">
                        <span style="color: rgba(196,181,253,0.6); font-size: 0.8rem; font-weight: 700;">
                            🏷️ KEYWORDS:
                        </span>
                        {"".join(
                            f'<span style="background: rgba(108,59,255,0.2); border: 1px solid rgba(130,80,255,0.3); '
                            f'color: #c4b5fd; border-radius: 15px; padding: 0.2rem 0.7rem; '
                            f'font-size: 0.8rem; margin: 0.2rem; display: inline-block;">{kw}</span>'
                            for kw in analysis.get("keywords", [])
                        )}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Show matching products
                matches = match_products(analysis)
                st.markdown(f"""
                <h3 style="color: #e8e0ff; font-weight: 800; margin: 1.5rem 0 1rem 0;">
                    🛒 Matching Products ({len(matches)} found)
                </h3>
                """, unsafe_allow_html=True)

                if matches:
                    match_cols = st.columns(3)
                    for i, product in enumerate(matches):
                        with match_cols[i % 3]:
                            stars = get_stars(product["rating"])
                            st.markdown(f"""
                            <div class="product-card">
                                <span class="product-emoji">{product['emoji']}</span>
                                <div class="product-name">{product['name']}</div>
                                <div class="product-rating">{stars}</div>
                                <div class="product-price">&#8377;{product['price']:,}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button(
                                "🛒 Add to Cart",
                                key=f"img_cart_{product['id']}_{i}",
                                use_container_width=True
                            ):
                                if st.session_state.get("user"):
                                    try:
                                        count = add_to_cart(
                                            product["id"],
                                            st.session_state.user["id"]
                                        )
                                        st.session_state.cart_count = count
                                        st.success(f"Added {product['emoji']} to cart!")
                                    except Exception as e:
                                        st.error(str(e))
                                else:
                                    st.warning("Please login first.")
                else:
                    st.markdown("""
                    <div style="text-align: center; padding: 2rem;
                         background: rgba(108,59,255,0.05); border-radius: 20px;
                         border: 1px dashed rgba(130,80,255,0.3);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">🤔</div>
                        <p style="color: #c4b5fd;">
                            No exact matches found. Try browsing our
                            <strong style="color: #a78bfa;">Products</strong> page instead.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

    # ── Tab 2: Text Description ────────────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div style="color: #c4b5fd; font-weight: 600; margin-bottom: 1rem; line-height: 1.6;">
            Don't have an image? Describe what you're looking for in plain English
            and our AI will find the best matching products for you!
        </div>
        """, unsafe_allow_html=True)

        text_query = st.text_area(
            "Describe what you want",
            placeholder=(
                "e.g. 'wireless earbuds under 3000 rupees with good bass'\n"
                "or 'blue running shoes for men'\n"
                "or 'gift for a 10 year old who loves reading'"
            ),
            height=120,
            key="text_search_input",
            label_visibility="collapsed"
        )

        # Quick suggestion chips
        st.markdown("""
        <div style="margin: 0.5rem 0;">
            <span style="color: rgba(196,181,253,0.6); font-size: 0.85rem; font-weight: 700;">
                💡 Try:
            </span>
        </div>
        """, unsafe_allow_html=True)

        suggestions = [
            "Wireless earbuds under ₹3000",
            "Books for programming",
            "Indian ethnic wear for women",
            "Sports equipment for cricket"
        ]
        sug_cols = st.columns(len(suggestions))
        for i, sug in enumerate(suggestions):
            with sug_cols[i]:
                if st.button(sug, key=f"sug_{i}", use_container_width=True):
                    st.session_state["text_search_prefill"] = sug
                    st.rerun()

        if "text_search_prefill" in st.session_state:
            text_query = st.session_state["text_search_prefill"]
            del st.session_state["text_search_prefill"]

        search_text_btn = st.button(
            "🔍 Find Products",
            key="search_text_btn",
            use_container_width=True,
            type="primary",
            disabled=not text_query.strip()
        )

        if search_text_btn and text_query.strip():
            with st.spinner("🤖 Finding the best matches..."):
                if api_available:
                    analysis = analyze_text_query_with_ai(text_query, client)
                else:
                    analysis = {
                        "category": "Other",
                        "keywords": text_query.lower().split()[:6],
                        "product_type": text_query
                    }

            st.markdown(f"""
            <div style="background: rgba(108,59,255,0.1); border: 1px solid rgba(130,80,255,0.2);
                 border-radius: 15px; padding: 1rem; margin: 1rem 0;">
                <p style="color: #c4b5fd; margin: 0; font-size: 0.9rem;">
                    <strong>AI mapped your query to:</strong>
                    Category: <span style="color: #a78bfa;">{analysis.get('category', 'All')}</span> |
                    Type: <span style="color: #a78bfa;">{analysis.get('product_type', 'product')}</span> |
                    Keywords: <span style="color: #a78bfa;">{', '.join(analysis.get('keywords', []))}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

            matches = match_products(analysis)
            st.markdown(f"""
            <h3 style="color: #e8e0ff; font-weight: 800; margin: 1rem 0;">
                🛒 Results for "{text_query}" ({len(matches)} found)
            </h3>
            """, unsafe_allow_html=True)

            if matches:
                match_cols = st.columns(3)
                for i, product in enumerate(matches):
                    with match_cols[i % 3]:
                        stars = get_stars(product["rating"])
                        st.markdown(f"""
                        <div class="product-card">
                            <span class="product-emoji">{product['emoji']}</span>
                            <div class="product-name">{product['name']}</div>
                            <div class="product-rating">{stars}</div>
                            <div class="product-price">&#8377;{product['price']:,}</div>
                            <div style="color: rgba(196,181,253,0.7); font-size: 0.8rem; margin-top: 0.5rem;">
                                {product['description'][:80]}...
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(
                            "🛒 Add to Cart",
                            key=f"txt_cart_{product['id']}_{i}",
                            use_container_width=True
                        ):
                            if st.session_state.get("user"):
                                try:
                                    count = add_to_cart(
                                        product["id"],
                                        st.session_state.user["id"]
                                    )
                                    st.session_state.cart_count = count
                                    st.success(f"Added {product['emoji']} to cart!")
                                except Exception as e:
                                    st.error(str(e))
                            else:
                                st.warning("Please login first.")
            else:
                st.info("No matching products found. Try different keywords or browse our Products page.")

    # ── Search History ────────────────────────────────────────────────────────
    if st.session_state.get("search_history"):
        st.markdown("---")
        st.markdown("""
        <h3 style="color: #e8e0ff; font-weight: 800; margin-bottom: 1rem;">
            🕐 Recent Searches
        </h3>
        """, unsafe_allow_html=True)

        hist_cols = st.columns(5)
        for i, item in enumerate(st.session_state.search_history[:5]):
            with hist_cols[i]:
                st.markdown(f"""
                <div style="background: rgba(108,59,255,0.1); border: 1px solid rgba(130,80,255,0.2);
                     border-radius: 15px; padding: 1rem; text-align: center;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">
                        {"📸" if item["type"] == "image" else "✍️"}
                    </div>
                    <div style="color: #c4b5fd; font-size: 0.8rem; font-weight: 600;
                         word-break: break-all; max-width: 100px; margin: 0 auto;">
                        {item.get("name", "Search")[:20]}
                    </div>
                </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(page_title="Trovia Image Search", layout="wide")
    show_image_search()
