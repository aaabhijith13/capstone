import streamlit as st
import pandas as pd
import os

# Sidebar
st.sidebar.title("Stock Predictor")

# Pre-defined list of popular stocks (can be expanded)
stock_list = ["AAPL", "GOOGL", "AMZN", "MSFT"]

# Multi-input for stock tickers using multiselect dropdown
tickers = st.sidebar.multiselect("Select a Stock Ticker to predict: ", stock_list)

# Choice of prediction duration
options = ["Next Day", "Next 7 Days", "Next 14 Days", "Next 30 Days"]
choice = st.sidebar.radio("Predict Adjusted Close Prices for: ", options)

# Action button
if st.sidebar.button("Predict"):

    for ticker in tickers:
        # Path for image and CSV
        image_path = os.path.join("images", f"predictions_{ticker}.png")
        csv_path = os.path.join("data", f"{ticker}_data.csv")

        # Display image
        if os.path.exists(image_path):
            st.image(image_path, caption=f"Prediction for {ticker}")

        # Display table data from CSV
        if os.path.exists(csv_path):
            data = pd.read_csv(csv_path)
            st.write(data)

# To run the app, you would use the command: streamlit run your_script_name.py
