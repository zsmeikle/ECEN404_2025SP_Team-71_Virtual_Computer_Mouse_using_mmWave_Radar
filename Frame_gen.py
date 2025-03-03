import queue
import time
from pynput.mouse import Button, Controller

#IMPORTANT################################################################
#                                                                        #
# Make sure to tun "shared_queue.put((0, 0, 0, False))" before joing     #
# thread or the thread will not die and will break the python terminal!! #
#                                                                        #
##########################################################################

def run_frame_gen(shared_queue, refresh_rate, frames, lol):#generates frames inbetween data points
    mouse = Controller()#start mouse thing
    not_kill = True #to keep loop running
    while not_kill:#loop until told to end
        try:
            X, Y, not_kill= shared_queue.get(timeout=1/refresh_rate) #get data from queue

            if(lol):
                print("Joe Biden")
             
            for  i in range(0, frames, 1):#generate frames inbetween
                mouse.move(X/frames, Y/frames) #move mouse
                time.sleep(1/refresh_rate/frames) #wait till next time to move
        except queue.Empty:#if nothing in queue continue
            pass