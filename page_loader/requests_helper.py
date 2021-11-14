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
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        error_msg = "Failed to get '{}' with error: {}".format(url, err.args)
        raise PageRequestError(error_msg) from err
    else:
        return response
