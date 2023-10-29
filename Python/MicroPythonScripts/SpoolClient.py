import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led, Button
import machine
from machine import PWM, Pin
import sys
import socket
import _thread
import utime
import gc
import select
#import ipaddress
#import wifi
dance_router = {"ssid": 'NETGEAR80', 'password': 'yellowwater460'}
home_router = {"ssid": 'Linksys03016', 'password': 'q21ruweiq3'} 
program_running = True

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.3"
ADDR = (SERVER, PORT)

program_finished = False


motor1 = machine.PWM(Pin(1))
motor1.freq(50)

set_point = 0
a_lock = _thread.allocate_lock()
enc_lock = _thread.allocate_lock()
encoder_val = 0



### TEST  LIGHTS ###
top_green = PWM(Pin(3))
top_yellow = PWM(Pin(5))
top_red = PWM(Pin(8))

bottom_green = PWM(Pin(10))
bottom_yellow = PWM(Pin(13))
bottom_red = PWM(Pin(15))



LED_list = [top_green, top_yellow, top_red, bottom_green, bottom_yellow, bottom_red]

for light in LED_list:
    light.freq(2000)
    
duty_cycle = 65535
### _____________________ ###

def update_encoder_value(new_val):
    pass
    #if(enc_lock.acquire()):
    #    encoder_val = new_val
    #    enc_lock.release()

def get_encoder_value():
    if(enc_lock.acquire()):
        temp = encoder_val
        enc_lock.release()
        return temp
        

def set_set_point(new_set_point):
    print("set attempting to acquire!")
    if(a_lock.acquire()):
        print("set acquired!")
        global set_point
        set_point = new_set_point
        print(f"Set point is now {set_point}")
        a_lock.release()
        print("set released!")

def get_set_point():
    cur_set_point = 0
    print("get attempting to acquire!")
    if(a_lock.acquire(True, 0.1)):
        print("get acquire!")
        global set_point
        cur_set_point = set_point
        a_lock.release()
        print("get release!")
        return cur_set_point
    else:
        return None


def updateMotorValues():

        goal = set_point#get_set_point()
        cur_pos = get_encoder_value()
        motor_power = (goal - cur_pos) / 100 + 0.1
        setMotor(motor_power)
        print(f"Setpoint: {goal} Encoder Value: {cur_pos} Error: {goal - cur_pos} Motor Power: {motor_power}")
        
    
def updateMotorValuesThread():
    print("Starting thread")
    count = 0
    while not program_finished:
        #updateMotorValues()
        count = count + 1
        print(f"I'm running! {count}")
        print(get_encoder_value())
        '''
        goal = set_point#get_set_point()
        print(goal, type(goal))
        if (goal is not None):
            setMotor((goal - Qtr_Cntr) / 700)
            print(goal, Qtr_Cntr, (goal - Qtr_Cntr) / 700)
        else:
            print("None!!")'''
        utime.sleep(0.02)
        gc.collect()
    setMotor(0.0)
    print("Thread tired, I'm done now")




def Enc_Handler(Source):
    global Enc_Counter
    global Qtr_Cntr
    global Enc_A_State
    global Enc_A_State_old
    global Enc_B_State
    global Enc_B_State_old
    global error
    #s = str(Source)  #useful for debugging and setup to see which pin triggered interupt
    #print(s[4:6])
        
    Enc_A_State = Enc_Pin_A.value()  #Capture the current state of both A and B
    Enc_B_State = Enc_Pin_B.value()
    if Enc_A_State == Enc_A_State_old and Enc_B_State == Enc_B_State_old:  #Probably 'bounce" as there was a trigger but no change
        error += 1  #add the error event to a variable - may by useful in debugging
    elif (Enc_A_State == 1 and Enc_B_State_old == 0) or (Enc_A_State == 0 and Enc_B_State_old == 1):
        # this will be clockwise rotation
        # A   B-old
        # 1 & 0 = CW rotation
        # 0 & 1 = CW rotation
        Enc_Counter += 1  #Increment counter by 1 - counts ALL transitions
        Qtr_Cntr = round(Enc_Counter/4)  #Calculate a new 1/4 counter value
        update_encoder_value(Qtr_Cntr)
    elif (Enc_A_State == 1 and Enc_B_State_old == 1) or (Enc_A_State == 0 and Enc_B_State_old == 0):
        # this will be counter-clockwise rotation
        # A   B-old
        # 1 & 1 = CCW rotation
        # 0 & 0 = CCW rotation
        Enc_Counter -= 1 # Decrement counter by 1 - counts ALL transitions
        Qtr_Cntr = round(Enc_Counter/4)  #Calculate a new 1/4 counter value
        update_encoder_value(Qtr_Cntr)
    else:  #if here, there is a combination we don't care about, ignore it, but track it for debugging
        error += 1
    Enc_A_State_old = Enc_A_State     # store the current encoder values as old values to be used as comparison in the next loop
    Enc_B_State_old = Enc_B_State       


