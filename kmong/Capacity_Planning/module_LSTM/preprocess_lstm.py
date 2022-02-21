import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

def load_data(file_name, look_back, split, cols):
    df = pd.read_excel(file_name)
    data_all = df.copy()#np.array(df).astype(float)
    
    # 이부분은 추후 교수님의 말씀대로 training의 scaling 이후 추출되는 각 feature들의 mean, std 값을 이용하여
    # test의 동일한 feature들에 대해서 featurewise scaling normalization을 수행하는 것으로 코드 변경 예정
    scaler_x_tr = MinMaxScaler()
    scaler_x_te = MinMaxScaler()
    scaler_x_va = MinMaxScaler()
    scaler_y_tr = MinMaxScaler()
    scaler_y_te = MinMaxScaler()
    scaler_y_va = MinMaxScaler()

    train_size = int(len(data_all) * 0.7)
    valid_size = int(len(data_all) * 0.1)
    train, test = data_all.iloc[0:train_size, :], data_all.iloc[train_size - look_back:len(data_all), :]
    valid, test = test.iloc[0:valid_size, :], test.iloc[valid_size - look_back:len(test), :]
    
    #print(train.shape)
    #print(valid.shape)
    #print(test.shape)
    
    lst_test_date = test.Date
    lst_valid_date = valid.Date
    train.drop(['Date'], axis=1, inplace=True)
    valid.drop(['Date'], axis=1, inplace=True)
    test.drop(['Date'], axis=1, inplace=True)
    
    lst_cols_x = list(set(cols)-set(["N_Order"]))
    cols_y = "N_Order"

    train[lst_cols_x] = scaler_x_tr.fit_transform(train[lst_cols_x].values)
    test[lst_cols_x] = scaler_x_te.fit_transform(test[lst_cols_x].values)
    valid[lst_cols_x] = scaler_x_va.fit_transform(valid[lst_cols_x].values)

    train[cols_y] = scaler_y_tr.fit_transform(train[cols_y].values.reshape(-1,1))
    test[cols_y] = scaler_y_te.fit_transform(test[cols_y].values.reshape(-1,1))
    valid[cols_y] = scaler_y_va.fit_transform(valid[cols_y].values.reshape(-1,1))
 
    # Tensorflow 2에서 LSTM에 input으로 넣을 때 float32로 강제로 casting을 하므로, warning을 없애기 위해서 사전에 float32 type으로 변경 
    train = train[cols].values.astype(np.float32)
    test = test[cols].values.astype(np.float32)
    valid = valid[cols].values.astype(np.float32)
    
    return train, test, valid, scaler_y_tr, scaler_y_te, lst_test_date, lst_valid_date

#LSTM에 신경망에 넣을 데이터셋 가공
def create_dataset(dataset, look_back):

    data_x, data_y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), :]
        data_x.append(a)
        data_y.append(dataset[i + look_back, -1])
    return np.array(data_x), np.array(data_y)