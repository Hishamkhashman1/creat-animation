from PIL import Image
import cv2
import numpy as np

INPUT_IMAGE = "avatar_grid_12.png"
OUTPUT_VIDEO = "avatar_loop_clean.mp4"

COLS = 6
ROWS = 3

FPS = 6
LOOPS = 8
HOLD_FRAMES = 4

# use all 18 grid cells
USE_FRAMES = list(range(18))

# inner crop margins to remove neighboring frame bleed
MARGIN_LEFT = 45
MARGIN_RIGHT = 25
MARGIN_TOP = 5
MARGIN_BOTTOM = 5

img = Image.open(INPUT_IMAGE).convert("RGB")

w, h = img.size
frame_w = w // COLS
frame_h = h // ROWS

frames = []

for idx in USE_FRAMES:
    row = idx // COLS
    col = idx % COLS

    left = col * frame_w + MARGIN_LEFT
    top = row * frame_h + MARGIN_TOP
    right = (col + 1) * frame_w - MARGIN_RIGHT
    bottom = (row + 1) * frame_h - MARGIN_BOTTOM

    frame = img.crop((left, top, right, bottom))

    # resize to consistent video size
    frame = frame.resize((720, 720), Image.LANCZOS)

    frames.append(np.array(frame))

video_frames = []

for _ in range(LOOPS):
    for frame in frames:
        video_frames.extend([frame] * HOLD_FRAMES)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(
    OUTPUT_VIDEO,
    fourcc,
    FPS,
    (720, 720)
)

for frame in video_frames:
    out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

out.release()

print(f"Saved: {OUTPUT_VIDEO}")
