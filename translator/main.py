# ============================================================== #
#                                                                #
# main.py by Kai Sackville-Hii                                   #      
#                                                                #
# This file is an example of how to use the google translate     #
# api for appetize.it is based of the following tutorial         #
# https://cloud.google.com/translate/docs/basic/translating-text #
#                                                                #
# ============================================================== #

import os
from google.cloud import translate_v2 as translate

# This is the text we want to translate
text = "Poutine is a dish that includes french fries and cheese curds topped with a brown gravy."

# Language we want to translate too see link below for options
# https://cloud.google.com/translate/docs/languages 
target='fr'

# must set the environment variables for gcp, env.json file should
# exist in the same folder as this script
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r".\env.json"
translate_client = translate.Client()

# Text can also be a sequence of strings, in which case this method
# will return a sequence of results for each text.
result = translate_client.translate(text, target_language=target)

print(u'\nText: {}\n'.format(result['input']))
print(u'Translation: {}\n'.format(result['translatedText']))
print(u'Detected source language: {}\n'.format(result['detectedSourceLanguage']))