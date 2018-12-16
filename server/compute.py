# -*- encoding:gbk -*-
from process.video_process import VideoProcess
from process.image_process import ImageProcess
from model.face_recognize_easy import EasyDist
from model.face_recognize_sgd import SgdDist
import numpy,os,json,time
from multiprocessing import Process,Manager,Lock,Pool,freeze_support
from manage import Manage
from conf import *
ServerManage = Manage(file_config,sql_config)
global Model,Ip,Vp

hist = compute_config["hist"]
process_num = compute_config["process_num"]
Model = SgdDist(model_config["recognize_model_path"])
Ip = ImageProcess(
    face_detect_filename=model_config["face_detect_path"],
    face_vec_filename=model_config["face_vec_path"]
)
Vp = VideoProcess(model_config["ffmpge_path"])
url = "%s:%d"%(app_config["host"],app_config["port"]) +"/imgs/result?t=%s&hist=%s&videoname=%s"



def get_feature_spark(imgs_path,hist,feature_path):
    command = "spark-submit %s %s %s %s"%(model_config["spark_model_path"],
                                          imgs_path,
                                          hist,
                                          feature_path
                                          )
    os.popen(command)
    # spark-submit D:\\Code\Python3\\face_recognize\\spark\\feature_catch.py D:\\Code\\Python3\\face_recognize\\profile\\root\\data\\video\\广视新闻1201.mp4_temp 15 D:\\Code\\Python3\\face_recognize\\profile\\root\\feature\\video\\广视新闻1201.mp4

def video_processor_spark(video_path,feature_path):
    video_path_temp = video_path+"_temp"
    Vp.split_videos(video_path,video_path_temp,hist=hist)
    get_feature_spark(video_path_temp,hist,feature_path)


def get_img_url(t,hist,videoname):
    base_url = url%(t,hist,videoname)
    return base_url


def get_all_job():
    data = ServerManage.GetAllJobs()
    all_jobs = []
    for job in data:
        jobname,jobdetail,username,jobstatus,create_time = job
        print(jobdetail)
        one_job = {
            "username":username,
            "jobname":jobname,
            "create_time":create_time,
            "jobstatus":jobstatus,
            "jobdetail":json.loads(jobdetail)
        }
        all_jobs.append(one_job)
    return all_jobs






def imgdata2file(img_data,feature_path):
    f = open(feature_path,'w')
    f.write(json.dumps(img_data))
    f.close()
def file2imgdata(fetaure_path):
    f = open(fetaure_path,'r')
    s = f.read()
    img_data = json.loads(s)
    return img_data

def videodata2file(video_dict,feature_path):
    f = open(feature_path,'w')
    for i in video_dict:
        f.write(json.dumps({"time":i,"data":video_dict[i]})+"\n")
    f.close()

def file2videodata(feature_path):
    f = open(feature_path,'r')
    video_dict = {}
    s = f.readline()
    while s:
        data = json.loads(s)
        video_dict[data["time"]] = data["data"]
        s = f.readline()
    f.close()
    return video_dict


def image_processor(img_path,feature_path):
    vv, faces, edges = Ip.get_vector_from_image(img_path)
    vv = [list(v) for v in vv]
    imgdata2file(vv,feature_path)

# 线程池
'''
def video_processor(video_path,feature_path):
    def img2vec(img_path,t):
        vv, faces, edges = Ip.get_vector_from_image(img_path)
        video_dict[t] = [list(v) for v in vv]
    def name2time(name):
        return (float(int(name.split(".")[0]))-1)/hist
    video_dict = {}
    video_path_temp = video_path+"_temp"
    Vp.split_videos(video_path,video_path_temp,hist=hist)
    L = os.listdir(video_path_temp)
    var = []
    P = threadpool.ThreadPool(num_workers=100)
    for i in L:
        var.append(([os.path.join(video_path_temp,i),name2time(i)],None))
    workers = threadpool.makeRequests(img2vec, var)
    [P.putRequest(worker) for worker in workers]
    P.wait()
    videodata2file(video_dict,feature_path)
'''


def img2vec(img_path, t):
    vv, faces, edges = Ip.get_vector_from_image(img_path)
    print("Process Time: %f Min"%round(t/60,3))
    return t, [list(v) for v in vv]

def name2time(name):
    return (float(int(name.split(".")[0]))-1)/hist

def video_processor(video_path,feature_path):
    video_dict = {}
    video_path_temp = video_path+"_temp"
    Vp.split_videos(video_path,video_path_temp,hist=hist)
    L = os.listdir(video_path_temp)
    result = []
    P = Pool(processes=process_num)
    for i in L:
        result.append(P.apply_async(func=img2vec, args=(os.path.join(video_path_temp,i),name2time(i),)))
    P.close()
    P.join()
    for data in result:
        print(data.get())
        i,j = data.get()
        video_dict[i] = j
    videodata2file(video_dict,feature_path)


def distance(vv1,vv2):
    sim = 0
    for i in vv1:
        for j in vv2:
            s = Model.distance(numpy.array(i),numpy.array(j))
            if s > sim:
                sim = s
    return sim


def imgresult2file(result,result_path):
    f = open(result_path,'w')
    f.write("%s,%s,%s,%s,%s\n"%("img1_name","img1_face_num","img2_name","img2_face_num","max_sim"))
    for r in result:
        img1, n1, img2, n2, sim = r
        f.write("%s,%s,%s,%s,%s\n" % (img1, str(n1), img2, str(n2), str(sim)))
    f.close()

