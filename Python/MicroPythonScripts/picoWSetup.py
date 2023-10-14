import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led, Button
import machine
from machine import PWM, Pin
import sys
#import ipaddress
#import wifi

ssid = 'NETGEAR80'
password = 'yellowwater460'
home_router = {"ssid": 'Linksys03016', 'password': 'q21ruweiq3'}
#ssid = home_router.get("ssid")
#password = home_router.get("password")
program_running = True

motor1 = machine.PWM(Pin(1))
motor1.freq(50)

top_green = PWM(Pin(3))
top_yellow = PWM(Pin(5))
top_red = PWM(Pin(8))

bottom_green = PWM(Pin(10))
bottom_yellow = PWM(Pin(13))
bottom_red = PWM(Pin(15))



LED_list = [top_green, top_yellow, top_red, bottom_green, bottom_yellow, bottom_red]


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
    elif (Enc_A_State == 1 and Enc_B_State_old == 1) or (Enc_A_State == 0 and Enc_B_State_old == 0):
        # this will be counter-clockwise rotation
        # A   B-old
        # 1 & 1 = CCW rotation
        # 0 & 0 = CCW rotation
        Enc_Counter -= 1 # Decrement counter by 1 - counts ALL transitions
        Qtr_Cntr = round(Enc_Counter/4)  #Calculate a new 1/4 counter value
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







for light in LED_list:
    light.freq(2000)





def connect() -> str:
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("WLAN Active:",wlan.active())
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
    print(f'Connected on {ip}')
    #ipv4 =  ipaddress.IPv4Address("192.168.1.42")
    #netmask =  ipaddress.IPv4Address("255.255.255.0")
    #gateway =  ipaddress.IPv4Address("192.168.1.1")
    #wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)
    for i in range(10):
        pico_led.toggle()
        sleep(0.1)
    pico_led.off()
    LED_list[0].duty_u16(65535)
    return ip;

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    
    #Added below line to not accidentally leave a socket open
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, encoder_value, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <form action="./motorUp">
            <input type="submit" value="Move Motor Up" />
            </form>
            <form action="./motorDown">
            <input type="submit" value="Move Motor Down" />
            </form>
            <form action="./LowerPosition">
            <input type="submit" value="Lower the connector" />
            </form>
            <form action="./motorStop">
            <input type="submit" value="Stop Motor" />
            </form>
            <form action="./endprog">
            <input type="submit" value="End Program" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            <p>Encoder Value is {encoder_value}</p>
            </body>
            </html>
            """
    return str(html)

def end_webpage():
    html = f"""
            <!DOCTYPE html>
            <html>
            <body align="center" vertical-align='center' line-height=400px height=400px>
            <h3>This may be the end, but never stop</h3>
            
            <div class="rainbow-text" style="text-align: center;">
            <h1>
            <span class="block-line"><span><span style="color:#ff0000;">D</span><span style="color:#ff4000;">a</span><span style="color:#ff7b00;">y</span><span style="color:#ffbb00;">d</span><span style="color:#fff700;">r</span><span style="color:#ccff00;">e</span><span style="color:#8cff00;">a</span><span style="color:#51ff00;">m</span><span style="color:#11ff00;">i</span><span style="color:#00ff2b;">n</span><span style="color:#00ff6a;">g&nbsp;</span></span><span><span style="color:#00ffa6;">i</span><span style="color:#00ffe1;">n&nbsp;</span></span><span><span style="color:#00ddff;">A</span><span style="color:#00a1ff;">l</span><span style="color:#0062ff;">l&nbsp;</span></span><span><span style="color:#0026ff;">L</span><span style="color:#1500ff;">a</span><span style="color:#5500ff;">n</span><span style="color:#9000ff;">g</span><span style="color:#cc00ff;">u</span><span style="color:#ff00f2;">a</span><span style="color:#ff00b7;">g</span><span style="color:#ff0077;">e</span><span style="color:#ff003b;">s</span></span></span>
            </h1>
            </div>
            
            
            <p>Love you future Carl!</p>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = "ON"
        elif request =='/lightoff?':
            pico_led.off()
            state = "OFF"
        elif request == '/motorUp?':
            setMotor(0.30)
        elif request == '/motorDown?':
            setMotor(-0.15)
        elif request == '/motorStop?':
            setMotor(0.0)
        elif request == '/endprog?':
            break
            
        temperature = pico_temp_sensor.temp
        encoder_val = Qtr_Cntr
        html = webpage(temperature, encoder_val, state)
        client.send(html)
        client.close()
    print("Ending Socket Connection: " + str(connection))
    #print(end_program)
    #connection.shutdown(socket.SHUT_RDWR)
    html = end_webpage()
    client.send(html)
    client.close()
    connection.close()

def end_program(val):
    #print(program_running)
    print("Ending program!")
    global program_running
    program_running = False
    print(program_running)
    #sys.exit()
        
end_program_button = Button(18)

def setMotor(motorPower):
    if (motorPower > 0.5): motorPower = 0.5
    if (motorPower < -0.5): motorPower = -0.5
    
    max_duty_cycle_length = 65025
    freq = 50;
    one_mill_pulse_duration = max_duty_cycle_length / (1000/freq)
    duty_length = (1.5 + motorPower/2) * one_mill_pulse_duration
    motor1.duty_u16(int(duty_length))



#end_program_button.when_pressed = end_program("test")

try:
    ip = connect()
    print(type(ip))
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
    