# -*- coding: utf-8 -*-

import logging

import requests
import json

import config


def transcribe(audio_file: str) -> str:
    """Transcribe audio using the whisper api
    :return: the text transcribed
    """

    logging.info('Transcribing audio')

    url = config.WHISPER_API_URL

    files = {'audio_file': open(audio_file, 'rb')}

    response = requests.post(url, files=files)

    if response.status_code == 200:
        response.encoding = "utf-8"
        response = json.loads(response.text)

        logging.info('Successfully transcribed audio')
        if response["text"]:
            try:
                text = response["text"].encode("raw_unicode_escape").decode("utf-8")
            except UnicodeDecodeError:
                text = response["text"]
            logging.info("-->%s" % text)

            return text
        else:
            logging.info("--> No text found")
            return ""
    else:
        logging.error(f'Error while transcribing audio. Status code: {response.status_code}')
        raise Exception('Error while transcribing audio')
