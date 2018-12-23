from file_manage import FileManage
from mysql_conn import MysqlConn

class Manage:
    def __init__(self,file_config,sql_config):
        self.fm = FileManage(file_config)
        self.mc = MysqlConn(sql_config)

    def CreateUser(self,username,password):
        result1 = self.mc.AddUser(username, password)
        if result1["succ"] == True:
            result2 = self.fm.CreateUserDirs(username)
            if result2 == True:
                return True
        return False

    def RmUser(self,username):
        result1 = self.mc.RmUser(username)
        if result1["succ"] == True:
            result2 = self.fm.RmUserDirs(username)
            if result2 == True:
                return True
        return False

    def Validate(self,username, password):
        password1 = self.mc.GetPassword(username=username)["data"]
        if len(password1) == 1 and password.upper() == password1[0][0]:
            return True
        return False


    def AddUserImg(self,username,filename,file):
        result1 = self.fm.AddUserImg(username,filename,file)
        if result1 == True:
            img_name = filename
            img_path = self.fm.GetImgPath(username,img_name)
            result2 = self.mc.AddImgs(username,[(img_name, img_path)])
            if result2["succ"] == True:
                return True
        return False

    def AddUserVideo(self,username,filename,file):
        result1 = self.fm.AddUserVideo(username,filename,file)
        if result1 == True:
            video_name = filename
            video_path = self.fm.GetVideoPath(username,video_name)
            result2 = self.mc.AddVideos(username,[(video_name, video_path)])
            if result2["succ"] == True:
                return True
        return False

    def GetUserImgs(self,username):
        result1 = self.mc.GetImgs(username)
        imgs = []
        if result1["succ"] == True:
            for img_path,img_name,feature_path,create_time in result1["data"]:
                imgs.append(img_name)
        return imgs

    def GetUserVideos(self,username):
        result1 = self.mc.GetVideos(username)
        videos = []
        if result1["succ"] == True:
            for video_path,video_name,feature_path,create_time in result1["data"]:
                videos.append(video_name)
        return videos

    def RmUserImgs(self,username,imgs_name):
        for img_name in imgs_name:
            img_path = self.fm.GetImgPath(username,img_name)
            self.mc.RmImgs(username,[img_path])
        self.fm.RmUserImgs(username,imgs_name)
        return True

    def RmUserVideos(self,username,videos_name):
        for video_name in videos_name:
            video_path = self.fm.GetVideoPath(username,video_name)
            self.mc.RmVideos(username,[video_path])
        self.fm.RmUserImgs(username,videos_name)
        return True

    def AddJob(self,username,jobname,jobdetail):
        result1 = self.mc.AddJob(username,jobname,jobdetail)
        if result1["succ"] == True:
            return True
        return False


    def GetUserJobs(self,username):
        result1 = self.mc.GetJob(username)
        jobs = []
        if result1["succ"] == True:
            for jobname,jobdetail,username,jobstatus,create_time in result1["data"]:
                jobs.append((jobname,jobdetail,username,jobstatus,create_time))
        return jobs

    def RmUserJob(self,username,jobname):
        result1 = self.mc.RmJob(username,jobname)
        if result1["succ"] == True:
            result2 = self.fm.RmResult(username,jobname)
            if result2 == True:
                return True
        return False

    def UpdateUserJobstatus(self,jobname,jobstatus):
        self.mc.UpdateJob(jobname,jobstatus)

    def GetAllJobs(self):
        result1 = self.mc.GetAllJob()
        if result1["succ"] == True:
            return result1["data"]
        return []

    def GetResultPath(self,username,jobname):
        return self.fm.GetResultPath(username,jobname)
    def GetVideoPath(self,username,videoname):
        return self.fm.GetVideoPath(username,videoname)
    def GetImgPath(self,username,imgname):
        return self.fm.GetImgPath(username,imgname)
    def GetResultImgPath(self,username,videoname,t,hist):
        return self.fm.GetResultImgPath(username,videoname,t,hist)
    def GetImgFeaturePath(self,username,imgname):
        return self.fm.GetImgFeature(username,imgname)
    def GetVideoFeaturePath(self,username,videoname):
        return self.fm.GetVideoFeature(username,videoname)




