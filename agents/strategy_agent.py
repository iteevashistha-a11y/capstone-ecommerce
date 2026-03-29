"""
Go-to-Market Strategy Agent
Defines market entry, scaling strategy, and partnership approach
"""

def get_gtm_strategy():
    """Returns comprehensive go-to-market strategy"""
    
    strategy = {
        "phase_1_product_market_fit": {
            "duration": "Months 1-4",
            "target_customer": "Shopify Sellers",
            "TAM": "4.4M stores",
            "why_target": [
                "Easiest market to reach",
                "Clear pain point",
                "Willing to pay for productivity",
                "Organic distribution via app store"
            ],
            "distribution_channels": [
                "Shopify App Store (high-intent)",
                "Reddit communities (r/ecommerce, r/shopify)",
                "Indie Hackers launch",
                "Direct email outreach"
            ],
            "key_messages": [
                "Save 95% of description creation time",
                "Improve SEO rankings",
                "Faster product launches",
                "Increase conversions"
            ],
            "goals": {
                "beta_users": "100-500",
                "paying_customers": "50-100",
                "quality_rating": "85%+",
                "case_studies": "5-10"
            },
            "budget": 30000,
            "breakdown": {
                "paid_marketing": 10000,
                "community_engagement": 5000,
                "operations": 10000,
                "contingency": 5000
            }
        },
        "phase_2_market_expansion": {
            "duration": "Months 5-8",
            "new_targets": ["WooCommerce Sellers", "WordPress Users"],
            "TAM": "7M WooCommerce stores",
            "why_expand": [
                "Plugin distribution is organic",
                "Overlapping SMB audience",
                "Lower CAC than Shopify",
                "Higher LTV potential"
            ],
            "distribution_channels": [
                "WordPress plugin directory",
                "WooCommerce marketplace",
                "E-commerce forums",
                "Affiliate partnerships with agencies",
                "Paid advertising (Google, Facebook)"
            ],
            "new_messaging": [
                "Most affordable solution",
                "Works with all platforms",
                "No setup required",
                "Money-back guarantee"
            ],
            "goals": {
                "total_customers": "500-1000",
                "case_studies": "3-5",
                "press_mentions": "5-10",
                "mrr": "30000-50000"
            },
            "budget": 75000,
            "breakdown": {
                "paid_marketing": 30000,
                "pr_content_marketing": 15000,
                "sales_hire": 20000,
                "tools_operations": 10000
            }
        },
        "phase_3_enterprise_scaling": {
            "duration": "Months 9-12",
            "new_targets": [
                "Platforms (Myntra, Flipkart, Amazon)",
                "Brands (Nike, Adidas, etc.)",
                "Marketing Agencies",
                "Enterprise SaaS Companies"
            ],
            "why_enterprise": [
                "Highest revenue per customer",
                "Long-term contracts",
                "Expansion within platform",
                "Strategic partnerships"
            ],
            "distribution_channels": [
                "Direct sales team",
                "Industry conferences (Shoptalk, IAAI)",
                "Strategic partnerships",
                "Enterprise PR",
                "Analyst recognition"
            ],
            "enterprise_positioning": [
                "Reduce return rates by 20-30%",
                "Improve SEO rankings",
                "Scale content operations",
                "Custom integrations available"
            ],
            "goals": {
                "enterprise_customers": "10-20",
                "total_customers": "5000-10000",
                "enterprise_mrr": "100000-300000",
                "total_mrr": "50000-100000"
            },
            "budget": 150000,
            "breakdown": {
                "sales_team_2_people": 100000,
                "enterprise_marketing": 25000,
                "partnership_dev": 15000,
                "customer_success": 25000
            }
        }
    }
    
    return strategy


def get_customer_acquisition_strategy():
    """Returns detailed customer acquisition approach"""
    
    acquisition = {
        "awareness_stage": {
            "goal": "Reach target audience",
            "tactics": [
                "Content marketing (blogs, guides)",
                "Social media (Twitter, LinkedIn, Instagram)",
                "Paid ads (Google, Facebook, TikTok)",
                "Community building (Slack, Discord)"
            ],
            "budget_allocation": "30%",
            "key_channels": [
                "Organic search for 'product description tools'",
                "E-commerce blogs and publications",
                "Social proof (case studies, testimonials)"
            ]
        },
        "consideration_stage": {
            "goal": "Demonstrate value",
            "tactics": [
                "Free trial / freemium model",
                "Case studies with ROI",
                "Product demos (video, interactive)",
                "Webinars and workshops",
                "Comparison guides"
            ],
            "budget_allocation": "40%",
            "conversion_rate": "2-5% typical"
        },
        "decision_stage": {
            "goal": "Remove friction, close deal",
            "tactics": [
                "Transparent pricing",
                "Money-back guarantee",
                "Easy onboarding",
                "Personal support",
                "Integration assistance"
            ],
            "budget_allocation": "20%",
            "average_deal_size": "$100-500 monthly"
        },
        "retention_stage": {
            "goal": "Grow lifetime value",
            "tactics": [
                "Dedicated success manager",
                "Regular training sessions",
                "Product updates and features",
                "Community engagement",
                "Upselling to higher tiers"
            ],
            "budget_allocation": "10%",
            "target_churn": "<5% monthly"
        }
    }
    
    return acquisition


