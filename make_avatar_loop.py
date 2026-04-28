from PIL import Image
import cv2
import numpy as np

INPUT_IMAGE = "avatar_grid_12.png"
OUTPUT_VIDEO = "avatar_loop_12_frames.mp4"

COLS = 6
ROWS = 3

FPS = 6
LOOPS = 8

# Higher number = frame stays longer
HOLD_FRAMES = 3

img = Image.open(INPUT_IMAGE).convert("RGB")

w, h = img.size
frame_w = w // COLS
frame_h = h // ROWS

frames = []

for row in range(ROWS):
    for col in range(COLS):
        left = col * frame_w
        top = row * frame_h
        right = left + frame_w
        bottom = top + frame_h

        frame = img.crop((left, top, right, bottom))
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
