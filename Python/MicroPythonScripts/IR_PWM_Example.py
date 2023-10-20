import machine

# Get the PWM object for the specified pin
pwm = machine.PWM(machine.Pin(12))

# Set the PWM frequency
pwm.freq(38000)

# Set the PWM duty cycle
#pwm.duty_cycle(50)

# Read the PWM value
while True:
    value = pwm.value()
    print(value)