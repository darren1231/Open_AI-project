from PIL import Image
import numpy as np
import time
import psutil

im = Image.open( "test1.png" )
array=np.array(im)
im.show()
print array.shape

for interval in xrange(0,50,10):
	for i in xrange(interval+0,interval+10,1):
		for j in xrange(interval+0,interval+10,1):
			array[i][j][0]=0
			array[i][j][1]=0
			array[i][j][2]=0

	pic=Image.fromarray(array)
	pic.show()
	time.sleep(0.5)
	
	# With psutil , I can run through all program and find which is "display"
	for proc in psutil.process_iter():
		#list pid of all program
		#print proc.pid
		#list name of all program	
		#print proc.name	
		if proc.name == "display":
			proc.kill()




