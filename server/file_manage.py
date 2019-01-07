import os,shutil

class FileManage:
    def __init__(self,config):
        self.config = config
    def CreateUserDirs(self,username):
        os.makedirs(self.config["root_path"]%username)
        for key in self.config:
            if key != "root_path":
                os.makedirs(self.config[key]%username)
        return True

    def RmUserDirs(self,username):
        try:
            root_path = self.config["root_path"]%username
            shutil.rmtree(root_path)
            return True
        except:
            return False

    def AddUserImg(self,username,imgname,file):
        img_path = self.GetImgPath(username,imgname)
        if img_path != "":
            file.save(img_path)
            return True
        else:
            return False

    def AddUserVideo(self,username,videoname,file):
        video_path = self.GetVideoPath(username,videoname)
        if video_path != "":
            file.save(video_path)
            return True
        else:
            return False

    def GetUserImgs(self,username):
        img_path = self.config["img_path"]%(username)
        L = os.listdir(img_path)
        L1 = [i for i in L if os.path.isfile(os.path.join(img_path,i))]
        return L1

    def GetImgPath(self,username,imgname):
        img_path = os.path.join(self.config["img_path"]%(username),imgname)
        return img_path

    # 这里写死了提取图片配置，后面再改
    def GetResultImgPath(self,username,videoname,t,hist):
        imgname = str(int(round(float(t*hist)))).zfill(6) + ".jpg"
        img_path = os.path.join(os.path.join(self.config["video_path"]%(username),videoname+"_temp"),imgname)
        print(img_path)
        if os.path.exists(img_path):
            return img_path
        else:
            return ""

    def GetVideoPath(self,username,videoname):
        video_path = os.path.join(self.config["video_path"]%(username),videoname)
        return video_path

    def GetUserVideos(self,username):
        video_path = self.config["video_path"]%(username)
        L = os.listdir(video_path)
        L1 = [i for i in L if os.path.isfile(os.path.join(video_path, i))]
        return L1

    # 这里还有删除特征文件
    def RmUserImgs(self,username,imgs):
        img_path = self.config["img_path"]%(username)
        feature_path = self.config["feature_img_path"]%(username)
        for i in os.listdir(img_path):
            if i in imgs:
                print(os.path.join(img_path,i))
                os.remove(os.path.join(img_path,i))
        for i in os.listdir(feature_path):
            if i in imgs:
                os.remove(os.path.join(feature_path,i))
        return True

    # 这里还有删除特征文件
    def RmUserVideos(self,username,imgs):
        video_path = self.config["video_path"]%(username)
        feature_path = self.config["feature_img_path"]%(username)
        print(feature_path)
        for i in os.listdir(video_path):
            if i in imgs:
                os.rename(os.path.join(video_path,i),os.path.join(video_path,i)+".klp")
                os.remove(os.path.join(video_path,i))
        for i in os.listdir(feature_path):
            if i in imgs:
                os.remove(os.path.join(feature_path,i))
        return True

    # 获取比较结果
    def GetResultPath(self,username,jobname):
        result_path = os.path.join(self.config["result_path"]%(username),jobname) + ".csv"
        return result_path

    #删除结果
    def RmResult(self,username,jobname):
        result_path = os.path.join(self.config["result_path"]%(username),jobname)
        if os.path.exists(result_path):
            try:
                os.remove(result_path)
                return True
            except:
                return False


    def GetImgFeature(self,username,imgname):
        feature_path = os.path.join(self.config["feature_img_path"]%(username),imgname)
        return feature_path

    def GetVideoFeature(self,username,videoname):
        feature_path = os.path.join(self.config["feature_video_path"]%(username),videoname)
        return feature_path

