"""
Financial Analysis Agent - International Standard
Generates revenue projections, unit economics, and pricing models
Includes India vs International market segmentation
"""

def get_financial_projections():
    """Returns revenue projections and financial metrics (Global)"""
    
    projections = {
        "global": {
            "conservative": {
                "year_1": 0.85,  # $850K
                "year_2": 6.5,   # $6.5M
                "year_3": 32,    # $32M
                "year_4": 85,    # $85M
                "year_5": 125    # $125M
            },
            "optimistic": {
                "year_1": 2.0,   # $2.0M
                "year_2": 12,    # $12M
                "year_3": 55,    # $55M
                "year_4": 150,   # $150M
                "year_5": 200    # $200M
            }
        },
        "india": {
            "conservative": {
                "year_1": 0.30,  # $300K
                "year_2": 1.8,   # $1.8M
                "year_3": 8.5,   # $8.5M
                "year_4": 22,    # $22M
                "year_5": 35     # $35M
            },
            "optimistic": {
                "year_1": 0.65,  # $650K
                "year_2": 3.5,   # $3.5M
                "year_3": 15,    # $15M
                "year_4": 42,    # $42M
                "year_5": 65     # $65M
            }
        },
        "international": {
            "conservative": {
                "year_1": 0.55,  # $550K
                "year_2": 4.7,   # $4.7M
                "year_3": 23.5,  # $23.5M
                "year_4": 63,    # $63M
                "year_5": 90     # $90M
            },
            "optimistic": {
                "year_1": 1.35,  # $1.35M
                "year_2": 8.5,   # $8.5M
                "year_3": 40,    # $40M
                "year_4": 108,   # $108M
                "year_5": 135    # $135M
            }
        },
        "assumptions": {
            "year_1_customers": "500-1000",
            "year_3_customers": "20000-50000",
            "year_5_customers": "100000+",
            "payback_period": "2-4 weeks",
            "churn_rate": "5-15% annually",
            "india_smb_focus": "High volume, low ACV",
            "international_enterprise_focus": "Low volume, high ACV"
        }
    }
    
    return projections


def get_unit_economics():
    """Returns customer unit economics - India vs International"""
    
    economics = {
        "global": {
            "customer_acquisition_cost": {
                "low": 300,
                "high": 800,
                "average": 500
            },
            "lifetime_value": {
                "low": 3000,
                "high": 15000,
                "average": 9000
            },
            "ltv_cac_ratio": {
                "low": 4,
                "high": 18,
                "target": "Excellent (>3:1)"
            }
        },
        "india": {
            "customer_acquisition_cost": {
                "smb_seller": 150,
                "marketplace": 800,
                "brand": 400,
                "average": 300
            },
            "lifetime_value": {
                "smb_seller": 2000,
                "marketplace": 20000,
                "brand": 8000,
                "average": 8000
            },
            "ltv_cac_ratio": {
                "smb_seller": "13:1",
                "marketplace": "25:1",
                "brand": "20:1",
                "target": "Excellent (>8:1)"
            },
            "pricing": "$10-50/month SMB | $500-2000/month platforms",
            "payback_period": "2-3 weeks",
            "monthly_churn": "8-12%"
        },
        "international": {
            "customer_acquisition_cost": {
                "smb_seller": 200,
                "retailer": 1200,
                "enterprise": 5000,
                "average": 1000
            },
            "lifetime_value": {
                "smb_seller": 4000,
                "retailer": 40000,
                "enterprise": 500000,
                "average": 150000
            },
            "ltv_cac_ratio": {
                "smb_seller": "20:1",
                "retailer": "33:1",
                "enterprise": "100:1",
                "target": "Excellent (>10:1)"
            },
            "pricing": "$50-200/month SMB | $2000-10000/month enterprise",
            "payback_period": "4-8 weeks",
            "monthly_churn": "3-5%"
        },
        "common": {
            "gross_margin": "80-85%",
            "annual_roi_low": "2000%",
            "annual_roi_high": "3000%",
            "average_revenue_per_customer": {
                "starter": 100,
                "professional": 500,
                "enterprise": 5000
            }
        }
    }
    
    return economics


