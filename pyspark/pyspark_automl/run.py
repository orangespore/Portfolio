from pyspark.sql import SparkSession
from analysis import analysis_main

def run_pipeline():
    spark = SparkSession \
    .builder \
    .appName("AutoML") \
    .config("spark.driver.memory", "14g") \
    .getOrCreate()

    result = analysis_main(spark)

if __name__ == '__main__':
    run_pipeline()