"""
etl_job.py
~~~~~~~~~~
    $SPARK_HOME/bin/spark-submit \
    --master spark://localhost:7077 \
    --py-files packages.zip \
    --files configs/etl_config.json \
    jobs/etl_job.py
"""

from pyspark.sql import functions as f
from dependencies.spark import start_spark
from utils import flatten_array_struct_df, flatten_structs

def main():
    """Main ETL script definition.

    :return: None
    """
    # start Spark application and get Spark session, logger and config
    spark, log, config = start_spark(
        app_name='my_etl_job',
        files=['configs/etl_config.json'])

    # log that main ETL job is starting
    log.warn('etl_job is up-and-running')

    # execute ETL pipeline
    data = extract_data(spark)
    data_flatten = flatten_data(data)
    load_data(data_flatten)

    # log the success and terminate Spark application
    log.warn('test_etl_job is finished')
    spark.stop()
    return None


def extract_data(spark):
    """Load data from json file format.

    """
    df = spark.read.json("/data/log/210401.json")

    return df


def flatten_data(df):
    """Transform original dataset.
    """
    flat_df = flatten_array_struct_df(df.select(['adid', 'sid', 'events']))
    flat_df = flat_df.distinct()
    flat_df = flat_df.sort(['adid', 'sid'], ascending=True)
    return flat_df


def load_data(df):
    """Collect data locally and write to CSV.
    """
    (df
     .coalesce(1)
     .write
     .csv('loaded_data', mode='overwrite', header=True))
    return None

# entry point for PySpark ETL application
if __name__ == '__main__':
    main()
