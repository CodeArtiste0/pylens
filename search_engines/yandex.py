from search_engines.abs_search_engine import AbsSearchEngine
import requests
import json
from bs4 import BeautifulSoup


class YandexImageSearch(AbsSearchEngine):
    def __init__(self):
        self.base_url = 'https://yandex.com/images/search'

    def send_image(self, image_url: str, lang: str):
        params = {
            'rpt': 'imageview',
            'url': image_url
        }
        response = requests.get(self.base_url, params=params)
        return response.text if response.status_code == 200 else None

    def parse_results(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        data_div = soup.find(lambda tag: tag.name == 'div' and tag.get('id', '').startswith('CbirSites_infinite-'))

        if not data_div or 'data-state' not in data_div.attrs:
            print("Error: The expected content is not found on the page. This might be due to a change in the website's layout. Please report this issue for further assistance.")
            return []

        json_data = json.loads(data_div['data-state'])
        sites = json_data.get('sites', [])

        problematic_domains = ['yandex.com', 'yandex.ru', 'instagram.com', 'facebook.com', 'fbsbx.com', 'tiktok.com']
        image_urls = []

        for site in sites:
            img_url = site.get('url', '')
            img_is_problematic = any(domain in img_url for domain in problematic_domains)

            if img_url.startswith('x-raw-image') or img_is_problematic:
                img_url = site.get('thumb', {}).get('url', '')

            img_ref_url = site.get('originalImage', {}).get('url', '')
            image_urls.append((img_url, img_ref_url))

        return image_urls

