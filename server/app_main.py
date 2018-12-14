from flask import Flask,Response,render_template,request,session,url_for,redirect,send_from_directory
from manage import Manage
import json,os,time,sys
from conf import *
from result_transform import transform_result
ServerManage = Manage(file_config,sql_config)
app = Flask(app_config["app_name"],
            template_folder=app_config["template_path"],
            static_folder=app_config["static_path"])
app.config["ALLOWED_IMGS "] = set(app_config["img_type"])
app.config["ALLOWED_VIDEOS "] = set(app_config["video_type"])
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MIN_CONTENT_LENGTH'] = 1024

sys.path.insert(0, app_config["root_path"])
###############################################################
###############################################################
# 验证文件格式
def allowed_img(filename):
    if "." in filename:
        L = filename.split(".")
        n = len(L)
        if L[n-1] in app.config["ALLOWED_IMGS "]:
            return True
    return False
def allowed_video(filename):
    if "." in filename:
        L = filename.split(".")
        n = len(L)
        if L[n-1] in app.config["ALLOWED_VIDEOS "]:
            return True
    return False

###############################################################
###############################################################



# 前端界面
@app.route("/")
def main():
    return "Welcome To XXX!"

@app.route("/group")
def group():
    return "I am Not Fight By Myself!"

@app.route("/algorithms")
def algorithms():
    return "Noting Is Impossible!"

@app.route("/login")
def login():
    if request.method == "GET":
        username = request.values.get("username")
        password = request.values.get("password")
        if ServerManage.Validate(username,password):
            session['username'] = username
            session['password'] = password
            return redirect(url_for("manage"))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route("/result_detail/<jobname>")
def result_detail(jobname):
    username = session.get("username")
    result_path = ServerManage.GetResultPath(username,jobname)
    job = os.path.basename(result_path)
    dir = os.path.dirname(result_path)
    if os.path.exists(result_path) and os.path.isfile(result_path):
        result_url = "/result/%s"%jobname
        results,type = transform_result(result_path)
        if type == 'video':
            return render_template("result_video.html",results = results,result_url=result_url)
        elif type == 'img':
            return render_template("result_img.html", results=results, result_url=result_url)
        else:
            return "Unknow Error"
    else:
        return "Job Is Not Finished!"

@app.route("/manage",methods=["GET","POST"])
def manage():
    if request.method == "GET":
        username = session.get("username")
        password = session.get("password")
        if ServerManage.Validate(username,password):
            imgs = json.loads(get_imgs())["data"]
            videos = json.loads(get_videos())["data"]
            return render_template("manage.html",imgs = imgs,videos = videos)
        else:
            return redirect(url_for("login"))
    elif request.method == "POST":
        add_imgs()
        add_videos()
        imgs = json.loads(get_imgs())["data"]
        videos = json.loads(get_videos())["data"]
        print(videos)
        return render_template("manage.html", imgs = imgs,videos = videos)
    else:
        return redirect(url_for("login"))

@app.route("/compare_imgs")
def compare_imgs():
    if request.method == "GET":
        username = session.get("username")
        password = session.get("password")
        if ServerManage.Validate(username,password):
            imgs = json.loads(get_imgs())["data"]
            result = json.loads(get_jobs())["data"]
            results = []
            for i in result:
                detail = json.loads(i["jobdetail"].replace("\\",'/'))
                if "imgs1" in detail.keys() and "imgs2" in detail.keys():
                    j = {"jobname":i["jobname"],
                         "jobstatus":i["jobstatus"],
                         "create_time":i["create_time"],
                         "result":"/result_detail/%s"%i["jobname"]
                         }
                    results.append(j)
            return render_template("compare_imgs.html",imgs1=imgs,imgs2=imgs,results = results)
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route("/compare_videos")
def compare_videos():
    if request.method == "GET":
        username = session.get("username")
        password = session.get("password")
        if ServerManage.Validate(username,password):
            imgs = json.loads(get_imgs())["data"]
            videos = json.loads(get_videos())["data"]
            result = json.loads(get_jobs())["data"]
            results = []
            for i in result:
                detail = json.loads(i["jobdetail"].replace("\\", '/'))
                if "imgs" in detail.keys() and "videos" in detail.keys():
                    j = {"jobname":i["jobname"],
                         "jobstatus":i["jobstatus"],
                         "create_time":i["create_time"],
                         "result":"/result_detail/%s"%i["jobname"]
                         }
                    results.append(j)
            return render_template("compare_videos.html",imgs=imgs,videos=videos,results=results)
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


