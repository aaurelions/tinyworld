# tinyworld/audio.py

import uuid
import os
from gtts import gTTS
from moviepy import AudioFileClip, concatenate_audioclips

class TTS:
    def __init__(self, text, lang="en"):
        self.text = text
        self.lang = lang

    def generate_audio(self, filename=None):
        if not filename:
            filename = f"tts_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=self.text, lang=self.lang)
        tts.save(filename)
        return filename

def combine_audio_clips(clip_paths, output_path):
    clips = [AudioFileClip(p) for p in clip_paths]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)
    [c.close() for c in clips]
