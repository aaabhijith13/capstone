import streamlit as st
import pandas as pd
import os
import yfinance as yf
import requests
import matplotlib.pyplot as plt

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

def get_trend(current_price, previous_close):
    """Return 'up' if stock is trending upwards, 'down' otherwise, and 'unknown' if either value is None."""
    if current_price is None or previous_close is None:
        return 'unknown'
    return 'up' if current_price > previous_close else 'down'


# CSS for styling
st.markdown("""
<style>
body {
    font-family: 'Arial', sans-serif;
}

/* Setting the main background to white */
.css-1aumxhk {
    background-color: #FFFFFF;
}

/* Setting the sidebar background to white */
.css-j075dz, .css-1l02zno {
    background-color: #FFFFFF;
}

/* Setting font color to purple */
.css-901oao, .css-16my406, .css-1n6we3e {
    color: #800080;
}

.stButton > button {
    color: #800080;
    background-color: #FFFFFF;
    border: 1px solid #800080;
    transition: background-color 0.3s ease;
}
.stButton > button:hover {
    background-color: #800080;
    color: #FFFFFF;
}

/* CSS for scrollable news section */
.news-section {
    height: 100px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Stock Predictor")

# Pre-defined list of popular stocks (can be expanded)
stock_list = ["AMZN", "MSFT", "AAPL", "GOOGL"]
ticker = st.selectbox("Select a Stock Ticker to predict: ", stock_list)
options = ["Next 30 Day", "Next 60 Days", "Next 90 Days", "Next 130 Days"]
choice = st.sidebar.radio("Predict Adjusted Close Prices for: ", options)

# Action button
if st.sidebar.button("Predict"):
    left_name, right_name = st.columns(2)
    stock_info = yf.Ticker(ticker)
    info = stock_info.info
    with st.container():
        st.write(f"<h2 style='text-align: center; font-weight: bold;'>{info['longName']} - {ticker}</h2>", unsafe_allow_html=True)
        current_price = info.get('regularMarketPrice', None)
        previous_close = info.get('regularMarketPreviousClose', None)
        trend = get_trend(current_price, previous_close)
        trend_symbol = "🔼" if trend == "up" else "🔽"
    # with right_name:
    #     with st.container():
    #         st.write(f"{trend_symbol}")

    with st.container():  # Container for news and stock stats
        # Create two columns: one for news and one for stock details
        left_col, right_col = st.columns([4, 6])
        # Display news articles in a scrollable panel in the left column
        with left_col:
            news_data = get_news(ticker)
            left_col.markdown(f"<h3 style='text-align: center;'>Recent News for {ticker}</h2>", unsafe_allow_html=True)

            display_news_scrollable(news_data[:3])

        # Split stock details into left and right sections
        with right_col:
            right_col.markdown(f"<h3 style='text-align: center;'>Stats for {ticker}</h2>", unsafe_allow_html=True)

            # Left stats section
            stats_left, stats_right = right_col.columns(2)
            with stats_left:
                stats_left.markdown(f"<em>Volume:</em> {info.get('volume', 'N/A')}", unsafe_allow_html=True)
                stats_left.markdown(f"<em>Previous Close:</em> {previous_close}", unsafe_allow_html=True)
                stats_left.markdown(f"<em>Open:</em> ${info.get('regularMarketOpen', 'N/A')}", unsafe_allow_html=True)
                day_range = f"{info.get('regularMarketDayLow', 'N/A')} - {info.get('regularMarketDayHigh', 'N/A')}"
                stats_left.markdown(f"<em>Day's Range:</em> {day_range}", unsafe_allow_html=True)

            # Right stats section
            with stats_right:
                stats_right.markdown(f"<em>Market Cap:</em> ${info.get('marketCap', 'N/A')}", unsafe_allow_html=True)
                stats_right.markdown(f"<em>52 Week High:</em> ${info.get('fiftyTwoWeekHigh', 'N/A')}", unsafe_allow_html=True)
                stats_right.markdown(f"<em>52 Week Low:</em>${info.get('fiftyTwoWeekLow', 'N/A')}", unsafe_allow_html=True)
                stats_right.markdown(f"<em>PE Ratio:</em> {info.get('forwardPE', 'N/A')}", unsafe_allow_html=True)

            graph_col1, graph_col2 = st.columns(2)

            past_year = stock_info.history(period="5y")['Close']
            stats_left.markdown(f"<h3 style='text-align: center;'>Close Prices</h2>", unsafe_allow_html=True)
            stats_left.line_chart(past_year, height=300)

            # Display Sparkline for the last 5 years' Open data below stats_right
            past_year_open = stock_info.history(period="5y")['Open']
            stats_right.markdown(f"<h3 style='text-align: center;'>Open Prices</h2>", unsafe_allow_html=True)
            stats_right.line_chart(past_year_open, height=300)


    st.markdown(f"<h3 style='text-align: center;'>Predictions for {ticker}</h2>", unsafe_allow_html=True)

    csv_path = os.path.join("data", "results", "pred", f"{ticker}_data.csv")
    if os.path.exists(csv_path):
        data = pd.read_csv(csv_path)

        with st.container():  # Container for graph and table
            graph_col, table_col = st.columns(2)

            # Plot graph in the left column
            with graph_col:
                plt.figure(figsize=(10, 6))
                if choice == "Next 30 Day":
                    rows_to_display = data.tail(30)
                elif choice == "Next 60 Days":
                    rows_to_display = data.tail(60)
                elif choice == "Next 90 Days":
                    rows_to_display = data.tail(90)
                else:
                    rows_to_display = data
            with graph_col:
                graph_col.line_chart(rows_to_display.set_index('Date')[['Actual', 'Predictions']])


            # Display table data in the right column
            with table_col:
                table_col.write(rows_to_display)

    with st.container():  # Container for image
        plt.plot(rows_to_display['Date'], rows_to_display['Predictions'], label='Predictions')
        plt.plot(rows_to_display['Date'], rows_to_display['Actual'], label='Actual')
        plt.legend()
        plt.xticks(rotation=90)
        plt.title(f'{ticker} Predicted vs Actual Adjusted Close Prices')
        plt.xlabel("Dates from 2020 to 2023")
        plt.ylabel("Adjusted Close Prices")
        graph_col.pyplot(plt)


