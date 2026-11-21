"""make.fun news-image-20261120 entry: write the committed picture of
Friday 20 November 2026's world news to the output folder.

The image itself is drawn ahead of time by art/draw.py (Pillow) and
committed as art/entry.png; this program only copies its bytes, so both
graded runs write exactly the same file.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "art", "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT_DIR, "entry.png"))
