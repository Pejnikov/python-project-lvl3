from bs4 import BeautifulSoup


def need_localize(url: str) -> bool:
    pass


def localize_page_pictures(page: str, url: str, path: str):
    soup = BeautifulSoup(page, 'html.parser')
    image_tags = soup.find_all('img')
    for tag in image_tags:
        link = tag.get('src')
