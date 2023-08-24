import streamlit as st
import requests
import numpy as np
#import matplotlib.pyplot as plt

def main():
    st.markdown("<h1 style='text-align: center; color: white;'>Stock Price Prediction</h1>", unsafe_allow_html=True)

    # Collect input from the user
    stock = st.selectbox('Select a stock:', ['AAPL', 'TLSA', 'GOOGL'])
    days = st.slider('Number of days to predict:', 1, 30)

    # When user clicks the 'Predict' button, send data to SageMaker
    if st.button('Predict'):
        

        # Make the request to the SageMaker endpoint
        # response = requests.post(endpoint_url, json=payload)
        # predictions = response.json().get('predictions', [])

        # Display the predictions as a graph
        # plt.figure(figsize=(10, 6))
        # plt.plot(np.arange(len(predictions)), predictions, '-o')
        # plt.title(f"Predicted Prices for {stock} over {days} Days")
        # plt.xlabel("Days")
        # plt.ylabel("Predicted Price")
        # st.pyplot(plt)

if __name__ == "__main__":
    main()
