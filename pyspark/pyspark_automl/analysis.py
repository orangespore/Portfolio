from load_data import load_
from modelling import model_
from preprocessing import preproc_
from utils import *
import logging

def analysis_main(spark):
    """Run the AutoML pipeline."""
    print("-------------------------------------------------------------")
    print("---------------Starting the run of the pipeline--------------")
    print("-------------------------------------------------------------")
    print("The initial dataframe is the one below :")
    logging.getLogger().setLevel(logging.INFO)

    logging.info("AutoFE - loading dataset ... ")
    df = load_(spark)

    logging.info("AutoFE - Splitting dataset ... ")
    train_df, test_df = df.randomSplit([0.8 ,0.2])

    logging.info("AutoFE : Data preprocessing ... ")
    train_df = preproc_(spark,train_df)
    test_df = preproc_(spark,test_df)

    logging.info(f"AutoFE : Feature selection - Selecting the best subset of features ... ")


    logging.info("AutoFE : Evaluating the performance of the model on the hpo val set ... ")
    model_(spark,train_df)

    logging.info("AutoFE : exit model and spark session ... ")
    spark.stop()

    return
