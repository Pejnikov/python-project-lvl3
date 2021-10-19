import requests


def get_page_text(url: str) -> str:
    responce = requests.get(url)
    if responce.status_code != 200:
        raise ValueError('Wrong responce while page request (not 200)')
    return responce.text


def get_page_content(url: str) -> str:
    responce = requests.get(url)
    if responce.status_code != 200:
        raise ValueError('Wrong responce while page request (not 200)')
    return responce.content