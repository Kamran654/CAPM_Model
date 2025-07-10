import plotly.graph_objects as go

def interactive_plot(df):
    fig = go.Figure()

    for i in df.columns[1:]:
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[i],
            mode='lines',
            name=str(i)  # ✅ Yahan fix hai: i ko string bana diya
        ))

    fig.update_layout(
        title="Stock Prices Over Time",
        width=700,
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        xaxis_title='Date',
        yaxis_title='Price',
    )

    return fig

# function to normalize the price based on the initial  price

import plotly.graph_objects as go

# 📉 1. Plotting function
def interactive_plot(df):
    fig = go.Figure()

    for i in df.columns[1:]:  # Skipping 'Date'
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[i],
            mode='lines',
            name=str(i)  # Convert name to string to avoid error
        ))

    fig.update_layout(
        title="Stock Prices Over Time",
        width=700,
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        xaxis_title='Date',
        yaxis_title='Price',
    )

    return fig

# 📊 2. Normalization function
def normalize_prices(df):
    df_normalized = df.copy()
    for col in df.columns[1:]:  # Skip the 'Date' column
        df_normalized[col] = df[col] / df[col].iloc[0] * 100
    return df_normalized


#function to calculate daily returns

import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

# 🔹 Function 1: Plot interactive line chart
def interactive_plot(df):
    fig = go.Figure()
    for i in df.columns[1:]:  # skip the Date column
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[i],
            mode='lines',
            name=str(i)
        ))

    fig.update_layout(
        width=800,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig

# 🔹 Function 2: Normalize prices (base = 100)
def normalize_prices(df):
    df_normalized = df.copy()
    for col in df.columns[1:]:  # skip Date
        df_normalized[col] = df[col] / df[col].iloc[0] * 100
    return df_normalized

# 🔹 Function 3: Calculate daily returns
def calculate_daily_returns(df):
    """
    Calculate daily returns of stock prices as percentage change.
    """
    df_returns = df.copy()
    df_returns.set_index('Date', inplace=True)
    df_returns = df_returns.pct_change().dropna()
    df_returns.reset_index(inplace=True)
    return df_returns

import numpy as np

def calculate_beta(stocks_daily_return, stock):
    # Annualized average market return (optional, not used here)
    rm = stocks_daily_return['sp500'].mean() * 252  

    # Calculate beta and alpha using linear regression
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)

    return b, a

def calculate_beta(stocks_daily_return, stock):
    if stock not in stocks_daily_return.columns:
        raise ValueError(f"{stock} not found in DataFrame columns.")

    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)
    return b, a
