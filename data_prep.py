import numpy as np
import pandas as pd
import dbconnect as db
from sklearn.model_selection import train_test_split

def init_lstm():
    value_to_idx = 'dict value:idx'
    idx_to_value = 'dict idx:value'
    seq_size = 'Length of unique values'

    return value_to_idx,idx_to_value,len(seq_size)

def prep_dataset(path):
    df = pd.read_csv('path')
    mo = len(df) % 3
    if(mo != 0):
        df = df[:len(df)-mo]
    y = df['Date']
    X = df.drop('Date',  axis='columns', inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

    return X_train, X_test, y_train, y_test

#def cnn_dataset():


