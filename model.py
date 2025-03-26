import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

def train_model(file_path='data/network_logs.csv', model_path='models/isolation_forest_model.pkl'):
    df = pd.read_csv(file_path)
    df.columns=['ip_address','bytes_sent','bytes_received','connections']
    X = df[['bytes_sent', 'bytes_received', 'connections']]
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)
    df['anomaly'] = model.predict(X)
    df.to_csv('data/network_logs_with_anomalies.csv', index=False)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
