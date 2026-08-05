from pyspark.sql import SparkSession

def create_spark():
    return (
        SparkSession.builder
        .appName("FaersPipeline")
        .master("local[*]")
        .config(
        "spark.jars.packages",
        "com.databricks:spark-xml_2.12:0.17.0,org.postgresql:postgresql:42.7.3"
        )
        .getOrCreate()
    )