"""
Trovia Agent System — Ruflo-Inspired Multi-Agent Architecture
Agents: ProductSearchAgent, RecommendationAgent, PriceOptimizerAgent, SwarmOrchestrator
"""

import re
import math
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.products import PRODUCTS, COUPON_CODES


# ─── Agent Memory (Ruflo-style ReasoningBank) ─────────────────────────────────

class AgentMemory:
    """Simple in-process memory store — mirrors Ruflo's AgentDB concept."""

    def __init__(self):
        self._store: dict[str, Any] = {}
        self._history: list[dict] = []

    def set(self, key: str, value: Any):
        self._store[key] = value
        self._history.append({"ts": datetime.now().isoformat(), "op": "set", "key": key})

    def get(self, key: str, default=None):
        return self._store.get(key, default)

    def log(self) -> list[dict]:
        return self._history[-20:]


# ─── Base Agent ───────────────────────────────────────────────────────────────

@dataclass
class AgentResult:
    agent: str
    status: str          # "success" | "empty" | "error"
    data: Any = None
    message: str = ""
    latency_ms: float = 0.0


class BaseAgent:
    name: str = "base"
    capabilities: list[str] = []

    def __init__(self):
        self.memory = AgentMemory()

    def _timer(self):
        return datetime.now().timestamp() * 1000

    def run(self, *args, **kwargs) -> AgentResult:
        raise NotImplementedError


# ─── 1. Product Search Agent ──────────────────────────────────────────────────

class ProductSearchAgent(BaseAgent):
    """
    Tier-2 agent: natural-language product search.
    Ruflo equivalent: coder/retrieval agent with flash-attention scoring.
    """
    name = "ProductSearchAgent"
    capabilities = ["semantic-search", "filter", "ranking"]

    def run(self, query: str, filters: dict | None = None) -> AgentResult:
        t0 = self._timer()
        query_lower = query.lower()
        tokens = set(re.findall(r'\w+', query_lower))
        filters = filters or {}

        scored = []
        for p in PRODUCTS:
            score = 0.0

            # Name match (highest weight)
            name_lower = p["name"].lower()
            if query_lower in name_lower:
                score += 10
            for tok in tokens:
                if tok in name_lower:
                    score += 3

            # Tag match
            for tag in p.get("tags", []):
                if tag in tokens or any(t in tag for t in tokens):
                    score += 2

            # Category match
            if p.get("category", "").lower() in tokens:
                score += 4

            # Description match
            desc_lower = p.get("description", "").lower()
            for tok in tokens:
                if tok in desc_lower:
                    score += 0.5

            # Brand match
            if p.get("brand", "").lower() in tokens:
                score += 3

            # Filters
            if filters.get("max_price") and p["price"] > filters["max_price"]:
                continue
            if filters.get("min_price") and p["price"] < filters["min_price"]:
                continue
            if filters.get("category") and p.get("category") != filters["category"]:
                continue
            if filters.get("min_rating") and p["rating"] < filters["min_rating"]:
                continue
            if filters.get("in_stock") and not p.get("in_stock", True):
                continue

            if score > 0:
                scored.append({**p, "_score": round(score, 2)})

        results = sorted(scored, key=lambda x: x["_score"], reverse=True)
        latency = self._timer() - t0

        self.memory.set("last_query", query)
        self.memory.set("last_results_count", len(results))

        if not results:
            return AgentResult(self.name, "empty", [], f"No products found for '{query}'", latency)

        return AgentResult(self.name, "success", results[:10], f"Found {len(results)} products", latency)


# ─── 2. Recommendation Agent ─────────────────────────────────────────────────

