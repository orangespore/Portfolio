# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import numpy as np


#Import other files/modules
from reg_module.config import config
from reg_module.load_data.load_data import load_dataset
from reg_module.preprocessing.preprocessing import *
from reg_module.modelling.modelling import train_model
from reg_module.predict.predict import make_prediction
from reg_module.save_result.save_result import  save_pipeline
from reg_module.logging.logging import  *

def regression(VERSION):
    """Train the model"""
    create_logger(VERSION)

    print("1.load data\n")
    get_logger(VERSION).info("load data")
    train = load_dataset("train1.csv", VERSION)
    test = load_dataset("test.csv", VERSION)

    print("2.preprocess data\n")
    get_logger(VERSION).info("preprocess data")
    for data in [train,test]:
        numerical_imputer(data)
        categorical_imputer(data)
        rare_label_cat_imputer(data)
        categorical_encoder(data)
        temporal_transform(data)
        log_transform(data)
        drop_features(data)

    print("3.train data\n")
    get_logger(VERSION).info("train data")
    model=train_model(train)

    print("4.predict data\n")
    get_logger(VERSION).info("predict data")
    make_prediction(test, model)

    print("5.save result\n")
    get_logger(VERSION).info("save data")
    save_pipeline(model)


if __name__=='__main__':
    VERSION = "001"  # 実験番号


    print('start analysis\n')
    # logging
    regression(VERSION)

    print('end analysis\n')


