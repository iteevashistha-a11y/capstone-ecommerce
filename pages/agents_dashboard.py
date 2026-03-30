"""
Trovia — AI Agents Dashboard (Ruflo-inspired Swarm)
"""

import streamlit as st
import sys, os, sqlite3, json
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.trovia_agents import TroviaSwarm
from agents.market_agent import get_market_analysis, get_growth_drivers
from agents.financial_agent import get_financial_projections, get_unit_economics, get_profitability_timeline
from agents.strategy_agent import get_gtm_strategy, get_pricing_strategy, get_success_metrics
from agents.technical_agent import get_technology_stack, get_implementation_phases, get_performance_benchmarks
from agents.usecase_agent import get_use_cases, get_solution_types
from data.products import PRODUCTS, CATEGORIES


def get_swarm() -> TroviaSwarm:
    if "trovia_swarm" not in st.session_state:
        st.session_state.trovia_swarm = TroviaSwarm()
    return st.session_state.trovia_swarm


def get_cart_items(user_id: int) -> list[dict]:
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shopiq.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT c.product_id, c.quantity
        FROM cart c WHERE c.user_id = ?
    """, (user_id,))
    rows = c.fetchall()
    conn.close()
    cart = []
    for pid, qty in rows:
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if product:
            cart.append({**product, "quantity": qty})
    return cart


def render_agent_card(name: str, icon: str, capabilities: list[str], color: str, desc: str):
    caps = " • ".join(capabilities)
    st.markdown(f"""
    <div style="background: {color}; border-radius: 16px; padding: 1.2rem;
         border: 1px solid rgba(255,255,255,0.1); margin-bottom: 0.5rem;">
        <div style="font-size: 2rem; margin-bottom: 0.4rem;">{icon}</div>
        <div style="font-weight: 800; font-size: 1.1rem; color: #1e3a8a;">{name}</div>
        <div style="font-size: 0.8rem; color: #475569; margin: 0.3rem 0;">{caps}</div>
        <div style="font-size: 0.88rem; color: #334155;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


