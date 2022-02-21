from preprocess_ml import *
from modelling_ml import *
from viz_ml import *
import warnings
warnings.filterwarnings("ignore")

def main(config, flag):
    lst_result_entire = []
    lst_result_entire_valid = []
    for index, value in enumerate(config["lst_XY"]):
        
        print('=========================================================================================================================')
        print('(X,Y) {} 모델 별 결과'.format(value))
        print('=========================================================================================================================')
        
        # 용량예측을 위한 과거 관측기간 X, 최대 용량을 계산할 향후 기간 Y
        X, Y = value[0], value[1]#40, 60
        idx = "_X{}Y{}".format(X,Y)

        # 최종 데이터 저장 경로
        path_data_full = config["path"]+"Full_Data_X{}Y{}.xlsx".format(X,Y)
        # 분석할 데이터 불러오기
        df = load_data(config["path_data"])
        df.index = df['Date']
        # lag 변수 생성
        df_preproc = preprocess_data_lag(df, config["lst_sel_features"], X, Y)
        df_preproc1 = df_preproc.reset_index(drop=True)
       
        # 타겟 변수 생성
        df_target = generate_target(df_preproc1, df, config["lst_sel_features"], Y)
        # 최종 데이터 생성
        df_final = generate_dataset(df_preproc, df_target, path_data_full)
        df_final1 = df_final.reset_index(drop=True)
        
        # 데이터 1개에 대해서 분석할 때만 시각화 결과 출력
        if flag == 'one':
            # 상관관계 결과 저장하기
            save_data_corr(df, config["path_data_corr"])
            # 초기 데이터 시각화
            viz_data(df, config["lst_sel_features"])
            # 최종 데이터 시각화
            viz_data_2(df_final, df_final1, df, config["Stat_Features"])
            # 최종 데이터 시각화2
            viz_data_preproc(df_final)
        #a, b, c = df_final, df_final1, df
     
        # VKOPSI 포함여부에 따라 성능 차이를 확인하기 위함
        # df = remove_columns(df_final, lst_cols_remove)
        
        # Skewness > 3 이상인 경우 정규화 변환(log)
        df_final = transform_data(df_final)
        
        # 이상치 제거
        # df_final = generate_data_outlier(df_final, 2, df_final.columns)
        
        # 최종 x, y 생성
        df_X, df_Y = generate_XY(df_final)

        # 트레인/테스트 생성
        X_train, X_test, X_valid, Y_train,\
        Y_test, Y_valid, y_scaler_tr, y_scaler_te, lst_test_date = preprocess_XY(df_X, df_Y, X)

        lst_result_total = []
        lst_result_total_valid = []
        #print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
        #print('모델 별 성능 평가')
        for key in config["dict_modelling"].keys():
            
            # 모델링
            lst_y_test, lst_y_pred, lst_y_valid,\
            lst_y_valid_pred, model = modelling(X_train, X_test, X_valid, Y_train, Y_test, Y_valid, 
                                                config["dict_modelling"][key][1],
                                                config["dict_modelling"][key][0], 
                                                y_scaler_tr, y_scaler_te)
            # 예측 및 성능 평가
            print('=========================================================================================================================')
            print('{} 모델'.format(key))
            print('Test result')
            lst_result = evaluation(lst_y_test, lst_y_pred)
            lst_result_total.append(lst_result)
            #print('\n')
            print('Validation result')
            lst_result_valid = evaluation(lst_y_valid, lst_y_valid_pred)
            lst_result_total_valid.append(lst_result_valid)
            print('=========================================================================================================================')
            # 변수 중요도 시각화
            if flag == 'one':
                try:
                    viz_result(model, df_X)
                except:
                    print(key," has no attribute 'feature_importances function'")
                viz_result3(lst_y_test, lst_y_pred, lst_test_date)
            #print('===================================================================================')
            #print('===================================================================================')
            
        # validation / test 성능 결과 저장
        lst_cols_idx_test = ['Test_mae', 'Test_mse', 'Test_rmse', 'Test_mape', 'Test_mpe', 'Test_r2']
        lst_cols_idx_val = ['Valid_mae', 'Valid_mse', 'Valid_rmse', 'Valid_mape', 'Valid_mpe', 'Valid_r2']
        lst_cols_idx_test = [i+idx for i in lst_cols_idx_test]
        lst_cols_idx_val = [i+idx for i in lst_cols_idx_val]
        df_result_total = pd.DataFrame(lst_result_total,
                                       index=config["dict_modelling"].keys(),
                                       columns=lst_cols_idx_test).T
        df_result_total_valid = pd.DataFrame(lst_result_total_valid,
                                       index=config["dict_modelling"].keys(),
                                       columns=lst_cols_idx_val).T
        lst_result_entire.append(df_result_total)
        lst_result_entire_valid.append(df_result_total_valid)
        
    df_result_entire = pd.concat(lst_result_entire,axis=0)
    df_result_entire_valid = pd.concat(lst_result_entire_valid,axis=0)
    
    return df_result_entire, df_result_entire_valid