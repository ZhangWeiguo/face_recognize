# -*- encoding:gbk -*-
def common_str(names):
    n = len(names)
    if n == 0:
        return ""
    elif n == 1:
        return names[0]
    elif n>1:
        m = len(names[0])
        for i in range(1,m):
            s = names[0][0:i]
            for j in range(1,n):
                if s in names[j]:
                    s1 = s
                else:
                    if s1 == "":
                        return names[0]
                    else:
                        return s1

def time2str(t):
    m = int(t/60)
    s = int(t - m*60)
    return "%d Min %d S"%(m,s)

def transform_result(filename,sim_weak=0.85,sim_mid=0.88,sim_height = 0.90):
    f = open(filename,'r')
    columns = f.readline().split(",")
    Result = []
    if "video_name" in columns:
        type = "video"
    elif "img1_name" in columns:
        type = "img"
    else:
        type = "unknow"
    if type == "video":
        img_num = columns.count("img_name")
        result = {}
        s = f.readline()
        while s:
            L = s.split(",")
            t = int(float(L[1]))
            video_name = L[0]
            video_url = L[3*img_num+4]
            k = 1
            img_name = common_str([L[3 * ki] for ki in range(k,img_num)])
            sim = float(L[3*img_num+2])

            if sim >sim_weak:
                if (video_name,img_name) in result:
                    if t in result[(video_name,img_name)]:
                        if result[(video_name,img_name)][t][0] < sim:
                            result[(video_name,img_name)][t] = (sim,video_url)
                    else:
                        result[(video_name, img_name)][t] = (sim,video_url)
                else:
                    result[(video_name, img_name)] = {}
                    result[(video_name, img_name)][t] = (sim,video_url)
            s = f.readline()

        Result = []
        for (video_name,img_name) in result:
            info = result[(video_name,img_name)]
            start = 0
            end = 1
            max_sim = 0
            video_url = ""
            for t in sorted(info.keys()):
                if t - end > 1:
                    if start != 0:
                        start_time = time2str(start)
                        end_time = time2str(end)
                        time_range = "%s - %s"%(start_time,end_time)
                        if max_sim > sim_height:
                            sim = "强相似"
                        elif max_sim > sim_mid:
                            sim = "中相似"
                        else:
                            sim = "弱相似"
                        Result.append([video_name,img_name,time_range,round(max_sim,4),sim,video_url])
                    start = t
                    end = t
                    max_sim = info[t][0]
                    video_url = info[t][1]
                elif t - end == 1:
                    end = t
                    if info[t][0] > max_sim:
                        max_sim = info[t][0]
                        video_url = info[t][1]
        Result = sorted(Result,key=lambda x: (x[0], x[1], -x[3]))

    elif type == "img":
        Result = []
        s = f.readline()
        while s:
            L = s.split(",")
            L[4] = round(float(L[4]),4)
            Result.append(L[0:5])
            s = f.readline()
    f.close()
    return Result,type

# filename = "root_1516811653.csv"
# sim_mid = 0.85
# sim_height = 0.90


# def transform_result(filename,sim_mid=0.85,sim_height = 0.90):
#     f = open(filename,'r')
#     columns = f.readline().split(",")
#     Result = []
#     if "video_name" in columns:
#         type = "video"
#     elif "img1_name" in columns:
#         type = "img"
#     else:
#         type = "unknow"
#     if type == "video":
#         img_num = columns.count("img_name")
#         result = {}
#         s = f.readline()
#         while s:
#             L = s.split(",")
#             t = int(float(L[1]))
#             video_name = L[0]
#             video_url = L[3*img_num+3]
#             k = 1
#             while k<=img_num:
#                 img_name = L[3*k]
#                 img_sim = float(L[3*k+2])
#                 k += 1
#                 if img_sim >sim_mid:
#                     if (video_name,img_name) in result:
#                         if t in result[(video_name,img_name)]:
#                             if result[(video_name,img_name)][t][0] < img_sim:
#                                 result[(video_name,img_name)][t] = (img_sim,video_url)
#                         else:
#                             result[(video_name, img_name)][t] = (img_sim,video_url)
#                     else:
#                         result[(video_name, img_name)] = {}
#                         result[(video_name, img_name)][t] = (img_sim,video_url)
#             s = f.readline()
#
#         Result = []
#         for (video_name,img_name) in result:
#             info = result[(video_name,img_name)]
#             start = 0
#             end = 1
#             max_sim = 0
#             video_url = ""
#             for t in sorted(info.keys()):
#                 if t - end > 1:
#                     if start != 0:
#                         start_time = time2str(start)
#                         end_time = time2str(end)
#                         time_range = "%s - %s"%(start_time,end_time)
#                         if max_sim > sim_height:
#                             sim = "Height Similarity"
#                         else:
#                             sim = "Mid Similarity"
#                         Result.append([video_name,img_name,time_range,round(max_sim,4),sim,video_url])
#                     start = t
#                     end = t
#                     max_sim = info[t][0]
#                     video_url = info[t][1]
#                 elif t - end == 1:
#                     end = t
#                     if info[t][0] > max_sim:
#                         max_sim = info[t][0]
#                         video_url = info[t][1]
#         Result = sorted(Result,key=lambda x: (x[0], x[1], -x[3]))
#
#     elif type == "img":
#         Result = []
#         s = f.readline()
#         while s:
#             L = s.split(",")
#             L[4] = round(float(L[4]),4)
#             Result.append(L[0:5])
#             s = f.readline()
#     f.close()
#     return Result,type
