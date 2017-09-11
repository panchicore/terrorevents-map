import requests

def get_locations(text):
    res = requests.post('http://10.65.48.37:9000/?properties={"annotators":"tokenize,ssplit,pos,ner","outputFormat":"json"}',
                        data=text)

    res = res.json()

    locations = []

    for sentence in res['sentences']:
        for token in sentence['tokens']:
            if token['ner'] == 'LOCATION':
                locations.append(token['word'])
    
    return locations