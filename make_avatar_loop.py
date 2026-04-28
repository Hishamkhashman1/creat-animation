from PIL import Image
import cv2
import numpy as np

INPUT_IMAGE = "avatar_grid_12.png"
OUTPUT_VIDEO = "avatar_loop_fixed.mp4"

COLS = 6
ROWS = 3

FPS = 6
LOOPS = 8
HOLD_FRAMES = 4

# choose only clean frames, zero-indexed:
# row 0: 0 1 2 3 4 5
# row 1: 6 7 8 9 10 11
# row 2: 12 13 14 15 16 17
USE_FRAMES = [0, 1, 2, 3, 4, 5, 8, 10, 11, 14, 15, 16]

img = Image.open(INPUT_IMAGE).convert("RGB")

w, h = img.size
frame_w = w // COLS
frame_h = h // ROWS

frames = []

for idx in USE_FRAMES:
    row = idx // COLS
    col = idx % COLS

    left = col * frame_w
    top = row * frame_h
    right = left + frame_w
    bottom = top + frame_h

    frame = img.crop((left, top, right, bottom))

    # remove tiny edge artifacts
    frame = frame.crop((8, 8, frame_w - 8, frame_h - 8))

    # resize all frames back to same output size
    frame = frame.resize((frame_w, frame_h), Image.LANCZOS)

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
    (frame_w, frame_h)
)

for frame in video_frames:
    out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

out.release()

print(f"Saved: {OUTPUT_VIDEO}")
