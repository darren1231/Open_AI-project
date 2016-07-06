from PIL import Image
import numpy as np

array = np.zeros((300,300),dtype=np.int)
pic=Image.fromarray(array,mode='L')
pic.show()
pic.save('300_black.jpg')
print array
