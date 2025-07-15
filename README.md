# TinyWorld

<div style="text-align:center" align="center">
    

https://github.com/user-attachments/assets/68551adc-034b-46f1-9610-d35d30bc322f


</div>

**TinyWorld** is a Python library + CLI that generates short, dynamic, colorful videos with:

- **Text & Image** shapes
- **Transitions** (fade in/out, move, rotate, scale)
- **TTS Audio** (powered by Google gTTS)
- **Scene-based** timeline
- **Automatic** final MP4 creation

## Installation

```bash
pip install tinyworld
```

## Usage (CLI)

1. Create a JSON script (e.g. `example.json`) describing your **config**, **tts** text, **scenes**, **shapes**, **transitions**.
2. Run:

```bash
tinyworld example.json
```

This will produce frames, generate TTS audio if present, and create a final MP4 (the default is `tinyworld_output.mp4` or whatever you set in config).

## Demo

```json
{
  "config": {
    "width": 640,
    "height": 360,
    "fps": 30,
    "bg_color": "white",
    "font_path": null,
    "font_size": 32,
    "output_file": "my_dynamic_video.mp4",
    "tts_lang": "en"
  },
  "tts": "Welcome to the tiny world! Here, shapes and images come to life with simple transitions.",
  "scenes": [
    {
      "duration": 5,
      "bg_color": "white",
      "shapes": [
        {
          "type": "text",
          "id": "intro_text",
          "text": "Hello, TinyWorld!",
          "x": 320,
          "y": 180
        }
      ],
      "transitions": [
        {
          "name": "FadeIn",
          "shape_id": "intro_text",
          "start_time": 0,
          "end_time": 2
        }
      ]
    },
    {
      "duration": 4,
      "bg_color": "white",
      "shapes": [
        {
          "type": "image",
          "id": "logo_img",
          "image_path": "logo.png",
          "x": 200,
          "y": 180
        }
      ],
      "transitions": [
        {
          "name": "Move",
          "shape_id": "logo_img",
          "start_time": 0,
          "end_time": 3,
          "start_pos": [200, 180],
          "end_pos": [440, 180]
        },
        {
          "name": "Rotate",
          "shape_id": "logo_img",
          "start_time": 1,
          "end_time": 4,
          "start_angle": 0,
          "end_angle": 720
        }
      ]
    }
  ]
}
```

[Watch the demo video](my_dynamic_video.mp4)

## Features

- Scene-by-scene animation
- Easy text or image shapes
- Move, rotate, scale, fade in/out
- TTS to add narration over the video
- JSON-based script means **no coding** needed
- Uses [MoviePy](http://zulko.github.io/moviepy/) to merge frames & audio
