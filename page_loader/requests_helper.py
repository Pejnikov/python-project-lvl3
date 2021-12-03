from typing import Callable
import requests
from page_loader.internal_exceptions import PageRequestError  # type: ignore


def handle_requests_exceptions(func):
    def inner(url: str) -> Callable:
        try:
            return func(url)
        except requests.exceptions.RequestException as err:
            error_msg = f"Failed to get '{url}' with error: {err.args}"
            raise PageRequestError(error_msg) from err
    return inner


@handle_requests_exceptions
def get_page_text(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


@handle_requests_exceptions
def get_response_with_content(url: str) -> requests.Response:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    return response
