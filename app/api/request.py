import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, EmotionOptions
from app.main.models import *


key = 'LTyxv2Vrq0kOCnzgVGsfw7w4KsgxpL8_U9bxe2TD-JU6'
authenticator = IAMAuthenticator(key)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator)

natural_language_understanding.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')

def analyze(text):
    response = natural_language_understanding.analyze(
        text=text,

        features = Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        # keywords=KeywordsOptions(emotion=True, sentiment=True,
            #                         limit=2))).get_result()
            emotion = EmotionOptions())).get_result()

    print(json.dumps(response, indent=2))
    emotion = json.dumps(response)
    loaded_json = json.loads(emotion)
    #for x in loaded_json:
        #print("%s: %s" % (x, loaded_json[x]))
    emotions = loaded_json['emotion']['document']['emotion']

    max = 0
    emo = ""
    for key , value in emotions.items():

        if (value > max):
            max = value
            emo = key
            #print (key, value)
        #print(key, value)
    #print ("The max value is: " + str(max) + " and the emotion associated is: " + str(emo))

    return emo

#mystring = "I feel hungry and cold"
#analyze(mystring)