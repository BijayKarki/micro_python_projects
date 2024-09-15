from machine import Pin, I2C
from time import sleep
import sh1106

from DHT11_sensor import get_data
from startup_text import animate_text
from RGB_led import set_color

#### color codes
V = (148, 0, 211)     # violet
I = (75, 0, 130)      # Indigo
B = (0, 0, 255)       # Blue
G = (0, 255, 0)       # Green
Y = (255, 255, 0)     # Yellow
O = (255, 127, 0)     # Orange
R = (255, 0, 0)       # Red
W = (255, 255, 255)   # White
led_off = (0, 0, 0)
led_color = [V, I, B, G, Y, O, R, W]

# blinking Red LED to indicate pico is up running the main.py
for i in range(5):
    set_color(*R)
    sleep(.2)
    set_color(*led_off)
    sleep(.2)


# DHT sensor is connected to Pin 7
DHT_sensor = 7

# Initialize I2C
i2c = I2C(1, scl=Pin(15), sda=Pin(14))

# Initialize the OLED display
oled_width = 128
oled_height = 64
oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c, rotate=180)

oled.invert(False)
oled.contrast = int(10)  # 0 - 255 contrast 

greet = "Hello Bijay!"
terminate = "Bye bye"




# Start up message
animate_text()

# LED blinking + mock animation
oled.fill(0)
text1 = "Measurement"
text2 = "Starting" 
oled.text(text1, 0, 0)
oled.text(text2, 0, 15)
oled.show()

for i in range(len(led_color)):
    oled.text(".", (65 + (i*7)), 15)
    set_color(*led_color[i])
    oled.show()
    sleep(.45)
    set_color(*led_off)


def clear_line(y, length):
    """Clear a line of text at a specific y-coordinate"""
    oled.fill_rect(0, y, length, 2, 0)  # Adjust height (8) based on font size

try:
    while True:
        data = get_data(DHT_sensor)
        
        if isinstance(data, dict):
            # Clear the display
            oled.poweron()
            oled.fill(0)

            # Write static text
            oled.text(greet, 0, 0)

            # Clear and update the line for temperature and humidity
            clear_line(20, oled_width)  # Clear the area for temperature
            oled.text(f'Room temp:{data["temperature"]} degree', 0, 20)

            clear_line(40, oled_width)  # Clear the area for humidity
            oled.text(f'Humidity :{data["humidity"]} %', 0, 40)

            oled.show()
            sleep(2)
            #oled.poweroff()
            sleep(3)

        else:
            oled.fill(0)
            oled.text(greet, 0, 0)
            oled.text("Error", 0, 20)
            oled.show()

except KeyboardInterrupt:
    
    oled.fill(0)
    oled.text(terminate, 0, 0)
    oled.text("See you again!", 0, 20)
    oled.show()
    
    for i in range(3):
        set_color(*W)
        sleep(0.2)
        set_color(*led_off)
        sleep(0.2)

    oled.poweroff()