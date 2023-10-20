from machine import PWM, Pin
import utime

top_green = PWM(Pin(3))
top_yellow = PWM(Pin(5))
top_red = PWM(Pin(8))

bottom_green = PWM(Pin(10))
bottom_yellow = PWM(Pin(13))
bottom_red = PWM(Pin(15))



LED_list = [top_green, top_yellow, top_red, bottom_green, bottom_yellow, bottom_red]

for light in LED_list:
    light.freq(2000)

if __name__ == "__main__":
    while True:
        print("testing!")
        duty_cycle = 65535
        
        for i in range(len(LED_list) + 1):
            if not (i == 0):
                LED_list[i - 1].duty_u16(0)
            if not (i == len(LED_list)):
                LED_list[i].duty_u16(duty_cycle)
            utime.sleep_ms(100)
            