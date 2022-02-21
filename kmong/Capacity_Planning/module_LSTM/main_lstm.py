from preprocess_lstm import *
from modelling_lstm import *
from viz_lstm import *

def main(config):

    # split into train and test sets
    train, test, valid, \
    scaler_tr, scaler_te, \
    lst_test_date, lst_valid_date = load_data(config["path_data"], config['look_back'], config["train_size"], config["lst_cols_lstm"])

    # reshape into X=t and Y=t+1
    train_x, train_y = create_dataset(train, config['look_back'])
    test_x, test_y = create_dataset(test, config['look_back'])
    valid_x, valid_y = create_dataset(valid, config['look_back'])

    train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1], config['features']))
    test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], config['features']))
    valid_x = np.reshape(valid_x, (valid_x.shape[0], valid_x.shape[1], config['features']))

    # modelling
    print('=========================================================================================================================')
    print('1) 파라미터 튜닝 결과')
    print('=========================================================================================================================')
    predict_y, test_y = train_model(train_x, train_y, test_x, test_y, config["p"], 1)
    predict_y_valid, valid_y = train_model(train_x, train_y, valid_x, valid_y, config["p"], 0)

    # Evaluation result
    print('=========================================================================================================================')
    print('2) 성능 평가 결과')
    print('=========================================================================================================================')
    print('result - test data')
    lst_result, test_y, test_pred = evaluation(test_y, predict_y, scaler_te)
    #print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
    
    print('result - validation data')
    lst_result_valid, valid_y, valid_pred = evaluation(valid_y, predict_y_valid, scaler_tr)
       
    # viz result(test 전체 plot)     
    print('=========================================================================================================================')
    print('3) 실제값과 예측값 그래프')
    print('=========================================================================================================================')
    viz_result2(test_y, test_pred)
    
    # viz result(real-prediction)
    print('=========================================================================================================================')
    print('4) 실제값 - 예측값 비교 그래프')
    print('=========================================================================================================================')
    print('result - test data')
    viz_result(test_y, test_pred, lst_test_date, 'test')
    
    print('result - validation data')
    viz_result(valid_y, valid_pred, lst_valid_date, 'validation')

    return lst_result, lst_result_valid