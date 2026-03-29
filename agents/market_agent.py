"""
Market Analysis Agent - International Standard
Analyzes market opportunity with Indian vs International bifurcation
"""

def get_market_analysis():
    """Returns comprehensive global market analysis data"""
    
    market_data = {
        "global": {
            "tam": {
                "value": 5.2,  # $5.2B
                "description": "Total Addressable Market (Global)",
                "range": "$4-7 Billion"
            },
            "sam": {
                "value": 1.8,  # $1.8B
                "description": "Serviceable Addressable Market",
                "range": "$1.2-2.5B"
            },
            "som": {
                "value": 0.25,  # $250M Year 5
                "description": "Serviceable Obtainable Market (Year 5)",
                "range": "$150-400M"
            }
        },
        "india": {
            "tam": {
                "value": 0.85,  # $850M
                "description": "India TAM",
                "range": "$600M-1.2B"
            },
            "sam": {
                "value": 0.35,  # $350M
                "description": "India SAM",
                "range": "$250-500M"
            },
            "som": {
                "value": 0.04,  # $40M Year 5
                "description": "India SOM (Year 5)",
                "range": "$20-75M"
            },
            "growth_rate": "22-28% CAGR",
            "e_commerce_size": 55,  # $55B
            "sellers": 5200000,  # 5.2M
            "logistics_strength": "Advanced"
        },
        "international": {
            "tam": {
                "value": 4.35,  # $4.35B
                "description": "International TAM (excl. India)",
                "range": "$3.5-6B"
            },
            "sam": {
                "value": 1.45,  # $1.45B
                "description": "International SAM",
                "range": "$1-2B"
            },
            "som": {
                "value": 0.21,  # $210M Year 5
                "description": "International SOM (Year 5)",
                "range": "$130-330M"
            },
            "growth_rate": "14-18% CAGR",
            "e_commerce_size": 5500,  # $5.5T
            "sellers": 45000000,  # 45M
            "logistics_strength": "Mature & Established"
        },
        "annual_spend": {
            "current": 2.8,  # $2.8B
            "description": "Current annual spend on descriptions"
        },
        "products_per_year": 850000000,  # 850M
        "market_growth": "14-18% annually",
        "e_commerce_projection_2030": 7.5,  # $7.5T
        "ai_adoption_rate": "87% of enterprises"
    }
    
    return market_data


def get_market_segments():
    """Returns market segmentation analysis - India vs International"""
    
    segments = {
        "india_segments": {
            "large_platforms": {
                "name": "Amazon India, Flipkart, Myntra",
                "size": "$180M",
                "customers": "3-5",
                "difficulty": "Hard",
                "opportunity": "Highest value per customer",
                "growth_potential": "50-100M items/year"
            },
            "mid_marketplaces": {
                "name": "Meesho, Moonfrog, Tata Cliq, Jabong",
                "size": "$120M",
                "customers": "20-50",
                "difficulty": "Medium",
                "opportunity": "High growth tier",
                "growth_potential": "30-50M items/year"
            },
            "smb_sellers": {
                "name": "SMB Sellers on Amazon/Flipkart",
                "size": "$350M",
                "customers": "50,000+",
                "difficulty": "Easy - SaaS model",
                "opportunity": "Massive volume opportunity",
                "growth_potential": "Highest growth rate 35%+"
            },
            "brands": {
                "name": "Indian Brands & Retailers",
                "size": "$150M",
                "customers": "100,000+",
                "difficulty": "Medium",
                "opportunity": "Premium pricing",
                "growth_potential": "20-25% annual"
            },
            "emerging": {
                "name": "Tier-2 Platforms & Niche Marketplaces",
                "size": "$85M",
                "customers": "1,000+",
                "difficulty": "Easy",
                "opportunity": "Rapid expansion",
                "growth_potential": "40-50% CAGR"
            }
        },
        "international_segments": {
            "large_platforms": {
                "name": "Amazon Global, eBay, Walmart, Alibaba",
                "size": "$950M",
                "customers": "8-15",
                "difficulty": "Very Hard - Enterprise only",
                "opportunity": "Highest value contracts",
                "growth_potential": "200-400M items/year"
            },
            "regional_marketplaces": {
                "name": "Shopee, Tokopedia, OLX, Regional Players",
                "size": "$700M",
                "customers": "50-200",
                "difficulty": "Hard",
                "opportunity": "High-value accounts",
                "growth_potential": "100-200M items/year"
            },
            "smb_sellers": {
                "name": "Etsy, Shopify, WooCommerce Sellers",
                "size": "$1.2B",
                "customers": "200,000+",
                "difficulty": "Medium - SaaS model",
                "opportunity": "High volume, sustainable",
                "growth_potential": "25-30% annual"
            },
            "brands_retailers": {
                "name": "Multi-National Brands & Retailers",
                "size": "$800M",
                "customers": "2M+",
                "difficulty": "Medium",
                "opportunity": "Premium pricing, long contracts",
                "growth_potential": "18-22% annual"
            },
            "api_partners": {
                "name": "Software Integration Partners",
                "size": "$300M",
                "customers": "500+",
                "difficulty": "Medium-Hard",
                "opportunity": "Recurring revenue",
                "growth_potential": "20-40% annual"
            }
        }
    }
    
    return segments


