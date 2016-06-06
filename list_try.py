"""
a=[[2,3],[2,3],[2,3]]
b=[[2,3],[2,3],[2,3]]

c=[a,b]

for i in c:
	for j in i:
		for k in j:

			print k	
2
3
2
3
2
3
2
3
2
3
2
3
[Finished in 0.6s]
"""
import gym
import time
import numpy as np
    
env = gym.make('MsPacman-v0')
env.reset()
done=False
save_rgb=[]

for i in xrange(2):
	env.render(mode='human', close=False)
	time.sleep(0.05)
	#print i 
	rgb_pixcel=env.render(mode='rgb_array', close=False)
	save_rgb.append(rgb_pixcel)
	
	observation, reward, done, info=env.step(1)

	
    
    
print "game over"
print len(save_rgb)
print save_rgb
"""
re_shape=[]
for i in save_rgb:

	for j in i:
		for k in j:
			for m in k:
				re_shape[i].append(m)
print len(re_shape[0])

"""



test=np.array(save_rgb)
print test.shape
c=np.reshape(test,(2,160*210*3))
print c[1]