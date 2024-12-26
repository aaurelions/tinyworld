import os
from moviepy import ImageSequenceClip, AudioFileClip

class TinyWorldVideo:
    def __init__(self, config):
        self.config = config
        self.audio_clip = None
        self.frame_folder = None

    def set_audio(self, audio_path):
        print(f"Setting audio: {audio_path}")
        if os.path.exists(audio_path):
            self.audio_clip = AudioFileClip(audio_path)
            print(f"Audio clip loaded: {self.audio_clip.filename}")
        else:
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

    def create_video(self, frames_dir, output_path=None):
        """
        Create a video from the frames in the specified directory and optional audio.

        Args:
            frames_dir (str): Directory containing frame images.
            output_path (str): Path to save the output video. Defaults to config output_file.
        """
        self.frame_folder = frames_dir

        if not output_path:
            output_path = self.config.output_file

        # Collect frames from the directory
        frames_list = sorted(
            [
                os.path.join(frames_dir, f)
                for f in os.listdir(frames_dir)
                if f.lower().endswith(".png")
            ]
        )

        if not frames_list:
            raise ValueError(f"No frame images found in directory: {frames_dir}")

        # Create video clip from frames
        clip = ImageSequenceClip(frames_list, fps=self.config.fps)

        print(f"Video duration before audio: {clip.duration} seconds")

        # Add audio if available
        if self.audio_clip:
            audio_duration = self.audio_clip.duration
            video_duration = clip.duration
            final_duration = min(video_duration, audio_duration)

            print(f"Audio file: {self.audio_clip.filename}")
            print(f"Audio duration: {self.audio_clip.duration} seconds")
            print(f"Final duration for video and audio: {final_duration} seconds")

            # Trim audio to match video duration and forcefully set audio
            self.audio_clip = self.audio_clip.subclipped(0, final_duration)
            clip = clip.with_audio(self.audio_clip)
            clip = clip.with_duration(final_duration)

            # Debug: Verify audio stream is set
            assert clip.audio is not None, "Audio was not attached to the video."

        # Write the video file
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")



