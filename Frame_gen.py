import queue
import time
from pynput.mouse import Button, Controller

def F_gen(shared_queue):
    mouse = Controller()
    while True:
        try:
            X, Y, frames= shared_queue.get(timeout=1/22) 
             
            for  i in range(0, frames, 1):
                mouse.move(X, Y) 
                time.sleep(1/22/frames) 
                print("did thing")
        except queue.Empty:
            pass

if __name__ == "__main__":
    shared_queue = queue.Queue()
    F_gen(shared_queue)