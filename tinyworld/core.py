# tinyworld/core.py

import os
import math
from PIL import Image, ImageDraw, ImageFont

from .shapes import Shape, TextShape, ImageShape
from .transitions import (
    FadeIn, FadeOut, Move, Rotate, Scale
)

class Scene:
    def __init__(self, duration=5.0, bg_color="white"):
        self.duration = duration
        self.bg_color = bg_color
        self.shapes = {}
        self.transitions = []

    def add_shape(self, shape):
        self.shapes[shape.shape_id] = shape

    def add_transition(self, transition):
        self.transitions.append(transition)

class TinyWorldProject:
    def __init__(self, config):
        self.config = config
        self.scenes = []
        self.total_duration = 0.0

    def add_scene(self, scene):
        self.scenes.append(scene)
        self.total_duration += scene.duration

    def render_frames(self, outdir="tinyworld_frames"):
        os.makedirs(outdir, exist_ok=True)
        current_start_time = 0.0
        frame_index = 0

        # Attempt to load a user-provided font, else default
        try:
            font = ImageFont.truetype(
                self.config.font_path, self.config.font_size
            ) if self.config.font_path else ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        for scene in self.scenes:
            frames_in_scene = int(scene.duration * self.config.fps)
            for f in range(frames_in_scene):
                t = f / self.config.fps
                global_t = current_start_time + t

                # Create background
                img = Image.new("RGBA", (self.config.width, self.config.height), scene.bg_color)
                draw = ImageDraw.Draw(img)

                for shape_id, shape in scene.shapes.items():
                    shape_opacity = shape.opacity
                    shape_x = shape.x
                    shape_y = shape.y
                    shape_rotation = shape.rotation
                    shape_scale = shape.scale

                    # Apply transitions
                    relevant = [tr for tr in scene.transitions if tr.shape_id == shape_id]
                    for tr in relevant:
                        # If time is within or before/after transition
                        if tr.start_time <= t <= tr.end_time:
                            frac = (t - tr.start_time) / (tr.end_time - tr.start_time)
                            if isinstance(tr, FadeIn):
                                shape_opacity = frac
                            elif isinstance(tr, FadeOut):
                                shape_opacity = 1.0 - frac
                            elif isinstance(tr, Move):
                                sx, sy = tr.start_pos
                                ex, ey = tr.end_pos
                                shape_x = sx + (ex - sx) * frac
                                shape_y = sy + (ey - sy) * frac
                            elif isinstance(tr, Rotate):
                                shape_rotation = tr.start_angle + (tr.end_angle - tr.start_angle)*frac
                            elif isinstance(tr, Scale):
                                shape_scale = tr.start_scale + (tr.end_scale - tr.start_scale)*frac
                        else:
                            # times outside transitions
                            if isinstance(tr, FadeIn):
                                if t < tr.start_time:
                                    shape_opacity = 0.0
                                elif t > tr.end_time:
                                    shape_opacity = 1.0
                            elif isinstance(tr, FadeOut):
                                if t < tr.start_time:
                                    shape_opacity = 1.0
                                elif t > tr.end_time:
                                    shape_opacity = 0.0
                            elif isinstance(tr, Move):
                                if t < tr.start_time:
                                    shape_x, shape_y = tr.start_pos
                                elif t > tr.end_time:
                                    shape_x, shape_y = tr.end_pos
                            elif isinstance(tr, Rotate):
                                if t < tr.start_time:
                                    shape_rotation = tr.start_angle
                                elif t > tr.end_time:
                                    shape_rotation = tr.end_angle
                            elif isinstance(tr, Scale):
                                if t < tr.start_time:
                                    shape_scale = tr.start_scale
                                elif t > tr.end_time:
                                    shape_scale = tr.end_scale

                    # no need to draw if fully invisible
                    if shape_opacity <= 0:
                        continue

                    if isinstance(shape, TextShape):
                        # scale the font
                        scaled_font_size = int(self.config.font_size * shape_scale)
                        try:
                            shape_font = ImageFont.truetype(
                                self.config.font_path, scaled_font_size
                            ) if self.config.font_path else font
                        except:
                            shape_font = font

                        bbox = draw.textbbox((0, 0), shape.text, font=shape_font)
                        text_w = bbox[2] - bbox[0]
                        text_h = bbox[3] - bbox[1]                        
                        rx = shape_x - text_w/2
                        ry = shape_y - text_h/2
                        # draw text w/ alpha
                        # PIL doesn't do alpha in text directly, so we can cheat with a separate overlay
                        txt_img = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
                        d2 = ImageDraw.Draw(txt_img)
                        d2.text((0, 0), shape.text, font=shape_font, fill=(0, 0, 0, int(255*shape_opacity)))
                        # if shape_rotation != 0 => rotate txt_img
                        if shape_rotation != 0:
                            txt_img = txt_img.rotate(shape_rotation, expand=1)
                        img.alpha_composite(txt_img, (int(rx), int(ry)))

                    elif isinstance(shape, ImageShape):
                        from PIL import Image as PILImage
                        if os.path.exists(shape.image_path):
                            shape_img = PILImage.open(shape.image_path).convert("RGBA")
                            w, h = shape_img.size
                            nw, nh = int(w*shape_scale), int(h*shape_scale)
                            shape_img = shape_img.resize((nw, nh))
                            if shape_rotation != 0:
                                shape_img = shape_img.rotate(shape_rotation, expand=True)
                            # apply opacity
                            alpha = shape_img.split()[3]
                            alpha = alpha.point(lambda i: int(i * shape_opacity))
                            shape_img.putalpha(alpha)
                            px = int(shape_x - nw/2)
                            py = int(shape_y - nh/2)
                            img.alpha_composite(shape_img, (px, py))

                # Save frame
                outpath = os.path.join(outdir, f"tinyworld_{frame_index:06d}.png")
                img.save(outpath)
                frame_index += 1

            current_start_time += scene.duration

