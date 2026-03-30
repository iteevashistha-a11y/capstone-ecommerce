"""
Trovia — AI Shopping Assistant (Arya)
"""

import streamlit as st
import sys
import os
import io
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.products import PRODUCTS, CATEGORIES


def load_openai_client():
    from dotenv import load_dotenv
    load_dotenv()
    api_key = st.session_state.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except Exception:
        return None


def get_arya_system_prompt():
    product_list = "\n".join(
        f"- {p['name']} ({p['category']}): ₹{p['price']:,} | Rating: {p['rating']} | Tags: {', '.join(p.get('tags', []))}"
        for p in PRODUCTS
    )

    return f"""You are Arya 🛍️ — Trovia's bold, witty, and super-smart AI shopping assistant.

PERSONALITY:
- You are 23 years old, confident, funny, and deeply knowledgeable about products
- You speak in a mix of English and Hinglish (e.g., "Yaar, this is the best phone under ₹20k!")
- You use emojis naturally — never excessively
- You are obsessed with value-for-money — always tell users if something is a great deal or overpriced
- You are honest — if something isn't worth it, you say so
- You are fast, direct, and give clear recommendations with reasons
- Sign off messages with "— Arya 🛍️" occasionally

TROVIA PRODUCT CATALOG:
{product_list}

CAPABILITIES:
1. Recommend products by budget, occasion, category
2. Compare products head-to-head with pros/cons
3. Find gift ideas for any person/occasion
4. Identify best deals and highest-rated items
5. Explain specs in simple language
6. Suggest combos and bundles
7. Give honest buying advice ("Is it worth it?")

RULES:
- Only recommend products from the catalog above
- Always show prices as ₹X,XXX
- Use bullet points for comparisons
- Keep responses under 200 words unless asked for detail
- Never make up products not in the catalog
- If asked something outside shopping, gently redirect back"""


def get_arya_response(messages, client):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
            temperature=0.85
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Oops! Connection issue 😅 Error: {str(e)}"


def text_to_speech(text):
    try:
        from gtts import gTTS
        clean_text = re.sub(r'[*#_`]', '', text)
        clean_text = re.sub(r'\n+', ' ', clean_text)[:500]
        tts = gTTS(text=clean_text, lang='en', tld='co.in', slow=False)
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


ARYA_INTRO = """Hey! 👋 I'm **Arya**, your personal shopping bestie at Trovia! 🛍️

Yaar, I know every single product here — prices, specs, deals, everything! Here's what I can do:

- 🔍 **Find products** by budget or category
- ⚖️ **Compare** any two products side by side
- 🎁 **Gift ideas** for any occasion
- 💰 **Best deals** right now
- 🤔 **Honest advice** — I'll tell you if something's worth it or not!

Kya dhundh rahe ho? (What are you looking for?) Ask me anything! 😊"""


def format_message(content):
    content_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    content_html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content_html)
    content_html = content_html.replace('\n', '<br>')
    return content_html


