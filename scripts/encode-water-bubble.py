"""Encode Blender RGBA frames as a compact, browser-ready animated WebP."""

from __future__ import annotations

import glob
import os
import sys

from PIL import Image, ImageChops, ImageOps


source = os.path.abspath(sys.argv[1])
destination = os.path.abspath(sys.argv[2])
duration = int(sys.argv[3]) if len(sys.argv) > 3 else 56
mode = sys.argv[4] if len(sys.argv) > 4 else "dark"
paths = sorted(glob.glob(os.path.join(source, "frame_*.png")))

if len(paths) < 2:
	raise SystemExit(f"Expected an image sequence in {source}")

# The final Blender frame exactly repeats the first one, so dropping it avoids a visible pause.
if len(paths) > 2:
	paths = paths[:-1]

frames = []
for path in paths:
	frame = Image.open(path).convert("RGBA")
	if mode == "light":
		red, green, blue, alpha = frame.split()
		luminance = ImageOps.grayscale(frame)
		red = red.point(lambda value: min(255, 30 + round(value * 0.78)))
		green = green.point(lambda value: min(255, 42 + round(value * 0.8)))
		blue = blue.point(lambda value: min(255, 70 + round(value * 0.82)))
		alpha_factor = luminance.point(lambda value: 122 + round(value * 0.52))
		alpha = ImageChops.multiply(alpha, alpha_factor)
		frame = Image.merge("RGBA", (red, green, blue, alpha))
	frames.append(frame)
os.makedirs(os.path.dirname(destination), exist_ok=True)
frames[0].save(
	destination,
	format="WEBP",
	save_all=True,
	append_images=frames[1:],
	duration=duration,
	loop=0,
	quality=84,
	method=6,
	minimize_size=True,
	alpha_quality=92,
)
for frame in frames:
	frame.close()

print(f"Encoded {len(paths)} frames to {destination}")