#Configure the A channel and B channel pins and their associated interrupt handing
Enc_Pin_A = machine.Pin(20,machine.Pin.IN,machine.Pin.PULL_DOWN)
Enc_Pin_A.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=Enc_Handler)
Enc_Pin_B = machine.Pin(19,machine.Pin.IN,machine.Pin.PULL_DOWN)
Enc_Pin_B.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=Enc_Handler)

#Preset some variables to useful and known values
Enc_A_State_old = Enc_Pin_A.value()
Enc_B_State_old = Enc_Pin_B.value()
last_Enc_Counter = 0
Enc_Counter = 0
Last_Qtr_Cntr = 0
Qtr_Cntr = 0
error = 0



def connect(wifi: dict) -> str:
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("WLAN Active:",wlan.active())
    ssid = wifi.get("ssid")
    password = wifi.get("password")
    print(f"Attempting to connect on {ssid}")
    wlan.connect(ssid, password)
    count = 0
    while wlan.isconnected() == False:
        print('Waiting for connection...' + str(count))
        sleep(1)
        pico_led.toggle()
        count = count + 1
    ip = wlan.ifconfig()[0]
    #wlan.ifconfig(('192.168.1.3', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
    #ip = ('192.168.1.3', '255.255.255.0', '192.168.1.1', '8.8.8.8')[0]
    print(f'Connected on {ip} on {ssid}')
    #ipv4 =  ipaddress.IPv4Address("192.168.1.42")
    #netmask =  ipaddress.IPv4Address("255.255.255.0")
    #gateway =  ipaddress.IPv4Address("192.168.1.1")
    #wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)
    for i in range(10):
        pico_led.toggle()
        sleep(0.1)
    pico_led.off()
    return ip;

def connect_client():
    print(f"Trying to connect to {ADDR}")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
    except Exception as e:
        print(f"An exception occured: {e}")
    print("connected!")
    server_poll = select.poll()
    server_poll.register(client)

    while(True):    
        poll_results = server_poll.poll(100)[0]
        if (poll_results[1] == 5):
            msg_full = client.recv(2048).decode()
            msg = msg_full.split(",")
            if not DISCONNECT_MESSAGE in msg:
                print(msg)
            else:
                break
        else:
            pass 
    send(client, DISCONNECT_MESSAGE)
    utime.sleep(1)
    client.close()    
        
    
    
def send(client, msg):
    LED_list[3].duty_u16(duty_cycle)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    received_msg = client.recv(2048).decode()
    print(received_msg)
    if (msg == "GetPosition"):
        print(received_msg, Qtr_Cntr, float(received_msg) - Qtr_Cntr)
        set_set_point(float(received_msg))
        """
        for i in range(20):
            updateMotorValues()
            utime.sleep(0.02)"""
    LED_list[3].duty_u16(0)
    



def end_program(val):
    #print(program_running)
    print("Ending program!")
    global program_running
    program_running = False
    print(program_running)
    #sys.exit()
        
end_program_button = Button(18)

def setMotor(motorPower):
    #print(f"setting motor to: {motorPower}")
    if (motorPower > 0.4): motorPower = 0.4
    if (motorPower < -0.30): motorPower = -0.30
    
    max_duty_cycle_length = 65025
    freq = 50;
    one_mill_pulse_duration = max_duty_cycle_length / (1000/freq)
    duty_length = (1.5 + motorPower/2) * one_mill_pulse_duration
    motor1.duty_u16(int(duty_length))



#end_program_button.when_pressed = end_program("test")

try:
    #thread1 = _thread.start_new_thread(updateMotorValuesThread, ())
    
    ip = connect(dance_router)
    
    print(type(ip))
    connect_client()
    setMotor(0.0)
    
    program_finished = True
    
    utime.sleep(0.2)
    print("Goodnight all!")
    
    #connection = open_socket(ip)
    #serve(connection)
except KeyboardInterrupt:
    machine.reset()
    
