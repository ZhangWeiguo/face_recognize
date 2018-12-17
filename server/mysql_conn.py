# -*- encoding:utf8-*-
from mysql.connector import pooling
import time

class MysqlConn:
    def __init__(self,config):
        self.pool = pooling.MySQLConnectionPool(pool_name=config["pool_name"],
                                                pool_size=config["pool_size"],
                                                host=config["host"],
                                                port=config["port"],
                                                database=config["database"],
                                                user=config["user"],
                                                password=config["password"],
                                                charset="utf8",
                                                pool_reset_session=True)

        self.config = config
        # 用户信息
        self.add_user_sql = "insert into user_info values (\"%s\",\"%s\",%d)"
        self.rm_user_sql = "delete from user_info where username = \"%s\""
        self.get_password_sql = "select password from user_info where username=\"%s\""

        self.add_job_sql = "insert into job_info values('%s','%s','%s','%s',%d)"
        self.rm_job_sql = "delete from job_info where username=\"%s\" and jobname=\"%s\""
        self.get_job_sql = "select jobname,jobdetail,username,jobstatus,create_time from job_info where username=\"%s\" order by create_time"
        self.update_job_status_sql = "update job_info set jobstatus=\"%s\" where jobname=\"%s\""
        self.get_all_job_sql = "select jobname,jobdetail,username,jobstatus,create_time from job_info where jobstatus!=\"finished\" and jobstatus!=\"failed\" order by create_time"



        #图像增删查
        self.get_imgs_sql = "select img_path,img_name,feature_path,create_time from img_info where username=\"%s\""
        self.add_imgs_sql = "insert into img_info(img_path,img_name,username,create_time) values (%s,%s,%s,%s)"
        self.rm_imgs_sql = "delete from img_info where username=%s and img_path =%s"

        #视频增删查
        self.get_videos_sql = "select video_path,video_name,feature_path,create_time from video_info where username=\"%s\""
        self.add_videos_sql = "insert into video_info(video_path,video_name,username,create_time) values (%s,%s,%s,%s)"
        self.rm_videos_sql = "delete from video_info where username=%s and video_path =%s"

        ''' 暂时不通过Mysql查询，直接利用文件系统索引查询
    
        # 更新一个或多个图像视频的特征，查询直接用上面接口，不提供单独查询
        self.add_imgs_feature_sql = "update img_info set feature_path=%s where img_path=%s"
        self.add_videos_feature_sql = "update video_info set feature_path=%s where video_path=%s"

        # 每次只能操纵一条记录，只有在删除视频或者图像时，需要调用删除相应结果的接口
        self.add_result_sql = "insert into result values('%s','%s','%s','%s','%s')"
        self.rm_result_img_sql = "delete from result where file1_path=\"%s\" or file2_path=\"%s\""
        self.rm_result_video_sql = "delete from result where file2_path=\"%s\""
        self.get_result_sql = "select result_file from result where file1_path=\"%s\" and file2_path=\"%s\""
        '''

    def execute(self,sql):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        msg = "succ"
        succ = True
        try:
            cursor.execute(sql)
        except Exception as e:
            msg = str(e)
            succ = False
        result = {}
        result["msg"] = msg
        result["succ"] = succ
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def executemany(self,sql,data):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        msg = "succ"
        succ = True
        try:
            cursor.executemany(sql,data)
        except Exception as e:
            msg = str(e)
            succ = False
        result = {}
        result["msg"] = msg
        result["succ"] = succ
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def query(self,sql):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        msg = "succ"
        succ = True
        try:
            cursor.execute(sql)
        except Exception as e:
            msg = str(e)
            succ = False
        result = {}
        result["msg"] = msg
        result["succ"] = succ
        try:
            result["data"] = cursor.fetchall()
        except Exception as e:
            result["data"] = []
            result["succ"] = False
            result["msg"] = str(e)
        cursor.close()
        conn.close()
        return result


    def AddUser(self,username, password):
        t = int(time.time())
        sql = self.add_user_sql%(username,password,t)
        result = self.execute(sql)
        return result

    def RmUser(self,username):
        sql = self.rm_user_sql%(username)
        result = self.execute(sql)
        return result

    def GetPassword(self,username):
        sql = self.get_password_sql%(username)
        result = self.query(sql)
        return result

    def AddJob(self,username,jobname,jobdetail):
        status = "waiting"
        t = int(time.time())
        add_job_sql = self.add_job_sql%(jobname,jobdetail,username,status,t)
        print(add_job_sql)
        result = self.execute(add_job_sql)
        return result

    def RmJob(self,username,jobname):
        rm_job_sql = self.rm_job_sql%(username,jobname)
        result = self.execute(rm_job_sql)
        return result

    def GetJob(self,username):
        get_job_sql = self.get_job_sql%username
        print(get_job_sql)
        result = self.query(get_job_sql)
        return result

    def GetAllJob(self):
        get_job_sql = self.get_all_job_sql
        print(get_job_sql)
        result = self.query(get_job_sql)
        return result

    def UpdateJob(self,jobname,status):
        update_job_status_sql = self.update_job_status_sql%(status,jobname)
        result = self.execute(update_job_status_sql)
        return result

    def GetImgs(self,username):
        sql = self.get_imgs_sql%(username)
        result = self.query(sql)
        return result

    def GetVideos(self,username):
        sql = self.get_videos_sql%(username)
        result = self.query(sql)
        return result

    def RmImgs(self,username, imgs_path):
        data = []
        for i in imgs_path:
            data.append((username,i))
        sql = self.rm_imgs_sql
        result = self.executemany(sql, data)

        return result

    def RmVideos(self,username, videos_path):
        data = []
        for i in videos_path:
            data.append((username,i))
        sql = self.rm_videos_sql
        result = self.executemany(sql, data)
        return result


    def AddImgs(self,username, imgs_info):
        data = []
        t = int(time.time())
        for (img_name,img_path) in imgs_info:
            data.append((img_path,img_name,username,t))
        sql = self.add_imgs_sql
        print(data)
        print(sql%data[0])
        result = self.executemany(sql, data)
        return result


    def AddVideos(self, username, videos_info):
        data = []
        t = int(time.time())
        for (video_name,video_path) in videos_info:
            data.append((video_path,video_name,username,t))
        sql = self.add_videos_sql
        result = self.executemany(sql, data)
        return result

