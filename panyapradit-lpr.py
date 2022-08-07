import requests
import json

url = 'https://api.aiforthai.in.th/panyapradit-lpr'
files = {'file': open('imagefile.jpg', mode='rb')}
headers = {'Apikey': "===========API KEY ============"}

r = requests.post(url, files=files, headers=headers)
json_object = json.dumps(r.json(), indent=4, ensure_ascii=False)
with open("data.json", "w", encoding='utf8') as outfile:
    outfile.write(json_object)

print("ทะเบียน : {}".format(str(r.json()["recognition"]).replace('/', '')))


