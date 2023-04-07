# SpeEdLabs-AV-Report
Automatically generate AV Report videos from text and image inputs. Report based on student performance data fetched and anlyzed for SpeEdLabs Pvt. Ltd.

Archived on 2023-04-07

## Requirements:
* FFmpeg
* pillow
* azure-cognitiveservices-speech
* boto3
* google-cloud-texttospeech 

## Setup:
* Install FFmpeg on system / envionment
* Install python libraries
* Store key in aws_key.json / azure_key.json / gTTS_key.json in root of project
* Modify main file appropriately
* Run

## Setup gTTS Key:
* Export 'GOOGLE_APPLICATION_CREDENTIALS="[path to JSON]"' to path
