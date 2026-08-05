from pyspark.sql.functions import col


def rename_columns(df, rename_map):
    return df.select(
        [
            col(c).alias(rename_map.get(c, c))
            for c in df.columns
        ]
    )