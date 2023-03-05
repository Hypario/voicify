# -*- coding: utf-8 -*-

import logging

import pyaudio
import wave
import keyboard
import os

import config

from utils import whisperapi, deeplapi, voicevoxapi

logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    encoding="utf-8",
    level=logging.INFO)

chunk = 2048
format = pyaudio.paInt16
channels = 1
samplerate = 44100  # sample rate in Hz


def record_audio():
    """Record audio from microphone and save it to a file"""

    logging.info('Press space bar to start recording')
    keyboard.wait(config.RECORD_KEY, suppress=True)  # Wait for the 'space' key to be pressed, suppress its output

    logging.info('Recording started')
    keyboard.block_key(config.RECORD_KEY)  # Block the 'space' key

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=samplerate, input=True, frames_per_buffer=chunk)

    # record audio
    frames = []
    while keyboard.is_pressed(config.RECORD_KEY):
        data = stream.read(chunk)
        frames.append(data)

    # stop recording when key is released
    stream.stop_stream()
    stream.close()
    p.terminate()

    keyboard.unblock_key(config.RECORD_KEY)  # Unblock the record key

    # save the audio to a file
    wf = wave.open(config.INPUT_AUDIO_FILE, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(samplerate)
    wf.writeframes(b''.join(frames))
    wf.close()

    logging.info(f'Recording stopped. Audio saved to {config.INPUT_AUDIO_FILE}')


if __name__ == "__main__":
    while True:
        if os.path.isfile(config.INPUT_AUDIO_FILE):
            os.remove(config.INPUT_AUDIO_FILE)
            logging.info(f'File {config.INPUT_AUDIO_FILE} already exists. Deleting it.')

        if os.path.isfile(config.OUTPUT_AUDIO_FILE):
            os.remove(config.OUTPUT_AUDIO_FILE)
            logging.info(f'File {config.OUTPUT_AUDIO_FILE} already exists. Deleting it.')

        record_audio()
        transcribed = whisperapi.transcribe(config.INPUT_AUDIO_FILE)
        translated = deeplapi.translate("FR", "JA", transcribed)
        voicevoxapi.speak(translated)
