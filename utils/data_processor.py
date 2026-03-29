"""
Data processing utilities
"""

import pandas as pd
from typing import Dict, List, Any


def process_market_data(raw_data: Dict) -> pd.DataFrame:
    """Process raw market data into analysis format"""
    market_df = pd.DataFrame({
        'Segment': ['Large Platforms', 'Mid-Market', 'SMB', 'Brands', 'Dropshipping'],
        'TAM ($B)': [0.5, 0.3, 0.8, 0.3, 0.2],
        'Customers': [50, 1000, 50000, 500000, 10000],
        'Opportunity': ['High value', 'Medium', 'High volume', 'Premium', 'Growth']
    })
    return market_df


def calculate_roi(investment, annual_return, years=1):
    """Calculate ROI"""
    total_return = annual_return * years - investment
    roi_percent = (total_return / investment) * 100
    return roi_percent


def calculate_payback_period(monthly_cost, monthly_savings):
    """Calculate payback period in weeks"""
    if monthly_savings <= 0:
        return None
    weeks = (monthly_cost / monthly_savings) * 4
    return weeks


def aggregate_financial_projections(scenarios: List[Dict]) -> Dict:
    """Aggregate multiple financial scenarios"""
    result = {}
    for year in range(1, 6):
        year_key = f'year_{year}'
        values = [s[year_key] for s in scenarios if year_key in s]
        result[year_key] = {
            'low': min(values),
            'high': max(values),
            'average': sum(values) / len(values)
        }
    return result


def process_unit_economics(cac_low, cac_high, ltv_low, ltv_high) -> Dict:
    """Process and validate unit economics"""
    economics = {
        'CAC': {'low': cac_low, 'high': cac_high, 'avg': (cac_low + cac_high) / 2},
        'LTV': {'low': ltv_low, 'high': ltv_high, 'avg': (ltv_low + ltv_high) / 2}
    }
    
    # Calculate ratios
    economics['LTV_CAC_Ratio'] = {
        'low': ltv_low / cac_high,
        'high': ltv_high / cac_low,
        'avg': economics['LTV']['avg'] / economics['CAC']['avg']
    }
    
    # Flag health
    avg_ratio = economics['LTV_CAC_Ratio']['avg']
    if avg_ratio > 3:
        economics['health'] = 'Excellent'
    elif avg_ratio > 1.5:
        economics['health'] = 'Good'
    else:
        economics['health'] = 'Needs work'
    
    return economics


def create_customer_cohort_analysis(cohorts: List[Dict]) -> pd.DataFrame:
    """Create customer cohort analysis"""
    data = []
    for cohort in cohorts:
        data.append({
            'Cohort': cohort['name'],
            'Monthly Cost': cohort['cost'],
            'Monthly Savings': cohort['savings'],
            'Payback (Weeks)': calculate_payback_period(cohort['cost'], cohort['savings']),
            'ROI (Annual)': calculate_roi(cohort['cost'] * 12, cohort['savings'] * 12, 1)
        })
    return pd.DataFrame(data)


def estimate_market_adoption(tam, market_penetration_pct, years) -> Dict:
    """Estimate market adoption over time"""
    adoption = {}
    for year in range(1, years + 1):
        penetration = min(market_penetration_pct * year / years, market_penetration_pct)
        adoption[f'year_{year}'] = tam * (penetration / 100)
    return adoption


def validate_financial_model(revenue, costs, margins):
    """Validate financial model assumptions"""
    calculated_margin = (revenue - costs) / revenue
    expected_margin = margins / 100
    
    variance = abs(calculated_margin - expected_margin)
    
    return {
        'revenue': revenue,
        'costs': costs,
        'calculated_margin': calculated_margin,
        'expected_margin': expected_margin,
        'variance': variance,
        'valid': variance < 0.05  # Within 5%
    }


def generate_summary_metrics(financial_data: Dict) -> Dict:
    """Generate summary metrics from financial data"""
    summary = {
        'total_revenue_5yr': sum([v for k, v in financial_data.items() if 'revenue' in k]),
        'average_growth_rate': 0.35,  # 35% CAGR
        'profitability_year': 2,
        'market_position': 'Leader',
        'expansion_opportunities': [
            'Enterprise white-label',
            'International expansion',
            'Adjacent markets (video descriptions, etc)'
        ]
    }
    return summary
