# import libraries
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
import capm_function
from capm_function import interactive_plot, normalize_prices, calculate_beta

st.set_page_config(page_title="CAPM",
                   page_icon="chart_with_upwards_trend",
                
                   layout='wide')
st.title("Capital Asset Pricing Model")

#getting input from user 
col1,col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("choose 4 stocks", ('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),['TSLA','AAPL','AMZN','GOOGL'])
with col2:
    year = st.number_input("Number of years",1,10)

# downloading data for SP500
end = datetime.date.today()
start = datetime.date(datetime.date.today().year-year,datetime.date.today().month,datetime.date.today().day)
SP500 = yf.download('^GSPC', start=start, end=end)[['Close']]
SP500.rename(columns={'Close': 'sp500'}, inplace=True)
SP500.reset_index(inplace=True)
SP500['Date'] = pd.to_datetime(SP500['Date'])

stocks_df = pd.DataFrame()

for stock in stocks_list:
    data = yf.download(stock, start=start, end=end)[['Close']]
    data.rename(columns={'Close': stock}, inplace=True)
    data.reset_index(inplace=True)
    
    if stocks_df.empty:
        stocks_df = data
    else:
        stocks_df = pd.merge(stocks_df, data, on='Date', how='outer')


    
stocks_df.reset_index(inplace=True)
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])



# Merge with SP500
final_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

# Split date and time
final_df['Only_Date'] = final_df['Date'].dt.date
final_df['Only_Time'] = final_df['Date'].dt.time



# Optional: remove multilevel columns if they exist
if isinstance(final_df.columns, pd.MultiIndex):
    final_df.columns = final_df.columns.get_level_values(0)

# Select only required columns
columns_to_display = ['Only_Date', 'Only_Time'] + stocks_list + ['sp500']


col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### DataFrame Head")
    st.dataframe(stocks_df.head(), use_container_width=True)

with col2:
    st.markdown("### DataFrame Tail")
    st.dataframe(stocks_df.tail(), use_container_width=True)

# Flatten multi-level columns if any (precaution)
stocks_df.columns = [col if isinstance(col, str) else col[0] for col in stocks_df.columns]


from capm_function import interactive_plot

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Price of All the Stocks")
    fig = interactive_plot(stocks_df[['Date'] + stocks_list])  # Subset correct columns
    st.plotly_chart(fig, use_container_width=True)

from capm_function import interactive_plot, normalize_prices

# normalize data
normalized_df = normalize_prices(stocks_df[['Date'] + stocks_list])

# plot normalized prices
st.markdown("### Normalized Stock Prices (Base = 100)")
st.plotly_chart(interactive_plot(normalized_df), use_container_width=True)


from capm_function import interactive_plot, normalize_prices, calculate_daily_returns

# Example use:
daily_return_df = calculate_daily_returns(stocks_df[['Date'] + stocks_list])

st.markdown("### Daily Returns")
st.dataframe(daily_return_df.head(), use_container_width=True)

st.markdown("### Daily Returns Chart")
st.plotly_chart(interactive_plot(daily_return_df), use_container_width=True)

# Calculate beta and alpha for each stock

from capm_function import calculate_daily_returns  # make sure this function is defined

# Step 1: Combine stock data and S&P 500 into one DataFrame
returns_input_df = stocks_df[['Date'] + stocks_list].copy()
returns_input_df['sp500'] = SP500['sp500']  # merge or align by date if needed

# Step 2: Calculate daily returns
stocks_daily_return = calculate_daily_returns(returns_input_df)

beta = {}
alpha = {}

# Loop through each stock (excluding 'Date' and 'sp500')
for stock in stocks_daily_return.columns:
    if stock not in ['Date', 'sp500']:
        b, a = capm_function.calculate_beta(stocks_daily_return, stock)
        beta[stock] = b
        alpha[stock] = a

# Create a DataFrame for beta values
beta_df = pd.DataFrame({
    'Stock': list(beta.keys()),
    'Beta Value': [round(val, 2) for val in beta.values()]
})

# Display using Streamlit
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Calculated Beta Values")
    st.dataframe(beta_df, use_container_width=True)

rf = 0.045  # 4.5% annual risk-free rate
rm = stocks_daily_return['sp500'].mean() * 252  # Annualized market return

return_df = pd.DataFrame()
return_value = []

for stock, value in beta.items():
    expected_return = rf + value * (rm - rf)
    return_value.append(f"{expected_return * 100:.2f}%")

return_df['Stock'] = list(beta.keys())
return_df['Return Value (CAPM)'] = return_value

with col2:
    st.markdown('### Calculated Return using CAPM')
    st.dataframe(return_df, use_container_width=True)


