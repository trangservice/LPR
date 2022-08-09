import requests
import json

url = ' endpoint  '
files = {'file': open('imagefile.jpg', mode='rb')}
headers = {'Apikey': "===========API KEY ============"}

r = requests.post(url, files=files, headers=headers)
json_object = json.dumps(r.json(), indent=4, ensure_ascii=False)
with open("data.json", "w", encoding='utf8') as outfile:
    outfile.write(json_object)



