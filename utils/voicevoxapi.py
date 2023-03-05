import logging
from urllib.parse import urlencode
import requests
import winsound

import config


def speak(sentence):
    speaker_id = '14'
    params_encoded = urlencode({
        'text': sentence,
        'speaker': speaker_id
    })

    response = requests.post(f'{config.VOICEVOX_API_URL}/audio_query?{params_encoded}')

    voicevox_query = response.json()
    voicevox_query['volumeScale'] = 4.0
    voicevox_query['intonationScale'] = 1.5
    voicevox_query['prePhonemeLength'] = 1.0
    voicevox_query['postPhonemeLength'] = 1.0

    # synthesize voice as wav file
    logging.info(f'Synthesizing voice for sentence: {sentence}')

    params_encoded = urlencode({'speaker': speaker_id})
    response = requests.post(f'{config.VOICEVOX_API_URL}/synthesis?{params_encoded}', json=voicevox_query)

    if response.status_code == 200:
        logging.info(f'Voice synthesis successful. Saving audio to {config.OUTPUT_AUDIO_FILE}')

        # save the audio to a file
        with open(config.OUTPUT_AUDIO_FILE, 'wb') as f:
            f.write(response.content)

        logging.info(f'Audio saved to {config.OUTPUT_AUDIO_FILE}')

        # play audio file
        logging.info(f'Playing audio file {config.OUTPUT_AUDIO_FILE}')
        winsound.PlaySound(config.OUTPUT_AUDIO_FILE, winsound.SND_FILENAME)
