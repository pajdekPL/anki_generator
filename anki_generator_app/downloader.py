import requests
from pathlib import Path

REQUEST_HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}


def get_webpage_content(url: str):
    return requests.get(url, headers=REQUEST_HEADER).content


def download_file(file_url: str, path: Path):
    with open(path, "wb") as file:
        file.write(requests.get(file_url, headers=REQUEST_HEADER).content)
