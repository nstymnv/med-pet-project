from extract.spark import create_spark
# from pathlib import Path
# from extract.downloader import download_recent_faers
# from config import sf_options
from extract.scanner import extract_data

from load.parser import (
    extract_reports,
    extract_demographics,
    extract_drug,
    extract_reaction,
)

from load.loader import write_to_db
# from config import RAW_DATA_DIR


# xml_files = download_recent_faers(Path(RAW_DATA_DIR))

# raw_data = extract_data(
#     spark,
#     [str(path) for path in xml_files],
# )



spark = create_spark()

# for xml_file in xml_files:
raw_data = extract_data(
    spark, #xml_file
    "/home/nastya/projects/faers-pharmacovigilance-pipeline/data/raw/XML/*.xml",
)

df_reports = extract_reports(raw_data)
df_demographics = extract_demographics(raw_data)
df_drug = extract_drug(raw_data)
df_reaction = extract_reaction(raw_data)

#df_demographics.show()
#df_drug.filter("drugindication IS NOT NULL").show()
#df_reaction.show()
df_reports.filter("version IS NOT NULL").show()

# write_to_db(df_reports, "REPORTS", sf_options)
# write_to_db(df_demographics, "raw", "demographics")
# write_to_db(df_drug, "raw", "drug")
# write_to_db(df_reaction, "raw", "reaction")