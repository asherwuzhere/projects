# Uses stock market data found with prev_years_market_data.py to train the model and then uses current_market_data.py to actually run the model.

# MODEL OVERVIEW: For training, each stock is given a score of either 1 or 0. 1 meaning beats S&P 500 and 0 meaning loses to S&P 500 during a 52 week period. The model is then given a bunch of datapoints found with yfinance for each stock which is used to train the model to find patterns between companies that beat the S&P 500 and their datapoints. Once finished this training, the model is given this years stock market data and attempts to predict how the stock will perform compared to S&P 500.

# THIS IS NOT FINANCIAL ADVICE: You should always seek advice from a qualified financial advisor before making any financial decisions.

import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np

# Load dataset
dataset = pd.read_csv('stock_financial_analysis.csv')

# Prepare features and labels
x = dataset.drop(columns=["Ticker", "Price Change Last Year", "S&P 500 Change Last Year", "Beats S&P 500 (1=yes, 0=no)"])
y = dataset["Beats S&P 500 (1=yes, 0=no)"]

# Ensure numerical values (convert and fill missing)
x = x.apply(pd.to_numeric, errors='coerce').fillna(0)

# Split dataset
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Convert to NumPy arrays and ensure float32 type
x_train = np.array(x_train, dtype=np.float32)
x_test = np.array(x_test, dtype=np.float32)
y_train = np.array(y_train, dtype=np.float32)
y_test = np.array(y_test, dtype=np.float32)

# Print shape of x_train to verify it's (num_samples, num_features)
print("x_train shape:", x_train.shape)  # Debugging step

# Build the model with dropout and L2 regularization
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(256, input_shape=(x_train.shape[1],), activation='sigmoid',
                          kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(256, activation='sigmoid', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Add Early Stopping
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=50, restore_best_weights=True)

# Train the model with validation split
model.fit(x_train, y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

# Evaluate the model
loss, accuracy = model.evaluate(x_test, y_test)

# Print the results clearly
print(f"Test Loss: {loss:.4f}")
print(f"Test Accuracy: {accuracy:.4f}")
