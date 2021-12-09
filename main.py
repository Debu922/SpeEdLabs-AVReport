#####################################
#   Author: Debaditya Bhattacharya  #
#   Date:   09 Dec 2021             #
#   e-mail: debbh922@gmail.com      #
#   Desc:   Main file of AV Report  #
#           Generator for SpeEdLabs #
#####################################

# Imports
import sys
sys.path.append('./src/')
import json
import datetime
from driver import AVReportGen
from tts_engine import TTSEngine
from global_util import *



def main():
    # Change debug option in global_util module
    global debug

    # Load config
    config_file = open("config.json")
    config = json.load(config_file)

    # Initiate
    inst = AVReportGen(config)

    # Generate Report
    inst.generate_AVReport("./tests/data/images", "./tests/data/text.txt")

    return 0


if __name__ == "__main__":
    main()
