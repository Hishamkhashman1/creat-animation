from PIL import Image
import cv2
import numpy as np

INPUT_IMAGE = "avatar_grid.png"   # change this to your image filename
OUTPUT_VIDEO = "avatar_loop.mp4"

COLS = 3
ROWS = 2

FPS = 6
LOOPS = 8

img = Image.open(INPUT_IMAGE).convert("RGB")

w, h = img.size
frame_w = w // COLS
frame_h = h // ROWS

frames = []

# slice top-left to bottom-right
for row in range(ROWS):
    for col in range(COLS):
        left = col * frame_w
        top = row * frame_h
        right = left + frame_w
        bottom = top + frame_h

        frame = img.crop((left, top, right, bottom))
        frames.append(np.array(frame))

# repeat frames for loop duration
video_frames = frames * LOOPS

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(
    OUTPUT_VIDEO,
    fourcc,
    FPS,
    (frame_w, frame_h)
)

for frame in video_frames:
    # RGB to BGR for OpenCV
    out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

out.release()

print(f"Saved: {OUTPUT_VIDEO}")
