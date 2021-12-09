#####################################
#   Author: Debaditya Bhattacharya  #
#   Date:   09 Dec 2021             #
#   e-mail: debbh922@gmail.com      #
#   Desc:   Main file of AV Report  #
#           Generator for SpeEdLabs #
#####################################

from PIL import Image
import subprocess
from glob import glob
import os
from global_util import *


def resize_slide(imgPath, outPath, W, H):
    """Resizes images to specified dimentions.

    Args:
        sNo (int): Slide number
        W (int): Output width in px
        H (int): Output height in px
    """
    # TODO
    image = Image.open(imgPath, 'r')
    w, h = image.size
    ar = float(w/h)

    # Resizing while maintaining aspect ratio
    if w > W:
        w = W
        h = int(round(W/ar))

    if h > H:
        w = int(round(H*ar))
        h = H

    image = image.resize((w, h))

    # Generate whitebackground
    background = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    offset = (int(round(((W - w) / 2), 0)), int(round(((H - h) / 2), 0)))

    # Paste and save background
    background.paste(image, offset)
    background.save(outPath)


def gen_video(imgPath, audioPath, outPath):
    """Generate video by calling FFmpeg subprocess call. Length of video is length of audio.

    Args:
        imgPath (String): Path to image to be displayed
        audioPath ([type]): Path to audio to be played
        outPath ([type]): Output path
    """
    global debug
    if not debug:
        subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", imgPath, "-i",
                        audioPath, "-c:v", "libx264", "-tune", "stillimage",
                        "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest",
                        outPath], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    else:
        subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", imgPath, "-i",
                        audioPath, "-c:v", "libx264", "-tune", "stillimage",
                        "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest",
                        outPath])


def stitch_video(videoPath, outPath):
    """Stitches generated video slides into one final output video using FFmpeg

    Args:
        videoPath (string): Path to folder with video files
        outPath (string): Path to output
    """

    global debug
    # Remove file
    if os.path.isfile(videoPath+"videoList.txt"):
        os.remove(videoPath+"videoList.txt")

    files = sorted(glob(videoPath+"/*"))
    videoList = open(videoPath+"videoList.txt", "a")  # append mode
    for file in files:
        videoList.write("file '"+file+"'\n")
    videoList.close()

    if not debug:
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i",
                        videoPath+"videoList.txt", "-c", "copy", outPath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i",
                        videoPath+"videoList.txt", "-c", "copy", outPath])
    return
