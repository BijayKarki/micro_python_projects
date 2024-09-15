from machine import Pin
import neopixel
from time import sleep

# Number of LEDs
num_leds = 1

# Initialize neopixel on GPIO 16
np = neopixel.NeoPixel(Pin(16), num_leds)
brightness = 0.05


def set_color(red, green, blue):
    # Apply brightness to each color component
    red = int(red * brightness)
    green = int(green * brightness)
    blue = int(blue * brightness)
    np[0] = (red, green, blue)
    np.write()


if __name__ == "__main__":
    
    # Color codes
    V = (148, 0, 211)    # Violet
    I = (75, 0, 130)     # Indigo
    B = (0, 0, 255)      # Blue
    G = (0, 255, 0)      # Green
    Y = (255, 255, 0)    # Yellow
    O = (255, 127, 0)    # Orange
    R = (255, 0, 0)      # Red
    W = (255, 255, 255)  # White
    led_off = (0, 0, 0)


    rainbow = [V, I, B, G, Y, O, R]
    try:
        while True:
            for color in rainbow:
                print(*color)
                set_color(*color)
                sleep(.5)     
        
    except KeyboardInterrupt:
        print("program terminated")
        for i in range(3):
            set_color(*W)
            sleep(0.5)
            set_color(*led_off)
            sleep(0.5)