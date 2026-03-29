"""
Trovia — AI Shopping Assistant (Shopi)
"""

import streamlit as st
import sys
import os
import io

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.products import PRODUCTS, CATEGORIES


def load_openai_client():
    from dotenv import load_dotenv
    load_dotenv()
    api_key = st.session_state.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    else:
        return None

    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except Exception:
        return None


def get_arya_system_prompt():
    product_list = "\n".join(
        f"- {p['name']} ({p['category']}): ₹{p['price']:,} | Rating: {p['rating']} | {p['emoji']}"
        for p in PRODUCTS
    )

    return f"""You are Arya, Trovia's cheerful AI shopping assistant. You are:
- 22 years old, empathetic, helpful, and high-energy
- An expert in all products in the Trovia catalog
- Great at recommending products with value-for-money insight
- Fluent in both English and Hinglish (mix of Hindi + English)

PRODUCT CATALOG:
{product_list}

YOUR CAPABILITIES:
1. Recommend products based on budget (always mention price in ₹)
2. Compare products (e.g., boAt vs JBL earbuds)
3. Help find gifts for occasions and occasions
4. Explain product features with friendly tone
5. Suggest bundles and mobile-first deals
6. Help with order tracking and shipping updates
7. Provide shopping tips and buying checklists

PERSONALITY:
- Use emojis naturally but not excessively
- Be warm, conversational, and confident
- Use short sentences with clear bullet points when needed
- Keep responses concise and highly actionable

IMPORTANT:
- Only recommend products from the catalog above
- Always format prices as ₹X,XXX
- When comparing products, use bullet points for clarity
- Never make up products that aren't in the catalog"""


def get_shopi_response(messages, client):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=600,
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I'm having trouble connecting right now. Error: {str(e)}"


