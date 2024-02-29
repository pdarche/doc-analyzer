import os
import re
import multiprocessing
from openai import OpenAI

import time

client = OpenAI()


class WhisperProcessor(object):
    def __init__(self, datadir, source_path, bucket=None):
        # Processors like textract will sometimes have
        # some kind of python object intermediate representation
        # of the document.
        self.datadir = datadir
        self.source_path = source_path
        self.bucket = bucket

        self.num_subdocs = None
        self.num_pickles = None

    def process(self):
        text_path = f"{self.datadir}/text/chunks"
        chunks_path = f"{self.datadir}/audio/chunks"
        # Create the outut folder if it doesn't exist
        if not os.path.exists(text_path):
            os.mkdir(text_path)

        chunk_ixs = sorted(
            [
                int(re.findall(r"\d+", filename)[0])
                for filename in os.listdir(chunks_path)
            ]
        )

        with multiprocessing.Pool(processes=4) as pool:
            pool.map(self.process_chunk, chunk_ixs)


    def process_chunk(self, chunk_ix):
        text_path = f"{self.datadir}/text/chunks"
        chunks_path = f"{self.datadir}/audio/chunks"

        file_path = f"{chunks_path}/chunk_{chunk_ix}.mp3"
        chunk_text_path = f"{text_path}/chunk_{chunk_ix}.txt"

        if not os.path.exists(chunk_text_path):
            print(f"Chunk {chunk_ix} not found. Transcribing chunk: {file_path}")
            audio_file_chunk = open(file_path, "rb")
            transcript = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file_chunk
            )
            with open(chunk_text_path, "w") as f:
                f.write(transcript.text)


    def get_text(self):
        # Create the outut folder if it doesn't exist
        text_path = f"{self.datadir}/text/chunks"
        if not os.path.exists(text_path):
            os.mkdir(text_path)

        chunks_path = f"{self.datadir}/audio/chunks"
        chunk_ixs = sorted(
            [
                int(re.findall(r"\d+", filename)[0])
                for filename in os.listdir(chunks_path)
            ]
        )

        # Get the audio path chunks
        chunk_text = {}
        for ix in chunk_ixs:
            file_path = f"{chunks_path}/chunk_{ix}.mp3"
            chunk_text_path = f"{text_path}/chunk_{ix}.txt"
            if not os.path.exists(chunk_text_path):
                print(f"Chunk {ix} not found. Transcribing chunk: {file_path}")
                audio_file_chunk = open(file_path, "rb")
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file_chunk
                )
                text = transcript.text
                with open(chunk_text_path, "w") as f:
                    f.write(text)
            else:
                print(f"Chunk {ix} found. Skipping transcription")
                with open(chunk_text_path, "r") as f:
                    text = f.read()
            chunk_text[ix + 1] = text

        # Join the chunks
        full_text = "\n".join(chunk_text.values())
        return full_text, chunk_text
