from machine import Pin
import utime

from strip import updateStrip

CLK_PIN = Pin(0, Pin.IN, Pin.PULL_UP)
DT_PIN = Pin(1, Pin.IN, Pin.PULL_UP)
SW_PIN = Pin(2, Pin.IN, Pin.PULL_UP)

prevVal = CLK_PIN.value()

last5Ticks = [0]

SLOW_INCREMENT = 1
FAST_INCREMENT = 10
FAST_INCREMENT_CUTOFF = 100

def addTickTimestamp(newTimestamp):
    last5Ticks.append(newTimestamp)
    if len(last5Ticks) > 5:
        last5Ticks.pop(0)        


def avgTimeBetweenLast5Ticks():
    diffs = []
    
    for i, e in enumerate(last5Ticks):
        for j, f in enumerate(last5Ticks):
            if i != j: diffs.append(abs(e-f))
          
    if len(diffs) == 0:
        return 1000
    else:
        return sum(diffs)/len(diffs)
    

MIN_HUE = 0
MAX_HUE = 65535

MIN_SATURATION = 0
MAX_SATURATION = 255

MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 255

hue = 40 # warm yellow
saturation = MAX_SATURATION
brightness = MAX_BRIGHTNESS
counter = 0

currentMode = "hue" # or "saturation" or "brightness"

def changeMode():
    global currentMode
    
    if currentMode == "hue":
        currentMode = "saturation"
    elif currentMode == "saturation":
        currentMode = "brightness"
    elif currentMode == "brightness":
        currentMode = "hue"
    
    print('currentMode',currentMode)
    
def wrap(currentValue, increment, minValue, maxValue):
    return (currentValue + increment - minValue) % (maxValue - minValue) + minValue

def clamp(currentValue, minValue, maxValue):
    return max(minValue, min(currentValue, maxValue))
    
def incrementHue(increment):
    global hue
    hue = wrap(hue, increment * 100, MIN_HUE, MAX_HUE)
    print('hue', hue)
    
def incrementSaturation(increment):
    global saturation
    saturation = clamp(saturation + increment, MIN_SATURATION, MAX_SATURATION)
    print('saturation', saturation)
    
def incrementBrightness(increment):
    global brightness
    brightness = clamp(brightness + increment, MIN_BRIGHTNESS, MAX_BRIGHTNESS)
    print('brightness', brightness)
    
def updateCounterForMode(increment):
    if currentMode == 'hue':
        return incrementHue(increment)
    if currentMode == 'saturation':
        return incrementSaturation(increment)
    if currentMode == 'brightness':
        return incrementBrightness(increment)

def rotaryChanged():
    global prevVal
    
    val = CLK_PIN.value()
    
    
    if val != prevVal:
        addTickTimestamp(utime.ticks_ms())
        print('avgTimeBetweenLast5Ticks', avgTimeBetweenLast5Ticks())
        
        increment = SLOW_INCREMENT
        if avgTimeBetweenLast5Ticks() < FAST_INCREMENT_CUTOFF:
            increment = FAST_INCREMENT
        
        if DT_PIN.value() == val:
            increment = -increment
            print("anti-clockwise", counter)
        else:
            print("clockwise", counter)
            
        updateCounterForMode(increment)
        updateStrip(hue, saturation, brightness)
            
        prevVal = val

    if SW_PIN.value() == 0:
        changeMode()
        utime.sleep_ms(200)
        
while True:
    rotaryChanged()
        
