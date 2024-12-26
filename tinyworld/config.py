# tinyworld/config.py

class TinyWorldConfig:
    def __init__(
        self,
        width=1280,
        height=720,
        fps=30,
        bg_color="white",
        font_path=None,
        font_size=40,
        output_file="tinyworld_output.mp4",
        tts_lang="en"
    ):
        self.width = width
        self.height = height
        self.fps = fps
        self.bg_color = bg_color
        self.font_path = font_path
        self.font_size = font_size
        self.output_file = output_file
        self.tts_lang = tts_lang
