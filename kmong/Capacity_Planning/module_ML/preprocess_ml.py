import pandas as pd
import numpy as np
import seaborn as sns
#import plotly.express as px
import matplotlib.pyplot as plt
from collections import Counter
from xgboost import XGBRegressor
from sklearn import svm, metrics
from sklearn.pipeline import Pipeline
from sklearn import linear_model as lm
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTENC
from sklearn.linear_model import Ridge, Lasso
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler
from sklearn.metrics import accuracy_score, roc_curve, auc, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV

def load_data(path):
    df = pd.read_excel(path)
    df['Date']= pd.to_datetime(df['Date'], format='%Y%m%d')
    return df

def save_data_corr(df, path_corr):
    df_corr = df.corr(method = 'pearson').to_excel(path_corr)

def preprocess_data_lag(df, Selected_Features, X, Y):
    dynamic_feature_str =""
    for i in Selected_Features:
        j = 0
        while j < X:
            dynamic_feature_str = dynamic_feature_str + " {}_T{}".format(i, j+1)
            j=j+1

    dynamic_feature_list = dynamic_feature_str.split()
    df_sel = df[Selected_Features]
    df_lag = pd.DataFrame(index = df_sel.index, columns = dynamic_feature_list, dtype = np.float64)

    for i in Selected_Features:
        j = 0
        from_feature =i
        while j < X:
            to_feature = from_feature + "_T{}".format(j+1)
            df_lag[to_feature] = df_sel[from_feature].shift(j+1)
            j = j + 1
    df_lag = df_lag.dropna(axis=0)
    return df_lag
    
def generate_target(df_lag, df, Selected_Features, Y):
    df_sel = df[Selected_Features]
    df_max = pd.DataFrame(index = df_lag.index, columns = ['Max_Capacity'], dtype = np.float64)

    for i in df_lag.index:
        if i < max(df_lag.index) - Y+1:
            df_max.loc[i,'Max_Capacity'] = df_sel.iloc[i,0]
            j = 0
            while j < Y:
                if df_max.loc[i,'Max_Capacity'] < df_sel.iloc[i+j+1,0]:
                    df_max.loc[i,'Max_Capacity'] = df_sel.iloc[i+j+1,0]
                j = j + 1
    return df_max

def generate_dataset(df1, df2, path_data_full):
    df1['Max_Capacity'] = df2.values
    df_lag = df1
    df_lag = df_lag.dropna(axis=0)
    df_lag.to_excel(path_data_full, index = False) 
    return df_lag

def remove_columns(df, lst_cols_remove):
    df = df.drop(columns=lst_cols_remove)
    return df

def transform_data(df):
    for i in df.columns:
        if df[i].skew()>=3:
            df[i] = np.log1p(df[i])
        else:
            pass
    return df

def detect_outliers(df, n, features): 
    outlier_indices = [] 
    for col in features: 
        Q1 = np.percentile(df[col], 25) 
        Q3 = np.percentile(df[col], 75) 
        IQR = Q3 - Q1 
        outlier_step = 1.5 * IQR 
        outlier_list_col = df[(df[col] < Q1 - outlier_step) | (df[col] > Q3 + outlier_step)].index 
        outlier_indices.extend(outlier_list_col) 
    outlier_indices = Counter(outlier_indices) 
    return outlier_indices

def generate_data_outlier(df, cnt_cols, lst_cols):
    lst_date = df.index
    df = df.reset_index(drop=True)
    df['Date']=lst_date
    Outliers_to_drop = detect_outliers(df, cnt_cols, lst_cols)
    df = df.drop(index=Outliers_to_drop).reset_index(drop=True)
    df.index = df['Date']
    del df['Date']
    return df
    
def generate_XY(df):
    x_df = df.drop(columns=["Max_Capacity"])
    y = df["Max_Capacity"]
    y_df = pd.DataFrame(data = y, dtype = np.float64)
    return x_df, y_df

def preprocess_XY(x_df, y_df, X):
    x_scaler_tr = MinMaxScaler(feature_range = (0,1))
    x_scaler_te = MinMaxScaler(feature_range = (0,1))
    y_scaler_tr = MinMaxScaler(feature_range = (0,1))
    y_scaler_te = MinMaxScaler(feature_range = (0,1))
    
    X_train, X_test, Y_train, Y_test = train_test_split(x_df, y_df.values.ravel(), test_size=.2)
    # (확인 필요) 이부분은 어디에 사용하였더라? 시간에 따라 나누지도 않는데, lstm등 다른 모듈의 재사용성 때문인가?
    lst_test_date = X_test.index
    #x_df_tr = pd.DataFrame(data = x_df_cln_tr, columns = x_df.columns, dtype = np.float64)
    #x_df_te = pd.DataFrame(data = x_df_cln_te, columns = x_df.columns, dtype = np.float64)

    #y_df_tr = pd.DataFrame(data = y_df_cln_tr, columns = y_df.columns, dtype = np.float64)
    #y_df_te = pd.DataFrame(data = y_df_cln_te, columns = y_df.columns, dtype = np.float64)
    
    #num_transformer = SimpleImputer(strategy="constant", fill_value = 0)
    #preprocessor = ColumnTransformer(transformers=[("num", num_transformer, X)])

    X_train, X_valid, Y_train, Y_valid = train_test_split(X_train, Y_train, test_size=.1)
    X_train = x_scaler_tr.fit_transform(X_train.values)
    X_valid = x_scaler_tr.fit_transform(X_valid.values)
    X_test = x_scaler_te.fit_transform(X_test.values)
    Y_train = y_scaler_tr.fit_transform(Y_train.reshape(-1,1))
    Y_valid = y_scaler_tr.fit_transform(Y_valid.reshape(-1,1))
    Y_test = y_scaler_te.fit_transform(Y_test.reshape(-1,1))
    
    return X_train, X_test, X_valid, Y_train, Y_test, Y_valid, y_scaler_tr, y_scaler_te, lst_test_date