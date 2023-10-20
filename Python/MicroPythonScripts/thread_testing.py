
import time
from machine import Pin
import _thread
import gc
import utime

set_point = 0
a_lock = _thread.allocate_lock()

def set_set_point(new_set_point):
    #print("set attempting to acquire!")
    if(a_lock.acquire()):
        #print("set acquired!")
        global set_point
        set_point = new_set_point
        print(f"Set point is now {set_point}")
        a_lock.release()
        #print("set released!")

def get_set_point():
    cur_set_point = 0
    #print("get attempting to acquire!")
    if(a_lock.acquire(True, 0.1)):
        #print("get acquire!")
        global set_point
        cur_set_point = set_point
        a_lock.release()
        #print("get release!")
        return cur_set_point
    else:
        return None




        
    
def updateMotorValuesThread():
    print("Starting thread")
    while thread_running:
        goal = get_set_point()
        print(goal)
        utime.sleep(0.02)
        print(thread_running)
    print("Goodnight moon!")

def core0_thread():
    count = 0
    running = True
    while running:
        count += 1
        set_set_point(count)
        utime.sleep(1.0)
        if count == 10:
            running = False
            global thread_running
            thread_running = False
            utime.sleep(2.0)
            print("goodnight!")
            #_thread.exit()
            
thread_running = True
second_thread = _thread.start_new_thread(updateMotorValuesThread, ())

if __name__ == "__main__":
    print("hello world")


    #second_thread = _thread.start_new_thread(updateMotorValuesThread, ())
    core0_thread()

