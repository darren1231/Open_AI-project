import caffe
import numpy as np

np.set_printoptions(threshold='nan')
MODEL_FILE = 'grid_autoencoder_deploy.prototxt'
PRETRAIN_FILE = 'grid_autoencoder_iter_65000.caffemodel'
net = caffe.Net(MODEL_FILE, PRETRAIN_FILE, caffe.TEST)
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2, 0, 1))

transformer.set_raw_scale('data', 255)

net.blobs['data'].reshape(1, 1, 50, 50)

img = caffe.io.load_image('50_black.jpg', color=False)

print "Show the size of image:\n",img.shape,"\n"
net.blobs['data'].data[...] = transformer.preprocess('data', img)
out = net.forward()
print "The type of the data come from net is Blob:\n",out,"\n"

print "We need to convert it to matrix that we can use:\n",out[net.outputs[0]],"\n"

print "This is second method that can extract any data from any layer:\n",net.blobs['encode4neuron'].data,"\n"
