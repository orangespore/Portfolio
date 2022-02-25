from utils import *


def preproc_(spark, df):
    lst_catcols = get_categorical_columns(df)
    lst_numcols = get_numerical_columns(df)

    lst_numcols_null = get_numerical_columns_with_missing_values(df, lst_catcols)
    lst_catcols_null = get_categorical_columns_with_missing_values(df, lst_catcols)

    df = fill_missing_values_num(df, lst_numcols_null, 'mean')
    df = fill_missing_values_cat(df, lst_catcols_null, 'mode')

    df = normalize(df)
    df = remove_outliers(df, lst_numcols)
    df = encode_categorical_features(df, lst_catcols, 'freq-enc')
    df = transform_interaction(df, lst_numcols[0], lst_numcols[1])
    df = transform_agg(df, lst_catcols[0], lst_numcols[0])
    return df