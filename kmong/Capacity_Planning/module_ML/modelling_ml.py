import pandas as pd
import numpy as np
from sklearn import svm, metrics
from sklearn.metrics import accuracy_score, roc_curve, auc, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV

def modelling(X_train, X_test, X_valid, Y_train, Y_test, Y_valid, params, model, y_scaler_tr, y_scaler_te):
    grid = GridSearchCV(model, params, cv=5, n_jobs = -1, scoring="neg_mean_squared_error", return_train_score = True)
    grid = grid.fit(X_train, Y_train)
    model = grid.best_estimator_
    Y_test_pred = model.predict(X_test)
    Y_valid_pred = model.predict(X_valid)
    #print("model_name : ", model.__repr__().split('(')[0])
    #print("best params : ", grid.best_params_)  
    
    # MAE 등 성능 평가를 위해 MinMaxScaler 역변환
    Y_test_pred = Y_test_pred.reshape(Y_test_pred.size, 1)
    Y_valid_pred = Y_valid_pred.reshape(Y_valid_pred.size, 1)
    
    unnormalized_Y_test_pred = y_scaler_te.inverse_transform(Y_test_pred)
    unnormalized_Y_valid_pred = y_scaler_tr.inverse_transform(Y_valid_pred)

    Y_test = Y_test.reshape(Y_test.size, 1)
    Y_valid = Y_valid.reshape(Y_valid.size, 1)
    
    unnormalized_Y_test = y_scaler_te.inverse_transform(Y_test)
    unnormalized_Y_valid = y_scaler_tr.inverse_transform(Y_valid)
    
    return unnormalized_Y_test, unnormalized_Y_test_pred, unnormalized_Y_valid, unnormalized_Y_valid_pred, model

def evaluation(unnormalized_Y_test, unnormalized_Y_test_pred):
     
    Test_mae = MAE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_mse = MSE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_rmse = RMSE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_mape = MAPE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_mpe = MPE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_r2 = r2_score(unnormalized_Y_test, unnormalized_Y_test_pred)
    lst_result = [Test_mae, Test_mse, Test_rmse, Test_mape, Test_mpe, Test_r2]
    #참고용 Y_test의 평균치
    unnormalized_Y_test_Avg = np.average(unnormalized_Y_test)

    #print(f"Model               : LSTM")
    
    #print('Target Variable Avg : %.2f'   %(unnormalized_Y_test_Avg))
    print('R2                  : %.4f' %(Test_r2))  
    print('MAE                 : %.2f' %(Test_mae))
    print('MSE                 : %.2f' %(Test_mse))
    print('RMSE                : %.2f' %(Test_rmse))
    print('MAPE                : %.2f' %(Test_mape))
    print('MPE                 : %.2f' %(Test_mpe))
    #print('=========================================================================================================================')
    #print('========================================================================================================================\n')
    return lst_result

# 성능 평가 및 과적합 검증
def MAE(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred)))
def MSE(y_true, y_pred):
    return np.mean(np.square((y_true - y_pred)))
def RMSE(y_true, y_pred):
    return np.sqrt(MSE(y_true, y_pred))
def MAPE(y_true, y_pred): 
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
def MPE(y_true, y_pred): 
    return np.mean((y_true - y_pred) / y_true) * 100