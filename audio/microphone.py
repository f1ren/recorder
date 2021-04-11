import os
import wave

import pyaudio

from common.consts import RECORDS_PATH, WAV_FILE_NAME
from common.log import debug
from common.process_sync import should_stop

FRAME_RATE = 16000

SAMPLE_FORMAT = pyaudio.paInt16


class MicArray:
    def __init__(self, output_path=None, rate=FRAME_RATE, chunk_size=None):
        self.pyaudio_instance = None
        self.stream = None
        self.channels = None
        self.sample_rate = rate
        self.chunk_size = chunk_size if chunk_size else None
        os.makedirs(RECORDS_PATH, exist_ok=True)
        self._output_path = output_path if output_path else os.path.join(RECORDS_PATH, WAV_FILE_NAME)
        self.frames = []

    def _select_mic_device_index(self):
        max_channels = 0
        max_channels_device_index = None
        for i in range(self.pyaudio_instance.get_device_count()):
            dev = self.pyaudio_instance.get_device_info_by_index(i)
            name = dev['name'].encode('utf-8')
            input_channels = dev['maxInputChannels']
            debug(
                'Listing audio device',
                index=i,
                name=name,
                in_channels=input_channels
            )
            if input_channels > max_channels:
                max_channels = input_channels
                max_channels_device_index = i
        if max_channels_device_index is None:
            raise Exception('can not find input device')
        self.channels = max_channels
        self.chunk_size = self.chunk_size if self.chunk_size else self.sample_rate // self.channels
        debug('Audio device', channels=max_channels)
        return max_channels_device_index

    def run(self):
        self.frames = []
        self.pyaudio_instance = pyaudio.PyAudio()
        device_index = self._select_mic_device_index()
        self.stream = self.pyaudio_instance.open(
            format=SAMPLE_FORMAT,
            channels=self.channels,
            rate=self.sample_rate,
            frames_per_buffer=self.chunk_size,
            input=True,
            input_device_index=device_index,
        )

        debug('Recording audio')

        frames = []  # Initialize array to store frames


        try:
            while True:
                data = self.stream.read(self.chunk_size)
                frames.append(data)
                if should_stop():
                    raise KeyboardInterrupt()
        except KeyboardInterrupt:
            debug('Quitting audio recording')

        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()
        # Terminate the PortAudio interface
        self.pyaudio_instance.terminate()

        debug('Finished recording audio')

        # Save the recorded data as a WAV file
        wf = wave.open(self._output_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.pyaudio_instance.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()


def audio_capture():
    mic = MicArray()
    mic.run()
