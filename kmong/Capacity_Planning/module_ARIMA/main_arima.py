from preprocess_arima import *
from modelling_arima import *
from viz_arima import *

def main(config):
    # 데이터 불러오기
    df = load_data(config['path_data'])
    # 데이터 분리
    train, valid, test = split_data(df)
    df_train_valid = pd.concat([train,valid])
    # 데이터 시각화 - acf/pacf
    # 출력결과를 보면 acf가 느리게 감소하고 있어 비정상성을 나타내는 것을 알 수 있음
    print ('=========================================================================================================================')
    print('1) acf/pacf 시각화')
    print ('=========================================================================================================================')
    viz_acf_pacf(df_train_valid)
    print ('=========================================================================================================================')
    print('2) 정상성')
    print ('=========================================================================================================================')
    # 데이터 시각화 - 정상성
    viz_stationarity(df_train_valid)
    print ('=========================================================================================================================')
    # 데이터 시각화 - 계절성
    print('3) 계절성')
    print ('=========================================================================================================================')
    flag_model = Seasonality(df_train_valid)
    print ('=========================================================================================================================')
    print('4) 파라미터 튜닝 결과')
    print ('=========================================================================================================================')
    # 모델링
    if flag_model == 0:
        lst_pred_valid, lst_pred_test = evaluate_models(train, valid, test, config['p'], config['d'], config['q'])
        lst_pred_valid = [i[0] for i in lst_pred_valid]
        lst_pred_test = [i[0] for i in lst_pred_test]
    else:
        lst_pred_valid, lst_pred_test = modelling_SARIMA(df_train_valid, train, valid, test, config['p'], config['d'], config['q'])
    # 성능 평가
    
    print ('=========================================================================================================================')
    print('5) 성능 평가')
    print ('=========================================================================================================================')
    print('result - test data')
    lst_result, test_y, test_pred = evaluation(test.values, lst_pred_test, flag_model)
    #print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
    print('result - validation data')          
    lst_result_valid, valid_y, valid_pred = evaluation(valid.values, lst_pred_valid, flag_model)
    
    # 시각화
    print ('=========================================================================================================================')
    print('6) 예측값 - 실제값 비교')
    print ('=========================================================================================================================')
    print('result - test data')
    viz_result(test_y, test_pred, test.index)
    
    print('\n result - validation data')  
    viz_result(valid_y, valid_pred, valid.index)
    
    return lst_result, lst_result_valid