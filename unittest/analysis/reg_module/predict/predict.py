import numpy as np
import pandas as pd

from reg_module.config import config
from reg_module.save_result import save_result

pipeline_file_name = 'lasso_regression_v1.pkl'



def make_prediction(input_data, model):
    data = pd.DataFrame(input_data)
    prediction = model.predict(data[config.KEEP])
    output = np.exp(prediction)

    results = {
        'prediction': output,
        'model_name': pipeline_file_name,
        'version':'version1'
    }

    return results