import logging

import pyaudio
import wave
import keyboard
import os

from utils import whisperapi

logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)

filename = 'audio.wav'

chunk = 2048
format = pyaudio.paInt16
channels = 1
samplerate = 44100  # sample rate in Hz


# TODO : should return a byte array and send it to the whisper api, no need to save it to a file
def record_audio():
    """Record audio from microphone and save it to a file"""

    if os.path.isfile(filename):
        os.remove(filename)
        logging.info(f'File {filename} already exists. Deleting it.')

    logging.info('Press space bar to start recording')
    keyboard.wait("space")

    logging.info('Recording started')
    keyboard.block_key('space')  # Block the 'space' key

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=samplerate, input=True, frames_per_buffer=chunk)

    frames = []
    while keyboard.is_pressed('space'):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    keyboard.unblock_key('space')  # Unblock the 'space' key

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(samplerate)
    wf.writeframes(b''.join(frames))
    wf.close()

    logging.info(f'Recording stopped. Audio saved to {filename}')


if __name__ == "__main__":
    record_audio()
    transcribed = whisperapi.transcribe()
