def Weather():
    json_url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
    payload = {'city': '040010'}
    response = requests.get(json_url, params=payload)
    json = response.json()
    text = json['description']['text']
    return text
