import requests


def get_page_text(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError('Wrong response while page request (not 200)')
    return response.text


def get_page_content(url: str) -> bytes:
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError('Wrong response while page request (not 200)')
    return response.content
