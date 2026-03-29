"""
Use Cases Agent
Provides detailed use case scenarios and implementations
"""

def get_use_cases():
    """Returns comprehensive use case data"""
    
    use_cases = {
        "amazon_sellers": {
            "name": "Amazon Sellers",
            "segmentation": "1.7M third-party sellers, 500M-800M products",
            "problem": {
                "volume": "Millions of products need descriptions",
                "cost": "$2-5 per product",
                "time": "15-20 minutes per product",
                "annual_cost": "$1-4 Billion seller-wide"
            },
            "constraints": {
                "title_limit": "200 characters",
                "description_limit": "2000 characters",
                "no_html": "Plain text only",
                "keyword_stuffing": "Penalized"
            },
            "solution_features": [
                "A+ content generation",
                "Keyword optimization",
                "Multiple variants",
                "Backend keyword suggestion"
            ],
            "financial_impact": {
                "time_saved_annual": "260 days per 100 products",
                "cost_saved_annual": "$4K-40K",
                "roi": "40-80x",
                "payback_weeks": "2-4"
            }
        },
        "myntra_fashion": {
            "name": "Myntra (Fashion E-Commerce)",
            "segmentation": "700K+ listings, 5K-10K new daily",
            "problem": {
                "current_staff": "50-100 writers @ $50K each",
                "annual_cost": "$2.5M-5M",
                "new_daily": "5,000-10,000 products",
                "complexity": "Fashion vocabulary, variants"
            },
            "constraints": {
                "color_variations": "Peacock blue, burnt sienna, etc",
                "fabric_blends": "Cotton-polyester mixes",
                "fit_descriptions": "Slim, regular, oversize",
                "variants": "5-10 sizes, 10+ colors per item"
            },
            "solution_features": [
                "Fashion image analysis",
                "Style-specific templates",
                "Size & fit guides",
                "Return rate reduction",
                "Bulk processing"
            ],
            "financial_impact": {
                "annual_savings": "$4M-5M",
                "time_reduction": "82%",
                "payback_period": "1-2 months",
                "staff_reduction": "80%"
            }
        },
        "luxury_brands": {
            "name": "Luxury Brands",
            "segmentation": "500-5000 products per brand, $100-$10K price",
            "problem": {
                "portfolio": "Limited but curated collections",
                "time_per_product": "30-60 minutes",
                "challenge": "Maintain brand voice at scale",
                "annual_spend": "$300K-$1M"
            },
            "constraints": {
                "brand_consistency": "Must match brand tone",
                "storytelling": "Heritage and craftsmanship",
                "quality": "Premium positioning",
                "accuracy": "No margin for error"
            },
            "solution_features": [
                "Brand voice training",
                "Storytelling integration",
                "Multi-channel adaptation",
                "Personalization by segment",
                "Professional review"
            ],
            "financial_impact": {
                "annual_spend": "$300K-$1M",
                "time_reduction": "70%+",
                "conversion_uplift": "15-25%",
                "roi": "200-400%"
            }
        },
        "dropshipping": {
            "name": "Dropshipping Businesses",
            "segmentation": "100-1000 products per seller, solo/2-person",
            "problem": {
                "current_method": "Copy supplier descriptions",
                "quality": "Poor grammar, auto-translated",
                "budget": "$50-200/month for tools",
                "challenge": "Volume with minimal team"
            },
            "constraints": {
                "budget_limited": "Can't afford $500/month",
                "time_limited": "Solo entrepreneur",
                "seo_lacking": "No keyword optimization",
                "uniqueness": "Duplicate descriptions"
            },
            "solution_features": [
                "Auto-fix supplier descriptions",
                "Budget-friendly tier",
                "SEO optimization",
                "Unique, professional outputs",
                "Bulk upload"
            ],
            "financial_impact": {
                "monthly_sales_increase": "$6,250",
                "return_savings": "$6,000",
                "monthly_benefit": "$12,250",
                "annual_profit_increase": "$147K",
                "roi": "408x"
            }
        },
        "enterprise_platforms": {
            "name": "Enterprise Platforms",
            "segmentation": "50M-500M products, 10K-50K daily uploads",
            "problem": {
                "scale": "Millions of products to manage",
                "quality": "30-70% sellers have poor descriptions",
                "impact": "Bad search, high returns, poor reviews",
                "cost": "$15M-$60M annual on manual review"
            },
            "constraints": {
                "seller_variance": "Quality inconsistent",
                "coverage": "Can only review 10-20%",
                "returns": "20%+ return rate (description-related)",
                "seo": "Search quality suffers"
            },
            "solution_features": [
                "Description quality scorecard",
                "Bulk audit & improvement",
                "Seller enablement",
                "Return rate reduction",
                "White-label service"
            ],
            "financial_impact": {
                "return_reduction": "15-25%",
                "annual_savings": "$100M+",
                "search_improvement": "20-30%",
                "gmv_increase": "10-15%",
                "roi": "100x+"
            }
        }
    }
    
    return use_cases


def get_solution_types():
    """Returns different solution tiers"""
    
    solution_types = {
        "type_1_template": {
            "name": "Vision + Template-Based",
            "tier": "Tier 1: Fastest, Least Expensive",
            "approach": "Category detection + pre-built templates",
            "cost_per": "$0.01-0.03",
            "quality": "70-80%",
            "speed": "<1 second",
            "best_for": "Large volume, standard products"
        },
        "type_2_ai_model": {
            "name": "Vision + AI Language Model",
            "tier": "Tier 2: Balanced",
            "approach": "Advanced analysis + LLM generation",
            "cost_per": "$0.05-0.15",
            "quality": "85-92%",
            "speed": "2-5 seconds",
            "best_for": "Mid-tier platforms, quality-conscious"
        },
        "type_3_premium": {
            "name": "Vision + Fine-Tuned + Human Review",
            "tier": "Tier 3: Premium",
            "approach": "Custom models + professional review",
            "cost_per": "$0.20-1.00",
            "quality": "95%+",
            "speed": "10-30 seconds",
            "best_for": "Luxury brands, high-value products"
        },
        "type_4_advanced": {
            "name": "Multi-Image + Context Integration",
            "tier": "Tier 4: Advanced",
            "approach": "Multiple images + catalog integration",
            "cost_per": "$0.30-2.00",
            "quality": "98%+",
            "speed": "1-2 minutes",
            "best_for": "Enterprise platforms, data-rich"
        }
    }
    
    return solution_types


def get_example_outputs():
    """Returns sample description outputs"""
    
    examples = {
        "amazon_laptop_stand": {
            "product": "Ultra-Slim Laptop Stand",
            "category": "Office Products",
            "title": "Premium Aluminum Laptop Stand, Portable Laptop Holder for 10-17 Inch MacBook Pro Air Dell HP",
            "short": "Premium aluminum construction provides durability and professional look. Compatible with all laptops 10-17 inches. Foldable design fits easily in your bag. Elevates screen for ergonomic viewing. Anti-slip rubber pads protect your devices. Lifetime warranty.",
            "keywords": ["laptop stand", "laptop holder", "laptop riser", "aluminum", "ergonomic"]
        },
        "myntra_denim_shirt": {
            "product": "Women's Blue Denim Casual Shirt",
            "category": "Casual Shirts",
            "title": "Women's Blue Denim Casual Shirt",
            "highlights": [
                "100% premium cotton denim",
                "Comfortable loose-fit",
                "Full-length sleeves",
                "Button-down closure",
                "Machine washable"
            ],
            "fit": "Runs true to size, relaxed fit"
        }
    }
    
    return examples
