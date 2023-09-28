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
program_running = True

motor1 = machine.PWM(Pin(7))
motor1.freq(50)

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

def webpage(temperature, state):
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
            <form action="./motorStop">
            <input type="submit" value="Stop Motor" />
            </form>
            <form action="./endprog">
            <input type="submit" value="End Program" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
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
            setMotor(0.25)
        elif request == '/motorDown?':
            setMotor(-0.25)
        elif request == '/motorStop?':
            setMotor(0.0)
        elif request == '/endprog?':
            break
            
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
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
    if (motorPower > 0.25): motorPower = 0.25
    if (motorPower < -0.25): motorPower = -0.25
    
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
    