def write_to_db(df, table_name, sf_options):
    (
        df.write
        .format("net.snowflake.spark.snowflake")
        .options(**sf_options)
        .option("dbtable", table_name)
        .mode("append")
        .save()
        )
