from PIL import Image
import numpy as np
import time
import psutil

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
	
	#initial position	
	x=0
	y=0
	for step in xrange(200):
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

			

		pic=Image.fromarray(array, mode='L')
		pic.show()
		if step==0:
			time.sleep(10)
		time.sleep(0.1)

		for proc in psutil.process_iter():
			if proc.name == "display":
				proc.kill()

			

random_run()
#tr_coordinate_to_picture(9,9)
#print np.random.randint(5)
