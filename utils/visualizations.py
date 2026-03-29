"""
Visualization utilities for Streamlit presentation
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def create_revenue_chart(data):
    """Create revenue projection chart"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=['Y1', 'Y2', 'Y3', 'Y4', 'Y5'],
        y=data.get('revenue', []),
        mode='lines+markers',
        name='Revenue'
    ))
    return fig


def create_market_size_chart(tam, sam, som):
    """Create TAM/SAM/SOM visualization"""
    fig = go.Figure(data=[
        go.Bar(name='TAM', y=[tam]),
        go.Bar(name='SAM', y=[sam]),
        go.Bar(name='SOM', y=[som])
    ])
    return fig


def create_unit_economics_table(cac, ltv):
    """Create unit economics comparison"""
    data = {
        'Metric': ['CAC (Low)', 'CAC (High)', 'LTV (Low)', 'LTV (High)', 'Ratio'],
        'Value': [f'${cac[0]}', f'${cac[1]}', f'${ltv[0]}', f'${ltv[1]}', f'{ltv[0]/cac[1]}:1']
    }
    return pd.DataFrame(data)


def create_customer_roi_chart(segments):
    """Create customer ROI comparison"""
    fig = go.Figure()
    
    for segment, roi in segments.items():
        fig.add_trace(go.Bar(
            name=segment,
            y=[roi],
            text=[f'{roi}x'],
            textposition='outside'
        ))
    
    fig.update_layout(
        title='Customer ROI by Segment',
        yaxis_title='ROI Multiple',
        showlegend=True
    )
    return fig


def create_timeline_chart(milestones):
    """Create milestone timeline"""
    df = pd.DataFrame(milestones)
    fig = px.timeline(
        df,
        x_start='start',
        x_end='end',
        y='milestone',
        title='Project Timeline',
        labels={'milestone': 'Milestone', 'start': 'Start', 'end': 'End'}
    )
    return fig


def format_currency(value):
    """Format value as currency"""
    if value >= 1000000:
        return f'${value/1000000:.1f}M'
    elif value >= 1000:
        return f'${value/1000:.1f}K'
    else:
        return f'${value:.0f}'


def format_large_number(value):
    """Format large numbers with K/M/B suffix"""
    if value >= 1000000000:
        return f'{value/1000000000:.1f}B'
    elif value >= 1000000:
        return f'{value/1000000:.1f}M'
    elif value >= 1000:
        return f'{value/1000:.1f}K'
    else:
        return str(value)
