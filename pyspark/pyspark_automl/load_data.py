
def load_(spark):
    df = spark.read.csv(f"../datasets/{dataset}.csv/")

    return df