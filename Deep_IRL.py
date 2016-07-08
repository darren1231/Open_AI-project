import caffe
import numpy as np
from PIL import Image
import time
import psutil
import lmdb
import termios, sys, os

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
	
	
	#pic=Image.fromarray(array, mode='L')
	#pic.show()
	
	
	
	return array

def random_run():
	number_of_step=15
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
def getkey():
    term = open("/dev/tty", "r")
    fd = term.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] &= ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, old)
        term.close()
    return c

def kill_display():
	for proc in psutil.process_iter():
		#list pid of all program
		#print proc.pid
		#list name of all program	
		#print proc.name	
		if proc.name == "display":
			proc.kill()	
	
def creat_expert_experience():
	
	number_of_step=18
	full_array=[]
	#initial start position	
	x=0
	y=0
	tr_coordinate_to_picture(x,y)
	experience=np.zeros([30])
	gamma=0.9
	keyboard=0
	for step in xrange(number_of_step):

		"""record mue"""
		array=tr_coordinate_to_picture(x,y)
		re_array = array.reshape(array.shape[0],array.shape[1],1)
		experience=experience+pow(gamma,step)*threshold_data(read_caffe_model(re_array))
		print threshold_data(read_caffe_model(re_array))
		print 'experience: ',experience
		"""end record mue"""

		print 'x: ',x,'  y: ',y,' action: ',keyboard

		keyboard=getkey()		

		if keyboard=="8":    #up
			x_temp=x-1
			y_temp=y
		elif keyboard=="5":  #down
			x_temp=x+1
			y_temp=y
		elif keyboard=="4":  #left
			y_temp=y-1
			x_temp=x
		elif keyboard=="6":  #right
			y_temp=y+1
			x_temp=x
		else:
			print 'Your key is [',keyboard,']   please key 8(up) 5(down) 4(left) 6(right)'
			x_temp=x
			y_temp=y

		# restore original position
		if x_temp==-1 or x_temp==10 or y_temp==-1 or y_temp==10:
			x_temp=x
			y_temp=y
		
		x=x_temp
		y=y_temp
	
	
	return experience


def read_caffe_model(array):
	np.set_printoptions(threshold='nan')
	MODEL_FILE = 'grid_autoencoder_deploy.prototxt'
	PRETRAIN_FILE = 'grid_autoencoder_iter_65000.caffemodel'
	net = caffe.Net(MODEL_FILE, PRETRAIN_FILE, caffe.TEST)
	transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
	transformer.set_transpose('data', (2, 0, 1))
	transformer.set_raw_scale('data', 255)
	net.blobs['data'].reshape(1, 1, 50, 50)	

	#print "Show the size of image:\n",array.shape,"\n"
	net.blobs['data'].data[...] = transformer.preprocess('data', array)
	out = net.forward()
	#print "The type of the data come from net is Blob:\n",out,"\n"
	#print "We need to convert it to matrix that we can use:\n",out[net.outputs[0]],"\n"	
	#print "This is second method that can extract any data from any layer:\n",net.blobs['encode4neuron'].data,"\n"
		
	return net.blobs['encode4neuron'].data

def threshold_data(data):
	for i in xrange(data.shape[0]):
		for j in xrange(data.shape[1]):
			if data[i][j]>0.8:
				data[i][j]=1
			else:
				data[i][j]=0
	#print data	
	return data

def take_action(action,x_position,y_position):
	"""
    	situation:
	0:hit wall
	1:hit goal
	2:normal
	"""
	if action==0:           #up
		x_temp=x_position-1
		y_temp=y_position
	elif action==1:         #down
		x_temp=x_position+1
		y_temp=y_position
	elif action==2:         #left
		x_temp=x_position
		y_temp=y_position-1
	else :                  #right
		x_temp=x_position
		y_temp=y_position+1

	"""check situation"""	
	if x_temp==-1 or x_temp==10 or y_temp==-1 or y_temp==10:
		situation=0
	elif x_temp==9 and y_temp==9:
		situation=1
	else:
		situation=2
	    

	if situation == 2 or situation == 1:    #normal or hit goal
		return x_temp,y_temp,situation
	else:
		return x_position,y_position,situation

def cal_error(mue,mue_wall,mul,mul_wall):    
    diff = mue -mul
    error = sum(sum(pow(diff,2)))+pow(mue_wall-mul_wall,2)
    return pow(error,0.5)

def evaluation(q_table,x_position,y_position,epsilon):
    random_100=np.random.randint(100) #0~99
    rand_action = np.random.randint(4) #0~4
    if random_100 < epsilon:
        action = np.random.randint(4)
    else:
        temp_q = list(q_table[x_position,y_position,0:4])
        temp_action = temp_q.index(max(temp_q))
        if q_table[x_position,y_position,rand_action]>=max(temp_q):
            action = rand_action
        else:
            action = temp_action
    return action

