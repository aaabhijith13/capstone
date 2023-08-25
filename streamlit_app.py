import streamlit as st
import pandas as pd
import os
import yfinance as yf
import requests

API_KEY = '0999f084017643be9b8dc053c3a258e3'
ENDPOINT = 'https://newsapi.org/v2/everything'


def get_news(ticker):
    news_data = []
    params = {
        'q': ticker,
        'apiKey': API_KEY
    }
    response = requests.get(ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        return []


def display_news(articles, ticker):
    # Set the title to the ticker value and center it

    # Display the articles in batches of 3 in each row
    for i in range(0, len(articles), 3):
        batch = articles[i:i + 3]
        cols = st.columns(len(batch))  # Create columns for the current batch of articles

        for j, article in enumerate(batch):
            with cols[j]:  # Use the j-th column
                # Display the image in the column with rounded corners
                st.markdown(
                    f"<div style='border-radius: 15px; overflow: hidden;'><img src='{article['urlToImage']}' style='border-radius: 15px;' width='100%'></div>",
                    unsafe_allow_html=True)

                # Display the bold title in the column
                st.markdown(f"**{article['title']}**")


def display_news_scrollable(articles):
    for article in articles:
        # Display the image for the article
        st.image(article['urlToImage'], use_column_width=True)

        # Display the title for the article, making it clickable
        st.markdown(f"[**{article['title']}**]({article['url']})")


# CSS for styling
st.markdown("""
<style>
body {
    color: #333332;
    font-family: 'Arial', sans-serif;
    background-color: #400090;
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

# Input for stock tickers using multiselect dropdown
ticker = st.selectbox("Select a Stock Ticker to predict: ", stock_list)

# Choice of prediction duration
options = ["Next Day", "Next 7 Days", "Next 14 Days", "Next 30 Days"]
choice = st.sidebar.radio("Predict Adjusted Close Prices for: ", options)

# Action button
if st.sidebar.button("Predict"):
    stock_info = yf.Ticker(ticker)
    info = stock_info.info  # Fetching the stock details

    # Create two columns: one for news and one for stock details
    left_col, right_col = st.columns(2)

    # Display news articles in a scrollable panel in the left column
    with left_col:
        news_data = get_news(ticker)
        left_col.subheader('Recent News')
        display_news_scrollable(news_data[:6])  # Display the first 6 articles

    # Display stock details in the right column
    with right_col:
        right_col.subheader(f"Statisfor {info['longName']}")
        right_col.write(f"**{info['longName']} ({ticker})**")  # Display the stock name
        right_col.write(f"**Current Price:** ${info['regularMarketPrice'] if 'regularMarketPrice' in info else 'N/A'}")
        right_col.write(f"**Market Cap:** ${info['marketCap'] if 'marketCap' in info else 'N/A'}")
        right_col.write(f"**52 Week High:** ${info['fiftyTwoWeekHigh'] if 'fiftyTwoWeekHigh' in info else 'N/A'}")
        right_col.write(f"**52 Week Low:** ${info['fiftyTwoWeekLow'] if 'fiftyTwoWeekLow' in info else 'N/A'}")

    # Path for image and CSV
    image_path = os.path.join("Images", f"{ticker}_predictions.png")
    csv_path = os.path.join("data", "results", f"{ticker}_data.csv")
    print(csv_path)

    # Display image
    if os.path.exists(image_path):
        st.image(image_path, caption=f"Prediction for {ticker}")

    # Display table data from CSV
    if os.path.exists(csv_path):
        data = pd.read_csv(csv_path)
        # print(csv_path)
        # st.line_chart(data=data, x="Actual", y="Predictions", width=0, height=0, use_container_width=True)

        st.write(data)

