# -*- coding: utf-8 -*-
"""
Created on Tue Jan 09 21:58:11 2018

@author: zhangweiguo
"""

import dlib
import hashlib,time,re,os,numpy
from skimage import io
from matplotlib import pyplot

class ImageProcess:
    def __init__(self, face_detect_filename, face_vec_filename):
        self.face_detector = dlib.get_frontal_face_detector()
        self.face_point_predictor = dlib.shape_predictor(face_detect_filename)
        self.face_vector_model = dlib.face_recognition_model_v1(face_vec_filename)


    def read_image(self,image_path):
        img = io.imread(image_path)
        return img



    def get_face_form_image(self,image_path, draw = False):
        img = self.read_image(image_path)
        dets = self.face_detector(img, 1)
        n = len(dets)
        faces = []
        if draw:
            figure = pyplot.figure(image_path)
            pyplot.imshow(img)
        for det in dets:
            I = img[det.top():det.bottom(), det.left():det.right(), :]
            faces.append(I)
            if draw:
                y = [det.top(), det.bottom(), det.bottom(), det.top(), det.top()]
                x = [det.left(), det.left(), det.right(), det.right(), det.left()]
                pyplot.plot(x,y,color='red',linewidth=3)
        if draw:
            pyplot.show()
        return faces

    def get_vector_from_image(self,image_path):
        img = self.read_image(image_path)
        vv = []
        faces = []
        edges = []
        dets = self.face_detector(img, 1)
        for det in dets:
            shape = self.face_point_predictor(img, det)
            v = self.face_vector_model.compute_face_descriptor(img, shape)
            v = numpy.array(v)
            vv.append(v)

            I = img[det.top():det.bottom(), det.left():det.right(), :]
            faces.append(I)
            y = [det.top(), det.bottom(), det.bottom(), det.top(), det.top()]
            x = [det.left(), det.left(), det.right(), det.right(), det.left()]
            edges.append((x,y))
        return vv,faces,edges

    def get_vector_from_array(self,img):
        vv = []
        faces = []
        edges = []
        dets = self.face_detector(img, 1)
        for det in dets:
            shape = self.face_point_predictor(img, det)
            v = self.face_vector_model.compute_face_descriptor(img, shape)
            v = numpy.array(v)
            vv.append(v)

            I = img[det.top():det.bottom(), det.left():det.right(), :]
            faces.append(I)
            y = [det.top(), det.bottom(), det.bottom(), det.top(), det.top()]
            x = [det.left(), det.left(), det.right(), det.right(), det.left()]
            edges.append((x,y))
        return vv,faces,edges
