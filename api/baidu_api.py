# -*- coding: utf-8 -*-
"""
Created on Tue Jan 09 21:58:11 2018
@author: zhangweiguo
"""
import base64,json,time
from urllib import request,parse
ak = "mQwVjA4FKNhEwRfCPg4X9mo9"
sk = "6VqBeeY0UXetZQx3LxwjrzH9d1Iz11S9"
access_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'
match_url = "https://aip.baidubce.com/rest/2.0/face/v2/match"
detect_url = "https://aip.baidubce.com/rest/2.0/face/v2/detect"



def get_access(ak,sk):
    host = access_url%(ak,sk)
    headers = {
        'Content-Type':'application/json; charset=UTF-8'
    }
    req = request.Request(host, headers=headers)
    content = request.urlopen(req).read()
    access = json.loads(content)
    access_token = access["access_token"]
    return access_token




class BdRe:
    def __init__(self):
        global ak,sk
        global compare_url
        self.ak = ak
        self.sk = sk
        self.access_token = get_access(ak,sk)
        self.match_url = match_url
        self.detect_url = detect_url
    def match(self,img1_file,img2_file):
        f = open(img1_file, 'rb')
        img1 = base64.b64encode(f.read())
        f = open(img2_file, 'rb')
        img2 = base64.b64encode(f.read())
        params = {"images": img1 + ','.encode() + img2}
        params = parse.urlencode(params).encode('utf-8')
        request_url = self.match_url + "?access_token=" + self.access_token
        request_main = request.Request(url=request_url, data=params)
        request_main.add_header('Content-Type', 'application/x-www-form-urlencoded')
        for i in range(5):
            try:
                response = request.urlopen(request_main)
                if "result" in json.loads(response).keys():
                    break
            except:
                time.sleep(1)
        content = response.read()
        return json.loads(content)
    def detect(self,img1_file):
        f = open(img1_file, 'rb')
        img = base64.b64encode(f.read())
        params = {"face_fields": "age,beauty,expression,faceshape,gender,glasses,landmark,race,qualities",
                  "image": img,
                  "max_face_num": 5}
        params = parse.urlencode(params).encode("utf-8")

        request_url = self.detect_url + "?access_token=" + self.access_token
        request_main = request.Request(url=request_url, data=params)
        request_main.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = request.urlopen(request_main)
        content = response.read()
        return json.loads(content)

if __name__ == "__main__":
    img1 = "D:\\Code\\Python3\\face_recognize\\data\\lfw\\Alastair_Campbell\\Alastair_Campbell_0001.jpg"
    img2 = "D:\\Code\\Python3\\face_recognize\\data\\lfw\\Alastair_Campbell\\Alastair_Campbell_0003.jpg"
    B = BdRe()
    print(B.detect(img1))
    print(B.match(img1,img2))
