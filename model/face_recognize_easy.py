import numpy
class EasyDist:
    def __init__(self):
        pass
    def distance(self,v1,v2):
        d1 = numpy.sqrt(numpy.sum(numpy.square(v1-v2)))
        return numpy.exp(-d1)