def get_growth_drivers():
    """Returns key market growth drivers - India vs International"""
    
    drivers = [
        {
            "name": "E-Commerce Expansion",
            "india_impact": "22-28% CAGR",
            "international_impact": "14-18% CAGR",
            "driver": "India fastest growing, International mature but stable"
        },
        {
            "name": "AI Adoption Wave",
            "india_impact": "Accelerating (from 45% to 87%)",
            "international_impact": "Mature adoption (87%+)",
            "driver": "India catching up rapidly, International optimizing"
        },
        {
            "name": "Creator & Seller Economy",
            "india_impact": "5.2M sellers (40% growth YoY)",
            "international_impact": "45M+ sellers (15% growth YoY)",
            "driver": "India democratizing commerce, International consolidating"
        },
        {
            "name": "Market Expansion",
            "india_impact": "Tier-2/3 cities growing 2x faster",
            "international_impact": "New geographies (Africa, SE Asia)",
            "driver": "India penetration, International expansion"
        },
        {
            "name": "Mobile-First Commerce",
            "india_impact": "80%+ mobile traffic",
            "international_impact": "60-70% mobile traffic",
            "driver": "India mobile-native, International multi-device"
        },
        {
            "name": "Returns & Quality Problem",
            "india_impact": "45% return rate (critical issue)",
            "international_impact": "20-25% return rate",
            "driver": "India seeking solutions desperately"
        },
        {
            "name": "Logistics Infrastructure",
            "india_impact": "Same-day delivery in metro cities",
            "international_impact": "2-3 day standard shipping",
            "driver": "India tech-enabled, International efficient"
        },
        {
            "name": "Language & Localization",
            "india_impact": "12 languages, high localization need",
            "international_impact": "Multi-language, standardized",
            "driver": "India complex, International efficient"
        }
    ]
    
    return drivers


def get_india_vs_international_comparison():
    """Comprehensive comparison of India vs International markets"""
    
    comparison = {
        "market_size": {
            "india": {
                "current_tam": "$850M",
                "year_5_tam": "$1.8B",
                "growth": "112% in 5 years",
                "cagr": "25%"
            },
            "international": {
                "current_tam": "$4.35B",
                "year_5_tam": "$5.8B",
                "growth": "33% in 5 years",
                "cagr": "16%"
            }
        },
        "market_maturity": {
            "india": "Early-to-Growth Stage (2-3 years ahead)",
            "international": "Growth-to-Maturity Stage (Established)"
        },
        "seller_landscape": {
            "india": "Predominantly SMB (High fragmentation)",
            "international": "Mixed - Large enterprises + SMBs (Consolidating)"
        },
        "growth_drivers": {
            "india": "New sellers, mobile adoption, tier-2/3 expansion",
            "international": "Premium positioning, automation, partnerships"
        },
        "pricing_sensitivity": {
            "india": "High (cost-conscious market)",
            "international": "Low-to-Medium (value-based pricing)"
        },
        "support_needs": {
            "india": "Hand-holding, local support, simple solutions",
            "international": "API-first, integration, scalability"
        },
        "implementation_speed": {
            "india": "Fast (quick decisions)",
            "international": "Slower (enterprise processes)"
        },
        "technology_stack": {
            "india": "Mobile, offline-first, low-bandwidth",
            "international": "Cloud-native, API-first, bandwidth-rich"
        }
    }
    
    return comparison


def get_industry_growth_projections():
    """Industry growth projections for next 5 years"""
    
    projections = {
        "year_1": {
            "india": {
                "market_size": 0.95,  # $950M
                "sellers": 5800000,
                "products": 900000000,
                "growth_rate": "24%"
            },
            "international": {
                "market_size": 4.95,  # $4.95B
                "sellers": 48000000,
                "products": 1000000000,
                "growth_rate": "16%"
            }
        },
        "year_2": {
            "india": {
                "market_size": 1.15,  # $1.15B
                "sellers": 6800000,
                "products": 1100000000,
                "growth_rate": "26%"
            },
            "international": {
                "market_size": 5.65,  # $5.65B
                "sellers": 52000000,
                "products": 1200000000,
                "growth_rate": "15%"
            }
        },
        "year_3": {
            "india": {
                "market_size": 1.42,  # $1.42B
                "sellers": 8000000,
                "products": 1350000000,
                "growth_rate": "24%"
            },
            "international": {
                "market_size": 6.35,  # $6.35B
                "sellers": 56500000,
                "products": 1400000000,
                "growth_rate": "14%"
            }
        },
        "year_4": {
            "india": {
                "market_size": 1.70,  # $1.70B
                "sellers": 9200000,
                "products": 1600000000,
                "growth_rate": "20%"
            },
            "international": {
                "market_size": 7.10,  # $7.10B
                "sellers": 60000000,
                "products": 1550000000,
                "growth_rate": "12%"
            }
        },
        "year_5": {
            "india": {
                "market_size": 1.95,  # $1.95B
                "sellers": 10500000,
                "products": 1850000000,
                "growth_rate": "15%"
            },
            "international": {
                "market_size": 7.85,  # $7.85B
                "sellers": 62000000,
                "products": 1700000000,
                "growth_rate": "10%"
            }
        }
    }
    
    return projections
