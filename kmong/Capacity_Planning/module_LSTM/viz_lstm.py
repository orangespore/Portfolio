import pandas as pd
import matplotlib.pyplot as plt

def viz_result(true, pred, lst_test_date, name):
    # 적절한 시각화를 위해서 테스트 데이터 시작부터 100개만 visualize
    x_grid = lst_test_date[:100]
    true, pred = [int(i[0]/10000) for i in true[:100]], [int(i[0]/10000) for i in pred[:100]]

    plt.figure(figsize=(20,8))
    fig,ax = plt.subplots(figsize=(20,8))

    clrs = ['red' if (x-y>=0) else 'lightblue' for x,y in zip(true,pred)]
    true_, pred_ = pd.Series(true), pd.Series(pred)
    ax1 = plt.bar(true_.index, true_, color =clrs, width =0.3, edgecolor='black')
    ax2 = plt.plot(pred_.index, pred_, linewidth=3.5, dash_joinstyle='round', dash_capstyle='round')

    waste_cap = [] # 과소예측으로 인한 일별 추가 필요용량
    
    for i in range(len(true)):
        if true[i]-pred[i] >0:
            #print(true[i]-pred[i])
            plt.annotate(str(true[i]), xy=(true_.index[i],true_.index[i]), ha='center', va='bottom')
            waste_cap.append(true[i]-pred[i])
        else:
            pass
    #plt.minorticks_on()
    plt.title('result - {} data'.format(name))
    ax.set_xticks(list(range(len(x_grid))))
    ax.set_xticklabels(x_grid, rotation=90)
    plt.show()
    
    print('=========================================================================================================================')
    print('과소예측에 따른 최대 일별 필요용량(만건) : ', max(waste_cap))
    print('=========================================================================================================================')
    
def viz_result2(true, pred):

    # 실제 데이터와 예측 데이터 시각화
    plt.figure(figsize=(20, 8))
    plt.plot(true, label='actual', linewidth=3.5, dash_joinstyle='round', dash_capstyle='round')
    plt.plot(pred, label='prediction', linewidth=3.5, dash_joinstyle='round', dash_capstyle='round')
    plt.legend()
    plt.show()