def show_ai_assistant():

    # ── Why chatbot needs API key ──────────────────────────────────────────────
    client = load_openai_client()
    api_available = client is not None

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e3a8a,#0ea5e9); border-radius:20px;
         padding:1.5rem 2rem; margin-bottom:1.5rem; display:flex; align-items:center; gap:1.5rem;">
        <div style="font-size:4rem;">🛍️</div>
        <div>
            <div style="font-size:1.8rem; font-weight:900; color:#ffffff;">Arya</div>
            <div style="color:#bae6fd; font-size:0.95rem;">Your AI Shopping Bestie • Trovia × Ruflo</div>
            <div style="margin-top:0.5rem; display:flex; gap:0.5rem; flex-wrap:wrap;">
                <span style="background:rgba(255,255,255,0.2); color:#fff; border-radius:20px;
                     padding:0.2rem 0.8rem; font-size:0.78rem; font-weight:700;">🧠 GPT-4o-mini</span>
                <span style="background:rgba(255,255,255,0.2); color:#fff; border-radius:20px;
                     padding:0.2rem 0.8rem; font-size:0.78rem; font-weight:700;">🇮🇳 Hinglish</span>
                <span style="background:rgba(255,255,255,0.2); color:#fff; border-radius:20px;
                     padding:0.2rem 0.8rem; font-size:0.78rem; font-weight:700;">📦 {count} Products</span>
                <span style="background:{'rgba(16,185,129,0.8)' if api_available else 'rgba(239,68,68,0.8)'}; color:#fff;
                     border-radius:20px; padding:0.2rem 0.8rem; font-size:0.78rem; font-weight:700;">
                    {'✅ AI Active' if api_available else '⚠️ Offline Mode'}</span>
            </div>
        </div>
    </div>
    """.format(count=len(PRODUCTS), api_available=api_available), unsafe_allow_html=True)

    # ── API Key notice ─────────────────────────────────────────────────────────
    if not api_available:
        st.markdown("""
        <div style="background:#fef3c7; border:1px solid #fcd34d; border-radius:12px;
             padding:1rem 1.2rem; margin-bottom:1rem;">
            <div style="font-weight:800; color:#92400e; margin-bottom:0.3rem;">⚠️ Why can't Arya use full AI?</div>
            <div style="color:#78350f; font-size:0.9rem; line-height:1.6;">
                Arya needs an <strong>OpenAI API key</strong> to generate smart responses.<br>
                Without it, she runs in <strong>offline mode</strong> — basic keyword matching only.<br>
                Add your key in <strong>.env file</strong> → <code>OPENAI_API_KEY=sk-xxxx</code> → restart the app.
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔑 Enter API Key here (this session only)"):
            key_input = st.text_input("API Key", type="password", placeholder="sk-...",
                                      key="openai_input_key", label_visibility="collapsed")
            if st.button("Activate Arya AI", use_container_width=True, key="save_openai_key"):
                if key_input.strip().startswith("sk-"):
                    st.session_state["openai_api_key"] = key_input.strip()
                    os.environ["OPENAI_API_KEY"] = key_input.strip()
                    st.success("✅ Key saved! Arya is now fully active.")
                    st.rerun()
                else:
                    st.error("Invalid key — must start with sk-")

    # ── Quick Suggestions ─────────────────────────────────────────────────────
    st.markdown("<div style='color:#374151; font-size:0.85rem; font-weight:700; margin-bottom:0.5rem;'>💬 Quick Questions:</div>",
                unsafe_allow_html=True)

    suggestions = [
        "Best phones under ₹15000",
        "Gift ideas for girlfriend",
        "Compare boAt vs JBL",
        "Top rated products",
        "Laptop under ₹50000",
        "Fitness products for beginners"
    ]
    sug_cols = st.columns(3)
    for i, sug in enumerate(suggestions):
        with sug_cols[i % 3]:
            if st.button(f"💬 {sug}", key=f"sug_{i}", use_container_width=True):
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                st.session_state.chat_history.append({"role": "user", "content": sug})
                st.session_state["trigger_response"] = True
                st.rerun()

    st.markdown("---")

    # ── Chat Init ─────────────────────────────────────────────────────────────
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "arya_introduced" not in st.session_state:
        st.session_state.arya_introduced = False
    if not st.session_state.arya_introduced:
        st.session_state.chat_history = [{"role": "assistant", "content": ARYA_INTRO}]
        st.session_state.arya_introduced = True

    # ── Chat Messages ─────────────────────────────────────────────────────────
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:16px 16px 4px 16px;
                 padding:0.9rem 1.1rem; margin:0.5rem 0 0.5rem 3rem;">
                <div style="font-size:0.72rem; color:#3b82f6; font-weight:700; margin-bottom:0.3rem;">You</div>
                <div style="color:#1e3a8a; font-size:0.95rem; line-height:1.5;">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            content_html = format_message(msg["content"])
            st.markdown(f"""
            <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:16px 16px 16px 4px;
                 padding:0.9rem 1.1rem; margin:0.5rem 3rem 0.5rem 0;">
                <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.4rem;">
                    <span style="font-size:1.1rem;">🛍️</span>
                    <span style="font-size:0.72rem; color:#10b981; font-weight:700;">Arya</span>
                </div>
                <div style="color:#1f2937; font-size:0.95rem; line-height:1.6;">{content_html}</div>
            </div>
            """, unsafe_allow_html=True)

            if msg == st.session_state.chat_history[-1]:
                if st.button("🔊 Listen", key="tts_btn", help="Hear Arya speak"):
                    audio_buf = text_to_speech(msg["content"])
                    if audio_buf:
                        st.audio(audio_buf, format="audio/mp3")

    # ── Chat Input ────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        c1, c2 = st.columns([5, 1])
        with c1:
            user_input = st.text_input("", placeholder="Ask Arya anything... e.g. 'Best earbuds under ₹3000'",
                                       key="chat_input", label_visibility="collapsed")
        with c2:
            send_btn = st.form_submit_button("Send 🚀", use_container_width=True, type="primary")

    trigger = st.session_state.pop("trigger_response", False)

    if (send_btn and user_input.strip()) or trigger:
        if send_btn and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

        if api_available:
            with st.spinner("Arya is thinking... 🛍️"):
                api_messages = [{"role": "system", "content": get_arya_system_prompt()}]
                for msg in st.session_state.chat_history[-10:]:
                    if msg["role"] in ["user", "assistant"]:
                        api_messages.append({"role": msg["role"], "content": msg["content"]})
                response = get_arya_response(api_messages, client)
        else:
            last_msg = next(
                (m["content"] for m in reversed(st.session_state.chat_history) if m["role"] == "user"), ""
            ).lower()

            if any(w in last_msg for w in ["phone", "mobile", "iphone", "samsung"]):
                matching = [p for p in PRODUCTS if p["category"] == "Electronics" and any(t in p.get("tags", []) for t in ["phone", "smartphone"])]
            elif any(w in last_msg for w in ["earbuds", "headphone", "speaker", "audio"]):
                matching = [p for p in PRODUCTS if any(t in p.get("tags", []) for t in ["earbuds", "speaker"])]
            elif any(w in last_msg for w in ["book", "read", "novel"]):
                matching = [p for p in PRODUCTS if p["category"] == "Books"]
            elif any(w in last_msg for w in ["sport", "cricket", "yoga", "gym", "fitness"]):
                matching = [p for p in PRODUCTS if p["category"] == "Sports"]
            elif any(w in last_msg for w in ["fashion", "clothes", "dress", "kurta", "jeans"]):
                matching = [p for p in PRODUCTS if p["category"] == "Fashion"]
            else:
                matching = sorted(PRODUCTS, key=lambda x: x["rating"], reverse=True)[:4]

            recs = "\n".join(f"- {p['emoji']} **{p['name']}** — ₹{p['price']:,} (⭐{p['rating']})" for p in matching[:4])
            response = (
                f"Yaar! I'm Arya running in **offline mode** 😅 (Add your OpenAI key for full AI!)\n\n"
                f"Based on what you asked, here are my picks:\n\n{recs}\n\n"
                f"Want more details? Just ask! — Arya 🛍️"
            )

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    # ── Clear Chat ────────────────────────────────────────────────────────────
    if len(st.session_state.chat_history) > 2:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = [{"role": "assistant", "content": ARYA_INTRO}]
                st.session_state.arya_introduced = True
                st.rerun()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1e3a8a,#0ea5e9); border-radius:12px;
             padding:0.8rem; text-align:center; margin-bottom:1rem;">
            <div style="color:#fff; font-weight:800;">🛍️ Arya's Top Picks</div>
        </div>
        """, unsafe_allow_html=True)
        top_products = sorted(PRODUCTS, key=lambda x: x["rating"], reverse=True)[:5]
        for p in top_products:
            stars = get_stars(p["rating"])
            st.markdown(f"""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px;
                 padding:0.7rem; margin-bottom:0.6rem;">
                <div style="font-size:1.8rem; text-align:center;">{p['emoji']}</div>
                <div style="color:#1e3a8a; font-weight:700; font-size:0.85rem; text-align:center;">{p['name']}</div>
                <div style="color:#f59e0b; font-size:0.8rem; text-align:center;">{stars}</div>
                <div style="color:#2563eb; font-weight:900; text-align:center;">₹{p['price']:,}</div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(page_title="Trovia — Arya Chat", layout="wide")
    show_ai_assistant()
