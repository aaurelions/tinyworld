import json
import sys
import os
import uuid
import logging
import argparse
from .config import TinyWorldConfig
from .core import TinyWorldProject, Scene
from .shapes import TextShape, ImageShape
from .transitions import Move, FadeIn, FadeOut, Rotate, Scale
from .effects import CrossFade, Slide, Wipe
from .audio import TTS
from .video import TinyWorldVideo

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_script(json_path):
    """
    Parse a JSON file describing the entire video creation script.
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error("Error parsing JSON: %s", e)
        sys.exit(1)

    # Build config
    cfg_data = data.get("config", {})
    config = TinyWorldConfig(
        width=cfg_data.get("width", 1280),
        height=cfg_data.get("height", 720),
        fps=cfg_data.get("fps", 30),
        bg_color=cfg_data.get("bg_color", "white"),
        font_path=cfg_data.get("font_path", None),
        font_size=cfg_data.get("font_size", 40),
        output_file=cfg_data.get("output_file", "tinyworld_output.mp4"),
        tts_lang=cfg_data.get("tts_lang", "en")
    )

    # TTS text
    tts_text = data.get("tts", "")

    # Scenes
    scenes_data = data.get("scenes", [])

    return config, tts_text, scenes_data

def build_project(config, tts_text, scenes_data):
    project = TinyWorldProject(config)

    # Generate TTS (if text given)
    audio_file = None
    if tts_text.strip():
        tts = TTS(tts_text, lang=config.tts_lang)
        audio_file = f"tts_{uuid.uuid4().hex}.mp3"
        tts.generate_audio(audio_file)

    # Convert scenes data
    for sdata in scenes_data:
        duration = sdata.get("duration", 5)
        bg_color = sdata.get("bg_color", config.bg_color)
        scene = Scene(duration=duration, bg_color=bg_color)

        # Add shapes
        for shape_info in sdata.get("shapes", []):
            stype = shape_info.get("type", "text")
            sid = shape_info.get("id")
            x = shape_info.get("x", 0)
            y = shape_info.get("y", 0)

            if stype == "text":
                txt = shape_info.get("text", "Hello, TinyWorld!")
                new_shape = TextShape(sid, txt, x, y)
                scene.add_shape(new_shape)
            elif stype == "image":
                img_path = shape_info.get("image_path", "")
                new_shape = ImageShape(sid, img_path, x, y)
                scene.add_shape(new_shape)

        # Add transitions
        for tinfo in sdata.get("transitions", []):
            name = tinfo.get("name", "")
            shape_id = tinfo.get("shape_id")
            start_time = tinfo.get("start_time", 0.0)
            end_time = tinfo.get("end_time", 1.0)

            if name == "FadeIn":
                tr = FadeIn(shape_id, start_time, end_time)
                scene.add_transition(tr)
            elif name == "FadeOut":
                tr = FadeOut(shape_id, start_time, end_time)
                scene.add_transition(tr)
            elif name == "Move":
                sp = tinfo.get("start_pos", [0, 0])
                ep = tinfo.get("end_pos", [0, 0])
                tr = Move(shape_id, start_time, end_time, (sp[0], sp[1]), (ep[0], ep[1]))
                scene.add_transition(tr)
            elif name == "Rotate":
                sa = tinfo.get("start_angle", 0)
                ea = tinfo.get("end_angle", 360)
                tr = Rotate(shape_id, start_time, end_time, sa, ea)
                scene.add_transition(tr)
            elif name == "Scale":
                ss = tinfo.get("start_scale", 1.0)
                es = tinfo.get("end_scale", 2.0)
                tr = Scale(shape_id, start_time, end_time, ss, es)
                scene.add_transition(tr)

        project.add_scene(scene)

    return project, audio_file

def main():
    parser = argparse.ArgumentParser(description="Create a video with TinyWorld.")
    parser.add_argument("json_path", help="Path to the JSON script")
    args = parser.parse_args()

    json_path = args.json_path

    if not os.path.exists(json_path):
        logger.error("Error: %s not found.", json_path)
        sys.exit(1)

    config, tts_text, scenes_data = parse_script(json_path)
    project, audio_file = build_project(config, tts_text, scenes_data)

    # Render frames
    frames_dir = "tinyworld_frames"
    os.makedirs(frames_dir, exist_ok=True)
    project.render_frames(outdir=frames_dir)

    # Build final video
    tvideo = TinyWorldVideo(config)
    if audio_file:
        tvideo.set_audio(audio_file)
    tvideo.create_video(frames_dir, config.output_file)

    # Clean up temporary files
    if audio_file and os.path.exists(audio_file):
        os.remove(audio_file)

    logger.info("Video created: %s", config.output_file)

if __name__ == "__main__":
    main()
