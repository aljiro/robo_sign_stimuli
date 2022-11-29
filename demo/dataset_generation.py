import numpy as np
import cv2
import time

colors = [(0, 0, 0), (0, 255, 0), (255, 0, 0),  (255, 255, 255), (0, 0, 255)]

def draw_bar(bkg, v, dir, x, color):
    obj_dim1 = 100
    obj_dim2 = 20
    im = np.copy(bkg)
    if dir == 0:
        cv2.rectangle(im,(x,v),(x + obj_dim1,v + obj_dim2),color,-1)
    else:
        cv2.rectangle(im,(x,v),(x + obj_dim2,v + obj_dim1),color,-1)
    
    return im

# w, h = 540, 360
w, h = 320, 240
nframes = 30

def generate_sample( id, v, dir, color, f ):
    # choose a background
    bkg = np.random.rand(h,w,3)*255
    bkg = bkg.astype(np.uint8)

    size = (w, h)
    name = 'example_' + id + '.avi'
    path = 'horz' if dir == 0 else 'vert'
    f.write(path + '/' + name + "," + ("horizontal" if dir == 0 else "vertical") + "\n")
    result = cv2.VideoWriter(path + '/' + name, 
                            cv2.VideoWriter_fourcc(*'MJPG'),
                            10, size)
    x = 0
    # Create the frames
    for i in range(nframes):
        frame = draw_bar(bkg, v, dir, x, color)
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

def generate_dataset( N, prefix ):
    trainf = open(prefix + ".csv", "w")
    trainf.write( "video_name,tag\n" )

    for i in range(N):

        dir = np.random.rand() > 0.5
        v = int(np.random.rand()*(h))
        v = v if (v < 200) else (v - 100)
        
        color = colors[np.random.randint(len(colors))]	
        generate_sample(prefix + str(i), v, dir, color, trainf)


    trainf.close()


prefix = "train"
generate_dataset(100, prefix)
prefix = "test"
generate_dataset(100, prefix)