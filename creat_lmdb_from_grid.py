from PIL import Image
import numpy as np
import time
import psutil
import lmdb
import caffe

def tr_coordinate_to_picture(x,y):
	"""
	x:0~9
	y:0~9
        """

	x_interval=5*x
	y_interval=5*y
	#array = np.zeros((50,50),dtype=np.uint8)
	#array = np.ones((50,50),dtype=np.uint8)*256
	array = np.random.randint(100,size=(50,50)).astype('uint8')
	#print array.dtype
	for i in xrange(0+x_interval,5+x_interval,1):
		for j in xrange(0+y_interval,5+y_interval,1):
			array[i][j]=255
	return array

	#pic=Image.fromarray(array, mode='L')
	#pic.show()

def random_run():
	number_of_step=10
	full_array=[]
	#initial position	
	x=0
	y=0
	for step in xrange(number_of_step):
		rand_number=np.random.randint(4)
		if rand_number==0:    #up
			x_temp=x-1
			y_temp=y
		elif rand_number==1:  #down
			x_temp=x+1
			y_temp=y
		elif rand_number==2:  #left
			y_temp=y-1
			x_temp=x
		else:  		      #right
			y_temp=y+1
			x_temp=x

		# restore original position
		if x_temp==-1 or x_temp==10 or y_temp==-1 or y_temp==10:
			x_temp=x
			y_temp=y
		
		x=x_temp
		y=y_temp

		array=tr_coordinate_to_picture(x,y)
		print 'x: ',x,'  y: ',y,' action: ',rand_number
		full_array.append(array)
	return full_array

def creat_lmdb(X):
	N=X.shape[0]
	y = np.zeros(N, dtype=np.int64)

	map_size = X.nbytes * 10
	env = lmdb.open('grid_train', map_size=map_size)		
	with env.begin(write=True) as txn:
	    # txn is a Transaction object
	    for i in range(N):
		datum = caffe.proto.caffe_pb2.Datum()
		#set channels=1
		datum.channels = X.shape[1]
		#set height =50
		datum.height = X.shape[2]
		#set width = 50
		datum.width = X.shape[3]
		datum.data = X[i].tobytes()  # or .tostring() if numpy < 1.9
		datum.label = int(y[i])
		
		
		str_id = '{:08}'.format(i)

		# The encode is only essential in Python 3
		txn.put(str_id.encode('ascii'), datum.SerializeToString())
			

full_array=random_run()
np_full_array = np.array(full_array)
np_reshape_array=np_full_array.reshape(np_full_array.shape[0],1,np_full_array.shape[1],np_full_array.shape[2])
print np_reshape_array.shape

creat_lmdb(np_reshape_array)

#tr_coordinate_to_picture(9,9)
#print np.random.randint(5)
