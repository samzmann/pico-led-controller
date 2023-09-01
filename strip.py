from machine import Pin
from neopixel import Neopixel
import math

NUM_LEDS = 12
STATE_MACHINE = 0
STRIP_PIN = 5

NEOPIXEL_MIN_H = 0
NEOPIXEL_MAX_H = 65535

NEOPIXEL_MIN_S = 0
NEOPIXEL_MAX_S = 255

NEOPIXEL_MIN_V = 0
NEOPIXEL_MAX_V = 255

MIN_HUE = 0
MAX_HUE = 65535

strip = Neopixel(
    NUM_LEDS,
    STATE_MACHINE,
    STRIP_PIN,
    "GRB"
)

strip.brightness(255)
strip.fill((255,255,255))

def normalize(currentValue, minValue, maxValue):
    return math.floor((currentValue - minValue) / (maxValue - minValue))

def updateStrip(h, s, v):
    print('updateStrip')
    
#     nH = normalize(h, NEOPIXEL_MIN_H, NEOPIXEL_MAX_H),
#     nS = normalize(s, NEOPIXEL_MIN_S, NEOPIXEL_MAX_S),
#     nV = normalize(v, NEOPIXEL_MIN_V, NEOPIXEL_MAX_V)
    
    print('updateStrip', h, s, v)
    
    strip.fill(strip.colorHSV(h, s, v))
    strip.show()
    
    