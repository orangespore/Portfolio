import pyspark.sql.functions as F
from pyspark.sql.functions import udf
from pyspark.sql.types import *
from pyspark.ml.feature import Imputer
from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import Normalizer
from pyspark.ml.feature import OneHotEncoder
from pyspark.ml.feature import StringIndexer
from pyspark.sql.functions import monotonically_increasing_id

def get_categorical_columns(dataframe):
	"""Return the categorical columns."""
	columnList = [item[0] for item in dataframe.dtypes if item[1].startswith('string') or item[1].startswith('bool')]
	return columnList

def get_numerical_columns(dataframe):
	"""Return the numerical columns."""
	columnList = [item[0] for item in dataframe.dtypes if item[1].startswith('int') or item[1].startswith('double')]
	return columnList

def get_numerical_columns_with_missing_values(dataframe, lst_cols):
	"""Return the numeric columns wiht null values."""
	# Count the number of null in each columns
	null_counts = dataframe.select([F.count(F.when(F.col(c).isNull() |
												   F.isnan(F.col(c)) , c)).alias(c)
									for c in lst_cols]).collect()[0].asDict()
	numeric_columns_with_nulls = [k for k, v in null_counts.items() if v > 0]
	return numeric_columns_with_nulls

def get_categorical_columns_with_missing_values(dataframe, lst_cols):
	"""Return the categorical columns wiht null values."""
	# Count the number of null in each columns
	null_counts = dataframe.select([F.count(F.when(F.col(c).isNull()
												   | F.isnan(F.col(c))
												   , c)).alias(c)
									for c in lst_cols]).collect()[0].asDict()
	numeric_columns_with_nulls = [k for k, v in null_counts.items() if v > 0]
	return numeric_columns_with_nulls

def fill_missing_values_num(df, lst_cols, strategy):
	"""Fill the missing values by applying all possible transformation to each feature."""
	imputer = Imputer(inputCols=[*lst_cols],
					  outputCols=[*lst_cols]).setStrategy(strategy)
	model = imputer.fit(df)
	df = model.transform(df)
	return df

def get_most_frequent_feature_value(df, column_name):
	"""Return the most frequent feature value."""
	return df.groupby(f"{column_name}").count().orderBy("count", ascending=False).first()[0]

def fill_missing_values_cat(df, lst_cols, strategy):
	"""Do transformation."""

	for column in lst_cols:
		if strategy == 'mode':
			most_common_feature_value = get_most_frequent_feature_value(df, column)
			df = df.withColumn(column, F.when(
											F.col(f"{column}").isNull() |
											F.isnan(F.col(f"{column}")), most_common_feature_value).otherwise(df[f"{column}"]))
		elif strategy == 'unknown':
			df = df.withColumn(column, F.when(
											F.col(f"{column}").isNull() |
											F.isnan(F.col(f"{column}")) , "Unknown").otherwise(df[f"{column}"]))
	return df

def normalize(df, lst_cols):
	"""Normalize the columns from the dataframe."""
	normalizer = Normalizer(inputCol=[*lst_cols], outputCol=[*lst_cols], p=1.0)
	df = normalizer.transform(df)
	return df

def standardize(df, lst_cols):
	"""Standardize the columns from the dataframe."""
	scaler = StandardScaler(inputCol=[*lst_cols], outputCol=[*lst_cols],
						withStd=True, withMean=False)
	scalerModel = scaler.fit(df)
	df = scalerModel.transform(df)
	return df

def remove_outliers(df, lst_cols):
	"""remove outliers of the columns from the dataframe"""
	for column in lst_cols:
		less_Q1 = 'less_Q1_{}'.format(column)
		more_Q3 = 'more_Q3_{}'.format(column)
		Q1 = 'Q1_{}'.format(column)
		Q3 = 'Q3_{}'.format(column)

		# Q1 : First Quartile ., Q3 : Third Quartile
		Q1 = df.approxQuantile(column, [0.25], relativeError=0)
		Q3 = df.approxQuantile(column, [0.75], relativeError=0)
		IQR = Q3[0] - Q1[0]

		# selecting the data, with -1.5*IQR to + 1.5*IQR., where param = 1.5 default value
		less_Q1 = Q1[0] - 1.5 * IQR
		more_Q3 = Q3[0] + 1.5 * IQR

		isOutlierCol = 'is_outlier_{}'.format(column)
		df = df.withColumn(isOutlierCol, F.when((df[column] > more_Q3) | (df[column] < less_Q1), 1).otherwise(0))

	# Selecting the specific columns which we have added above, to check if there are any outliers
	selected_columns = [column for column in df.columns if column.startswith("is_outlier")]
	df = df.withColumn('total_outliers', sum(df[column] for column in selected_columns))

	# Dropping the extra columns created above, just to create nice dataframe., without extra columns
	df = df.drop(*[column for column in df.columns if column.startswith("is_outlier")])
	df = df.filter(df['total_Outliers'] <= 1)
	df = df.drop(["total_Outliers"])
	return df


def map_dict(mapping):
    def f(x):
        return mapping.get(x)
    return F.udf(f, StringType())

def encode_categorical_features(df, lst_cols, strategy):
	"""Encode categorical features and add to the column of the dataframe."""
	# Ordinal encoding
	if strategy == 'label-enc':
		ordinal_encoded_output_cols = ["ordinal_indexed_"+categorical_feature for categorical_feature in lst_cols]
		indexer = StringIndexer(inputCols=lst_cols, outputCols=ordinal_encoded_output_cols, handleInvalid="keep")
		df = indexer.fit(df).transform(df)

	# frequency encoding
	elif strategy == 'freq-enc':
		row = df.count()
		for column in lst_cols:
			new_col = f"gp_cnt_{column}"
			df_enc = df.groupBy(F.col(column)).agg(F.count(column).alias(new_col))
			df_enc = df_enc.withColumn(new_col, new_col/row)
			dict_enc = df_enc.select([column, new_col]).collect()[0].asDict() # {val : ratio}

			df = df.withColumn(f"freq_enc_{column}", map_dict(dict_enc)(F.col(column)))
			df = df.withColumn(f"freq_enc_{column}", round(f"freq_enc_{column}", 2))
	return df

def transform_interaction(df, col_a, col_b):
	"""Do transformation."""

	# Addition
	df = df.withColumn(f"{col_a}_plus_{col_b}", col_a + col_b)
	# Substraction
	df = df.withColumn(f"{col_a}_minus_{col_b}", col_a - col_b)
	df = df.withColumn(f"{col_b}_minus_{col_a}", col_b - col_a)
	# Mulitplication
	df = df.withColumn(f"{col_a}_x_{col_b}", col_a * col_b)
	# Division
	df = df.withColumn(f"{col_a}_per_{col_b}", F.when(col_b != 0, col_a / col_b).otherwise(0))
	df = df.withColumn(f"{col_b}_per_{col_a}", F.when(col_a != 0, col_b / col_a).otherwise(0))

	return df

def map_dict_agg(mapping):
    def f(x):
        return mapping.get(x)
    return F.udf(f, StringType())

def transform_agg(df, col_gp, col_fe):
	"""Do transformation."""
	new_col = f"gp_mean_{col_fe}"
	df_gp = df.groupBy(F.col(col_gp)).agg(F.mean(col_fe).alias(new_col))
	dict_enc = df_gp.select([col_gp, new_col]).collect()[0].asDict()  # {val : ratio}

	df = df.withColumn(f"gp_mean_{col_fe}", map_dict_agg(dict_enc)(F.col(col_fe)))

	return df