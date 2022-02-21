import math
import warnings
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import accuracy_score, roc_curve, auc, mean_absolute_error, r2_score, mean_squared_error

# evaluate an ARIMA model for a given order (p,d,q)
def evaluate_arima_model(train, test, arima_order):
    # prepare training dataset
    history = [x for x in train]
    # make predictions
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=arima_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
    # calculate out of sample error
    error = mean_squared_error(test, predictions)
    
    return error, predictions

# evaluate combinations of p, d and q values for an ARIMA model
def evaluate_models(train, valid, test, p_values, d_values, q_values):
    best_score, best_cfg = float("inf"), None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p,d,q)
                try:
                    mse, predictions = evaluate_arima_model(train, valid, order)
                    if mse < best_score:
                        best_score, best_cfg, predictions_valid = mse, order, predictions
                    #print('ARIMA%s MSE=%.3f' % (order,mse))
                except:
                    continue
    print('4) 파라미터 튜닝 결과 \n')
    print('Best (p,d,q) : ', best_cfg)
    mse, predictions_test = evaluate_arima_model(train, test, best_cfg)
    return predictions_valid, predictions_test

def modelling_SARIMA(df_train_valid, train, valid, test, p, d, q):
    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))
    # Generate all different combinations of seasonal p, q and q triplets
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    best_score, best_param, best_param_season = float("inf"), None, None

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(train,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)
                results = mod.fit()
                aic = results.aic
                if aic < best_score:
                    best_score, best_param, best_param_season = aic, param, param_seasonal
                pred_uc = results.get_forecast(steps=len(valid))
                lst_pred_valid = pred_uc.predicted_mean.values
                #print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue
    print('Best (p,d,q) : ', best_param)
    print('Best Seasonal (p,d,q) : ', best_param_season)
    mod = sm.tsa.statespace.SARIMAX(df_train_valid,
                                    order=best_param,
                                    seasonal_order=best_param_season,
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)

    results = mod.fit()
    pred_uc = results.get_forecast(steps=len(test))
    lst_pred_test = pred_uc.predicted_mean.values
    
    return lst_pred_valid, lst_pred_test

def evaluation(unnormalized_Y_test, unnormalized_Y_test_pred, flag_model):
    Test_mae = MAE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_mse = MSE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_rmse = RMSE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_mape = MAPE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_mpe = MPE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_r2 = r2_score(unnormalized_Y_test, unnormalized_Y_test_pred)
    lst_result = [Test_mae, Test_mse, Test_rmse, Test_mape, Test_mpe, Test_r2]
    #참고용 Y_test의 평균치
    unnormalized_Y_test_Avg = np.average(unnormalized_Y_test)
    
    if  flag_model ==1:
        model = "SARIMA"
    else:
        model = "ARIMA"
        
    print("Model               : {}".format(model))
    #print('Target Variable Avg : %.2f'   %(unnormalized_Y_test_Avg))
    print('R2                  : %.4f' %(Test_r2))  
    print('MAE                 : %.2f' %(Test_mae))
    print('MSE                 : %.2f' %(Test_mse))
    print('RMSE                : %.2f' %(Test_rmse))
    print('MAPE                : %.2f' %(Test_mape))
    print('MPE                 : %.2f' %(Test_mpe))
    return lst_result, unnormalized_Y_test, unnormalized_Y_test_pred
    
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