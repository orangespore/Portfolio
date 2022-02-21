import numpy as np
import pandas as pd

def load_data(path):
    df = pd.read_excel(path)
    df['Date']= pd.to_datetime(df['Date'], format='%Y%m%d')
    df_ts = pd.Series(df['N_Order'])
    df_ts.index = df['Date'].values
    df_ts = df_ts[:].astype(np.float)
    return df_ts

def split_data(df_ts):
    train_size = int(len(df_ts)*.7)
    valid_size = int(len(df_ts)*.1)

    features_train = df_ts.iloc[0:train_size]
    features_valid = df_ts.iloc[train_size+1:train_size+valid_size]
    features_test = df_ts.iloc[train_size+valid_size+1:]
    
    return features_train, features_valid, features_test