'''
    def AddImgsFeature(self,img_paths):
        data = []
        for (img_path,feature_path) in img_paths:
            data.append((feature_path,img_path))
        sql = self.add_imgs_feature_sql
        result = self.executemany(sql, data)
        return result

    def AddVideosFeature(self,video_paths):
        data = []
        for (video_path,feature_path) in video_paths:
            data.append((feature_path,video_path))
        sql = self.add_videos_feature_sql
        result = self.executemany(sql, data)
        return result


    # file1 只能是图像 file2可能是图像或者视频
    def AddResult(self,username,compare_kind,file1_path,file2_path,result_file):
        if compare_kind in ("img2img","img2video"):
            sql = self.add_result_sql % (username, compare_kind, file1_path, file2_path, result_file)
            result = self.execute(sql)
        else:
            result = {}
            result["msg"] = "Unknow kind"
            result["succ"] = False
        return result



    def RmResult(self,kind,file_path):
        if kind == "img":
            sql = self.rm_result_img_sql%(file_path,file_path)
        elif kind == "video":
            sql = self.rm_result_video_sql%(file_path)
        result = self.execute(sql)
        return result


    def GetResult(self,file1_path,file2_path):
        sql = self.get_result_sql%(file1_path,file2_path)
        result = self.query(sql)
        return result

'''



# config = {}
# config["pool_name"] = "face_recognize"
# config["pool_size"] = 20
# config["host"] = "127.0.0.1"
# config["port"] = "3306"
# config["database"] = "face_recognize"
# config["user"] = "sysu"
# config["password"] = "sysu1234"
# M = MysqlConn(config)
# print(M.AddUser("zhangweiguocopy","1234"))
# print(M.AddImgs("zhangweiguo",[("张wu","D:\\data\\zhangweiguo\\张wu.jpg"),("张s","D:\\data\\zhangweiguo\\张s.jpg")]))
# print(M.RmImgs("zhangweiguo",["D:\\data\\zhangweiguo\\张三.jpg"]))
# print(M.GetPassword("zhangweiguo"))
# print(M.GetImgs("zhangweiguo"))
# print(M.AddVideos("zhangweiguo",[("张wu","D:\\data\\zhangweiguo\\张wu.mp4"),("张s","D:\\data\\zhangweiguo\\张s.mp4")]))
# print(M.RmVideos("zhangweiguo",["D:\\data\\zhangweiguo\\张wu.mp4"]))
# print(M.GetVideos("zhangweiguo"))
# print(M.AddImgsFeature([("D:\\data\\zhangweiguo\\张s.jpg","D:\\data\\zhangweiguo\\张s.dat")]))
# print(M.AddVideosFeature([("D:\\data\\zhangweiguo\\张s.mp4","D:\\data\\zhangweiguo\\张s.dat")]))
# print(M.AddResult("zhangweiguo","img2img","D:\data\zhangweiguo\张wu.jpg","D:\data\zhangweiguo\张wu.jpg","D:\data\张wu.dat"))
# print(M.AddResult("zhangweiguo","img2img","D:\data\zhangweiguo\张w.jpg","D:\data\zhangweiguo\张s.mp4","D:\data\张sw.dat"))
# print(M.GetResult("D:\data\zhangweiguo\张w.jpg","D:\data\zhangweiguo\张s.mp4"))
# print(M.RmImgs("zhangweiguo",["D:\data\zhangweiguo\张wu.jpg"]))