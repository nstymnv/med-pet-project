from pyspark.sql.functions import col, explode_outer

from .df_schemas import (
    REPORTS_RENAME,
    DEMOGRAPHICS_RENAME,
    DRUG_RENAME,
    REACTION_RENAME,
)

from .utils import rename_columns

def extract_reports(df):
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
        col("reportduplicate.duplicatenumb"),
        col("reportduplicate.duplicatesource"),
        col("authoritynumb"),
        col("companynumb"),
    )
    return rename_columns(df_reports, REPORTS_RENAME)

def extract_demographics(df):
    df_demographics = df.select(
         col("safetyreportid"),
         col("safetyreportversion"),
         col("patient.patientagegroup"),
         col("patient.patientonsetage"),
         col("patient.patientonsetageunit"),
         col("patient.patientsex"),
         col("patient.patientweight"),
        )
    return rename_columns(df_demographics, DEMOGRAPHICS_RENAME)

def extract_drug(df):
    df_drug_exploded = df.select(
        col("safetyreportid"),
        col("safetyreportversion"),
        explode_outer(col("patient.drug")).alias("drug"),
    )
 
    df_drug_exploded = df_drug_exploded.select(
        col("safetyreportid"),
        col("safetyreportversion"),
        col("drug"),
        explode_outer(col("drug.drugrecurrence")).alias("drugrecurrence"),
    )
 
    df_drug = df_drug_exploded.select(
        col("safetyreportid"),
        col("safetyreportversion"),
        col("drug.medicinalproduct"),
        col("drug.activesubstance.activesubstancename"),
        col("drug.drugcharacterization"),
        col("drug.drugindication"),
        col("drug.drugbatchnumb"),
        col("drug.drugauthorizationnumb"),
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
    return rename_columns(df_drug, DRUG_RENAME)

def extract_reaction(df):
    df_reaction_exploded = df.select(
        col("safetyreportid"),
        col("safetyreportversion"),
        explode_outer(col("patient.reaction")).alias("reaction"),
    )
 
    df_reaction = df_reaction_exploded.select(
        col("safetyreportid"),
        col("safetyreportversion"),
        col("reaction.reactionmeddrapt"),
        col("reaction.reactionmeddraversionpt"),
        col("reaction.reactionoutcome"),
    )
    return rename_columns(df_reaction, REACTION_RENAME)