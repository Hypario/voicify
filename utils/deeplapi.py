# -*- coding: utf-8 -*-

import logging

import json
import requests

import config


def translate(source_lang, target_lang, text):
    """Translate text using DeepL API"""

    url = config.DEEPL_API_URL
    params = {
        'auth_key': config.DEEPL_API_KEY,
        'source_lang': source_lang,
        'target_lang': target_lang,
        'text': text
    }
    response = requests.post(url, data=params)

    if response.status_code == 200:
        response.encoding = "utf-8"
        response = json.loads(response.text)

        if response['translations']:
            translated = response['translations'][0]['text']

            logging.info("--> %s" % translated)
            return translated
    else:
        logging.error("Error in Deepl API : %s - Fallback to French --> %s" % (response.reason, text))

    return text
