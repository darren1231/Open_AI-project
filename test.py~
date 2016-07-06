import gym
import time



import termios, sys, os
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








env = gym.make('MsPacman-v0')
env.reset()
done=False
save_rgb=[]
while (done==False):
    
    	
	    env.render(mode='human', close=False)
	    #time.sleep(0.05)
	    #print i 
	    rgb_pixcel=env.render(mode='rgb_array', close=False)
	    save_rgb.append(rgb_pixcel)

	    direction = getkey()
	    if(direction=="8"):		#up
	    	observation, reward, done, info=env.step(1)
	    elif(direction=="5"):	#down
	    	observation, reward, done, info=env.step(4)
	    elif(direction=="4"):	#left
	    	observation, reward, done, info=env.step(3)
	    elif(direction=="6"):	#right
	    	observation, reward, done, info=env.step(2)
	    else:
	    	print "wrong key"
	
    
    
print "game over"
print len(save_rgb)

    #env.step(1) # take a random action
    
    



