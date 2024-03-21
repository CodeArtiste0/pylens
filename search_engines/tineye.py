from search_engines.abs_search_engine import AbsSearchEngine
import requests
import json
from bs4 import BeautifulSoup


class TineyeImageSearch(AbsSearchEngine):
    def __init__(self):
        self.search_url = 'https://tineye.com/result_json/?sort=score&order=desc'

    def send_image(self, image_url: str, lang: str):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        files = {'url': (None, image_url)}
        response = requests.post(self.search_url, headers=headers, files=files)
        if response.status_code < 200 or response.status_code > 299:
            raise Exception(f"Could not send request to Tineye. Status code: {response.status_code}")
        return response.json()

    def parse_results(self, response):
        image_urls = []
        if response and 'matches' in response:
            for match in response['matches']:
                for backlink in match.get('backlinks'):
                    print(backlink)
                    image_urls.append((match.get('image_url'), backlink['backlink']))

        return image_urls
