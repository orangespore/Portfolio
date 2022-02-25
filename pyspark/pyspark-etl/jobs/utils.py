from pyspark.sql.types import *
from pyspark.sql import functions as f

def flatten_structs(nested_df):
    stack = [((), nested_df)]
    columns = []

    while len(stack) > 0:

        parents, df = stack.pop()

        array_cols = [
            c[0]
            for c in df.dtypes
            if c[1][:5] == "array"
        ]

        flat_cols = [
            f.col(".".join(parents + (c[0],))).alias("_".join(parents + (c[0],)))
            for c in df.dtypes
            if c[1][:6] != "struct"
        ]

        nested_cols = [
            c[0]
            for c in df.dtypes
            if c[1][:6] == "struct"
        ]

        columns.extend(flat_cols)

        for nested_col in nested_cols:
            projected_df = df.select(nested_col + ".*")
            stack.append((parents + (nested_col,), projected_df))

    return nested_df.select(columns)


def flatten_array_struct_df(df):
    array_cols = [
        c[0]
        for c in df.dtypes
        # 해당 컬럼의 데이터 타입이 array인지 유무 확인
        if c[1][:5] == "array"  # df.dtypes[4][1].split('<')[0]
    ]

    while len(array_cols) > 0:

        for array_col in array_cols:
            cols_to_select = [x for x in df.columns if x != array_col]

            df = df.withColumn(array_col, f.explode(f.col(array_col)))

        df = flatten_structs(df)

        array_cols = [
            c[0]
            for c in df.dtypes
            if c[1][:5] == "array"
        ]
    return df