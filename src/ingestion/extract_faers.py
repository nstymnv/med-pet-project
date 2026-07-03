import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode_outer

from df_schemas import (
    REPORTS_RENAME,
    DEMOGRAPHICS_RENAME,
    DRUG_RENAME,
    REACTION_RENAME,
)

spark = (
        SparkSession.builder
        .appName("FaersPipeline")
        .master("local[*]")
        .config(
        "spark.jars.packages",
        "com.databricks:spark-xml_2.12:0.17.0"
        )
        .getOrCreate()
        )


report_path = "/home/nastya/projects/faers-pharmacovigilance-pipeline/data/raw/XML/*.xml"

def extract_reports(path):
    df =  (
        spark.read.format("xml")
       .option("rowTag", "safetyreport")
       .load(path)
    )
    df.cache()

    return df

df = extract_reports(report_path)

def rename(df, rename_map):
    return df.select([
        col(c).alias(rename_map[c]) if c in rename_map else col(c)
        for c in df.columns
    ])

df_reports = df.select(
    col("safetyreportid"),
    col("safetyreportversion"),
    col("receiptdate"),
    col("transmissiondate"),
    col("primarysourcecountry"),
    col("occurcountry"),
    col("reporttype"),
    col("serious"),
    col("seriousnesscongenitalanomali"),
    col("seriousnessdeath"),
    col("seriousnessdisabling"),
    col("seriousnesshospitalization"),
    col("seriousnesslifethreatening"),
    col("seriousnessother"),
    col("fulfillexpeditecriteria"),
    col("duplicate"),
    col("reportduplicate"),
    col("authoritynumb"),
    col("companynumb"),
)
df_reports = rename(df_reports, REPORTS_RENAME)

df_demographics = df.select(
    col("safetyreportid"),
    col("patient.patientagegroup"),
    col("patient.patientonsetage"),
    col("patient.patientonsetageunit"),
    col("patient.patientsex"),
    col("patient.patientweight"),
)
df_demographics = rename(df_demographics, DEMOGRAPHICS_RENAME)

df_drug_exploded = df.select(
    col("safetyreportid"),
    explode_outer(col("patient.drug")).alias("drug"),
)
 
df_drug_exploded = df_drug_exploded.select(
    col("safetyreportid"),
    col("drug"),
    explode_outer(col("drug.drugrecurrence")).alias("drugrecurrence"),
)
 
df_drug = df_drug_exploded.select(
    col("safetyreportid"),
    col("drug.medicinalproduct"),
    col("drug.activesubstance.activesubstancename"),
    col("drug.drugcharacterization"),
    col("drug.drugindication"),
    col("drug.drugbatchnumb"),
    col("drug.drugadministrationroute"),
    col("drug.drugstructuredosagenumb"),
    col("drug.drugstructuredosageunit"),
    col("drug.drugstartdate"),
    col("drug.drugenddate"),
    col("drug.drugtreatmentduration"),
    col("drug.drugtreatmentdurationunit"),
    col("drug.drugrecurreadministration"),
    col("drugrecurrence.drugrecuraction"),
    col("drug.actiondrug"),
    col("drug.drugadditional"),
)
df_drug = rename(df_drug, DRUG_RENAME)

df_reaction_exploded = df.select(
    col("safetyreportid"),
    explode_outer(col("patient.reaction")).alias("reaction"),
)
 
df_reaction = df_reaction_exploded.select(
    col("safetyreportid"),
    col("reaction.reactionmeddrapt"),
    col("reaction.reactionmeddraversionpt"),
    col("reaction.reactionoutcome"),
)
df_reaction = rename(df_reaction, REACTION_RENAME)

df_drug.printSchema()

df_drug.select("active_substance", "dosage_amount", "start_date" ).show(truncate=False)
