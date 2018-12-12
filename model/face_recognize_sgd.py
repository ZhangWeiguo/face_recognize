import numpy
from sklearn.externals import joblib

def dist_e(v1,v2):
    return numpy.sqrt(numpy.sum(numpy.square(v1-v2)))
def dist_c(v1,v2):
    return numpy.dot(v1.reshape(1,-1),v2.reshape(-1,1))[0,0]/(numpy.linalg.norm(v1)*numpy.linalg.norm(v2))


class SgdDist:
    def __init__(self,model_path):
        self.model = joblib.load(model_path)
    def distance(self,v1,v2):
        d1 = dist_c(v1, v2)
        d2 = dist_e(v2, v2)
        vv = numpy.c_[v1.reshape(1, -1), d1, d2, v2.reshape(1, -1)].reshape(-1, )
        p = self.model.predict_proba([vv])[0][1]
        return p