def get_pricing_strategy():
    """Returns pricing tiers and strategy"""
    
    pricing = {
        "tier_1_freemium": {
            "name": "Free / Freemium",
            "monthly_cost": "$0",
            "descriptions_per_month": 50,
            "features": [
                "Basic description generation",
                "Limited customization",
                "Standard templates",
                "Web interface only"
            ],
            "goal": "Prove value, build user base",
            "conversion_rate": "2-5% to paid"
        },
        "tier_2_starter": {
            "name": "Starter",
            "monthly_cost": "$99",
            "descriptions_per_month": 1000,
            "features": [
                "Core features",
                "Category templates",
                "Basic SEO",
                "Email support",
                "API access"
            ],
            "ideal_for": "SMB sellers with 100-500 products"
        },
        "tier_3_professional": {
            "name": "Professional",
            "monthly_cost": "$499",
            "descriptions_per_month": 10000,
            "features": [
                "Advanced features",
                "Brand voice learning",
                "SEO optimization",
                "Multi-language",
                "Priority support",
                "Analytics dashboard"
            ],
            "ideal_for": "Growing e-commerce businesses"
        },
        "tier_4_enterprise": {
            "name": "Enterprise",
            "monthly_cost": "Custom (typically $5K-50K+)",
            "descriptions_per_month": "Unlimited",
            "features": [
                "All features",
                "Custom integrations",
                "Dedicated support",
                "SLA guarantees",
                "Training included",
                "Custom models",
                "White-label option"
            ],
            "ideal_for": "Large platforms, brands, agencies"
        }
    }
    
    return pricing


def get_partnership_strategy():
    """Returns partnership and ecosystem approach"""
    
    partnerships = {
        "platform_integrations": {
            "priority_1": [
                "Shopify",
                "WooCommerce",
                "Amazon Seller Central"
            ],
            "priority_2": [
                "Myntra API",
                "Flipkart API",
                "eBay API"
            ],
            "benefit": "Pre-built integrations reduce friction",
            "timeline": "Integrated during Phase 1-2"
        },
        "agency_partnerships": {
            "target": "Digital marketing agencies",
            "benefit": "Resell to their e-commerce clients",
            "model": "25-30% revenue share",
            "timeline": "Phase 2"
        },
        "tech_partnerships": {
            "potential": [
                "Google Cloud (AI/ML)",
                "AWS (Infrastructure)",
                "OpenAI (Language models)"
            ],
            "benefit": "Co-marketing, joint go-to-market",
            "timeline": "Phase 3"
        },
        "strategic_investors": {
            "potential": [
                "E-commerce platforms",
                "AI/ML companies",
                "SaaS VCs"
            ],
            "funding_rounds": [
                "Seed: $500K-1M (proof of concept)",
                "Series A: $3-5M (product scale)",
                "Series B: $10-15M (market expansion)"
            ]
        }
    }
    
    return partnerships


def get_success_metrics():
    """Returns key metrics to track"""
    
    metrics = {
        "acquisition_metrics": {
            "customer_acquisition_cost": "Target $300-800",
            "monthly_new_customers": "Target 50+ by Month 6",
            "conversion_rate": "Target 2-5% from free to paid",
            "channel_performance": "Track by source"
        },
        "retention_metrics": {
            "monthly_churn": "Target <5%",
            "customer_lifetime_value": "Target $3,000-15,000",
            "nps_score": "Target 50+",
            "expansion_revenue": "Target 20% from upsells"
        },
        "product_metrics": {
            "description_accuracy": "Target 90%+",
            "processing_speed": "Target <5 sec",
            "user_satisfaction": "Track via NPS",
            "feature_adoption": "Track by paid tier"
        },
        "business_metrics": {
            "monthly_revenue": "Target $50K+ by Month 12",
            "gross_margin": "Target 80%+",
            "unit_economics": "LTV:CAC target 4:1+",
            "payback_period": "Target <12 weeks"
        }
    }
    
    return metrics
