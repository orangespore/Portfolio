from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.mllib.evaluation import BinaryClassificationMetrics
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score

def model_(spark, df):
    train, valid = df.randomSplit([0.7, 0.3], seed=42)

    ipindexer = StringIndexer(
        inputCol="international_plan",
        outputCol="iplanIndex")
    labelindexer = StringIndexer(
        inputCol="churn",
        outputCol="label")

    featureCols = ["account_length", "iplanIndex",
                   "num_voice_mail", "total_day_mins",
                   "total_day_calls", "total_evening_mins",
                   "total_evening_calls", "total_night_mins",
                   "total_night_calls", "total_international_mins",
                   "total_international_calls", "total_international_num_calls"]

    # VectorAssembler for training features
    assembler = VectorAssembler(
        inputCols=featureCols,
        outputCol="features")

    rf = (RandomForestClassifier()
          .setFeaturesCol("features")
          .setLabelCol("label")
          )

    pipeline = Pipeline().setStages([
        ipindexer,  # categorize internation_plan
        labelindexer,  # categorize churn
        assembler,  # assemble the feature vector for all columns
        rf])

    numFolds = 3
    paramGrid = ParamGridBuilder().addGrid(rf.maxDepth, [2, 5, 10, 20, 30]).\
                                   addGrid(rf.maxBins,  [10, 20, 40, 80, 100]).\
                                   addGrid(rf.numTrees, [10, 30, 100]).build()

    evaluator = (BinaryClassificationEvaluator()
                 .setLabelCol("label")
                 .setRawPredictionCol("prediction"))

    cv = (CrossValidator()
          .setEstimator(pipeline)
          .setEvaluator(evaluator)
          .setEstimatorParamMaps(paramGrid)
          .setNumFolds(numFolds))

    cvModel = cv.fit(train)

    predictions = cvModel.transform(valid)
    predictions_pandas = predictions.toPandas()
    resultDF = predictions.select("label", "prediction", "churn")

    # Calculate and print f1, recall, precision, accuracy scores
    f1 = f1_score(predictions_pandas.label, predictions_pandas.prediction)
    recall = recall_score(predictions_pandas.label, predictions_pandas.prediction)
    precision = precision_score(predictions_pandas.label, predictions_pandas.prediction)
    accuracy = accuracy_score(predictions_pandas.label, predictions_pandas.prediction)
    print('F1-Score: {}, Recall: {}, Precision: {}, Accuracy: {}'.format(f1, recall, precision, accuracy))