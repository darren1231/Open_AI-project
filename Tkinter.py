from Tkinter import *
from PIL import ImageTk, Image
import os
import numpy as np

interval=0
array = np.zeros([30,30],dtype=np.int)
for i in xrange(interval+0,interval+5,1):
	for j in xrange(interval+0,interval+5,1):
		array[i][j]=120
print array
pic=Image.fromarray(array,mode='I')



root = Tk()
img = ImageTk.PhotoImage(pic)
panel = Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

root.mainloop()

#root.destroy()




