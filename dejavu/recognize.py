from __future__ import absolute_import
import dejavu.fingerprint as fingerprint
import dejavu.decoder as decoder
import numpy as np
import pyaudio
import time
from six.moves import range
from six.moves import zip

import concurrent.futures
import logging
import traceback
import sys
from config import ChunksTime

logger = logging.getLogger(__name__)


class BaseRecognizer(object):
    def __init__(self, dejavu):
        self.dejavu = dejavu
        self.Fs = fingerprint.DEFAULT_FS

    def _recognize(self, *data):
        matches = []
        for d in data:
            matches.extend(self.dejavu.find_matches(d, Fs=self.Fs)) 
        return self.dejavu.align_matches(matches)

    def recognize(self):
        pass  # base class does nothing
    
    def recognize_chunks(self, filename):
        pass


class FileRecognizer(BaseRecognizer):
    def __init__(self, dejavu):
        super(FileRecognizer, self).__init__(dejavu)

    def recognize_file(self, filename):
        frames, self.Fs = decoder.read(filename, self.dejavu.limit)

        t = time.time()
        match = self._recognize(*frames)
        t = time.time() - t

        if match:
            match['match_time'] = t
        return match

    def recognize_chunks(self, filename):
        frames, self.Fs = decoder.read_chunks(filename, self.dejavu.limit)
        chunk_matches = []
        t = time.time()
        for i, val in enumerate(frames):
            match = self._recognize(*val)
            match['segment_id'] = i
            match['start_time'] = i*ChunksTime/1000
            chunk_matches.append(match)
        t = time.time() - t

        #if match:
        #    match['match_time'] = t
        return chunk_matches
    

    def recognize(self, filename):
        return self.recognize_file(filename)
    
    def find_fingerprint_matches(self, worker_input):
        return self.dejavu.find_matches(worker_input[0], worker_input[1])


class MicrophoneRecognizer(BaseRecognizer):
    default_chunksize = 8192
    default_format = pyaudio.paInt16
    default_channels = 2
    default_samplerate = 44100

    def __init__(self, dejavu):
        super(MicrophoneRecognizer, self).__init__(dejavu)
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.data = []
        self.channels = MicrophoneRecognizer.default_channels
        self.chunksize = MicrophoneRecognizer.default_chunksize
        self.samplerate = MicrophoneRecognizer.default_samplerate
        self.recorded = False

    def start_recording(
        self,
        channels=default_channels,
        samplerate=default_samplerate,
        chunksize=default_chunksize
    ):
        self.chunksize = chunksize
        self.channels = channels
        self.recorded = False
        self.samplerate = samplerate

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        self.stream = self.audio.open(
            format=self.default_format,
            channels=channels,
            rate=samplerate,
            input=True,
            frames_per_buffer=chunksize,
        )

        self.data = [[] for i in range(channels)]

    def process_recording(self):
        data = self.stream.read(self.chunksize)
        nums = np.fromstring(data, np.int16)
        for c in range(self.channels):
            self.data[c].extend(nums[c::self.channels])

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        self.recorded = True

    def recognize_recording(self):
        if not self.recorded:
            raise NoRecordingError("Recording was not complete/begun")
        return self._recognize(*self.data)

    def get_recorded_time(self):
        return len(self.data[0]) / self.rate

    def recognize(self, seconds=10):
        self.start_recording()
        for i in range(0, int(self.samplerate / self.chunksize * seconds)):
            self.process_recording()
        self.stop_recording()
        return self.recognize_recording()


class NoRecordingError(Exception):
    pass
