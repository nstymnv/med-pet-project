from config import DB_USERNAME, DB_PASSWORD, DB_URL

def write_to_db(df, schema, db_name):
    (
        df.write \
        .format("jdbc") \
        .option("url", DB_URL) \
        .option("dbtable", f"{schema}.{db_name}") \
        .option("user", DB_USERNAME) \
        .option("password", DB_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
        )
