from PIL import Image
import cv2
import numpy as np

INPUT_IMAGE = "avatar_grid.png"
OUTPUT_VIDEO = "avatar_loop_slow.mp4"

COLS = 3
ROWS = 2

FPS = 4
LOOPS = 6

HOLD_FRAMES = {
    0: 8,   # neutral smirk
    1: 2,   # blink
    2: 5,   # mouth slightly open
    3: 5,   # eyebrow raised
    4: 5,   # speaking mouth
    5: 8,   # back to neutral
}

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
    for i, frame in enumerate(frames):
        video_frames.extend([frame] * HOLD_FRAMES[i])

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
