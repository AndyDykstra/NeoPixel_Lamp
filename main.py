    """
A CircuitPython LED Lamp with animations
Uses a Trinket M0 + Rotary Encoder with neopixel ring
"""
 
import time
from digitalio import *
from board import *
import neopixel

# multiplier for LEDs, too high and it will draw too much power
ANIMATION_INTENSITY = .25

animationIndex = 0
animationColorIndex = 0
animationColors = [[255,0,0],[170,85,0],[85,170,0],[0,255,0],[0,170,85],[0,85,170],[0,0,255],[85,0,170],[170,0,85]]

# NeoPixel LED ring on pin D1
neoRing = neopixel.NeoPixel(D1, 16, brightness=ANIMATION_INTENSITY)

# Encoder button is a digital input with pullup on D2
button = DigitalInOut(D2)
button.direction = Direction.INPUT
button.pull = Pull.UP

# Rotary encoder inputs with pullup on D3 & D4
dialA = DigitalInOut(D3)
dialA.direction = Direction.INPUT
dialA.pull = Pull.UP
dialB = DigitalInOut(D4)
dialB.direction = Direction.INPUT
dialB.pull = Pull.UP

######################### MAIN LOOP ##############################

# get initial/prev state and store at beginning
buttonPrevious = button.value
rotaryPrevious = [dialA.value, dialB.value]
directionChange = 0

while True:
    # reset encoder and wait for the next turn
    encoder_direction = 0

    # take a 'snapshot' of the rotary encoder state at this time
    rotaryCurrent = [dialA.value, dialB.value]

    if rotaryCurrent != rotaryPrevious: # it changed
        if rotaryPrevious == [False, False]: # both were low
            if rotaryCurrent[0]: # if output A is now low it's clockwise
                directionChange = 1
            elif rotaryCurrent[1]: # if output B is now low it's counterclockwise
                directionChange = -1
            else:
                # uhh something went deeply wrong, lets start over
                continue

    animationColorIndex += directionChange
    
    if animationColorIndex < 0:
      animationColorIndex = len(animationColors) - 1
    if animationColorIndex >= len(animationColors):
      animationColorIndex = 0

    rotaryPrevious = rotaryCurrent

    # Button was 'just pressed'
    if (not button.value) and last_button:
        animationIndex ++
        
    elif button.value and (not last_button):
        print("Button Released!")
        # kbd.press(Keycode.SHIFT, Keycode.SIX)
        # kbd.release_all()
        ring[dot_location] = DOT_COLOR      # show it was released on ring
        
    buttonPrevious = button.value

    if encoder_direction != 0:
       
        # spin neopixel LED around!
        previous_location = dot_location
        dot_location += encoder_direction   # move dot in the direction
        dot_location += len(ring)           # in case we moved negative, wrap around
        dot_location %= len(ring)
        if button.value:
            ring[dot_location] = DOT_COLOR  # turn on new dot
        else:
            ring[dot_location] = PRESSED_DOT_COLOR # turn on new dot
        ring[previous_location] = 0         # turn off previous dot

    if time.monotonic() > timestamp + LIT_TIMEOUT:
        ring[dot_location] = 0   # turn off ring light temporarily

  
