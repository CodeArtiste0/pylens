from search_engines.abs_search_engine import AbsSearchEngine
from time import time
from io import BytesIO
import requests
from urllib.parse import urlparse, parse_qs, unquote, quote
from bs4 import BeautifulSoup


class GoogleImageSearch(AbsSearchEngine):
    def __init__(self):
        pass

    def send_image(self, image_url: str, lang: str):
        headers = {
            'Cookie': 'NID=511=eoiYVbD3qecDKQrHrtT9_jFCqvrNnL-GSi7lPJANAlHOoYlZOhFjOhPvcc'
                      '-43ZSGmBx_L5D_Irknb8HJvUMo41sCh1i0homN3Taqg2z7mdjnu3AQe-PbpKAyKE4zW1'
                      '-N6niKTJAMkV6Jq4AWPwp6txH_c24gjt7fU3LWAfNIezA'
        }
        timestamp = int(time() * 1000)
        url = f'https://lens.google.com/v3/upload?hl={lang}&re=df&stcs={timestamp}&vpw=1500&vph=1500'

        file_content = self.__load_image_from_url(image_url)
        files = {'encoded_image': (image_url, file_content, 'image/jpeg')}
        response = requests.post(url, files=files, headers=headers)
        return response.text if response.status_code == 200 else None

    def __load_image_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            raise Exception(f"Error fetching image from {url}: Status code {response.status_code}")

    def parse_results(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        divs = soup.find_all('div', class_='Vd9M6')

        if not divs:
            print("Error: The expected content is not found on the page. This might be due to a change in the website's "
                  "layout. Please report this issue for further assistance.")
            return []

        problematic_domains = ['yandex.com', 'yandex.ru', 'instagram.com', 'facebook.com', 'fbsbx.com', 'tiktok.com']

        image_urls = []
        for div in divs:
            action_url = div.get('data-action-url')
            if action_url:
                parsed_url = urlparse(action_url)
                query_params = parse_qs(parsed_url.query)
                img_url = unquote(query_params.get('imgurl', [None])[0])
                img_ref_url = unquote(query_params.get('imgrefurl', [None])[0])

                img_is_problematic = any([p in img_url for p in problematic_domains])
                if img_url.startswith('x-raw-image') or img_is_problematic:
                    div_thumb = div.find(lambda tag:tag.name == "div" and 'data-thumbnail-url' in tag.attrs)
                    img_url = div_thumb.get('data-thumbnail-url')

                image_urls.append((img_url, img_ref_url))

        return image_urls
