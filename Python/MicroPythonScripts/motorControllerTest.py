import machine
from machine import PWM, Pin
import utime

motor1 = machine.PWM(Pin(1))
motor1.freq(50)

def setMotor(motorPower):
    if (motorPower > 0.5): motorPower = 0.5
    if (motorPower < -0.5): motorPower = -0.5
    
    max_duty_cycle_length = 65025
    freq = 50;
    one_mill_pulse_duration = max_duty_cycle_length / (1000/freq)
    duty_length = (1.5 + motorPower/2) * one_mill_pulse_duration
    motor1.duty_u16(int(duty_length))
    
while True:
    print("cycle!")
    setMotor(0.0)
    utime.sleep_ms(1000)
    setMotor(0.9)
    utime.sleep_ms(1000)
    setMotor(-0.9)
    utime.sleep_ms(1000)