from skimage import io
import numpy as np
import tensorflow as tf
import scipy.io as sio
import os,gc
STYLE_WEIGHT = 1
CONTENT_WEIGHT = 1
STYLE_LAYERS = ['relu1_2','relu2_2','relu3_2']
CONTENT_LAYERS = ['relu1_2']

class VggVec:
    def __init__(self,model_file):
        self.vgg_params = sio.loadmat(model_file)

    def get_vec(self,images):
        layers = (
            'conv1_1', 'relu1_1', 'conv1_2', 'relu1_2', 'pool1',
            'conv2_1', 'relu2_1', 'conv2_2', 'relu2_2', 'pool2',
            'conv3_1', 'relu3_1', 'conv3_2', 'relu3_2', 'conv3_3', 'relu3_3', 'conv3_4', 'relu3_4', 'pool3',
            'conv4_1', 'relu4_1', 'conv4_2', 'relu4_2', 'conv4_3', 'relu4_3', 'conv4_4', 'relu4_4', 'pool4',
            'conv5_1', 'relu5_1', 'conv5_2', 'relu5_2', 'conv5_3', 'relu5_3', 'conv5_4', 'relu5_4', 'pool5'
        )
        weights = self.vgg_params['layers'][0]
        net = images
        for i, name in enumerate(layers):
            layer_type = name[:4]
            if layer_type == 'conv':
                kernels, bias = weights[i][0][0][0][0]
                kernels = np.transpose(kernels, (1, 0, 2, 3))
                conv = tf.nn.conv2d(net, tf.constant(kernels), strides=(1, 1, 1, 1), padding='SAME', name=name)
                net = tf.nn.bias_add(conv, bias.reshape(-1))
                net = tf.nn.relu(net)
            elif layer_type == 'pool':
                net = tf.nn.max_pool(net, ksize=(1, 2, 2, 1), strides=(1, 2, 2, 1), padding='SAME')
        return net


_vgg_params = sio.loadmat('D:/Code/Python3/face_recognize/dat/imagenet-vgg-verydeep-19.mat')
def vgg19(input_image):
    layers = (
        'conv1_1', 'relu1_1', 'conv1_2', 'relu1_2', 'pool1',
        'conv2_1', 'relu2_1', 'conv2_2', 'relu2_2', 'pool2',
        'conv3_1', 'relu3_1', 'conv3_2', 'relu3_2', 'conv3_3', 'relu3_3', 'conv3_4', 'relu3_4','pool3',
        'conv4_1', 'relu4_1', 'conv4_2', 'relu4_2', 'conv4_3', 'relu4_3', 'conv4_4', 'relu4_4', 'pool4',
        'conv5_1', 'relu5_1', 'conv5_2', 'relu5_2', 'conv5_3', 'relu5_3', 'conv5_4', 'relu5_4', 'pool5'
    )
    print(_vgg_params.__class__,_vgg_params.keys())
    weights = _vgg_params['layers'][0]
    net = input_image
    network = {}
    for i,name in enumerate(layers):
        layer_type = name[:4]
        if layer_type == 'conv':
            kernels,bias = weights[i][0][0][0][0]
            kernels = np.transpose(kernels,(1,0,2,3))
            conv = tf.nn.conv2d(net,tf.constant(kernels),strides=(1,1,1,1),padding='SAME',name=name)
            net = tf.nn.bias_add(conv,bias.reshape(-1))
            net = tf.nn.relu(net)
        elif layer_type == 'pool':
            net = tf.nn.max_pool(net,ksize=(1,2,2,1),strides=(1,2,2,1),padding='SAME')
        network[name] = net

    return network

if __name__ == "__main__":
    # path = "D:\\Code\\Python3\\face_recognize\\profile\\root\\data\\video\\广视新闻1201.mp4_temp"
    # L = [os.path.join(path,i) for i in os.listdir(path)]
    Vec = VggVec('D:/Code/Python3/face_recognize/dat/imagenet-vgg-verydeep-19.mat')
    with tf.Session() as session:
        data = []
        data.append(io.imread("1.jpg"))
        input = tf.constant(np.array(data), dtype=tf.float32)
        output = Vec.get_vec(input)
        print(output)
        print(session.run(output))
        # k = 0
        # data = []
        # for p in range(20):
        #     while k < 20:
        #         data.append(io.imread("1.jpg"))
        #         k += 1
        #     input = tf.constant(np.array(data),dtype=tf.float32)
        #     output = Vec.get_vec(input)
        #     print(session.run(output))
        #     gc.collect()