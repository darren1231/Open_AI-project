from PIL import Image
import numpy as np
import time
import psutil

#im = Image.open( "30_black.jpg" )
#array=np.array(im)
#im.show()

#print 'array.shape:',array.shape


for interval in xrange(0,30,5):
	#add noise
	#array = np.random.randint(50,size=[30,30])
	#array=np.random.randint(50,size=[30,30])
	array = np.zeros((30,30),dtype=np.uint8)
	for i in xrange(interval+0,interval+5,1):
		for j in xrange(interval+0,interval+5,1):
			array[i,j]=255

	
  	print array	
	
	pic=Image.fromarray(array, mode='L')	
	
	print pic.size
	#pic.resize((30,30))
	pic.show()
	#pic.save('why.jpg')
	time.sleep(2)
	
	# With psutil , I can run through all program and find which is "display"
	for proc in psutil.process_iter():
		#list pid of all program
		#print proc.pid
		#list name of all program	
		#print proc.name	
		if proc.name == "display":
			proc.kill()

#print np.random.randint(255,size=(30,30))


