# Stock Market Analysis and Prediction - Udacity Capstone Machine Learning Engineer Project

## Domain Background
Stock market analysis and prediction have been crucial areas of study in finance. Over the years, numerous methods ranging from fundamental analysis, technical analysis, and more recently, artificial intelligence and machine learning have been employed to predict stock prices. Traditional techniques such as fundamental analysis delve deep into a company's financial statements, market trends, and macroeconomic variables. This project aims to leverage historical stock data from companies like Google, Amazon, Microsoft and Apple alongside financial indicators, to forecast future stock prices.

## Problem Statement
The primary objective is to develop a predictive model that can accurately forecast 5% of the future price movement (next day, within the next 7 days, or up to 14 days and up to 30 days.) of a given stock. The final predictor for the problem will be the Adjusted Close value. The testing data is till 3/23/2023.

## Datasets and Inputs
The project will utilize historical stock data sourced from Yahoo Finance, which typically includes:

- **Open Price**: Starting trading price for a period.
- **Close Price**: Final trading price for a period.
- **High Price**: Maximum price during a period.
- **Low Price**: Minimum price during a period.
- **Adjusted Close Price**: Closing price adjusted for dividends, stock splits, etc.
- **Date**: The date of the stock data.

Initial stocks under consideration:
- Apple - "AAPL"
- Amazon - "AMZN"
- Microsoft - "MSFT"
- Google - "GOOGL"

## Solution Statement
During the EDA and after further research, I found out that it would be better to utilize a univariate model, instead of utilizing a multi-variate approach, as the variables - Open, Close, High, Low and Adjusted Prices are all highly correlated amongst each other. Hence, utilizing a univariate model with Adj Close was the only variable used for analysis. A time window (time steps) was utilized around 7 days, of data was used to predict 1 day. So the previous 7 days of Adjusted Close data would be used to predict the next days data. The data was split into 80-10-10 split of train-validation-test. LSTM (Long Short-Term Memory) model, a type of recurrent neural network (RNN), will be employed using PyTorch to make predictions. LSTM networks are adept at capturing long-term dependencies in sequential data, making them apt for stock forecasting. The model will be trained on up to 3 years of data, from 2020 to 2023.

## Benchmark Model
A suitable benchmark model for stock forecasting could be:
- A simple LSTM Model that will compute the MSE with an Input layer of 7,1 - time steps, features
- 64 LSTM units
- Adam Optimizer with learning rate of 0.001
- 50 Epochs
- Metrics - Mean Absolute Error, Val Loss

## Evaluation Metrics
To assess the performance of the predictive model, the following metrics will be employed:
- Mean Absolute Error -  MAE is less sensitive to outliers. In the context of stock prices, sudden spikes or drops.
- Validation Loss - Validation loss provides an indication of how well the model is generalizing to new, unseen data. By monitoring the validation loss during training, you can detect overfitting early on.


## Project Design
1. **Data Collection**: Retrieve the past 10 years of historical stock data for selected symbols.
2. **Data Preprocessing**: Cleanse the data, handle missing values, and format it for analysis. Conduct EDA of data. 
3. **Model Development and Evaluation**: Train deep learning models and evaluate their performance against the benchmark model using the chosen metrics.
4. **Model Fine-tuning**: Adjust model hyperparameters based on evaluation results.
5. **Prediction and Analysis**: Apply the model to forecast future stock prices and compare predictions against current trends.
6. **Interface and Visualization**: Showcase the findings using visualizations on platforms like GitHub. A user-friendly interface will be built using Streamlit and deployed on Streamlit cloud enviorment. Users can select from the available symbols and request predictions for specific date ranges.

## Additional Suggestions to Increase Project Complexity
1. **Sentiment Analysis**: Incorporate news sentiment analysis to gauge the impact of news on stock price movements. With more time, this would defentively be a good input for the analysis. Stock Prices alone aren't good indicators for predicting prices as the stock market is much more volatility and depth to it, utilization of current events through the use of news API will yield better results. 
2. **Incorporate Macroeconomic Data**: Use macroeconomic indicators like GDP growth, interest rates, and unemployment rates to enhance predictions.
3. **Real-time Prediction**: Implement a real-time stock price prediction feature using live data feeds. Utilizing Sagemaker Multi-model Endpoint to make real-time predictions for multiple stocks and the main app can be hosted using an EC2 instance. 

