from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_URL = os.getenv("POSTGRES_URL")
FAERS_INDEX_URL = (
    "https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html"
)
YEARS_TO_DOWNLOAD = 5
RAW_DATA_DIR = "data/raw"

private_key = Path(
    os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
).read_bytes()


sf_options = {
    "sfURL": f"{os.getenv('SNOWFLAKE_ACCOUNT')}.snowflakecomputing.com",
    "sfUser": os.getenv("SNOWFLAKE_USER"),
    "pem_private_key": private_key,
    "sfWarehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "sfDatabase": os.getenv("SNOWFLAKE_DATABASE"),
    "sfSchema": os.getenv("SNOWFLAKE_SCHEMA"),
    "sfRole": os.getenv("SNOWFLAKE_ROLE"),
}