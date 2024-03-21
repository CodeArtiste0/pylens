#!/usr/bin/env python3
import os
import sys
import json
from typing import Tuple
from base64 import b64encode
from urllib.parse import urlparse, quote
from flask import Flask, request, render_template
from search_engines.abs_search_engine import AbsSearchEngine
from search_engines.bing import BingImageSearch
from search_engines.google import GoogleImageSearch
from search_engines.tineye import TineyeImageSearch
from search_engines.yandex import YandexImageSearch

app = Flask(__name__)

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

def search_image(image_url, langs, selected_engines) -> Tuple:
    processed_urls = set()
    all_images = []
    search_engines = []

    if 'google' in selected_engines:
        search_engines.append(GoogleImageSearch())
    if 'bing' in selected_engines:
        search_engines.append(BingImageSearch())
    if 'yandex' in selected_engines:
        search_engines.append(YandexImageSearch())
    if 'tineye' in selected_engines:
        search_engines.append(TineyeImageSearch())

    errors = []

    for search_engine in search_engines:
        for lang in langs:
            try:
                html_content = search_engine.send_image(image_url, lang)
                if html_content:
                    image_urls = search_engine.parse_results(html_content)
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_url = request.form['image_url']
        langs = read_langs('langs.txt') or ['fr', 'en', 'ru', "il"]
        selected_engines = request.form.getlist('search_engine')
        images, errors = search_image(image_url, langs, selected_engines)
        return render_template('results.html', images=images, errors=errors)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
