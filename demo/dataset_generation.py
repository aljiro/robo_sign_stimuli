import numpy as np
import cv2
import time

colors = [(0, 0, 0), (0, 255, 0), (255, 0, 0),  (255, 255, 255), (0, 0, 255)]

def draw_bar(bkg, v, dir, x):
	obj_dim1 = 100
	obj_dim2 = 20
	im = np.copy(bkg)
	if dir == 0:
		cv2.rectangle(im,(x,v),(x + obj_dim1,v + obj_dim2),color,-1)
	else:
		cv2.rectangle(im,(x,v),(x + obj_dim2,v + obj_dim1),color,-1)
	
	return im

w, h = 200, 300
nframes = 30

def generate_sample( id, v, dir, color ):
	# choose a background
	bkg = np.random.rand(h,w,3)*255
	bkg = bkg.astype(np.uint8)

	size = (w, h)
	name = 'example_' + str(id) + '.avi'
	path = 'horz' if dir == 0 else 'vert'
	print(name)
	result = cv2.VideoWriter(path + '/' + name, 
							cv2.VideoWriter_fourcc(*'MJPG'),
							10, size)
	x = 0
	# Create the frames
	for i in range(nframes):
		frame = draw_bar(bkg, v, dir, x)
		result.write(frame)
		# Display the frame
		# # saved in the file
		# cv2.imshow('Frame', frame)
		# Press S on keyboard 
		# to stop the process
		# if cv2.waitKey(1) & 0xFF == ord('s'):
		# 	break
		x += 10

	result.release()
	# cv2.destroyAllWindows()



for i in range(20):
	dir = np.random.rand() > 0.5
	v = int(np.random.rand()*(h))
	v = v if (v < 200) else (v - 100)
	
	print(v)	
	color = colors[np.random.randint(len(colors))]	
	generate_sample(i, v, dir, color)