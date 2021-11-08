import requests
from page_loader.internal_exceptions import PageRequestError  # type: ignore


def get_page_text(url: str) -> str:
    response = get_response(url)
    return response.text


def get_page_content(url: str) -> bytes:
    response = get_response(url)
    return response.content


def get_response(url: str) -> requests.models.Response:
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as err:
        raise PageRequestError(err.args) from err
    else:
        return response
