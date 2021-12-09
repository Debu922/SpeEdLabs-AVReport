
#####################################
#   Author: Debaditya Bhattacharya  #
#   Date:   09 Dec 2021             #
#   e-mail: debbh922@gmail.com      #
#   Desc:   Main file of AV Report  #
#           Generator for SpeEdLabs #
#####################################

import json

from boto3 import Session as awsSession
from botocore.exceptions import BotoCoreError, ClientError

from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from azure.cognitiveservices.speech.speech import SpeechConfig

from google.cloud import texttospeech

import sys
from contextlib import closing

from global_util import *

class TTSEngine():
    """Text To Speech Engine which when input with text, and output path, will generate TTS audio from chosen API client.

    Supported API Calls:
    * Amazon Web Services Polly (aws)
    * Microsoft Azure (azure)
    * Google Text To Speech (gTTS)

    """

    def __init__(self, ttsConfig) -> None:
        """TTSEngine constructor

        Args:
            ttsConfig (dict): ttsConfig file from config.
        """
        global debug

        # Initiate Configs
        self.ttsConfig = ttsConfig
        service = ttsConfig["service"]
        self.serviceConfig = ttsConfig[service]

        # Setup AWS
        if ttsConfig["service"] == "aws":
            with open("./aws_key.json", "r") as key:
                self.key = json.load(key)
            if debug:
                print("Connecting to AWS")
            self.connect_AWS()
            return

        # Setup Azure
        elif ttsConfig["service"] == "azure":
            with open("./azure_key.json", "r") as key:
                self.key = json.load(key)
            if debug:
                print("Connecting to Azure...")
            self.connect_Azure()
            return

        # Setup gTTS
        elif ttsConfig["service"] == "gTTS":
            if debug:
                print("Connecting to gTTS")
            self.connect_gTTS()
            return

        # Fallthrough
        else:
            print("Error: Please choose a valid TTS service in config.")
            sys.exit(-1)

    def connect_AWS(self):
        """Initate AWS Session and polly client using credentials.
        """
        global debug
        self.session = awsSession(self.key["key_id"],
                                  self.key["key"],
                                  region_name=self.key["region"])
        if debug:
            print("AWS Session initiated")
        self.client = self.session.client("polly")
        if debug:
            print("AWS Client initiated")
        return


    def connect_Azure(self):
        """Initiate Azure Session and client using credentials.
        """
        self.speech_config = SpeechConfig(subscription=self.key["key"],
                                          region=self.key["region"])
        return

    def connect_gTTS(self):
        """Initiate Azure Session and client. Path to credentails saved as environment variable.
        """
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(language_code=self.serviceConfig["language_code"], ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3)
        return

    def get_response(self, text, outPath):
        """Fetch response from pre_initated client.

        Args:
            text (String): Text to be spoken
            outPath (String): Output path
        """

        # Get AWS Response
        if self.ttsConfig["service"] == "aws":
            self.get_AWS_response(text, outPath)
            return

        # Get Azure Response
        elif self.ttsConfig["service"] == "azure":
            self.get_Azure_response(text, outPath)
            return

        # Get gTTS Response
        elif self.ttsConfig["service"] == "gTTS":
            self.get_gTTS_response(text, outPath)
            return

    def get_AWS_response(self, text, path):
        """Speech synthesis using AWS's TTS Service.

        Args:
            text (string): String to be converted into speech.
            path (string): Output path.
        """
        # Try to fetch response, else print forwaded error and exit.
        try:
            response = self.client.synthesize_speech(
                Text=text, OutputFormat=self.ttsConfig["output_format"], VoiceId=self.serviceConfig["voice_id"])
            if debug:
                print("Audio stream recieved")
        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)

        # Write response
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                try:
                    with open(path, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    print(error)
                    sys.exit(-1)
            if debug:
                print("Audio stream converted")
        else:
            print("Stream did not contain Audio")
            sys.exit(-1)
        return

    def get_Azure_response(self, text, path):
        """Speech synthesis using Azure's TTS Service.

        Args:
            text (string): String to be converted into speech.
            path (string): Output path.
        """
        audio_config = AudioOutputConfig(filename=path)
        synthesizer = SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config)
        if debug:
            print("Audio synthesizer initialized")
        synthesizer.speak_text(text)
        if debug:
            print("Audio stream converted")
        return

    def get_gTTS_response(self, text, path):
        """Speech synthesis using Google's TTS Service.

        Args:
            text (string): String to be converted into speech.
            path (string): Output path.
        """
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )
        with open(path, "wb") as out:
            out.write(response.audio_content)

        return
