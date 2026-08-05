def extract_data(spark, path):
    df =  (
        spark.read.format("xml")
       .option("rowTag", "safetyreport")
       .load(path)
    )
    df.cache()

    return df