def rule_without_bad(mue,mue_wall,mul,mul_wall,F_matrix,F_wall):
	parameter_a = 0.1
	col= mue.shape[1]
        
	correct = np.zeros([1,col])
	
        F_matrix=F_matrix.reshape(1,30)
	
	
	for j in range(col):
		
		if mue[0,j]==mul[0,j]:
			correct[0,j]=1
		else:
			correct[0,j]=0
    
	
	for j in range(col):
		if correct[0,j]==0:     #wrong
			F_matrix[0,j]=F_matrix[0,j]+(1-F_matrix[0,j])*parameter_a
		else:                   #right
			F_matrix[0,j]=(1-parameter_a)*F_matrix[0,j]

	if mue_wall == mul_wall:
        	F_wall = (1-parameter_a)*F_wall
	else:
		F_wall = F_wall + (1-F_wall)*parameter_a
    
	return F_matrix,F_wall

def omg_update(omg,omg_wall,mue,mue_wall,mul,mul_wall,F_matrix,F_wall):
	omg = omg + (mue-mul)*F_matrix
	omg_wall = omg_wall + (mue_wall-mul_wall)*F_wall
	return omg,omg_wall

def reward_function(omg):
	reward=np.zeros((10,10),dtype=np.float32)
	for i in xrange(10):
		for j in xrange(10):
			array=tr_coordinate_to_picture(i,j)
			re_array = array.reshape(array.shape[0],array.shape[1],1)
			data=read_caffe_model(re_array)
			mul_temp=threshold_data(data)    #shape:(1,30)			
			
			reward[i][j]=np.dot(mul_temp,omg.reshape(30,1))/sum(sum(mul_temp))
	print reward	
	getkey()		
	return reward

#expert_experience=creat_expert_experience()
#np.savetxt('expert.txt', expert_experience, delimiter=',')
out=np.loadtxt('expert.txt', delimiter=',')
print out.shape
print out
#random_run()
"""
array = np.random.randint(100,size=(50,50)).astype('uint8')
re_array = array.reshape(array.shape[0],array.shape[1],1)
print re_array.shape
data=read_caffe_model(re_array)
print data
threshold_data(data)
"""

"""main"""
N=10
Gamma = 0.9


"""get mue  shape:(30,1)-->reshape(1,30)"""
#expert_experience=creat_expert_experience()
mue=np.loadtxt('expert.txt', delimiter=',')
mue=mue.reshape(1,30)
mue_wall=0
"""initial"""
omg = np.zeros([1,30])
omg_wall = 0
q_table = np.zeros([N,N,4])
F_matrix = np.ones([1,30])*0.9
F_wall = 0.9

"""Start learning"""""""""""""""""""""""""""

for trial in range(1):
	mul = np.zeros([1,30])
	mul_wall = 0
	x_position,y_position = 0,0
	
	array=tr_coordinate_to_picture(x_position,y_position)
	re_array = array.reshape(array.shape[0],array.shape[1],1)
	data=read_caffe_model(re_array)
	mul=threshold_data(data)    #shape:(1,30)
		
	square_error=0

	"""agent start learning"""

	for i in range(1,18):
		action = evaluation(q_table,x_position,y_position,0)
		x_position,y_position,situation = take_action(action,x_position,y_position)
		
		if situation == 0:      #hit wall
	        	mul_wall = mul_wall + pow(Gamma,i)
		elif situation == 1:    #hit goal
			break
		else:
			
			array=tr_coordinate_to_picture(x_position,y_position)
			re_array = array.reshape(array.shape[0],array.shape[1],1)
			data=read_caffe_model(re_array)
			mul_temp=threshold_data(data)    #shape:(1,30)

			mul = mul + pow(Gamma,i)*mul_temp

	print 'Square error: ',cal_error(mue,mue_wall,mul,mul_wall),'trail: ',trial

	square_error = cal_error(mue,mue_wall,mul,mul_wall)

	if (square_error<0.00000001):
        	print 'success'
        	#break
    	else:
		F_matrix,F_wall=rule_without_bad(mue,mue_wall,mul,mul_wall,F_matrix,F_wall)
		omg,omg_wall = omg_update(omg,omg_wall,mue,mue_wall,mul,mul_wall,F_matrix,F_wall)
				
		reward=reward_function(omg)
	      	#q_table = np.zeros([N,N,4])	
	"""RL learning"""
	#q_table =RL(reward,omg_wall,q_table)




