import pandas as pd
import numpy as np
import seaborn as sns
#import plotly.express as px
import matplotlib.pyplot as plt


def viz_data(df, Selected_Features):
    #viz 1
    print('viz 1 : Histogram of all variables (before preprocessing)')
    df_no_date = df.drop(columns=["Date"])
    df_no_date.hist(bins=50, figsize=(20,15))
    plt.show()
    print('=========================================================================================================================')
    print('=========================================================================================================================')
    #viz 2
    print('viz 2 : Heatmap(correlation) of all variables (before preprocessing)')
    plt.figure(figsize = (20, 20))
    sns.heatmap(data = df.corr(), annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')
    plt.show()
    print('=========================================================================================================================')
    print('=========================================================================================================================')
    #viz 3
    print('viz 3 : Correlation(by N_Order) of all variables (before preprocessing)')
    cancel_corr = df.corr()["N_Order"]
    print(cancel_corr.abs().sort_values(ascending=False)[1:])
    print('=========================================================================================================================')
    print('=========================================================================================================================')
    #viz 4
    print('viz 4 : Correlation(by N_Order) of selected variables (before preprocessing)')
    df_sel = df[Selected_Features]
    Sel_corr = df_sel.corr()["N_Order"]
    print(Sel_corr.abs().sort_values(ascending=False)[1:])
    print('=========================================================================================================================')
    print('=========================================================================================================================')
    #viz 5
    print('viz 5 : Histogram of selected variables (before preprocessing)')
    df_sel = df[Selected_Features]
    df_sel.hist(bins=50, figsize=(20,15))
    plt.show()
    print('=========================================================================================================================')
    print('=========================================================================================================================')
    
def viz_data_2(df_lag, df_lag1, df, Stat_Features):
    #viz 1
    print('viz 1 : Discription of P_VKOSPI_T1 (after preprocessing)')
    print(df_lag["P_VKOSPI_T1"].describe())
    print('=========================================================================================================================')
    print('=========================================================================================================================')
    #viz 2
    print('viz 2 : Discription of Stat_Features (after preprocessing)')
    df_stat = df_lag[Stat_Features]
    df_stat['Date'] = df_lag.index
    df_stat.reset_index(drop=True)
    
    df_stat1 = df_lag1[Stat_Features]
    df_stat1['Date'] = df_lag.index
    df_stat1.reset_index(drop=True)
    print(df_stat.describe())
    print('=========================================================================================================================')
    print('=========================================================================================================================')
    #viz 3
    print('viz 3 : Plot comparison of major variables (after preprocessing)')
    fig, ax1 = plt.subplots(figsize = (12, 8))
    ax2 = ax1.twinx()
    Order_line = ax1.plot(df_stat['Date'], df_stat['N_Order_T1'], color='b', linestyle='-', label = "Number of Orders")
    Vkospi_line = ax2.plot(df_stat['Date'], df_stat['P_VKOSPI_T1'], color='r', linestyle='-', label = "VKOSPI")
    frequency = 90 # x_ticks 표시 빈도수
    ax1.set_xticks(df_stat['Date'].dt.date[::frequency])
    ax1.set_xticklabels(df_stat['Date'].dt.date[::frequency], rotation = 30)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number[Order]')
    ax2.set_ylabel('Points[VKOSPI]')
    plt.title('Comparison of Major Variables', fontsize=20) 
    # 그래프 limit 설정
    ax1.set_ylim(0, 60000000)
    ax2.set_ylim(0, 70.0)
    # plot legends
    lines = Order_line + Vkospi_line
    labels = [l.get_label() for l in lines]
    plt.legend(lines, labels, loc = 2)
    plt.grid(False)
    plt.show()
    print('=========================================================================================================================')
    print('=========================================================================================================================')  
    #viz 4
    print('viz 4 : Plot comparison of capacity efficiency (after preprocessing)')
    df_cap = pd.DataFrame(index = df_stat1.index, columns = ['Cap'], dtype = np.float64)
    cap = pd.Series(df_stat1['Max_Capacity'])

    # 가장 큰 값으로 모두 채우기
    for i in df_cap.index:
            df_cap.loc[i,'Cap'] = cap.max()
            i = i + 1
    #최대치 경신한 일자 찾기
    for i in df_stat1.index:
            if df_stat1.loc[i,'N_Order_T1'] == cap.max() :
                print(df_stat1.loc[i,'Date'])
            i = i + 1

    fig, ax1 = plt.subplots(figsize = (12, 8))

    #Plot 설정
    Order_line = ax1.plot(df_stat1['Date'], df_stat1['N_Order_T1'], color='b', linestyle='-', label = "Number of Orders")
    Capacity_line = ax1.plot(df_stat1['Date'], df_stat1['Max_Capacity'], color='g', linestyle='-', label = "Predicted_Capacity")
    Legacy_capacity_line = ax1.plot(df_stat1['Date'], df_cap['Cap'], color='r', linestyle='-', label = "Legacy_Capacity") 

    # 날짜에 맞춰서 x_ticks 설정
    ax1.set_xticks(df_stat1['Date'].dt.date[::frequency])
    ax1.set_xticklabels(df_stat1['Date'].dt.date[::frequency], rotation = 30)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number[Order, Capacity]')
    plt.title('Comparison of Capacity Efficiency', fontsize=20) 

    # 그래프 limit 설정
    ax1.set_ylim(0, 60000000)

    # plot legends
    lines = Order_line + Capacity_line + Legacy_capacity_line
    labels = [l.get_label() for l in lines]
    plt.legend(lines, labels, loc = 4)
    plt.grid(False)
    plt.show()
    print('=========================================================================================================================')
    print('=========================================================================================================================')
    
def viz_data_preproc(df):
    #viz 1
    print('viz 1 : Correlation (by Max_Capacity) of all variables (after preprocessing)')
    # 타겟변수와의 corr 확인
    cancel_corr = df.corr()["Max_Capacity"]
    print(cancel_corr.abs().sort_values(ascending=False)[1:])
    print('=========================================================================================================================')
    print('=========================================================================================================================')   
    #viz 2-1
    print('viz 2-1 : Check Skewness / Kurtosis of numeric features before normalization (after preprocessing)')
    # 최초 Skewness와 Kurtosis 확인
    for col in df:
        print ('{:30}'.format(col), 
               'Skewness: {:05.2f}'.format(df[col].skew()),
               '    ',
               'Kurtosis: {:06.2f}'.format(df[col].kurt())
              )
    print('=========================================================================================================================')
    print('=========================================================================================================================')    
    #viz 2-2
    print('viz 2-2 : Check Skewness / Kurtosis of numeric features after normalization (after preprocessing)')
    
    #Skewness가 3 이상인 변수 Normalization
    for i in df.columns:
        if df[i].skew()>=3:
            df[i] = np.log1p(df[i])
            
    # log 후 Skewness와 Kurtosis 확인
    print("Skewness and Kurtosis of numeric features")
    for col in df:
        print ('{:30}'.format(col), 
               'Skewness: {:05.2f}'.format(df[col].skew()),
               '    ',
               'Kurtosis: {:06.2f}'.format(df[col].kurt())
              )
    print('=========================================================================================================================')
    print('=========================================================================================================================')    
    #Outlier 제거는 연구의 취지상 하지 않아야함(Max Capacity의 outlier들을 잘 예측하는 것이 목표이므로)
    #테스트 목적으로 코딩만 함
    #viz 3-1
    #print('viz 3-1 : Check before outlier elimination (after preprocessing)')
    #plt.figure(figsize = (15, 15))
    #df.boxplot(rot = 45)
    #plt.title("Box Plot Before Outlier Elimination", fontsize=16)
    #plt.show()
    #print('=========================================================================================================================')
    #print('=========================================================================================================================')    
    #viz 3-2
    #print('viz 3-2 : Check after outlier elimination (after preprocessing)')
    # Outlier 제거 후 outlier확인을 위한 Box plot 확인
    #plt.figure(figsize = (15, 15))
    #df.boxplot(rot = 45)
    #plt.title("Box Plot After Outlier Elimination : X variables", fontsize=16)
    #plt.show()
    #print('=========================================================================================================================')
    #print('=========================================================================================================================')
    
def viz_result(model, df, figsize=(15, 18)):
    sns.set_style('whitegrid')
    
    feature_importance = model.feature_importances_
    feature_importance_rel = 100.0 * (feature_importance / feature_importance.max())
    sorted_idx = np.argsort(feature_importance)
    sorted_idx_rel = np.argsort(feature_importance_rel)
    ypos = np.arange(sorted_idx_rel.shape[0]) + .5
    
    n=0
    print("Feature Importance of ", model.__repr__().split('(')[0])
    for index in feature_importance:   
        print ('{:30}'.format(df.columns[n]), 
               'importance: {:05.4f}'.format(index)
              )
        n = n+1
        
    plt.figure(figsize=figsize)
    plt.barh(ypos, feature_importance[sorted_idx_rel], align='center', color = "Green")
    plt.yticks(ypos, df.columns[sorted_idx_rel])
    plt.xlabel('Relative importance')
    plt.title('Feature importance')
    plt.show()

#def viz_result2(true, pred, lst_test_date):
#    plt.figure(figsize=(20,8))
#    print(true)
#    print(pred)
#    clrs = ['lightblue' if (x-y>=0) else 'red' for x,y in zip(true,pred)]
#    true_, pred_ = pd.Series(true[:100]), pd.Series(pred[:100])
#    ax1 = plt.bar(lst_test_date, true_, color =clrs, width =0.3, edgecolor='black')
#    ax2 = plt.plot(lst_test_date, pred_, linewidth=3.5, dash_joinstyle='round', dash_capstyle='round')

#    for i in range(len(true)):
#        if true[i]-pred[i] <0:
#            print(true[i]-pred[i])
#            plt.annotate(str(true[i]), xy=(true_.index[i],true_.index[i]), ha='center', va='bottom')
#        else:
#            pass
    #plt.minorticks_on()
#    plt.title('Difference Between Real and Predicted Max_Capacity')
#    plt.show()

# 실제 과대예측, 과소예측 여부를 보여주는 그래프
def viz_result3(true, pred, lst_test_date):
    x_grid = [str(i)[:10] for i in lst_test_date[:100]] # time을 제외하고 date만을 가져옴
    
    true, pred = [int(i[0]/10000) for i in true[:100]], [int(i[0]/10000) for i in pred[:100]]
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
    #plt.locator_params(axis='x', nbins=10)
    #plt.xticks(x_grid, rotation=90)
    plt.title('Difference Between Real and Predicted Max_Capacity')
    plt.show()   
    
    print ('=========================================================================================================================')
    print('과소예측에 따른 최대 일별 필요용량(만건) : ', max(waste_cap) )
    print ('=========================================================================================================================')

# Feature Importance
def plot_feature_importance(model, df, figsize=(15, 18)):
    sns.set_style('whitegrid')
    
    feature_importance = model.feature_importances_
    feature_importance_rel = 100.0 * (feature_importance / feature_importance.max())
    sorted_idx = np.argsort(feature_importance)
    sorted_idx_rel = np.argsort(feature_importance_rel)
    ypos = np.arange(sorted_idx_rel.shape[0]) + .5
    
    n=0
    print("Feature Importance of ", model.__repr__().split('(')[0])
    for index in feature_importance:   
        print ('{:30}'.format(df.columns[n]), 
               'importance: {:05.4f}'.format(index)
              )
        n = n+1
        
    plt.figure(figsize=figsize)
    plt.barh(ypos, feature_importance[sorted_idx_rel], align='center', color = "Green")
    plt.yticks(ypos, df.columns[sorted_idx_rel])
    plt.xlabel('Relative importance')
    plt.title('Feature importance')
    plt.show()
    
def viz_total_evaluation(result, flag):
    if flag == 'Test': 
        metric = ['Test_mae', 'Test_mse', 'Test_rmse', 'Test_mape', 'Test_mpe', 'Test_r2']
    else :
        metric = ['Valid_mae', 'Valid_mse', 'Valid_rmse', 'Valid_mape', 'Valid_mpe', 'Valid_r2']
    
    for i in metric:
        df = result.loc[result.index.str.contains(i)]
        # multiple line plots
        plt.figure(figsize=(20,8))
        plt.plot(df.index,df['Randomforest'], color='brown', linewidth=3, marker="o")
        plt.plot(df.index,df['Decisiontree'], color='blue', linewidth=3, marker="o")
        plt.plot(df.index,df['Lasso'],  color='black', linewidth=3, marker="o")
        plt.plot(df.index,df['Ridge'], color='green', linewidth=3, marker="o")
        plt.plot(df.index,df['Xgboost'], color='orange', linewidth=2)
        # show legend
        plt.legend(['randomforest','decisiontree','lasso','ridge','xgboost'])
        plt.title("comparision of models by {}".format(i))
        # show graph
        plt.grid(True)
        plt.show()