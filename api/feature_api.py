from io import BytesIO
from skimage import io
import base64,json,random
from urllib import request as UrllibRequest
from urllib import parse as UrllibParse

def img2str(img_path):
    with open(img_path,'rb') as f:
        s = f.read()
        s1 = base64.b64encode(s).decode()
    return s1

def str2img(s):
    s1 = base64.b64decode(s)
    f1 = BytesIO(s1)
    I = io.imread(f1)
    return I


class FeatureApi:
    def __init__(self,urls = []):
        self.urls = urls

    def get_feature(self,img_path):
        vv = []
        for i in range(5):
            url = random.choice(self.urls)
            s = img2str(img_path)
            data = UrllibParse.urlencode({"img": s}).encode("utf-8")
            request = UrllibRequest.Request(url, data=data)
            result = json.loads(UrllibRequest.urlopen(request).read())
            if result["succ"] == True:
                vv = result["data"]
                break
        return vv



