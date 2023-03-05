import logging

import requests
import json


def transcribe() -> str:
    """Transcribe audio using the whisper api
    :return: the text transcribed
    """

    logging.info('Transcribing audio')

    # url of the whisper api, TODO : make it configurable
    url = 'http://localhost:9000/asr?task=transcribe&language=fr&output=json'

    # open the audio file, TODO : pass it through parameters
    files = {'audio_file': open('audio.wav', 'rb')}

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
            logging.info("\t--> %s" % text)

            return text
        else:
            logging.info("\t--> No text found")
            return ""
    else:
        logging.error(f'Error while transcribing audio. Status code: {response.status_code}')
        raise Exception('Error while transcribing audio')