def show_agents_dashboard():
    swarm = get_swarm()
    user = st.session_state.get("user")
    cart_items = get_cart_items(user["id"]) if user else []
    cart_ids = [item["id"] for item in cart_items]

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a, #0ea5e9);
         border-radius: 20px; padding: 1.8rem; margin-bottom: 1.5rem; text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🤖</div>
        <div style="font-size: 2rem; font-weight: 900; color: #fff;">Trovia AI Swarm</div>
        <div style="color: #bae6fd; font-size: 1rem; margin-top: 0.3rem;">
            Ruflo-inspired multi-agent intelligence • 3 specialized agents running in parallel
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Swarm Status ──────────────────────────────────────────────────────────
    status = swarm.status()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Agents Active", 8)
    c2.metric("Total Runs", status["runs"])
    c3.metric("Topology", status["topology"].title())
    c4.metric("Inspired By", "Ruflo v3.5")

    st.markdown("---")

    # ── Agent Cards ────────────────────────────────────────────────────────────
    st.markdown("### 🧩 Shopping Agents")
    col1, col2, col3 = st.columns(3)
    with col1:
        render_agent_card(
            "ProductSearchAgent", "🔍",
            ["semantic-search", "filter", "ranking"],
            "linear-gradient(135deg, #dbeafe, #eff6ff)",
            "Natural-language search across all products. Scores by name, tags, category, brand & description."
        )
    with col2:
        render_agent_card(
            "RecommendationAgent", "💡",
            ["personalization", "cross-sell", "trending"],
            "linear-gradient(135deg, #dcfce7, #f0fdf4)",
            "Analyses your cart to suggest related products using category affinity + rating scoring."
        )
    with col3:
        render_agent_card(
            "PriceOptimizerAgent", "💰",
            ["deal-detection", "coupon-matching", "budget-fit"],
            "linear-gradient(135deg, #fef9c3, #fefce8)",
            "Evaluates your cart, finds best coupons, checks budget and scores each item's value."
        )

    st.markdown("### 🧠 Business Intelligence Agents")
    b1, b2, b3 = st.columns(3)
    with b1:
        render_agent_card(
            "MarketAnalysisAgent", "📊",
            ["TAM/SAM/SOM", "India vs Global", "growth-drivers"],
            "linear-gradient(135deg, #ede9fe, #f5f3ff)",
            "Analyses global e-commerce market opportunity, India vs International segmentation, and growth drivers."
        )
    with b2:
        render_agent_card(
            "FinancialAgent", "📈",
            ["revenue-projections", "unit-economics", "profitability"],
            "linear-gradient(135deg, #fce7f3, #fdf2f8)",
            "Models 5-year revenue projections, LTV:CAC ratios, and path to profitability across markets."
        )
    with b3:
        render_agent_card(
            "StrategyAgent", "🎯",
            ["GTM-phases", "pricing-tiers", "partnerships"],
            "linear-gradient(135deg, #ffedd5, #fff7ed)",
            "Defines go-to-market phases, customer acquisition strategy, pricing tiers and success metrics."
        )

    b4, b5, _ = st.columns(3)
    with b4:
        render_agent_card(
            "TechnicalAgent", "⚙️",
            ["tech-stack", "roadmap", "benchmarks"],
            "linear-gradient(135deg, #d1fae5, #ecfdf5)",
            "Designs technology architecture, phased implementation roadmap and performance benchmarks."
        )
    with b5:
        render_agent_card(
            "UseCasesAgent", "🎪",
            ["Amazon", "Myntra", "Enterprise"],
            "linear-gradient(135deg, #fef3c7, #fffbeb)",
            "Detailed use-case scenarios for Amazon sellers, Myntra, luxury brands, dropshipping and enterprise."
        )

    st.markdown("---")

    # ── Tabs for each agent ────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "🔍 Smart Search", "💡 Recommendations", "💰 Price Optimizer", "⚡ Full Swarm Run",
        "📊 Market Analysis", "📈 Financial", "🎯 Strategy", "⚙️ Technical", "🎪 Use Cases"
    ])

    # ── Tab 1: Product Search Agent ───────────────────────────────────────────
    with tab1:
        st.markdown("#### 🔍 ProductSearchAgent — Natural Language Search")
        st.caption("Type anything: *'budget phones under 20000'*, *'running shoes nike'*, *'4k tv samsung'*")

        col_q, col_f = st.columns([3, 1])
        with col_q:
            query = st.text_input("Search query", placeholder="e.g. wireless headphones under 5000",
                                  key="agent_search_query")
        with col_f:
            max_price = st.number_input("Max price (₹)", min_value=0, value=0, step=500,
                                        key="agent_max_price")

        col_cat, col_rat = st.columns(2)
        with col_cat:
            cat_filter = st.selectbox("Category", ["All"] + list(CATEGORIES.keys()), key="agent_cat")
        with col_rat:
            min_rating = st.slider("Min rating", 0.0, 5.0, 0.0, 0.5, key="agent_min_rating")

        if st.button("🚀 Run Search Agent", key="run_search_agent", use_container_width=True):
            if not query.strip():
                st.warning("Enter a search query.")
            else:
                filters = {}
                if max_price > 0:
                    filters["max_price"] = max_price
                if cat_filter != "All":
                    filters["category"] = cat_filter
                if min_rating > 0:
                    filters["min_rating"] = min_rating

                with st.spinner("Agent running..."):
                    result = swarm.search(query, filters)

                if result.status == "empty":
                    st.info(result.message)
                elif result.status == "success":
                    st.success(f"✅ {result.message} • `{result.latency_ms:.1f}ms`")
                    cols = st.columns(3)
                    for i, product in enumerate(result.data):
                        with cols[i % 3]:
                            st.markdown(f"""
                            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:12px;
                                 padding:1rem; margin-bottom:0.8rem;">
                                <div style="font-size:2rem; text-align:center">{product['emoji']}</div>
                                <div style="font-weight:700; color:#1e3a8a; font-size:0.95rem;">{product['name']}</div>
                                <div style="color:#475569; font-size:0.8rem;">{product['category']}</div>
                                <div style="color:#0ea5e9; font-weight:800; font-size:1rem;">₹{product['price']:,}</div>
                                <div style="font-size:0.8rem; color:#64748b;">⭐ {product['rating']} | Score: {product['_score']}</div>
                            </div>
                            """, unsafe_allow_html=True)

    # ── Tab 2: Recommendation Agent ────────────────────────────────────────────
    with tab2:
        st.markdown("#### 💡 RecommendationAgent — Personalised Picks")

        if not cart_items:
            st.info("Your cart is empty. Add some products to get personalized recommendations!")
            st.caption("Showing top-rated picks instead:")
            budget_rec = st.number_input("Budget filter (₹, 0 = none)", min_value=0, value=0, step=1000,
                                         key="rec_budget")
        else:
            st.markdown(f"**Based on your cart:** {', '.join(i['emoji'] + ' ' + i['name'] for i in cart_items[:3])}")
            budget_rec = st.number_input("Max budget per item (₹, 0 = no limit)", min_value=0, value=0, step=1000,
                                         key="rec_budget2")

        if st.button("💡 Run Recommendation Agent", key="run_rec_agent", use_container_width=True):
            with st.spinner("Agent analysing your preferences..."):
                result = swarm.recommend(
                    cart_ids,
                    budget=budget_rec if budget_rec > 0 else None
                )

            if result.status == "success":
                st.success(f"✅ {result.message} • `{result.latency_ms:.1f}ms`")
                cols = st.columns(4)
                for i, product in enumerate(result.data):
                    with cols[i % 4]:
                        reason = product.get("_reason", "")
                        st.markdown(f"""
                        <div style="background:#fff; border:1px solid #e2e8f0; border-radius:12px;
                             padding:0.9rem; margin-bottom:0.8rem;">
                            <div style="font-size:1.8rem; text-align:center">{product['emoji']}</div>
                            <div style="font-weight:700; color:#1e3a8a; font-size:0.88rem;">{product['name']}</div>
                            <div style="color:#0ea5e9; font-weight:800;">₹{product['price']:,}</div>
                            <div style="font-size:0.75rem; color:#64748b;">⭐ {product['rating']}</div>
                            <div style="font-size:0.72rem; color:#7c3aed; margin-top:0.3rem;">{reason}</div>
                        </div>
                        """, unsafe_allow_html=True)

    # ── Tab 3: Price Optimizer Agent ──────────────────────────────────────────
    with tab3:
        st.markdown("#### 💰 PriceOptimizerAgent — Smart Pricing Analysis")

        if not cart_items:
            st.info("Add items to your cart to run price optimization.")
        else:
            total_items = sum(i.get("quantity", 1) for i in cart_items)
            subtotal = sum(i["price"] * i.get("quantity", 1) for i in cart_items)
            st.markdown(f"**Cart:** {total_items} item(s) · Subtotal: ₹{subtotal:,}")

            col_c, col_b = st.columns(2)
            with col_c:
                coupon = st.text_input("Coupon code", placeholder="e.g. TROVIA20", key="opt_coupon")
            with col_b:
                budget = st.number_input("Your budget (₹, 0 = no limit)", min_value=0, value=0, step=500,
                                         key="opt_budget")

            if st.button("💰 Run Price Optimizer", key="run_price_agent", use_container_width=True):
                with st.spinner("Optimizing pricing..."):
                    result = swarm.optimize(cart_items, coupon, budget if budget > 0 else None)

                if result.status == "success":
                    d = result.data
                    st.success(f"✅ {result.message} • `{result.latency_ms:.1f}ms`")

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Subtotal", f"₹{d['subtotal']:,.0f}")
                    m2.metric("Discount", f"₹{d['total_savings']:,.0f}", delta=f"-{d['total_savings']:,.0f}")
                    m3.metric("Final Price", f"₹{d['final_price']:,.0f}")
                    savings_pct = (d['total_savings'] / d['subtotal'] * 100) if d['subtotal'] > 0 else 0
                    m4.metric("Savings %", f"{savings_pct:.1f}%")

                    st.markdown(f"**{d['savings_tip']}**")

                    # Coupon info
                    if d["coupon"]["valid"]:
                        st.success(f"✅ Coupon **{d['coupon']['code']}** applied: {d['coupon']['description']}")
                    elif d["coupon"]["code"]:
                        st.error(f"❌ Coupon `{d['coupon']['code']}` is invalid.")

                    if d["best_coupon_available"].get("code") and not d["coupon"]["valid"]:
                        bc = d["best_coupon_available"]
                        st.info(f"💡 Best coupon: **{bc['code']}** — saves ₹{bc['savings']:,.0f} ({bc['description']})")

                    # Item value scores
                    st.markdown("**Item Value Scores:**")
                    for item in d["item_deals"]:
                        delta_text = f"{item['vs_category_avg']:+.1f}% vs category avg"
                        color = "#16a34a" if item['vs_category_avg'] >= 0 else "#dc2626"
                        st.markdown(f"""
                        <div style="display:flex; justify-content:space-between; padding:0.5rem;
                             background:#f8fafc; border-radius:8px; margin-bottom:0.3rem;">
                            <span style="font-weight:600">{item['name']}</span>
                            <span>Value Score: <b>{item['value_score']}/5</b></span>
                            <span style="color:{color}">{delta_text}</span>
                        </div>
                        """, unsafe_allow_html=True)

    # ── Tab 4: Full Swarm Run ─────────────────────────────────────────────────
    with tab4:
        st.markdown("#### ⚡ Full Swarm — All 3 Agents in One Shot")
        st.caption("Ruflo-style: Queen orchestrator runs all agents, aggregates results")

        fs_query = st.text_input("What are you looking for?", placeholder="e.g. running gear",
                                 key="swarm_query")
        fs_coupon = st.text_input("Coupon code (optional)", key="swarm_coupon")
        fs_budget = st.number_input("Budget (₹, 0 = no limit)", min_value=0, value=0, key="swarm_budget")

        if st.button("⚡ Launch Full Swarm", key="run_full_swarm", use_container_width=True):
            with st.spinner("🐝 Swarm running — 3 agents in parallel..."):
                output = swarm.full_analysis(
                    query=fs_query,
                    cart_ids=cart_ids,
                    cart_items=cart_items,
                    coupon=fs_coupon,
                    budget=fs_budget if fs_budget > 0 else None
                )

            st.success(f"⚡ Swarm complete in `{output['total_latency_ms']:.1f}ms` — {output['agents_run']} agents ran")

            r1, r2, r3 = st.columns(3)

            with r1:
                sr = output["search"]
                if sr:
                    st.markdown(f"**🔍 Search** — {sr.message}")
                    if sr.status == "success":
                        for p in sr.data[:3]:
                            st.markdown(f"- {p['emoji']} **{p['name']}** ₹{p['price']:,}")
                else:
                    st.markdown("**🔍 Search** — No query provided")

            with r2:
                rr = output["recommendations"]
                st.markdown(f"**💡 Recommendations** — {rr.message}")
                if rr.status == "success":
                    for p in rr.data[:3]:
                        st.markdown(f"- {p['emoji']} **{p['name']}** ₹{p['price']:,}")

            with r3:
                pr = output["pricing"]
                st.markdown(f"**💰 Pricing** — {pr.message}")
                if pr.status == "success":
                    d = pr.data
                    st.markdown(f"- Subtotal: ₹{d['subtotal']:,.0f}")
                    st.markdown(f"- Final: ₹{d['final_price']:,.0f}")
                    st.markdown(f"- {d['savings_tip']}")

            with st.expander("📋 Raw Swarm Log"):
                log = swarm._run_log[-6:]
                for entry in log:
                    st.json(entry)

    # ── Tab 5: Market Analysis Agent ─────────────────────────────────────────
    with tab5:
        st.markdown("#### 📊 MarketAnalysisAgent — Global Market Opportunity")
        market = get_market_analysis()

        c1, c2, c3 = st.columns(3)
        c1.metric("Global TAM", f"${market['global']['tam']['value']}B", market['global']['tam']['range'])
        c2.metric("Global SAM", f"${market['global']['sam']['value']}B", market['global']['sam']['range'])
        c3.metric("Year 5 SOM", f"${market['global']['som']['value']*1000:.0f}M", market['global']['som']['range'])

        st.markdown("---")
        col_i, col_int = st.columns(2)
        with col_i:
            st.markdown("**🇮🇳 India**")
            st.metric("TAM", market['india']['tam']['range'])
            st.metric("Growth Rate", market['india']['growth_rate'])
            st.metric("E-Commerce Size", f"${market['india']['e_commerce_size']}B")
            st.metric("Sellers", f"{market['india']['sellers']:,}")
        with col_int:
            st.markdown("**🌍 International**")
            st.metric("TAM", market['international']['tam']['range'])
            st.metric("Growth Rate", market['international']['growth_rate'])
            st.metric("E-Commerce Size", f"${market['international']['e_commerce_size']:,}T")
            st.metric("Sellers", f"{market['international']['sellers']:,}")

        st.markdown("##### 📈 Key Growth Drivers")
        for d in get_growth_drivers():
            with st.expander(d['name']):
                st.markdown(f"🇮🇳 **India:** {d['india_impact']}")
                st.markdown(f"🌍 **International:** {d['international_impact']}")
                st.caption(d['driver'])

    # ── Tab 6: Financial Agent ────────────────────────────────────────────────
    with tab6:
        st.markdown("#### 📈 FinancialAgent — Revenue Projections & Unit Economics")
        projections = get_financial_projections()

        scenario = st.radio("Scenario", ["conservative", "optimistic"], horizontal=True, key="fin_scenario")
        years = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
        global_vals = [projections['global'][scenario][f'year_{i}'] for i in range(1, 6)]
        india_vals  = [projections['india'][scenario][f'year_{i}'] for i in range(1, 6)]
        intl_vals   = [projections['international'][scenario][f'year_{i}'] for i in range(1, 6)]

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Global', x=years, y=global_vals, marker_color='#0ea5e9'))
        fig.add_trace(go.Bar(name='India', x=years, y=india_vals, marker_color='#f97316'))
        fig.add_trace(go.Bar(name='International', x=years, y=intl_vals, marker_color='#8b5cf6'))
        fig.update_layout(title="Revenue Projections ($M)", barmode='group', height=350,
                          plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### Unit Economics")
        econ = get_unit_economics()
        c1, c2, c3 = st.columns(3)
        c1.metric("Avg CAC (Global)", f"${econ['global']['customer_acquisition_cost']['average']}")
        c2.metric("Avg LTV (Global)", f"${econ['global']['lifetime_value']['average']:,}")
        c3.metric("LTV:CAC Target", econ['global']['ltv_cac_ratio']['target'])

        st.markdown("##### Path to Profitability (Global)")
        for yr, data in get_profitability_timeline()['global'].items():
            ca, cb, cc = st.columns([1, 3, 2])
            ca.markdown(f"**{yr.replace('_', ' ').title()}**")
            cb.markdown(f"Revenue: **${data['revenue']:,}** | Costs: ${data['costs']:,}")
            icon = "🟢" if data['profit'] >= 0 else "🔴"
            cc.markdown(f"{icon} {data['status']}")

    # ── Tab 7: Strategy Agent ─────────────────────────────────────────────────
    with tab7:
        st.markdown("#### 🎯 StrategyAgent — Go-to-Market Strategy")
        for phase_key, phase in get_gtm_strategy().items():
            label = phase_key.replace('_', ' ').title()
            with st.expander(f"📅 {phase.get('duration', '')} — {label}"):
                c1, c2 = st.columns(2)
                with c1:
                    target = phase.get('target_customer') or ', '.join(phase.get('new_targets', []))
                    st.markdown(f"**Target:** {target}")
                    if 'TAM' in phase:
                        st.markdown(f"**TAM:** {phase['TAM']}")
                    st.markdown(f"**Budget:** ${phase.get('budget', 0):,}")
                with c2:
                    channels = phase.get('distribution_channels', [])
                    if channels:
                        st.markdown("**Channels:**")
                        for ch in channels:
                            st.markdown(f"- {ch}")

        st.markdown("##### 💵 Pricing Tiers")
        pcols = st.columns(4)
        for i, (_, tier) in enumerate(get_pricing_strategy().items()):
            with pcols[i]:
                st.markdown(f"""
                <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;
                     padding:1rem;text-align:center;margin-bottom:0.5rem;">
                    <div style="font-weight:800;color:#1e3a8a;">{tier['name']}</div>
                    <div style="font-size:1.1rem;color:#0ea5e9;font-weight:700;">{tier['monthly_cost']}</div>
                    <div style="font-size:0.78rem;color:#64748b;">{tier.get('descriptions_per_month','Unlimited')} desc/mo</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("##### 📊 Success Metrics")
        for cat, vals in get_success_metrics().items():
            with st.expander(cat.replace('_', ' ').title()):
                for k, v in vals.items():
                    st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")

    # ── Tab 8: Technical Agent ────────────────────────────────────────────────
    with tab8:
        st.markdown("#### ⚙️ TechnicalAgent — Architecture & Implementation")

        st.markdown("##### 🛠️ Technology Stack")
        stack = get_technology_stack()
        tcols = st.columns(len(stack))
        for i, (layer, tools) in enumerate(stack.items()):
            with tcols[i]:
                st.markdown(f"**{layer.upper()}**")
                for k, v in tools.items():
                    if isinstance(v, list):
                        st.caption(f"{k}: {', '.join(v[:2])}")
                    else:
                        st.caption(f"{k}: {v}")

        st.markdown("##### 🗺️ Implementation Phases")
        for phase_key, phase in get_implementation_phases().items():
            with st.expander(f"{phase_key.replace('_',' ').title()} — {phase['duration']} | {phase['budget']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Deliverables:**")
                    for d in phase['deliverables']:
                        st.markdown(f"- {d}")
                with c2:
                    st.markdown("**Target Metrics:**")
                    for k, v in phase['metrics'].items():
                        st.markdown(f"- {k.replace('_',' ')}: {v}")

        st.markdown("##### 🚀 Performance Benchmarks")
        benchmarks = get_performance_benchmarks()
        bcols = st.columns(len(benchmarks))
        for i, (cat, vals) in enumerate(benchmarks.items()):
            with bcols[i]:
                st.markdown(f"**{cat.replace('_',' ').title()}**")
                for k, v in vals.items():
                    st.caption(f"{k.replace('_',' ')}: {v}")

    # ── Tab 9: Use Cases Agent ────────────────────────────────────────────────
    with tab9:
        st.markdown("#### 🎪 UseCasesAgent — Customer Scenarios")
        for uc_key, uc in get_use_cases().items():
            with st.expander(f"📦 {uc['name']}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("**Problem:**")
                    for k, v in uc['problem'].items():
                        st.caption(f"{k.replace('_',' ')}: {v}")
                with c2:
                    st.markdown("**Solution Features:**")
                    for f in uc['solution_features']:
                        st.markdown(f"- {f}")
                with c3:
                    st.markdown("**Financial Impact:**")
                    for k, v in uc['financial_impact'].items():
                        st.markdown(f"**{k.replace('_',' ').title()}:** {v}")

        st.markdown("##### 🔧 Solution Tiers")
        scols = st.columns(4)
        for i, (_, sol) in enumerate(get_solution_types().items()):
            with scols[i]:
                st.markdown(f"""
                <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1rem;">
                    <div style="font-weight:800;color:#1e3a8a;font-size:0.9rem;">{sol['name']}</div>
                    <div style="color:#64748b;font-size:0.75rem;">{sol['tier']}</div>
                    <div style="color:#0ea5e9;font-weight:700;margin-top:0.3rem;">{sol['cost_per']}/desc</div>
                    <div style="font-size:0.75rem;color:#475569;">Quality: {sol['quality']}</div>
                    <div style="font-size:0.75rem;color:#475569;">Speed: {sol['speed']}</div>
                </div>
                """, unsafe_allow_html=True)
