import requests
from pathlib import Path

REQUEST_HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}


class WebPageContentRequestException(requests.RequestException):
    pass


def get_webpage_content(url: str):
    """
    If response is redirected then response.history is not empty
    :param url:
    :return:
    """
    response = requests.get(url, headers=REQUEST_HEADER)
    if response.status_code == 200 and not response.history:
        return response.content
    raise WebPageContentRequestException(f"Request returned status code different than 200: {response.status_code}")


def download_file(file_url: str, path: Path):
    with open(path, "wb") as file:
        file.write(requests.get(file_url, headers=REQUEST_HEADER).content)