class RecommendationAgent(BaseAgent):
    """
    Tier-2 agent: personalized recommendations using collaborative-style scoring.
    Ruflo equivalent: swarm memory + HNSW vector similarity (simplified).
    """
    name = "RecommendationAgent"
    capabilities = ["personalization", "cross-sell", "trending"]

    # Category affinity map (which categories pair well)
    AFFINITY = {
        "Electronics": ["Electronics", "Sports"],
        "Sports":       ["Sports", "Fashion", "Beauty"],
        "Fashion":      ["Fashion", "Beauty", "Sports"],
        "Beauty":       ["Beauty", "Fashion", "Home"],
        "Home":         ["Home", "Electronics", "Beauty"],
        "Books":        ["Books", "Electronics"],
        "Food":         ["Food", "Beauty", "Home"],
    }

    def run(self, cart_product_ids: list[int], viewed_ids: list[int] | None = None,
            budget: float | None = None) -> AgentResult:
        t0 = self._timer()
        viewed_ids = viewed_ids or []
        seen_ids = set(cart_product_ids + viewed_ids)

        # Build interest profile from cart
        cart_items = [p for p in PRODUCTS if p["id"] in cart_product_ids]
        if not cart_items:
            # Cold-start: return top-rated
            top = sorted(PRODUCTS, key=lambda x: x["rating"], reverse=True)
            results = [p for p in top if p["id"] not in seen_ids][:6]
            return AgentResult(self.name, "success", results,
                               "Top-rated picks (no cart data)", self._timer() - t0)

        cart_categories = [p["category"] for p in cart_items]
        avg_price = sum(p["price"] for p in cart_items) / len(cart_items)
        price_ceiling = budget or avg_price * 2

        # Score candidates
        scored = []
        for p in PRODUCTS:
            if p["id"] in seen_ids:
                continue
            if p["price"] > price_ceiling:
                continue

            score = 0.0

            # Category affinity
            for cat in cart_categories:
                affinity_cats = self.AFFINITY.get(cat, [cat])
                if p["category"] in affinity_cats:
                    score += 3 if p["category"] == cat else 1.5

            # Rating boost
            score += p["rating"]

            # Price similarity (prefer similar price range)
            price_diff = abs(p["price"] - avg_price) / max(avg_price, 1)
            score += max(0, 2 - price_diff)

            # Tag overlap
            cart_tags = set(t for item in cart_items for t in item.get("tags", []))
            overlap = len(set(p.get("tags", [])) & cart_tags)
            score += overlap * 0.5

            if score > 0:
                scored.append({**p, "_score": round(score, 2), "_reason": self._reason(p, cart_categories)})

        results = sorted(scored, key=lambda x: x["_score"], reverse=True)[:8]
        latency = self._timer() - t0

        self.memory.set("last_cart_size", len(cart_product_ids))
        self.memory.set("last_rec_count", len(results))

        return AgentResult(self.name, "success", results,
                           f"Recommended {len(results)} products based on your cart", latency)

    def _reason(self, product: dict, cart_categories: list[str]) -> str:
        if product["category"] in cart_categories:
            return f"More {product['category']} you might like"
        return f"Pairs well with your {cart_categories[0] if cart_categories else 'items'}"


# ─── 3. Price Optimizer Agent ─────────────────────────────────────────────────

class PriceOptimizerAgent(BaseAgent):
    """
    Tier-1 agent: fast price analysis, deal detection, coupon optimization.
    Ruflo equivalent: Agent Booster (sub-1ms transforms) for pricing logic.
    """
    name = "PriceOptimizerAgent"
    capabilities = ["deal-detection", "coupon-matching", "budget-fit"]

    DEAL_THRESHOLD = 0.15   # 15%+ discount = "deal"

    def run(self, cart_items: list[dict], coupon_code: str = "",
            budget: float | None = None) -> AgentResult:
        t0 = self._timer()

        if not cart_items:
            return AgentResult(self.name, "empty", {}, "Cart is empty", self._timer() - t0)

        subtotal = sum(item["price"] * item.get("quantity", 1) for item in cart_items)

        # Coupon evaluation
        coupon_result = self._evaluate_coupon(coupon_code, subtotal)

        # Find best available coupon if none given
        best_coupon = self._find_best_coupon(subtotal)

        # Budget analysis
        budget_analysis = self._budget_analysis(subtotal, coupon_result["final"], budget)

        # Deal score per item
        item_deals = self._score_items(cart_items)

        # Savings opportunity
        savings_tip = self._savings_tip(subtotal, coupon_result, best_coupon, budget_analysis)

        result = {
            "subtotal": subtotal,
            "coupon": coupon_result,
            "best_coupon_available": best_coupon,
            "final_price": coupon_result["final"],
            "budget_analysis": budget_analysis,
            "item_deals": item_deals,
            "savings_tip": savings_tip,
            "total_savings": subtotal - coupon_result["final"],
        }

        latency = self._timer() - t0
        return AgentResult(self.name, "success", result,
                           f"Optimized ₹{subtotal:,.0f} → ₹{coupon_result['final']:,.0f}", latency)

    def _evaluate_coupon(self, code: str, subtotal: float) -> dict:
        code = code.strip().upper()
        if code and code in COUPON_CODES:
            coupon = COUPON_CODES[code]
            if coupon["type"] == "percent":
                discount = subtotal * coupon["value"] / 100
            else:
                discount = min(coupon["value"], subtotal)
            return {"code": code, "valid": True, "discount": discount,
                    "final": subtotal - discount, "description": coupon["description"]}
        return {"code": code, "valid": False, "discount": 0, "final": subtotal, "description": ""}

    def _find_best_coupon(self, subtotal: float) -> dict:
        best = {"code": "", "savings": 0}
        for code, coupon in COUPON_CODES.items():
            if coupon["type"] == "percent":
                savings = subtotal * coupon["value"] / 100
            else:
                savings = min(coupon["value"], subtotal)
            if savings > best["savings"]:
                best = {"code": code, "savings": savings, "description": coupon["description"]}
        return best

    def _budget_analysis(self, subtotal: float, final: float, budget: float | None) -> dict:
        if budget is None:
            return {"has_budget": False}
        within = final <= budget
        overage = max(0, final - budget)
        return {
            "has_budget": True,
            "budget": budget,
            "within_budget": within,
            "overage": overage,
            "remaining": max(0, budget - final),
        }

    def _score_items(self, items: list[dict]) -> list[dict]:
        result = []
        all_prices = [p["price"] for p in PRODUCTS if p.get("in_stock")]
        for item in items:
            cat_prices = [p["price"] for p in PRODUCTS
                          if p.get("category") == item.get("category") and p.get("in_stock")]
            avg_cat = sum(cat_prices) / len(cat_prices) if cat_prices else item["price"]
            value_score = min(5.0, round((avg_cat / max(item["price"], 1)) * item.get("rating", 4), 1))
            result.append({
                "id": item["id"],
                "name": item["name"],
                "value_score": value_score,
                "vs_category_avg": round(((avg_cat - item["price"]) / avg_cat) * 100, 1),
            })
        return result

    def _savings_tip(self, subtotal, coupon_result, best_coupon, budget_analysis) -> str:
        if not coupon_result["valid"] and best_coupon.get("code"):
            return f"💡 Use code **{best_coupon['code']}** to save ₹{best_coupon['savings']:,.0f}!"
        if coupon_result["valid"]:
            return f"✅ You're saving ₹{coupon_result['discount']:,.0f} with {coupon_result['code']}!"
        if budget_analysis.get("overage", 0) > 0:
            return f"⚠️ You're ₹{budget_analysis['overage']:,.0f} over budget. Remove 1 item to stay within."
        return "🎉 Great cart! You're getting excellent value."