###############################################################
###############################################################
# 配置图像视频展示,下载结果文件
@app.route("/img/<imgname>")
def img(imgname):
    username = session.get('username')
    img_path = ServerManage.GetImgPath(username,imgname)
    f = open(img_path,'rb')
    res = Response(f,mimetype="image/jpeg")
    return res

@app.route("/video/<videoname>")
def video(videoname):
    username = session.get("username")
    video_path = ServerManage.GetVideoPath(username,videoname)
    print(video_path)
    f = open(video_path,'rb')
    res = Response(f,mimetype="video/x-msvideo")
    return res

@app.route("/imgs/result")
def imgs():
    username = session.get('username')
    videoname = request.values.get("videoname")
    t = float(request.values.get("t"))
    hist = int(request.values.get("hist"))
    img_path =ServerManage.GetResultImgPath(username,videoname,t,hist)
    print(img_path)
    f = open(img_path,'rb')
    res = Response(f,mimetype="image/jpeg")
    return res



@app.route("/result/<jobname>")
def result(jobname):
    username = session.get("username")
    result_path = ServerManage.GetResultPath(username,jobname)
    job = os.path.basename(result_path)
    dir = os.path.dirname(result_path)
    if os.path.exists(result_path) and os.path.isfile(result_path):
        return send_from_directory(dir,job,as_attachment=True)
    else:
        return "Job Is Not Finished!"


###############################################################
###############################################################
# 后端数据请求
@app.route("/add_imgs",methods=["POST"])
def add_imgs():
    username = session.get("username")
    password = session.get("password")
    if ServerManage.Validate(username,password):
        if request.method == "POST":
            try:
                upload_files = request.files.getlist('img')
                for file in upload_files:
                    filename = file.filename
                    filename = filename.replace(" ","")
                    if allowed_img(filename):
                        ServerManage.AddUserImg(username,filename,file)
                result = {"msg": "upload succ", "succ": True}
            except:
                result = {"msg": "upload fail", "succ": False}
        else:
            result = {"msg": "post fail", "succ": False}
    else:
        result = {"msg": "login fail", "succ": False}
    return result

@app.route("/add_videos",methods=["POST"])
def add_videos():
    username = session.get("username")
    password = session.get("password")
    if ServerManage.Validate(username,password):
        if request.method == "POST":
            try:
                upload_files = request.files.getlist('video')
                for file in upload_files:
                    filename = file.filename
                    if allowed_video(filename):
                        ServerManage.AddUserVideo(username,filename,file)
                result = {"msg": "upload succ", "succ": True}
            except:
                result = {"msg": "upload fail", "succ": False}
        else:
            result = {"msg": "post fail", "succ": False}
    else:
        result = {"msg": "login fail", "succ": False}
    return json.dumps(result)



@app.route("/rm_videos")
def rm_videos():
    username = session.get("username")
    password = session.get("password")
    videosname = request.values.get("videosname")
    result = {"msg":"","succ":True}
    if ServerManage.Validate(username,password):
        if videosname:
            videos = videosname.split(',')
            r = ServerManage.RmUserVideos(username,videos)
            if r == False:
                result["succ"] = False
                result["msg"] = "rm error"
        else:
            result["succ"] = False
            result["msg"] = "data error"
    else:
        result = {"msg": "login fail", "succ": False}
    return json.dumps(result)

@app.route("/rm_imgs")
def rm_imgs():
    username = session.get("username")
    password = session.get("password")
    imgsname = request.values.get("imgsname")
    result = {"msg":"","succ":True}
    if ServerManage.Validate(username, password):
        if imgsname:
            imgs = imgsname.split(',')
            r = ServerManage.RmUserImgs(username,imgs)
            if r == False:
                result["succ"] = False
                result["msg"] = "rm error"
        else:
            result["succ"] = False
            result["msg"] = "data error"
    else:
        result = {"msg": "login fail", "succ": False}
    return json.dumps(result)

@app.route("/get_imgs")
def get_imgs():
    username = session.get("username")
    result = {"data":[],"succ":True,"msg":""}
    L = ServerManage.GetUserImgs(username)
    for i in range(len(L)):
        L[i] = ("img/%s"%(L[i]),L[i])
    result["data"] = L
    return json.dumps(result)

@app.route("/get_videos")
def get_videos():
    username = session.get("username")
    result = {"data":[],"succ":True,"msg":""}
    L = ServerManage.GetUserVideos(username)
    for i in range(len(L)):
        L[i] = ("video/%s"%(L[i]),L[i])
    result["data"] = L
    return json.dumps(result)


###############################################################
###############################################################


