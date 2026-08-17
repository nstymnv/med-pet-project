from config import POSTGRES_URL, POSTGRES_USER, POSTGRES_PASSWORD

def write_to_db(df, schema, db_name):
    (
        df.write \
        .format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", f"{schema}.{db_name}") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
        )
