import numpy as np
from sklearn.linear_model import Lasso
from reg_module.config import config

def train_model(train):
    y = np.log(train[config.TARGET])
    train.drop([config.TARGET], axis=1, inplace=True)
    model=Lasso(alpha=0.05, random_state=42)
    model.fit(train[config.KEEP], y)

    return model
