from machine import Pin, I2C
from DHT11_sensor import get_data
from time import sleep
import sh1106

DHT_sensor = 7

# Initialize I2C
i2c = I2C(1, scl=Pin(15), sda=Pin(14))

# Initialize the OLED display
oled_width = 128
oled_height = 64
oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c, rotate=180)

oled.invert(False)
oled.contrast = int(255 * .01)  # 20% contrast 

greet = "Hello Bijay"
terminate = "Bye bye"

def clear_line(y, length):
    """Clear a line of text at a specific y-coordinate"""
    oled.fill_rect(0, y, length, 8, 0)  # Adjust height (8) based on font size

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
            sleep(5)

        else:
            oled.fill(0)
            oled.text(greet, 0, 0)
            oled.text("Error", 0, 20)
            oled.show()

except KeyboardInterrupt:
    oled.poweron()
    oled.fill(0)
    oled.text(terminate, 0, 0)
    oled.text("See you again!", 0, 20)
    oled.show()
    sleep(3)
    oled.poweroff()