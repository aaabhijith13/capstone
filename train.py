import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
import argparse
import os
import logging
import sys
import boto3 

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

def test(model, test_loader):
    loss, _ = model.evaluate(test_loader, verbose=1)
    logger.info(f"Testing Loss: {loss}")

def train(model, train_loader, validation_loader, epochs):
    history = model.fit(train_loader, validation_data=validation_loader, epochs=epochs)
    val_mae = history.history.get('val_mae') or history.history.get('val_mean_absolute_error')
    val_mae = val_mae[-1]
    logger.info(f"Validation MAE: {val_mae}")  # Logging the validation MAE
    return model

def model_fn(learning_rate, lstm_units, dense_units):
    model = Sequential([
        layers.Input((3, 1)),
        layers.LSTM(lstm_units),  # Using lstm_units parameter
        layers.Dense(dense_units, activation='relu'),  # First Dense layer using dense_units parameter
        layers.Dense(dense_units, activation='relu'),
        layers.Dense(1)
    ])
    
    optimizer = Adam(learning_rate=learning_rate)  # Using learning_rate parameter
    model.compile(optimizer=optimizer, loss='mse',  metrics=['mae'])
    
    return model



def create_data_loaders(batch_size):
    train_data_path = os.environ['SM_CHANNEL_TRAIN']
    validation_data_path = os.environ['SM_CHANNEL_VALID']
    test_data_path = os.environ['SM_CHANNEL_TEST']
    
    # Load Training Data
    X_train = np.load(os.path.join(train_data_path, "X.npy"))
    y_train = np.load(os.path.join(train_data_path, "y.npy"))
    
    # Load Validation Data
    X_val = np.load(os.path.join(validation_data_path, "X.npy"))
    y_val = np.load(os.path.join(validation_data_path, "y.npy"))

    # Load Testing Data
    X_test = np.load(os.path.join(test_data_path, "X.npy"))
    y_test = np.load(os.path.join(test_data_path, "y.npy"))
    
    train_loader = tf.data.Dataset.from_tensor_slices((X_train, y_train)).batch(batch_size)
    test_loader = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(batch_size)
    validation_loader = tf.data.Dataset.from_tensor_slices((X_val, y_val)).batch(batch_size)
    
    return train_loader, test_loader, validation_loader

def main(args):
    
    train_loader, test_loader, validation_loader = create_data_loaders(args.batch_size)
    model = model_fn(args.learning_rate, args.lstm_units, args.dense_units)

    logger.info("Starting Model Training")
    model = train(model, train_loader, validation_loader, args.epochs)
    
    logger.info("Testing Model")
    test(model, test_loader)
    
    logger.info("Saving Model")
    local_model_path = "/tmp/model.h5"
    model.save(local_model_path)
    s3 = boto3.client('s3')
    s3.upload_file(local_model_path, 'sagemaker-us-east-1-464589117859','finalModels/model.h5')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning-rate', type=float)
    parser.add_argument('--lstm_units', type=int)
    parser.add_argument('--dense_units', type=int)
    parser.add_argument('--batch-size', type=int, default= 32)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--train', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    parser.add_argument('--valid', type=str, default=os.environ['SM_CHANNEL_VALID'])
    parser.add_argument('--test', type=str, default=os.environ['SM_CHANNEL_TEST'])

    parser.add_argument('--model_dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--output-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    
    args = parser.parse_args()
    print(args)
    
    main(args)
