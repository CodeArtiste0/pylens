#!/usr/bin/env python3
import os
import sys
import json
from typing import Tuple
from base64 import b64encode
from urllib.parse import urlparse, quote
from search_engines.abs_search_engine import AbsSearchEngine
from search_engines.bing import BingImageSearch

from search_engines.google import GoogleImageSearch
from search_engines.tineye import TineyeImageSearch
from search_engines.yandex import YandexImageSearch

def normalize_url(url):
    parsed_url = urlparse(url)
    url_path = os.path.dirname(parsed_url.path)
    normalized_path = quote(url_path)
    normalized_url = f'{parsed_url.scheme}://{parsed_url.netloc}{normalized_path}'
    return normalized_url


def filter_unique_images(image_urls, processed_urls, lang):
    unique_images = []
    for img_url, img_ref_url in image_urls:
        normalized_url = normalize_url(img_url)
        if normalized_url not in processed_urls:
            processed_urls.add(normalized_url)
            unique_images.append((img_url, img_ref_url, lang))
    return unique_images


def read_langs(file_path):
    if os.path.exists(file_path):
        with open(file_path) as file:
            return [line.strip() for line in file.readlines()]
    else:
        print(f"Language file not found: {file_path}")
        return None


def get_base64_image_uri(image_url, file_content):
    img_type = 'image/png' if image_url.endswith('.png') else 'image/jpeg'
    img_encoded = b64encode(file_content).decode()

    return f"data:{img_type};base64,{img_encoded}"

def search_image(image_url, langs) -> Tuple:
    processed_urls = set()
    all_images = []

    search_engines: list[AbsSearchEngine] = [
        GoogleImageSearch(),
        #BingImageSearch(),
        YandexImageSearch(),
        #TineyeImageSearch()
    ]

    errors = []

    for search_engine in search_engines:
        for lang in langs:
            try:
                html_content = search_engine.send_image(image_url, lang)
                if html_content:
                    image_urls = search_engine.parse_results(html_content)
                    #unique_images = filter_unique_images(image_urls, processed_urls, lang)
                    for img in image_urls:
                        all_images.append({
                            'image_url': img[0],
                            'reference_url': img[1],
                            'language': lang,
                            'search_engine': search_engine.get_name()
                        })
            except Exception as e:
                errors.append(e)

    return (all_images, errors)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("nope, it needs an image!")
        exit()

    image_url = sys.argv[1]

    langs = read_langs('langs.txt') or ['fr', 'en', 'ru', "il"]
    images = search_image(image_url, langs)
    print(json.dumps(images))