# ─── 4. Swarm Orchestrator (Ruflo Queen pattern) ──────────────────────────────

class TroviaSwarm:
    """
    Queen-led orchestrator — runs all agents in sequence, aggregates results.
    Ruflo equivalent: Queen agent coordinating worker swarm with consensus.
    """

    def __init__(self):
        self.search_agent    = ProductSearchAgent()
        self.rec_agent       = RecommendationAgent()
        self.price_agent     = PriceOptimizerAgent()
        self._run_log: list[dict] = []

    def search(self, query: str, filters: dict | None = None) -> AgentResult:
        result = self.search_agent.run(query, filters)
        self._log("search", query, result)
        return result

    def recommend(self, cart_ids: list[int], viewed_ids: list[int] | None = None,
                  budget: float | None = None) -> AgentResult:
        result = self.rec_agent.run(cart_ids, viewed_ids, budget)
        self._log("recommend", cart_ids, result)
        return result

    def optimize(self, cart_items: list[dict], coupon: str = "",
                 budget: float | None = None) -> AgentResult:
        result = self.price_agent.run(cart_items, coupon, budget)
        self._log("optimize", coupon, result)
        return result

    def full_analysis(self, query: str, cart_ids: list[int],
                      cart_items: list[dict], coupon: str = "",
                      budget: float | None = None) -> dict:
        """Run all 3 agents and return combined swarm result."""
        t0 = datetime.now().timestamp() * 1000

        search  = self.search(query) if query else None
        recs    = self.recommend(cart_ids)
        pricing = self.optimize(cart_items, coupon, budget)

        return {
            "swarm": "TroviaSwarm",
            "agents_run": 3,
            "total_latency_ms": round(datetime.now().timestamp() * 1000 - t0, 2),
            "search":  search,
            "recommendations": recs,
            "pricing": pricing,
            "timestamp": datetime.now().isoformat(),
        }

    def status(self) -> dict:
        return {
            "swarm": "TroviaSwarm v1.0",
            "agents": [
                {"name": self.search_agent.name, "capabilities": self.search_agent.capabilities,
                 "last_query": self.search_agent.memory.get("last_query", "—"),
                 "last_results": self.search_agent.memory.get("last_results_count", 0)},
                {"name": self.rec_agent.name, "capabilities": self.rec_agent.capabilities,
                 "last_cart_size": self.rec_agent.memory.get("last_cart_size", 0)},
                {"name": self.price_agent.name, "capabilities": self.price_agent.capabilities},
            ],
            "runs": len(self._run_log),
            "topology": "hierarchical",
            "inspired_by": "Ruflo v3.5",
        }

    def _log(self, op: str, input_: Any, result: AgentResult):
        self._run_log.append({
            "op": op, "status": result.status,
            "latency_ms": result.latency_ms,
            "ts": datetime.now().isoformat(),
        })
