from conf import *
import sys
sys.path.insert(0, app_config["root_path"])
from flask import Flask,request
from io import BytesIO
from skimage import io
from process.image_process import ImageProcess
import base64,json
import copy,random


Ip = ImageProcess(
    face_detect_filename=model_config["face_detect_path"],
    face_vec_filename=model_config["face_vec_path"]
)

Ips = [Ip] * 10


def get_vec_from_array(img):
    Ipi = random.choice(Ips)
    vv,faces,edges = Ipi.get_vector_from_array(img)
    vv1 = [list(v) for v in vv]
    return vv1


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

app = Flask("img_feature")


@app.route("/")
def main():
    return "Hello SYSU!"
@app.route("/hello")
def hello():
    return "Hello SYSU!"


@app.route("/get_feature",methods=["POST"])
def get_feature():
    img_string = request.values.get("img")
    print(img_string)
    img = str2img(img_string)
    result = {"succ":True,"data":[]}
    try:
        vv = get_vec_from_array(img)
        result["data"] = vv
    except:
        result["succ"] = False
    return json.dumps(result)

if __name__ == "__main__":
    app.run(port=8080,host="0.0.0.0",threaded=True)