def text_to_speech(text, lang='en', tld='co.in'):
    try:
        from gtts import gTTS
        # Clean text for TTS (remove markdown)
        import re
        clean_text = re.sub(r'[*#_`]', '', text)
        clean_text = re.sub(r'\n+', ' ', clean_text)
        clean_text = clean_text[:500]  # Limit TTS length

        tts = gTTS(text=clean_text, lang=lang, tld=tld, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception:
        return None


def get_stars(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty


ARYA_INTRO = """Hey there! 👋 I'm **Arya**, your personal AI shopping assistant at Trovia!

I'm here to help you find the perfect products, compare options, and make your shopping experience awesome! 🛒✨

Here's what I can do for you:
- 🔍 **Find products** based on your budget and preferences
- ⚖️ **Compare products** side by side
- 🎁 **Gift recommendations** for any occasion
- 💰 **Best deals** within your budget
- 📦 **Product info** — specs, features, and more

What are you looking to shop for today? Ask me anything! 😊"""


def show_ai_assistant():
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0 0.5rem 0;">
        <h1 style="font-size: 2.5rem; font-weight: 900;
             background: linear-gradient(135deg, #0ea5e9, #38bdf8);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             background-clip: text;">
            � Arya Chat
        </h1>
        <p style="color: #1e3a8a; font-size: 1rem;">
            Your AI Shopping Assistant — Powered by GPT-4o-mini
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = ""

    with st.expander("🔑 OpenAI API Key for Trovia Chat (optional)", expanded=True):
        key_input = st.text_input(
            "Enter API Key", 
            value=st.session_state.openai_api_key,
            type="password",
            key="openai_input_key",
            placeholder="sk-..."
        )
        if st.button("Save API Key", key="save_openai_key", use_container_width=True):
            st.session_state.openai_api_key = key_input.strip()
            st.success("OpenAI API key saved for this session. Re-run to activate GPT-4o responses.")
            st.rerun()

    client = load_openai_client()
    api_available = client is not None

    if not api_available:
        st.markdown("""
        <div style="background: rgba(34,197,94,0.14); border: 1px solid rgba(34,197,94,0.3);
             border-radius: 15px; padding: 1rem; margin-bottom: 1rem;">
            <p style="color: #065f46; margin: 0; font-weight: 700;">
                ⚠️ OpenAI API key not found. Set it above or in .env (OPENAI_API_KEY) for full GPT responses.
            </p>
            <p style="color: #065f46; margin: 0.35rem 0 0 0; font-size:0.9rem;">
                Using lightweight offline Shopi fallback while key is not set.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Shopi Profile Card ────────────────────────────────────────────────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(108,59,255,0.15), rgba(168,85,247,0.1));
         border: 1px solid rgba(130,80,255,0.25); border-radius: 20px; padding: 1.2rem;
         display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
        <div style="font-size: 3.5rem;">🤖</div>
        <div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #1e3a8a;">Arya</div>
            <div style="color: rgba(196,181,253,0.7); font-size: 0.9rem;">AI Shopping Assistant • Age 22</div>
            <div style="margin-top: 0.4rem;">
                <span style="background: #10b981; color: white; border-radius: 15px; padding: 0.2rem 0.7rem;
                     font-size: 0.75rem; font-weight: 700;">● Online</span>
                <span style="color: rgba(196,181,253,0.6); font-size: 0.8rem; margin-left: 0.5rem;">
                    Knows all {count} Trovia products
                </span>
            </div>
        </div>
    </div>
    """.format(count=len(PRODUCTS)), unsafe_allow_html=True)

    # ── Quick Suggestion Chips ─────────────────────────────────────────────────
    st.markdown("""
    <div style="color: rgba(196,181,253,0.7); font-size: 0.85rem; font-weight: 700; margin-bottom: 0.5rem;">
        💡 Quick Questions:
    </div>
    """, unsafe_allow_html=True)

    suggestions = [
        "Best phones under ₹15000",
        "Gift ideas for kids",
        "Compare boAt vs JBL",
        "Best deals today",
        "Budget laptop under ₹50000",
        "Fitness products for beginners"
    ]

    sug_cols = st.columns(3)
    for i, sug in enumerate(suggestions):
        with sug_cols[i % 3]:
            if st.button(f"💬 {sug}", key=f"suggestion_{i}", use_container_width=True):
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                st.session_state.chat_history.append({"role": "user", "content": sug})
                st.session_state["trigger_response"] = True
                st.rerun()

    st.markdown("---")

    # ── Chat History Init ──────────────────────────────────────────────────────
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "shopi_introduced" not in st.session_state:
        st.session_state.shopi_introduced = False

    # Auto-introduce on first load
    if not st.session_state.shopi_introduced:
        st.session_state.chat_history = [
            {"role": "assistant", "content": SHOPI_INTRO}
        ]
        st.session_state.shopi_introduced = True

    # ── Chat Container ────────────────────────────────────────────────────────
    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-user">
                    <div style="font-size: 0.75rem; color: rgba(196,181,253,0.5);
                         font-weight: 700; margin-bottom: 0.3rem;">You</div>
                    <div style="color: #1e3a8a; font-size: 1rem; line-height: 1.5;">
                        {msg["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Format markdown in Shopi's messages
                content = msg["content"]
                # Convert **bold** to HTML
                import re
                content_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
                content_html = content_html.replace('\n', '<br>')

                st.markdown(f"""
                <div class="chat-bot">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.2rem;">�</span>
                        <span style="font-size: 0.75rem; color: rgba(196,181,253,0.5); font-weight: 700;">
                            Arya
                        </span>
                    </div>
                    <div style="color: #1e3a8a; font-size: 1rem; line-height: 1.6;">
                        {content_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # TTS button for last assistant message
                if msg == st.session_state.chat_history[-1] and msg["role"] == "assistant":
                    if st.button("🔊 Listen to Shopi", key="tts_btn", help="Play as audio"):
                        audio_buf = text_to_speech(msg["content"])
                        if audio_buf:
                            st.audio(audio_buf, format="audio/mp3")
                        else:
                            st.info("gTTS not available. Install it with: pip install gtts")

    # ── Chat Input ────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        input_col, btn_col = st.columns([5, 1])
        with input_col:
            user_input = st.text_input(
                "Message",
                placeholder="Ask Shopi anything... e.g. 'Best earbuds under ₹3000'",
                key="chat_input",
                label_visibility="collapsed"
            )
        with btn_col:
            send_btn = st.form_submit_button("Send 🚀", use_container_width=True, type="primary")

    # Handle suggestion trigger
    trigger = st.session_state.pop("trigger_response", False)

    # Process message
    if (send_btn and user_input.strip()) or trigger:
        if send_btn and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

        if api_available:
            with st.spinner("Shopi is thinking... 🤔"):
                # Build messages for API
                api_messages = [{"role": "system", "content": get_arya_system_prompt()}]

                # Include recent history (last 10 messages for context)
                recent_history = st.session_state.chat_history[-10:]
                for msg in recent_history:
                    if msg["role"] in ["user", "assistant"]:
                        api_messages.append({"role": msg["role"], "content": msg["content"]})

                response = get_shopi_response(api_messages, client)
        else:
            # Fallback response without API
            last_user_msg = next(
                (m["content"] for m in reversed(st.session_state.chat_history) if m["role"] == "user"),
                ""
            ).lower()

            # Simple keyword matching fallback
            if any(w in last_user_msg for w in ["phone", "mobile", "iphone", "samsung"]):
                matching = [p for p in PRODUCTS if p["category"] == "Electronics" and "phone" in p["tags"]]
            elif any(w in last_user_msg for w in ["earbuds", "headphone", "audio", "speaker"]):
                matching = [p for p in PRODUCTS if any(t in ["earbuds", "speaker", "audio"] for t in p["tags"])]
            elif any(w in last_user_msg for w in ["book", "read", "novel"]):
                matching = [p for p in PRODUCTS if p["category"] == "Books"]
            elif any(w in last_user_msg for w in ["sport", "cricket", "yoga", "gym", "fitness"]):
                matching = [p for p in PRODUCTS if p["category"] == "Sports"]
            elif any(w in last_user_msg for w in ["fashion", "clothes", "wear", "dress", "kurta", "jeans"]):
                matching = [p for p in PRODUCTS if p["category"] == "Fashion"]
            else:
                matching = sorted(PRODUCTS, key=lambda x: x["rating"], reverse=True)[:4]

            product_recs = "\n".join(
                f"- {p['emoji']} **{p['name']}** — ₹{p['price']:,} (⭐{p['rating']})"
                for p in matching[:4]
            )
            response = (
                f"Hi! I'm Arya 🧠 (running in offline mode — add your OpenAI API key for full AI responses!)\n\n"
                f"Based on your query, here are some recommendations:\n\n{product_recs}\n\n"
                f"Want to know more about any of these? Just ask! 😊"
            )

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    # ── Product Description from Image ─────────────────────────────────────────
    with st.expander("📷 Generate Product Description from Image", expanded=False):
        uploaded_image = st.file_uploader(
            "Upload product image (JPG/PNG/WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            key="image_upload"
        )
        client_name = st.text_input("Client/Project", value="General", key="client_name")
        tone = st.selectbox("Tone", ["Professional", "Friendly", "Sales", "Technical"], index=1, key="description_tone")
        length = st.selectbox("Length", ["Short", "Medium", "Long"], index=1, key="description_length")

        if st.button("Generate description", key="generate_description", use_container_width=True):
            if not uploaded_image:
                st.warning("Please upload an image first.")
            else:
                if api_available:
                    prompt = (
                        "You are Arya, a confident e-commerce copy expert."
                        " Create a product description for a product image provided, "
                        f"client={client_name}, tone={tone}, length={length}. "
                        "Use concise bullet points, include benefits, features, and call to action. "
                        "Assume this is a consumer item sold in India and international marketplaces."
                    )

                    try:
                        image_bytes = uploaded_image.read()
                        # note: openai image-to-text not used in this fallback data-only mode.
                        messages = [
                            {"role": "system", "content": get_arya_system_prompt()},
                            {"role": "user", "content": prompt}
                        ]
                        response = get_shopi_response(messages, load_openai_client())
                        result_text = response
                    except Exception as e:
                        result_text = (
                            "Could not generate from API. "
                            f"Fallback description generated, error: {e}"
                        )
                else:
                    result_text = (
                        f"Arya Product Description for '{client_name}' (offline):\n"
                        f"- Tone: {tone}, Length: {length}\n"
                        "- A crisp product overview that reads like a premium e-commerce listing.\n"
                        "- Include price-friendly and premium position variations depending on target audience.\n"
                        "- Highlight top features, use-cases, and customer benefit statements.\n"
                        "- Add call-to-action: 'Buy now and elevate your style/utility'."
                    )

                st.markdown("### Generated Product Description", unsafe_allow_html=True)
                st.code(result_text)
                st.download_button(
                    "Download description",
                    result_text,
                    file_name="arya_product_description.txt",
                    mime="text/plain"
                )

    # ── Clear Chat ────────────────────────────────────────────────────────────
    if len(st.session_state.chat_history) > 2:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.chat_history = [
                    {"role": "assistant", "content": SHOPI_INTRO}
                ]
                st.rerun()

    # ── Featured Products in Sidebar ──────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #6c3bff, #a855f7);
             border-radius: 15px; padding: 1rem; text-align: center; margin-bottom: 1rem;">
            <h3 style="color: white; margin: 0; font-weight: 800;">🤖 Shopi Recommends</h3>
        </div>
        """, unsafe_allow_html=True)

        top_products = sorted(PRODUCTS, key=lambda x: x["rating"], reverse=True)[:5]
        for p in top_products:
            stars = get_stars(p["rating"])
            st.markdown(f"""
            <div style="background: rgba(108,59,255,0.1); border: 1px solid rgba(130,80,255,0.2);
                 border-radius: 15px; padding: 0.8rem; margin-bottom: 0.8rem; text-align: center;">
                <div style="font-size: 2rem;">{p['emoji']}</div>
                <div style="color: #1e3a8a; font-weight: 700; font-size: 0.9rem;">{p['name']}</div>
                <div style="color: #fbbf24; font-size: 0.85rem;">{stars}</div>
                <div style="color: #a78bfa; font-weight: 800;">&#8377;{p['price']:,}</div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(page_title="Trovia AI Assistant", layout="wide")
    show_ai_assistant()
