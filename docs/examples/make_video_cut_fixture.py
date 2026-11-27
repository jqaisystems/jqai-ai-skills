"""Build fictional review media in a NEW directory: python make_video_cut_fixture.py DIR."""

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def make_fixture(out):
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("Fixture creation requires an existing FFmpeg installation.")
    out.mkdir(exist_ok=False)
    width, height = 320, 180
    font = ImageFont.load_default(size=40)
    with tempfile.TemporaryDirectory() as scratch:
        frames = Path(scratch)
        for i, (word, color) in enumerate([
            ("FOLD", "#165c56"), ("OPEN", "#733b65"), ("PLACE", "#294a88")
        ]):
            image = Image.new("RGB", (width, height), color)
            ImageDraw.Draw(image).text((160, 90), word, font=font, anchor="mm", fill="white")
            image.save(frames / f"card{i}.png")

        run = [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-n"]
        cut = out / "edition-a.mp4"
        subprocess.run(run + [
            "-framerate", "1/2", "-i", str(frames / "card%d.png"),
            "-f", "lavfi", "-i", "sine=frequency=660:duration=0.25",
            "-af", "adelay=4000,apad", "-vf", "fps=12", "-t", "6",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
            "-map_metadata", "-1", str(cut),
        ], check=True)
        # Sample the encoded cut, not the input drawings. No timecodes in the grid.
        grid = Image.new("RGB", (3 * width, height))
        for i, t in enumerate(("1", "3", "5")):
            raw = subprocess.run(run + [
                "-ss", t, "-i", str(cut), "-frames:v", "1", "-f", "rawvideo",
                "-pix_fmt", "rgb24", "pipe:1",
            ], check=True, stdout=subprocess.PIPE).stdout
            grid.paste(Image.frombytes("RGB", (width, height), raw), (i * width, 0))
        grid.save(out / "ordered-grid.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    make_fixture(parser.parse_args().directory)
