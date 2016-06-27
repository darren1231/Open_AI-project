import numpy as np
import lmdb
import caffe
import gym
from PIL import Image

# gym model
env = gym.make('Pong-v0')
env.reset()
empty=[]
for i in range(1000):
    picture=env.render(mode="rgb_array")
    env.step(env.action_space.sample()) # take a random action
    img = Image.fromarray(picture, 'RGB')
    img_grey=img.convert('L')
    array=np.array(img_grey.getdata())
    print i
    empty.append(array)
    #img_grey.save('small_'+str(i)+'.jpg')
    
All_picture= np.array(empty)
print All_picture.shape
Resize_picture = All_picture.reshape(All_picture.shape[0],1,210,160)
print Resize_picture.shape


  
N = 1000
X=Resize_picture
# Let's pretend this is interesting data
#X = np.zeros((N, 3, 32, 32), dtype=np.uint8)
print "x shape is :",X.shape
y = np.zeros(N, dtype=np.int64)
print "y shape is :",y.shape

# We need to prepare the database for the size. We'll set it 10 times
# greater than what we theoretically need. There is little drawback to
# setting this too big. If you still run into problem after raising
# this, you might want to try saving fewer entries in a single
# transaction.
map_size = X.nbytes * 10

print "map_size is:1*210*160*1000*10 --",map_size

env = lmdb.open('pong_grey_test', map_size=map_size)

with env.begin(write=True) as txn:
    # txn is a Transaction object
    for i in range(N):
        datum = caffe.proto.caffe_pb2.Datum()
        #set channels=3
        datum.channels = X.shape[1]
        #set height =32
        datum.height = X.shape[2]
        #set width = 32
        datum.width = X.shape[3]
        datum.data = X[i].tobytes()  # or .tostring() if numpy < 1.9
        datum.label = int(y[i])
        
        
        str_id = '{:08}'.format(i)

        # The encode is only essential in Python 3
        txn.put(str_id.encode('ascii'), datum.SerializeToString())