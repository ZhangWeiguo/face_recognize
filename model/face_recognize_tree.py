# -*-encoding:utf-8 -*-
'''
created by zwg in 2018-01-10
'''

from sklearn import ensemble,neural_network
from sklearn.externals import joblib


class TreeModel:
    def __init__(self,n_estimators=200,max_depth=10):
        self.model = ensemble.ExtraTreesClassifier(n_jobs=-1,n_estimators=n_estimators,max_depth=max_depth)
        # self.model = ensemble.RandomForestClassifier(n_jobs=-1, n_estimators=n_estimators, max_depth=max_depth)
    def train(self,data,target):
        self.model.fit(data, target)
    def score(self,data,target):
        return self.model.score(data,target)
    def predict(self,data):
        return self.model.predict(data)
    def predict_pro(self,data):
        return self.model.predict_proba(data)
    def save(self,filename):
        joblib.dump(self.model,filename)
    def restore(self,filename):
        self.model = joblib.load(filename)


