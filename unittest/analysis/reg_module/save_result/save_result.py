from reg_module.config import config
import pandas as pd
import joblib

def save_pipeline(pipeline_to_save):
    save_file_name = 'lasso_regression_v1.pkl'
    save_path = config.SAVED_MODEL_PATH+save_file_name
    joblib.dump(pipeline_to_save, save_path)
    print("Saved Pipeline : ",save_file_name)

def load_pipeline(pipeline_to_load):
    save_path = config.SAVED_MODEL_PATH
    trained_model = joblib.load(save_path+pipeline_to_load)
    return trained_model