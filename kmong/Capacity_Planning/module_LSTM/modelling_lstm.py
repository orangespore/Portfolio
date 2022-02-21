import talos
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, roc_curve, auc, mean_absolute_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Activation

# add input parameters to the function
        
def model_lstm(x_train, y_train, x_val, y_val, params):

    # 모델 생성
    model = Sequential()
    model.add(LSTM(params['first_neuron'], 
                   dropout=params['dropout'],
                   activation='relu')
             )
    #model.add(Dense(8, activation=params['activation']))
    
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', metrics=['mae', 'mape'], optimizer=tf.keras.optimizers.Adam(lr=0.02))
    
    history = model.fit(x=x_train, 
                    y=y_train,
                    #validation_data=[x_val, y_val],
                    validation_split=0.1,
                    epochs=params['epochs'],
                    batch_size=params['batch_size'],
                    verbose=0,
                    shuffle=False
                    )
    
    model.summary()
    
    #오버피팅 검증을 위한 learning curve 그리기
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(loss) + 1)
    plt.figure(figsize=(8,6))
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()
    
    plt.clf()   # clear figure

    mae = history.history['mae']
    val_mae = history.history['val_mae']
    plt.figure(figsize=(8,6))
    plt.plot(epochs, mae, 'bo', label='Training MAE')
    plt.plot(epochs, val_mae, 'b', label='Validation MAE')
    plt.title('Training and validation MAE')
    plt.xlabel('Epochs')
    plt.ylabel('MAE')
    plt.legend()
    plt.show()

    return history, model


def train_model(train_x, train_y, test_x, test_y, params, flag):
    #print(train_x)
    t = talos.Scan(x=train_x, y=train_y, params=params, model=model_lstm, print_params = True, experiment_name='model_lstm')
    #model=t.best_model(metric='acc', asc=False)
    t_analyze = talos.Analyze(t)
       
    if flag == 0:
        df_best_params = t_analyze.data.sort_values(by='val_loss').head(1)[['batch_size', 'dropout', 'epochs', 'first_neuron']]
        
        print(
            "LSTM: Best parameters : \n{}".format(df_best_params.to_dict('index').values())
             )
    #print(model)
    #model.fit(train_x, train_y, epochs=30, validation_split=0.1, shuffle=False)
    predict = talos.Predict(t).predict(test_x, metric='mae', asc=True)
    #predict = model.predict(test_x)
    predict = np.reshape(predict, (predict.size, ))

    return predict, test_y

def evaluation(unnormalized_Y_test, unnormalized_Y_test_pred, scaler):
    unnormalized_Y_test_pred = scaler.inverse_transform([[i] for i in unnormalized_Y_test_pred])
    unnormalized_Y_test = scaler.inverse_transform(unnormalized_Y_test.reshape(-1,1))

    
    Test_mae = MAE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_mse = MSE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_rmse = RMSE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_mape = MAPE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_mpe = MPE(unnormalized_Y_test, unnormalized_Y_test_pred)
    Test_r2 = r2_score(unnormalized_Y_test, unnormalized_Y_test_pred)
    lst_result = [Test_mae, Test_mse, Test_rmse, Test_mape, Test_mpe, Test_r2]
    #참고용 Y_test의 평균치
    unnormalized_Y_test_Avg = np.average(unnormalized_Y_test)

    print(f"Model               : LSTM")
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