#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# test_code
# rpi zero passed

import requests
import json
import sys, os, uuid, time
from PIL import Image, ImageDraw, ImageFont

rootPath = os.path.dirname(os.path.abspath(__file__))
url = ' url / endpoint'
headers = {'Apikey': ""}
root_path = os.path.dirname(os.path.realpath(sys.argv[0]))

class CarLpr:
    def __init__(self, ApiEndpoint=url, ApiKey=headers):
        self.ApiEndpoint = ApiEndpoint
        self.ApiKey = ApiKey
    def setImage(self, imageFile=None):
        reSize = Image.open(imageFile)
        imageUpload = '{}/{}'.format(rootPath,resizeImage(reSize))
        self.requestApi(imageUpload)
    def requestApi(self, imagePath):
        print(imagePath)
        self.files = {'file': open(imagePath, mode='rb')}
        try:
            print(':) Try.. requests API.')
            jsonPath = str(imagePath.split('.jpg')[0]) + '.json'
            self.res = requests.post(self.ApiEndpoint, files=self.files, headers=self.ApiKey)
            # print(self.res.headers) # check return rate limit
            # print(self.res.json())
            json_lpr = json.dumps(self.res.json(), indent=4, ensure_ascii=False)
            with open(jsonPath, "w", encoding='utf8') as outfile:
                outfile.write(json_lpr)
                outfile.close()
            self.processImage(str(jsonPath), str(imagePath))
        except Exception as e:
            print(e)
            pass
        # os.remove(imagePath)
        # os.remove(jsonPath)

    def processImage(self, jsonPath, imagePath):
        print(";) Running processImage.")
        try:
            with open(jsonPath, encoding="utf8") as json_file:
                data = json.load(json_file)
                r_char = data['r_char']
                r_digit = data['r_digit']
                r_province = data['r_province']
                box = data['box']
                txt = '{} {}, {}'.format(r_char, r_digit, r_province)

        except Exception as e:
            print(e)
            pass
        im = Image.open(imagePath)
        im_width, im_height = im.size
        # กำหนด x:y
        pt_x = int(box[1] * im_width)
        pt_y = int(box[0] * im_height)
        # กำหนด w x h
        pt_w = int(box[3] * im_width)
        pt_h = int(box[2] * im_height)
        # print(pt_x, pt_y, pt_w, pt_h)
        # crop lpr
        print(':) Cropping Lpr image.')
        im1 = im.crop((pt_x, pt_y, pt_w, pt_h))
        im1.save('lpr_output_crop.jpg')
        # draw bounding box, label
        print(':) Drawing boundingbox, label.')
        imgcp = im
        padding = 10
        font = ImageFont.truetype('Font-Sarun.ttf', 40)
        plate_id = str(txt)
        plate_dt = 'ch:xx 00/00/00' # get from event camera

        imgcp_draw = ImageDraw.Draw(imgcp)
        imgcp_draw.rectangle((pt_x - padding, pt_y - padding, pt_w + padding, pt_h + padding), fill=None, outline="yellow", width=3)
        imgcp_draw.text((20, 20), plate_id, fill='yellow', font=font, stroke_width=1, stroke_fill='black')
        imgcp_draw.text((20, 60), plate_dt, fill='yellow', font=font, stroke_width=1, stroke_fill='black')
        im.save('lpr_output_bbox.jpg')

        try:
            os.remove(imagePath)
            os.remove(jsonPath)
            print(':) imagePath, jsonPath was Removed')
        except Exception as e:
            print('Error:: Remove temp imagePath, jsonPath')
            print(e)


def bytesto(bytes, bsize=1024):
    # convert bytes to mb
    return bytes / (bsize ** 2)

def resizeImage(im, basewidth = 1024):
    tempImage = im
    tempImageName = '{}.jpg'.format(str(uuid.uuid4()))
    width = (basewidth/float(tempImage.size[0]))
    height = int((float(tempImage.size[1])*float(width)))
    newImage = tempImage.resize((basewidth,height), Image.Resampling.LANCZOS)
    newImage.save(tempImageName)
    return tempImageName

def main():
    setTempImage = ''
    if len(sys.argv) > 1:
        try:
            im=Image.open(str(sys.argv[1]))
            imSize = bytesto(len(im.fp.read()))
            if round(imSize, 2) >= 1.0:
                print('{}: {} Mb'.format('Error:: Over Limit size.', round(imSize, 2)))
                return False         
            return True
        except IOError:
            print("Error:: Not found input image file.")
            return False
    else:
        print('Error:: Input image Argument.')
        return False

# if __name__ == '__main__':
#     if main():
#         lpr = CarLpr()
#         lpr.setImage(str(sys.argv[1]))
#     else:
#         exit(0)
