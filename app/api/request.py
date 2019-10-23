import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, EmotionOptions

authenticator = IAMAuthenticator('LTyxv2Vrq0kOCnzgVGsfw7w4KsgxpL8_U9bxe2TD-JU6')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator)

natural_language_understanding.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')

response = natural_language_understanding.analyze(
    text='I hate Mondays just as much as mornings'
    'My foot hurts and my hair is frizzy '
    'Mustard is disgusting',

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

def analyze(text):
    max = 0
    emo = 0
    for key , value in emotions.items():
    # print (emotion)
        max = value
        emo = key
        #values = emotions.values()
        if (value in emotions.items() > max):
            max = value
            emo = key
            print (key, value)

        print(key, value)

    print ("The max value is: " + str(max) + " and the emotion associated is: " + str(emo))

analyze(response.text)