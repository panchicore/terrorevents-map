import requests
from config import STANDFORD_NLP_API

def get_locations(text):
    """

    :param text:
    :return:
    """
    res = requests.post(STANDFORD_NLP_API, data=text)

    res = res.json()

    locations = []

    for sentence in res['sentences']:
        for token in sentence['tokens']:
            if token['ner'] == 'LOCATION':
                locations.append(token['word'])
    
    return res, locations