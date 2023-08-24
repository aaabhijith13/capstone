import streamlit as st
import pandas as pd
import os
import yfinance as yf
import requests

API_KEY = '0999f084017643be9b8dc053c3a258e3'
ENDPOINT = 'https://newsapi.org/v2/everything'

def get_news(ticker):
    params = {
        'q': ticker,
        'apiKey': API_KEY
    }
    response = requests.get(ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        return []

# CSS for styling
st.markdown("""
<style>
body {
    color: #333333;
    font-family: 'Arial', sans-serif;
    background-color: #f7f7f7;
}
.stButton > button {
    color: #fff;
    background-color: #400090;
}
</style>
""", unsafe_allow_html=True)


# Sidebar
st.sidebar.title("Stock Predictor")

# Pre-defined list of popular stocks (can be expanded)
stock_list = ["AAPL", "GOOGL", "AMZN", "MSFT"]

# Multi-input for stock tickers using multiselect dropdown
ticker = st.selectbox("Select a Stock Ticker to predict: ", stock_list)

# Choice of prediction duration
options = ["Next Day", "Next 7 Days", "Next 14 Days", "Next 30 Days"]
choice = st.sidebar.radio("Predict Adjusted Close Prices for: ", options)

# Action button
if st.sidebar.button("Predict"):
    stock_info = yf.Ticker(ticker)
    news_data = get_news(ticker)
    st.subheader('Recent News')
    for article in news_data[:3]:  # Display top 3 news articles
        st.write(f"**{article['title']}**")
        st.write(article['description'])
        st.image(article['urlToImage'])
        info = stock_info.info
    
    # Display stock details
    st.write(f"**{info['longName']} ({ticker})**")
    st.write(f"**Current Price:** ${info['regularMarketPrice'] if 'regularMarketPrice' in info else 'N/A'}")
    st.write(f"**Market Cap:** ${info['marketCap'] if 'marketCap' in info else 'N/A'}")
    st.write(f"**52 Week High:** ${info['fiftyTwoWeekHigh'] if 'fiftyTwoWeekHigh' in info else 'N/A'}")
    st.write(f"**52 Week Low:** ${info['fiftyTwoWeekLow'] if 'fiftyTwoWeekLow' in info else 'N/A'}")


    
    # Placeholder for news (this is just a mockup, in reality you'd want to fetch real news data)
    st.subheader('Recent News')
    st.write("1. Stock XYZ has reached an all-time high!")
    st.write("2. Analysts predict a bullish trend for Stock XYZ.")
    st.write("3. Stock XYZ announces quarterly dividends.")

    # Path for image and CSV
    image_path = os.path.join("Images", f"{ticker}_predictions.png")
    csv_path = os.path.join("data","results", f"{ticker}_data.csv")
    print(csv_path)

    # Display image
    if os.path.exists(image_path):
        st.image(image_path, caption=f"Prediction for {ticker}")

    # Display table data from CSV
    if os.path.exists(csv_path):
        data = pd.read_csv(csv_path)
        #print(csv_path)
        #st.line_chart(data=data, x="Actual", y="Predictions", width=0, height=0, use_container_width=True)

        st.write(data)

# To run the app, you would use the command: streamlit run your_script_name.py
