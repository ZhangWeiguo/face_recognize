from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
import dlib,sys,uuid,shutil
sys.path.insert(0, "D:/Code/Python3/face_recognize")
import hashlib,time,re,os,numpy,json
from skimage import io
from server.conf import *

filename = "file:///D:/Code/Python3/face_recognize/profile/"+str(uuid.uuid1())
filename_copy = filename[8:]
video_path = sys.argv[1]
hist = int(sys.argv[2])
feature_path = sys.argv[3]
imgs_path = [os.path.join(video_path,i) for i in os.listdir(video_path)]


face_detect_filename=model_config["face_detect_path"]
face_vec_filename=model_config["face_vec_path"]
face_detector = dlib.get_frontal_face_detector()
face_point_predictor = dlib.shape_predictor(face_detect_filename)
# face_vector_model = dlib.face_recognition_model_v1(face_vec_filename)


def result2file():
    f1 = open(feature_path,'w')
    for i in os.listdir(filename_copy):
        path = os.path.join(filename_copy,i)
        if i.startswith("part"):
            with open(path,'r') as f:
                s = f.read()
                f1.write(s)
    f1.close()
    shutil.rmtree(filename_copy)



def get_vector_from_image(image_path):
    img = io.imread(image_path)
    vv = []
    dets = face_detector(img, 1)
    for det in dets:
        shape = face_point_predictor(img, det)
        # 不能用spark问题就在下面这行
        face_vector_model = dlib.face_recognition_model_v1(face_vec_filename)
        v = face_vector_model.compute_face_descriptor(img, shape)
        v = numpy.array(v)
        vv.append(v)
    return vv





def save(rdd):
    try:
        rdd.saveAsTextFile(filename)
    except:
        print("save failed!")

def img2vec(img_path):
    vv = get_vector_from_image(img_path)
    t = name2time(os.path.basename(img_path))
    print("Process Time: %f Min"%round(t/60,3))
    return (t, [list(v) for v in vv])

def name2time(name):
    return (float(int(name.split(".")[0]))-1)/hist
def result2json(feature):
    t = feature[0]
    v = feature[1]
    S = json.dumps({"time": t, "data": v})
    return S

def cal():
    appName ="Test"
    conf = SparkConf().setAppName(appName)
    sc = SparkContext(conf=conf)
    data = sc.parallelize(imgs_path)
    result = data.map(img2vec).map(result2json)
    result.saveAsTextFile(filename)


if __name__=="__main__":
    cal()
    result2file()

'''
spark-submit feature_catch.py D:\\Code\\Python3\\face_recognize\\data\\test\\temp 15 D:\\Code\\Python3\\face_recognize\\data\\test\\feature
'''