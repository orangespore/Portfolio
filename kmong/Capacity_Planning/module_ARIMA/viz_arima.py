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


def viz_acf_pacf(df_ts):
    # Draw Plot
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(16,6), dpi= 80)
    plot_acf(df_ts, ax=ax1, lags=50)
    plot_pacf(df_ts, ax=ax2, lags=20)

    # Decorate
    # lighten the borders
    ax1.spines["top"].set_alpha(.3); ax2.spines["top"].set_alpha(.3)
    ax1.spines["bottom"].set_alpha(.3); ax2.spines["bottom"].set_alpha(.3)
    ax1.spines["right"].set_alpha(.3); ax2.spines["right"].set_alpha(.3)
    ax1.spines["left"].set_alpha(.3); ax2.spines["left"].set_alpha(.3)

    # font size of tick labels
    ax1.tick_params(axis='both', labelsize=12)
    ax2.tick_params(axis='both', labelsize=12)
    plt.show()
    
def test_stationarity(timeseries, plot=True):
    # Dickey-Fuller test를 통해 정상성 여부 확인
    #Judgment:
    #(null-hypothesis: TS is non-stationary)
    #p-value < 0.05: reject null-hypothesis –> Stationary
    #p-value > 0.05: accept –> non-Stationary
    #https://h3imdallr.github.io/2017-08-19/arima/ 참고
    
    print ('< Dickey-Fuller Test 결과 >')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], 
                         index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    if plot:
        print (dfoutput)
    else:
        pass
    
    return dfoutput

def Seasonality(DataSet): 
    uniData =  DataSet        # Univariate Data
    lag_acf = acf(uniData.diff().dropna(), nlags=50)
    acf1 = []
    acf2 = []
    for i in range(1,5):
        if i%2 == 0:
            acf2.append(lag_acf[i*12])
        else:
            acf1.append(lag_acf[i*12])
    # Check for seasonality with the (12,36) lag and (24,48) lag  
    if (abs(acf1[0]-acf1[1]) < 0.1) and (abs(acf2[0]-acf2[1])<0.1):
        print("이 데이터는 계절성이 보이므로 SARIMA 적용")
        return 1
    else:
        print("이 데이터는 계절성이 보이지 않으므로 ARIMA 적용")
        return 0

def viz_stationarity(features_train):
    print ('< 원본 결과 >')
    p_value = test_stationarity(features_train).iloc[1]
    
    #First Differencing
    print ('< 1차 차분 결과 >')
    features_train_diff = features_train - features_train.shift(1)
    features_train_diff.dropna(inplace=True)
    p_value_diff = test_stationarity(features_train_diff).iloc[1]
    
    #Second Differencing
    print ('< 2차 차분 결과 >')
    features_train_diff2 = features_train_diff - features_train_diff.shift(1)
    features_train_diff2.dropna(inplace=True)
    p_value_diff2 = test_stationarity(features_train_diff2).iloc[1]
    
    #find best transformation
    p_value_list = [p_value, p_value_diff, p_value_diff2]

    winner_index = p_value_list.index(min(p_value_list))
    
    print('정상성 만족 차분 : ', winner_index)
    
def viz_result(true, pred, lst_test_date):
    x_grid = lst_test_date[:100]
    true, pred = [int(i/10000) for i in true[:100]], [int(i/10000) for i in pred[:100]]

    plt.figure(figsize=(20,8))
    fig,ax = plt.subplots(figsize=(20,8))

    clrs = ['red' if (x-y>=0) else 'lightblue' for x,y in zip(true,pred)]
    true_, pred_ = pd.Series(true), pd.Series(pred)
    ax1 = plt.bar(true_.index, true_, color =clrs, width =0.3, edgecolor='black')
    ax2 = plt.plot(pred_.index, pred_, linewidth=3.5, dash_joinstyle='round', dash_capstyle='round')
    
    waste_cap = [] #일별 낭비용량
    
    for i in range(len(true)):
        if true[i]-pred[i] >0:
            #print(true[i]-pred[i])
            plt.annotate(str(true[i]), xy=(true_.index[i],true_.index[i]), ha='center', va='bottom')
            waste_cap.append(true[i]-pred[i])
        else:
            pass
    #plt.minorticks_on()
    ax.set_xticks(list(range(len(x_grid))))
    ax.set_xticklabels(x_grid, rotation=90)
    plt.show()
    
    print ('=========================================================================================================================')
    print('과소예측에 따른 최대 일별 필요용량(만건)', max(waste_cap) )
    print ('=========================================================================================================================')