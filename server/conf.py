app_config = {
    "root_path":"D:/Code/Python3/face_recognize",
    "template_path":"D:/Code/Python3/face_recognize/server/templates",
    "static_path":"D:/Code/Python3/face_recognize/server/static",
    "app_name":"SMF",
    "port":8080,
    "host":"http://imath.sysu.edu.cn",
    "img_type":["jpg"],
    "video_type":["mp4"]
}

sql_config = {
    "host":"localhost",
    "port":"3306",
    "user":"sysu",
    "password":"sysu1234",
    "database":"face_recognize",
    "pool_name":"face_recognize",
    "pool_size":20
}

file_config = {
    "root_path":"D:\\Code\\Python3\\face_recognize\\profile\\%s",
    "img_path":"D:\\Code\\Python3\\face_recognize\\profile\\%s\\data\\img",
    "video_path":"D:\\Code\\Python3\\face_recognize\\profile\\%s\\data\\video",
    "feature_img_path":"D:\\Code\\Python3\\face_recognize\\profile\\%s\\feature\\img",
    "feature_video_path":"D:\\Code\\Python3\\face_recognize\\profile\\%s\\feature\\video",
    "result_path":"D:\\Code\\Python3\\face_recognize\\profile\\%s\\result"
}


model_config = {
    "recognize_model_path":"D:\\Code\\Python3\\face_recognize\\dat\\SGD.model",
    "face_detect_path":"D:\\Code\Python3\\face_recognize\\dat\\shape_predictor_68_face_landmarks.dat",
    "face_vec_path":"D:\\Code\Python3\\face_recognize\\dat\\dlib_face_recognition_resnet_model_v1.dat",
    "ffmpge_path":"D:\\ffmpeg\\bin\\ffmpeg.exe",
    "spark_model_path":"D:\\Code\Python3\\face_recognize\\spark\\feature_catch.py",
    "request_host":[]
}

compute_config = {
    "hist":15,
    "process_num":20
}