#####################################
#   Author: Debaditya Bhattacharya  #
#   Date:   09 Dec 2021             #
#   e-mail: debbh922@gmail.com      #
#   Desc:   Main file of AV Report  #
#           Generator for SpeEdLabs #
#####################################

# Imports
from tts_engine import TTSEngine
import tempfile
import os
from glob import glob
from text_util import *
from video_util import *
from global_util import *

class AVReportGen():
    """AV Report Generator
    """
    def __init__(self, config) -> None:
        """Constructor for AV Report Generator.

        Args:
            config (default): config.json present in root
        """
        global debug

        # Setup configurations
        self.ttsConfig = config["tts"]
        self.audioConfig = config["audio"]
        self.videoConfig = config["video"]
        self.outputConfig = config["output"]

        # Make Temporary Directory
        self.tempDir = tempfile.TemporaryDirectory()
        os.mkdir(self.tempDir.name+"/audio")
        os.mkdir(self.tempDir.name+"/images")
        os.mkdir(self.tempDir.name+"/video")

        self.audioDir = self.tempDir.name+"/audio/"
        self.imageDir = self.tempDir.name+"/images/"
        self.videoDir = self.tempDir.name+"/video/"

        # Debug Temporary
        # self.audioDir = "./temp"+"/audio/"
        # self.imageDir = "./temp"+"/images/"
        # self.videoDir = "./temp"+"/video/"

        if debug:
            print("Temp folders initiated at",self.tempDir.name)

        # Init TTS Engine
        self.ttsEngine = TTSEngine(self.ttsConfig)
        return

    def generate_AVReport(self, imagePath, textPath):
        """Main driver function. Takes input as path to folder with images, and text file containing lines to be spoken.

        Args:
            imagePath (String): Path to folder with images
            textPath (String): Path to file with text
        """
        global debug
        if debug:
            print("Generating AV Report")

        # Parse Text
        text = parse_text(textPath)
        nSlides = len(text)
        if debug:
            print("Text parsed successfully")

        # Format Text
        paras = merge_lines(text)
        if debug:
            print("Text formatted successfully")
        
        # Speech Synthesis
        for idx, para in enumerate(paras):
            outPath = self.audioDir+str(idx)+".mp3"
            self.ttsEngine.get_response(para, outPath)
        if debug:
            print("Audio samples generated")
        
        # Process Images
        imagePaths = sorted(glob(imagePath+"/*"))
        for idx, imgPath in enumerate(imagePaths):
            outPath = self.imageDir +str(idx) + ".png"
            resize_slide(imgPath,outPath,self.videoConfig["width"],self.videoConfig["height"])
        if debug:
            print("Images resized successfully")

        # Make Videos
        for idx in range(nSlides):
            gen_video(self.imageDir +str(idx) + ".png",self.audioDir+str(idx)+".mp3",self.videoDir +str(idx) + ".mp4")
        if debug:
            print("Videos generated successfully")

        # Stitch Videos:
        stitch_video(self.videoDir,self.outputConfig["path"])
        if debug:
            print("Video output generated")
        return

    def refresh(self):
        """Refresh temporary directory
        """
        self.tempDir.cleanup()
        self.tempDir = tempfile.TemporaryDirectory()
