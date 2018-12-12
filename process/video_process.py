# -*-encoding:utf-8 -*-
'''
created by zwg in 2018-01-10
'''


import os,re,shutil
import subprocess

class VideoProcess:
    def __init__(self,ffmpeg_path):
        self.ffmpeg_path = ffmpeg_path
        self.duration_pattern = re.compile("Duration: (\d*:\d*:\d*\.\d*)")
    def get_duration(self, video_path):
        try:
            os.remove("t123456.jpg")
        except:
            pass
        command1 = "%s " \
                   "-i %s t123456.jpg " % (self.ffmpeg_path, video_path)
        s = subprocess.getstatusoutput(command1)

        ts = self.duration_pattern.findall(s[1])[0]
        ts = ts.split(":")
        t = float(ts[2]) + int(ts[1]) * 60 + int(ts[0]) * 60 * 60
        try:
            os.remove("t123456.jpg")
        except:
            pass
        return t

    def split_videos(self,video_path,image_dir,hist = 1):
        if os.path.exists(image_dir):
            shutil.rmtree(image_dir)
        os.makedirs(image_dir)
        command1 = "%s " \
                   "-i %s " \
                   "-r %d -threads 20 -f image2 " \
                   "%s" % (self.ffmpeg_path, video_path, hist, image_dir + "\\%06d.jpg")
        print(command1)
        r = os.system(command1)
        return r


