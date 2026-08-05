from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse
import requests
import zipfile
import re
from bs4 import BeautifulSoup

from config import FAERS_INDEX_URL, YEARS_TO_DOWNLOAD

def get_faers_xml_urls() -> list[str]:
    """
    Scrape the FDA FAERS page and return all XML ZIP URLs.
    """
    response = requests.get(FAERS_INDEX_URL, timeout=60)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    urls = []

    for link in soup.find_all("a", href=True):
        href = link["href"]

        if href.endswith(".zip") and "xml" in href.lower():
            urls.append(urljoin(FAERS_INDEX_URL, href))

    return urls


def last_five_years(urls: list[str]) -> list[str]:
    current_year = datetime.now().year
    min_year = current_year - YEARS_TO_DOWNLOAD + 1

    selected = []

    for url in urls:
        match = re.search(r"(20\d{2})Q[1-4]", url)

        if match and int(match.group(1)) >= min_year:
            selected.append(url)

    return sorted(selected)


def _download(url: str, destination: Path) -> Path:
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    destination.write_bytes(response.content)

    return destination


def _extract(zip_path: Path, output_dir: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(output_dir)


def _scan(directory: Path) -> list[Path]:
    return list(directory.rglob("*.xml"))


def get_xml_files(url: str, directory: Path) -> list[Path]:
    directory.mkdir(parents=True, exist_ok=True)

    # save the archive using its real filename
    zip_path = directory / Path(urlparse(url).path).name

    _download(url, zip_path)
    _extract(zip_path, directory)

    return _scan(directory)


def download_recent_faers(output_dir: Path) -> list[Path]:
    xml_files = []

    urls = last_five_years(get_faers_xml_urls())

    for url in urls:
        xml_files.extend(get_xml_files(url, output_dir))

    return xml_files