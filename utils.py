import pandas as pd
import numpy as np
import os

def generate_dataset(file_path='data/network_logs.csv'):
    if not os.path.exists(file_path):
        os.makedirs('data', exist_ok=True)
        data = {
            'ip_address': [f'192.168.1.{i % 255}' for i in range(1000)],
            'bytes_sent': np.random.randint(100, 10000, 1000),
            'bytes_received': np.random.randint(100, 10000, 1000),
            'connections': np.random.randint(1, 50, 1000)
        }
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
    print(f"Dataset saved at {file_path}")
