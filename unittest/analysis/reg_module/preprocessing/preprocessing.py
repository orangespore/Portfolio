from reg_module.config import config
import numpy as np
import pandas as pd


# Numerical Imputer
def numerical_imputer(_data):
    for var in config.NUMERICAL_FEATURES:
        _data[var].fillna(_data[var].mode()[0], inplace=True)
    return _data


# Categorical Imputer
def categorical_imputer(_data):
    for var in config.CATEGORICAL_FEATURES:
        _data[var].fillna(_data[var].mode()[0], inplace=True)
    return _data


# Rare label Categorical Encoder
def rare_label_cat_imputer(_data):
    encoder_dict_ = {}
    tol = 0.05

    for var in config.FEATURES_TO_ENCODE:
        # the encoder will learn the most frequent categories
        t = pd.Series(_data[var].value_counts() / np.float(len(_data)))
        # frequent labels:
        encoder_dict_[var] = list(t[t >= tol].index)

    for var in config.FEATURES_TO_ENCODE:
        _data[var] = np.where(_data[var].isin(
            encoder_dict_[var]), _data[var], 'Rare')

    return _data

# Categorical Encoder
def categorical_encoder(_data):
    encoder_dict_ = {}
    for var in config.FEATURES_TO_ENCODE:
        t = _data[var].value_counts().sort_values(ascending=True).index
        encoder_dict_[var] = {k: i for i, k in enumerate(t, 0)}

    ## Mapping using the encoder dictionary
    for var in config.FEATURES_TO_ENCODE:
        _data[var] = _data[var].map(encoder_dict_[var])

    return _data


# Temporal Variables
def temporal_transform(_data):
    for var in config.TEMPORAL_FEATURES:
        _data[var] = _data[var] - _data[config.TEMPORAL_COMPARISON]

    return _data


# Log Transformations
def log_transform(_data):
    for var in config.LOG_FEATURES:
        _data[var] = np.log(_data[var])
    return _data


def drop_features(_data):
    _data.drop(config.DROP_FEATURES, axis=1, inplace=True)
    return _data
