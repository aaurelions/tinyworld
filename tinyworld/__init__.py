# tinyworld/__init__.py

__version__ = "0.1.0"

from .audio import TTS, combine_audio_clips
from .cli import main as cli_main
from .config import TinyWorldConfig
from .core import TinyWorldProject, Scene
from .effects import CrossFade, Slide, Wipe
from .shapes import Shape, TextShape, ImageShape
from .transitions import (
    Transition, FadeIn, FadeOut, Move, Rotate, Scale
)
from .video import TinyWorldVideo