@app.route("/get_jobs")
def get_jobs():
    username = session.get("username")
    password = session.get("password")
    result = {"succ": True, "msg": "", "data": []}
    if ServerManage.Validate(username,password):
        r = ServerManage.GetUserJobs(username)
        for i in r:
            jobname, jobdetail, username, jobstatus, create_time = i
            data1 = {"jobname":jobname,
                     "jobdetail":jobdetail,
                     "username":username,
                     "jobstatus":jobstatus,
                     "create_time":time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(create_time))}
            result["data"].append(data1)
    else:
        result = {"succ": False, "msg": "login fail","data": []}
    return json.dumps(result)


@app.route("/rm_job")
def rm_job():
    result = {"succ": True, "msg": ""}
    username = session.get("username")
    password = session.get("password")
    jobname = request.values.get("jobname")
    if ServerManage.Validate(username,password):
        try:
            if jobname:
                r = ServerManage.RmUserJob(username,jobname)
                if r == True:
                    result = {"succ": True, "msg": ""}
            else:
                result = {"succ": False, "msg": "jobname error"}
        except:
            pass
    else:
        result = {"succ": False, "msg": "login fail"}
    return json.dumps(result)

@app.route("/get_job_status")
def get_job_status():
    username = session.get("username")
    password = session.get("password")
    jobname = request.values.get("jobname")
    if ServerManage.Validate(username,password):
        if jobname:
            r = ServerManage.GetUserJobs(username)
            for i in r:
                name, jobdetail, username, jobstatus, create_time = i
                if name == jobname:
                    result = {"succ": True, "msg": "", "status": jobstatus, "jobname":jobname}
                    break
                else:
                    result = {"succ": True, "msg": "", "status": "job not exist","jobname":jobname}
        else:
            result = {"succ": False, "msg": "jobname error"}
    else:
        result = {"succ": False, "msg": "login fail"}
    return json.dumps(result)


@app.route("/commit_job")
def commit_job():
    result = {"succ": True, "msg": ""}
    username = session.get("username")
    password = session.get("password")
    if ServerManage.Validate(username,password):
        try:
            kind = request.values.get("kind")
            if kind == "img":
                try:
                    username = session.get("username")
                    imgsname1 = request.values.get("imgsname1").split(",")
                    imgsname2 = request.values.get("imgsname2").split(",")
                    jobname = username + "_" + str(int(time.time()))
                    jobdetail = {"imgs1":[],"imgs2":[],"result_path":""}
                    for i in imgsname1:
                        r = {"name":i,"path":ServerManage.GetImgPath(username,i),"feature_path":ServerManage.GetImgFeaturePath(username,i)}
                        jobdetail["imgs1"].append(r)
                    for i in imgsname2:
                        r = {"name":i,"path":ServerManage.GetImgPath(username,i),"feature_path":ServerManage.GetImgFeaturePath(username,i)}
                        jobdetail["imgs2"].append(r)
                    jobdetail["result_path"] = ServerManage.GetResultPath(username,jobname)
                    jobdetail = json.dumps(jobdetail)
                    jobdetail = jobdetail.replace("\\","\\\\")
                    r = ServerManage.AddJob(username=username, jobdetail=jobdetail, jobname=jobname)
                    if r == True:
                        result = {"succ": True, "msg": ""}
                except:
                    result = {"succ": False, "msg": "parameter error"}
            elif kind == "video":
                try:
                    username = session.get("username")
                    imgsname = request.values.get("imgsname").split(",")
                    videosname = request.values.get("videosname").split(",")
                    jobname = username + "_" + str(int(time.time()))
                    jobdetail = {"imgs":[],"videos":[],"result_path":""}
                    for i in imgsname:
                        r = {"name":i,"path":ServerManage.GetImgPath(username,i),"feature_path":ServerManage.GetImgFeaturePath(username,i)}
                        jobdetail["imgs"].append(r)
                    for i in videosname:
                        r = {"name":i,"path":ServerManage.GetVideoPath(username,i),"feature_path":ServerManage.GetVideoFeaturePath(username,i)}
                        jobdetail["videos"].append(r)
                    jobdetail["result_path"] = ServerManage.GetResultPath(username,jobname)
                    jobdetail = json.dumps(jobdetail)
                    jobdetail = jobdetail.replace("\\", "\\\\")
                    result = ServerManage.AddJob(username=username, jobdetail=jobdetail, jobname=jobname)
                except:
                    result = {"succ": False, "msg": "parameter error"}
            else:
                result = {"succ": False, "msg": "comapare kind error"}
        except:
            result = {"succ": False, "msg": "login fail"}
    return json.dumps(result)

if __name__=="__main__":
    app.run(threaded=True,port=8080,host="0.0.0.0")