def videoresult2file(result,result_path):
    f = open(result_path,'w')
    n = len(result[0])
    m = n/3-1
    s = "%s,"*int(n)
    s = s[0:-1]
    s1 = "video_name,time,video_face_num"
    s2 = ",img_name,img_face_num,max_sim"*int(m)
    s3  =s1+s2
    f.write(s3+",sim,video_img_url\n")
    for i in result:
        j = [str(ii) for ii in i]
        videoname = j[0]
        t = j[1]
        k = 1
        sim = 1
        while k <= m:
            if float(j[3*k+2]) <= sim:
                sim = float(j[3*k+2])
            k += 1
        url = get_img_url(t,hist,videoname)
        f.write(s%tuple(j)+",%f,%s\n"%(sim,url))
    f.close()


def img_distance(img1_feature_path_dict,img2_feature_path_dict):
    '''
    img1_feature_path_dict: {img1_name:img1_path,img2_name:img2_path}
    img2_feature_path_dict: {img1_name:img1_path,img2_name:img2_path}
    result :  [(img1_name,img1_face_num,img2_name,img2_face_num,max_sim)]
    '''
    img1_dict = {}
    img2_dict = {}
    result = []
    for img in img1_feature_path_dict:
        img1_dict[img] = file2imgdata(img1_feature_path_dict[img])
    for img in img2_feature_path_dict:
        img2_dict[img] = file2imgdata(img2_feature_path_dict[img])
    for img1 in img1_dict:
        for img2 in img2_dict:
            vv1 = img1_dict[img1]
            vv2 = img2_dict[img2]
            n1 = len(vv1)
            n2 = len(vv2)
            sim = distance(vv1,vv2)
            r = (img1,n1, img2,n2, sim)
            result.append(r)
    return result

def video_distance(video_feature_path_dict,img_feature_path_dict):
    '''
    video_feature_path_dict =
    {
        video1_name:video1_path,
        video2_name:video2_path
    }
    img_feature_path_dict =
    {
        img1_name:img1_path,
        img2_name:img2_path
    }
    result =[
    [video1_name,time1,face_num,img1_name,img1_face_num,img2_sim,img2_name,img2_face_num,img2_sim],
    [video1_name,time2,face_num,img1_name,img1_face_num,img2_sim,img2_name,img2_face_num,img2_sim],
    .....
    ]

    '''
    R = []
    for video_name in video_feature_path_dict:
        video_feature_path = video_feature_path_dict[video_name]
        video_dict = file2videodata(video_feature_path)
        img_dict = {}
        result = []
        for i in img_feature_path_dict:
            img_dict[i] = file2imgdata(img_feature_path_dict[i])
        for t in video_dict:
            vv1 = video_dict[t]
            if len(vv1)>0:
                r = [video_name, t, len(vv1)]
                for i in img_dict:
                    vv2 = img_dict[i]
                    sim = distance(vv1,vv2)
                    r.extend([i,len(vv2),sim])
                result.append(r)
        result = sorted(result,key=lambda x:float(x[1]))
    R.extend(result)
    return R

def worker(job):
    jobname = job["jobname"]
    result_path = job["jobdetail"]["result_path"]
    if os.path.exists(job["jobdetail"]["result_path"]):
        return
    if "imgs" in job["jobdetail"].keys() and "videos" in job["jobdetail"].keys():
        img_feature_path_dict = {}
        video_feature_path_dict = {}
        ServerManage.UpdateUserJobstatus(jobname, "running")

        for data in job["jobdetail"]["imgs"]:
            img_feature_path_dict[data["name"]] = data["feature_path"]
            if os.path.exists(data["feature_path"]):
                pass
            else:
                image_processor(data["path"],data["feature_path"])
            print("%s feature process is finished!"%data["path"])


        for data in job["jobdetail"]["videos"]:
            video_feature_path_dict[data["name"]] = data["feature_path"]
            if os.path.exists(data["feature_path"]):
                pass
            else:
                # 这里有两种方法，一种是自带的进程池，第二种是spark
                video_processor(data["path"],data["feature_path"])
                # video_processor_spark(data["path"], data["feature_path"])
            print("%s feature process is finished!"% data["path"])


        result = video_distance(video_feature_path_dict,img_feature_path_dict)
        videoresult2file(result,result_path)


    elif "imgs1" in job["jobdetail"].keys() and "imgs2" in job["jobdetail"].keys():
        img1_feature_path_dict = {}
        img2_feature_path_dict = {}

        for data in job["jobdetail"]["imgs1"]:
            img1_feature_path_dict[data["name"]] = data["feature_path"]
            if os.path.exists(data["feature_path"]):
                pass
            else:
                image_processor(data["path"],data["feature_path"])
            print("%s feature process is finished!"%data["path"])
        for data in job["jobdetail"]["imgs2"]:
            img2_feature_path_dict[data["name"]] = data["feature_path"]
            if os.path.exists(data["feature_path"]):
                pass
            else:
                image_processor(data["path"],data["feature_path"])
            print("%s feature process is finished!"% data["path"])

        result = img_distance(img1_feature_path_dict,img2_feature_path_dict)
        imgresult2file(result,result_path)
        ServerManage.UpdateUserJobstatus(jobname, "finished")

if __name__ == "__main__":
    while True:
        all_jobs = get_all_job()
        for job in all_jobs:
            jobname = job["jobname"]
            try:
                worker(job)
                ServerManage.UpdateUserJobstatus(jobname, "finished")
                print("work finished!")
            except:
                ServerManage.UpdateUserJobstatus(jobname,"failed")
                print("work failed!")
        time.sleep(30)
