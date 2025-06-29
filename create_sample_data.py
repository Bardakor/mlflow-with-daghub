#!/usr/bin/env python3
"""
Create sample dataset for the ML pipeline.
This ensures we always have data available, even if DVC fails.
"""

import os
import pandas as pd
import numpy as np
from sklearn.datasets import load_digits

def create_sample_data():
    """Create sample dataset from sklearn digits dataset"""
    print("Creating sample dataset...")
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    
    # Load sklearn digits dataset
    digits = load_digits()
    
    # Create DataFrame
    feature_names = [f"pixel_{i}" for i in range(digits.data.shape[1])]
    df = pd.DataFrame(digits.data, columns=feature_names)
    df['target'] = digits.target
    
    # Save to CSV
    csv_path = "data/raw_dataset.csv"
    df.to_csv(csv_path, index=False)
    
    print(f"Sample dataset created: {csv_path}")
    print(f"Dataset shape: {df.shape}")
    print(f"File size: {os.path.getsize(csv_path) / 1024 / 1024:.1f} MB")
    
    return csv_path

if __name__ == "__main__":
    create_sample_data() 