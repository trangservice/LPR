import requests
import json

# ระบบรู้จำป้ายทะเบียนรถยนต์ (Panyapradit-License Plate Recognition: Panyapradit-LPR )
# Link : https://aiforthai.in.th/aiplatform/#/panyalpr

url = 'https://api.aiforthai.in.th/panyapradit-lpr'

# file : ภาพที่จะใช้ค้นหาและอ่านตัวอักษรป้ายทะเบียนในรูปจะรองรับเฉพาะไฟล์สกุล Jpg หรือ jpeg เท่านั้น
files = {'file': open('imagefile.jpg', mode='rb')}

# API Key ต้องลงทะเบียนที่ https://aiforthai.in.th/
headers = {'Apikey': "===========API KEY ============"}

r = requests.post(url, files=files, headers=headers)

# เก็บเป็น json ใว้ใช้งาน
# ตัวอักษรภาษาไทย ensure_ascii=False >> เขียน json encoding='utf8'
json_object = json.dumps(r.json(), indent=4, ensure_ascii=False)
with open("data.json", "w", encoding='utf8') as outfile:
    outfile.write(json_object)

## หรือ test print return value
print("ทะเบียน : {}".format(str(r.json()["recognition"]).replace('/', '')))


