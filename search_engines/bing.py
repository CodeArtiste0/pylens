from search_engines.abs_search_engine import AbsSearchEngine
from time import time
from io import BytesIO
import requests
from urllib.parse import urlparse, parse_qs, unquote, quote
from bs4 import BeautifulSoup


class BingImageSearch(AbsSearchEngine):
    def __init__(self):
        self.base_url = 'https://www.bing.com/images/searchbyimage'

    def send_image(self, image_url: str, lang: str):
        params = {
            'cbir': 'sbi',
            'imgurl': image_url
        }
        response = requests.get(self.base_url, params=params)
        return response.text if response.status_code == 200 else None

    def parse_results(self, response):
        with open('./bing.html', 'a') as fs:
            fs.write(response)
        soup = BeautifulSoup(response, 'html.parser')
        #divs = soup.find_all('div', class_='relImg')

        if not divs:
            print("Error: The expected content is not found on the page. This might be due to a change in the website's "
                  "layout. Please report this issue for further assistance.")
            return []

        problematic_domains = ['yandex.com', 'yandex.ru', 'instagram.com', 'facebook.com', 'fbsbx.com', 'tiktok.com']

        image_urls = []
        for div in divs:
            print(div)
            # action_url = div.get('data-action-url')
            # if action_url:
            #     parsed_url = urlparse(action_url)
            #     query_params = parse_qs(parsed_url.query)
            #     img_url = unquote(query_params.get('imgurl', [None])[0])
            #     img_ref_url = unquote(query_params.get('imgrefurl', [None])[0])

            #     img_is_problematic = any([p in img_url for p in problematic_domains])
            #     if img_url.startswith('x-raw-image') or img_is_problematic:
            #         div_thumb = div.find(lambda tag:tag.name == "div" and 'data-thumbnail-url' in tag.attrs)
            #         img_url = div_thumb.get('data-thumbnail-url')

            #     print(f"Working on image {img_url} from {img_ref_url}")
            #     image_urls.append((img_url, img_ref_url))

        return image_urls

