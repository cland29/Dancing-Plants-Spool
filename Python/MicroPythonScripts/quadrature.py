# SPDX-FileCopyrightText: 2022 Jamon Terrell <github@jamonterrell.com>
# SPDX-License-Identifier: MIT

from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
import utime
@asm_pio(autopush=True, push_thresh=32)
def pio_quadrature_encoder():
    label("start")
    wait(0, pin, 0)         # Wait for CLK to go low
    jmp(pin, "WAIT_HIGH")   # if Data is low
    mov(x, invert(x))           # Increment X
    jmp(x_dec, "nop1")
    label("nop1")
    mov(x, invert(x))
    label("WAIT_HIGH")      # else
    jmp(x_dec, "nop2")          # Decrement X
    label("nop2")
    
    wait(1, pin, 0)         # Wait for CLK to go high
    jmp(pin, "WAIT_LOW")    # if Data is low
    jmp(x_dec, "nop3")          # Decrement X
    label("nop3")
    
    label("WAIT_LOW")       # else
    mov(x, invert(x))           # Increment X
    jmp(x_dec, "nop4")
    label("nop4")
    mov(x, invert(x))
    wrap()

class quadrature_encoder():
    
    def __init__(self, pin_a: int, pin_b: int):
        self.sm1 = StateMachine(1, pio_quadrature_encoder, freq=125_000_000, in_base=Pin(pin_a), jmp_pin=Pin(pin_b))
        self.sm1.active(1)
        self.invert = False
    
    def get_raw_pos(self):
        self.sm1.exec("in_(x, 32)")
        raw_pos = self.sm1.get()
        if not self.invert:
            return raw_pos
        else:
            return -raw_pos
        
    def get_pos(self):
        #This code prevents wrap around where, instead of giving a negative pos, it returns 2**32
        pos = self.get_raw_pos()
        if pos > 2**31:
            return pos - 2**32
        elif pos < -2**31:
            return pos + 2**32
        else:
            return pos
    
    def set_invert(self, is_invert: bool):
        self.invert = is_invert
    
    
if __name__ == "__main__":
    encoder = quadrature_encoder(20, 19)
    encoder.set_invert(False)

    while(True):
        utime.sleep(1)
        print(encoder.get_pos())