def get_revenue_models():
    """Returns different revenue model options - India vs International"""
    
    models = {
        "india_models": {
            "model_1_per_description": {
                "name": "Per-Description SaaS (India)",
                "pricing": "$0.02-0.05 per description",
                "tier_1": {"name": "Starter", "monthly": 49, "limit": 500},
                "tier_2": {"name": "Professional", "monthly": 199, "limit": 5000},
                "tier_3": {"name": "Growth", "monthly": 499, "limit": 25000},
                "potential_annual": "$500K-$3M"
            },
            "model_2_smb_focused": {
                "name": "Volume-Based SMB (India)",
                "pricing": "Per product + usage",
                "startup": {"monthly": 29, "products": 100},
                "growth": {"monthly": 99, "products": 500},
                "scale": {"monthly": 299, "products": 2000},
                "potential_annual": "$1M-$5M",
                "strategy": "High volume, low price"
            }
        },
        "international_models": {
            "model_1_enterprise_licensing": {
                "name": "Enterprise License (International)",
                "pricing": "$50K-$500K/year",
                "tier_1": {"name": "Platform", "quarterly": 25000},
                "tier_2": {"name": "Enterprise", "quarterly": 100000},
                "tier_3": {"name": "Global", "quarterly": 250000},
                "potential_annual": "$10M-$50M"
            },
            "model_2_api_volume": {
                "name": "API Volume Pricing (International)",
                "pricing": "$0.05-0.15 per API call",
                "volume_discounts": "At 1M+ calls/month",
                "minimum_commitment": "$5K-$20K/month",
                "potential_annual": "$2M-$15M"
            }
        },
        "hybrid_global": {
            "model_freemium_plus": {
                "name": "Freemium + Premium (Global)",
                "free_tier": "50 descriptions/month",
                "india_paid": "₹500-5000/month ($6-60)",
                "international_paid": "$50-500/month",
                "conversion_rate": "2-5% typical",
                "potential_annual": "$3M-$20M"
            }
        }
    }
    
    return models


def get_customer_payback():
    """Returns payback analysis by customer segment - India vs International"""
    
    payback = {
        "india": {
            "smb_seller": {
                "monthly_cost": 25,
                "monthly_savings": 500,
                "payback_weeks": 2,
                "annual_roi": "2400%"
            },
            "marketplace": {
                "monthly_cost": 500,
                "monthly_savings": 15000,
                "payback_weeks": 1,
                "annual_roi": "3000%"
            },
            "brand": {
                "monthly_cost": 250,
                "monthly_savings": 8000,
                "payback_weeks": 1,
                "annual_roi": "3200%"
            }
        },
        "international": {
            "smb_seller": {
                "monthly_cost": 100,
                "monthly_savings": 2000,
                "payback_weeks": 2.5,
                "annual_roi": "2400%"
            },
            "retailer": {
                "monthly_cost": 2000,
                "monthly_savings": 75000,
                "payback_weeks": 1,
                "annual_roi": "4500%"
            },
            "enterprise": {
                "monthly_cost": 25000,
                "monthly_savings": 500000,
                "payback_weeks": 0.5,
                "annual_roi": "2400%"
            }
        },
        "key_insight": {
            "india": "Faster payback, smaller deals, higher churn tolerance",
            "international": "Slower payback, larger deals, strong retention focus"
        }
    }
    
    return payback


def get_profitability_timeline():
    """Returns path to profitability - Global, India, and International"""
    
    timeline = {
        "global": {
            "year_1": {
                "revenue": 850000,
                "costs": 1100000,
                "profit": -250000,
                "status": "Investment phase"
            },
            "year_2": {
                "revenue": 6500000,
                "costs": 3500000,
                "profit": 3000000,
                "status": "Break-even achieved"
            },
            "year_3": {
                "revenue": 32000000,
                "costs": 17000000,
                "profit": 15000000,
                "status": "Strong profitability (47%)"
            },
            "year_5": {
                "revenue": 125000000,
                "costs": 62500000,
                "profit": 62500000,
                "status": "Market leader (50%)"
            }
        },
        "india": {
            "year_1": {
                "revenue": 300000,
                "costs": 450000,
                "profit": -150000,
                "status": "Market entry"
            },
            "year_2": {
                "revenue": 1800000,
                "costs": 1000000,
                "profit": 800000,
                "status": "Profitable from Y2"
            },
            "year_3": {
                "revenue": 8500000,
                "costs": 4500000,
                "profit": 4000000,
                "status": "Scaling (47% margin)"
            },
            "year_5": {
                "revenue": 35000000,
                "costs": 15000000,
                "profit": 20000000,
                "status": "Dominant player (57%)"
            },
            "strategy": "Fast growth, volume focus, lower margins initially"
        },
        "international": {
            "year_1": {
                "revenue": 550000,
                "costs": 650000,
                "profit": -100000,
                "status": "Establishment"
            },
            "year_2": {
                "revenue": 4700000,
                "costs": 2500000,
                "profit": 2200000,
                "status": "Break-even to profitable"
            },
            "year_3": {
                "revenue": 23500000,
                "costs": 12500000,
                "profit": 11000000,
                "status": "Strong growth (47%)"
            },
            "year_5": {
                "revenue": 90000000,
                "costs": 40000000,
                "profit": 50000000,
                "status": "Market leader (56%)"
            },
            "strategy": "Enterprise focus, long contracts, premium positioning"
        }
    }
    
    return timeline
