from __future__ import annotations

import math
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WIDTH, HEIGHT = 960, 540
FPS = 12
FRAMES = 72


def font(name: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = {
        "regular": [
            Path("C:/Windows/Fonts/segoeui.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ],
        "bold": [
            Path("C:/Windows/Fonts/segoeuib.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ],
        "mono": [
            Path("C:/Windows/Fonts/consola.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
        ],
        "mono_bold": [
            Path("C:/Windows/Fonts/consolab.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"),
        ],
    }[name]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


F_REG = font("regular", 18)
F_SMALL = font("regular", 14)
F_TINY = font("regular", 12)
F_BOLD = font("bold", 24)
F_HERO = font("bold", 34)
F_MONO = font("mono", 17)
F_MONO_SMALL = font("mono", 14)
F_MONO_BOLD = font("mono_bold", 17)


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def blend(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(round(lerp(a, b, t)) for a, b in zip(c1, c2))


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, fill: str, fnt: ImageFont.ImageFont) -> None:
    draw.text(xy, value, fill=fill, font=fnt)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: str, outline: str | None = None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def soft_shadow(base: Image.Image, box: tuple[int, int, int, int], radius: int, color=(0, 0, 0, 120), blur=18) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    offset = 8
    d.rounded_rectangle((box[0], box[1] + offset, box[2], box[3] + offset), radius=radius, fill=color)
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def wrap_lines(draw: ImageDraw.ImageDraw, value: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = value.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def terminal_text(t: float) -> tuple[str, list[str], str]:
    install_cmd = ".\\install.ps1 release-announcement-writer"
    prompt = "Use $release-announcement-writer to turn this changelog into release notes and a launch post."

    install_t = ease((t - 0.08) / 0.22)
    typed_install = install_cmd[: round(len(install_cmd) * install_t)]

    output: list[str] = []
    if t > 0.33:
        output.append("Installed release-announcement-writer -> ~/.codex/skills/release-announcement-writer")
    if t > 0.44:
        output.append("Restart Codex so the skill list refreshes.")

    prompt_t = ease((t - 0.52) / 0.28)
    typed_prompt = prompt[: round(len(prompt) * prompt_t)]
    return typed_install, output, typed_prompt


def draw_terminal(draw: ImageDraw.ImageDraw, t: float) -> None:
    box = (52, 150, 590, 430)
    rounded(draw, box, 14, "#09111a", "#1f3545", 1)
    rounded(draw, (52, 150, 590, 186), 14, "#101d29", "#1f3545", 1)
    draw.rectangle((52, 172, 590, 186), fill="#101d29")

    for i, col in enumerate(["#ff5f57", "#ffbd2e", "#28c840"]):
        draw.ellipse((74 + i * 24, 163, 86 + i * 24, 175), fill=col)
    text(draw, (488, 160), "PowerShell", "#7fa2b7", F_TINY)

    typed_install, output_lines, typed_prompt = terminal_text(t)
    y = 208
    text(draw, (76, y), "PS> ", "#00a8d6", F_MONO_BOLD)
    text(draw, (118, y), typed_install, "#e6f4fb", F_MONO)
    if typed_install and t < 0.32 and int(t * 20) % 2 == 0:
        x = 118 + round(draw.textlength(typed_install, font=F_MONO))
        draw.rectangle((x + 2, y + 3, x + 9, y + 22), fill="#00a8d6")

    y += 38
    for line in output_lines:
        for wrapped in wrap_lines(draw, line, F_MONO_SMALL, 480):
            text(draw, (76, y), wrapped, "#8ad7a6" if line.startswith("Installed") else "#9fb3c1", F_MONO_SMALL)
            y += 24

    if t > 0.50:
        y += 12
        text(draw, (76, y), "Prompt", "#00d4a6", F_MONO_BOLD)
        y += 28
        for wrapped in wrap_lines(draw, typed_prompt, F_MONO_SMALL, 470):
            text(draw, (76, y), wrapped, "#eaf6fb", F_MONO_SMALL)
            y += 23


def draw_output_panel(draw: ImageDraw.ImageDraw, t: float) -> None:
    box = (620, 150, 908, 430)
    rounded(draw, box, 14, "#0c1621", "#213747", 1)
    text(draw, (646, 174), "Release pack", "#eaf6fb", F_BOLD)
    text(draw, (646, 206), "Generated from one skill prompt", "#88a0ad", F_SMALL)

    items = [
        ("GitHub release notes", "Version, highlights, install notes"),
        ("Website blurb", "Short case-study update copy"),
        ("Launch post", "LinkedIn/GitHub/X ready text"),
    ]

    start = 0.62
    for idx, (title, desc) in enumerate(items):
        item_t = ease((t - (start + idx * 0.09)) / 0.18)
        y = 250 + idx * 56
        alpha_shift = round(18 * (1 - item_t))
        rounded(draw, (646 + alpha_shift, y, 878 + alpha_shift, y + 42), 10, "#111f2a", "#254455", 1)
        if item_t > 0.15:
            draw.ellipse((662 + alpha_shift, y + 13, 678 + alpha_shift, y + 29), fill="#00d4a6")
            text(draw, (690 + alpha_shift, y + 7), title, "#f4fbff", F_SMALL)
            text(draw, (690 + alpha_shift, y + 25), desc, "#8ea4b1", F_TINY)

    if t > 0.86:
        pulse = 0.5 + 0.5 * math.sin(t * math.pi * 10)
        rounded(draw, (756, 408, 878, 426), 9, blend((0, 126, 170), (0, 212, 166), pulse * 0.35), None)
        text(draw, (781, 410), "READY", "#041018", F_TINY)


def draw_timeline(draw: ImageDraw.ImageDraw, t: float) -> None:
    x0, y = 94, 472
    width = 772
    draw.line((x0, y, x0 + width, y), fill="#203442", width=4)
    draw.line((x0, y, x0 + round(width * t), y), fill="#00a8d6", width=4)
    steps = [("Install", 0.20), ("Invoke", 0.55), ("Publish copy", 0.86)]
    for label, pos in steps:
        x = x0 + round(width * pos)
        active = t >= pos - 0.08
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill="#00d4a6" if active else "#0f1d28", outline="#00a8d6", width=2)
        tw = draw.textlength(label, font=F_TINY)
        text(draw, (round(x - tw / 2), y + 18), label, "#c7d8e2" if active else "#6f8796", F_TINY)


def draw_frame(index: int) -> Image.Image:
    t = index / (FRAMES - 1)
    img = Image.new("RGBA", (WIDTH, HEIGHT), "#071018")
    d = ImageDraw.Draw(img)

    for y in range(HEIGHT):
        d.line((0, y, WIDTH, y), fill=blend((6, 13, 20), (12, 25, 34), y / HEIGHT))

    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((620, -90, 1080, 310), fill=(0, 168, 214, 42))
    gd.ellipse((-120, 170, 300, 610), fill=(110, 74, 255, 34))
    gd.ellipse((480, 250, 1100, 740), fill=(0, 212, 166, 24))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(42)))

    soft_shadow(img, (52, 150, 590, 430), 14)
    soft_shadow(img, (620, 150, 908, 430), 14)

    d = ImageDraw.Draw(img)
    text(d, (52, 42), "JQ AI Skills", "#f3fbff", F_HERO)
    rounded(d, (258, 48, 338, 76), 14, "#0e2f3d", "#00a8d6", 1)
    text(d, (276, 54), "v0.2.5", "#9be9ff", F_TINY)
    text(d, (52, 90), "Install a reusable workflow, then ask it to write release copy.", "#a9bcc8", F_REG)

    rounded(d, (52, 116, 240, 136), 10, "#112332", "#244456", 1)
    text(d, (68, 119), "Codex / Claude-style skill folders", "#9ec8d8", F_TINY)

    draw_terminal(d, t)
    draw_output_panel(d, t)
    draw_timeline(d, t)
    return img.convert("RGB")


def run_ffmpeg(args: list[str]) -> bool:
    try:
        subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    frames = [draw_frame(i) for i in range(FRAMES)]

    poster = ASSETS / "skill-install-demo-poster.png"
    frames[0].save(poster)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for i, frame in enumerate(frames):
            frame.save(tmp_path / f"frame_{i:03d}.png")

        pattern = str(tmp_path / "frame_%03d.png")
        mp4 = ASSETS / "skill-install-demo.mp4"
        gif = ASSETS / "skill-install-demo.gif"

        run_ffmpeg([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(FPS), "-i", pattern,
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(mp4),
        ])

        palette = tmp_path / "palette.png"
        if run_ffmpeg([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(FPS), "-i", pattern,
            "-vf", "palettegen=max_colors=128", str(palette),
        ]):
            run_ffmpeg([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-framerate", str(FPS), "-i", pattern, "-i", str(palette),
                "-lavfi", "paletteuse=dither=bayer:bayer_scale=5",
                "-loop", "0", str(gif),
            ])
        else:
            frames[0].save(gif, save_all=True, append_images=frames[1:], duration=round(1000 / FPS), loop=0, optimize=True)

    print(f"Wrote {poster.relative_to(ROOT)}")
    print(f"Wrote {(ASSETS / 'skill-install-demo.gif').relative_to(ROOT)}")
    print(f"Wrote {(ASSETS / 'skill-install-demo.mp4').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
