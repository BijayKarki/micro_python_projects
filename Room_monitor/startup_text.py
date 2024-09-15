from machine import Pin, I2C
import sh1106
from time import sleep

# Initialize I2C
i2c = I2C(1, scl=Pin(15), sda=Pin(14))

# Initialize the OLED display
oled_width = 128
oled_height = 64
oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c, rotate=180)

oled.invert(False)
oled.contrast = int(10)  # 0 - 255 contrast

# Start up LED and text message
text1 = "WELCOME TO"
text2 = "Indoor weather"
text3 = "Monitoring"

def animate_text():

    # Display the first line (static)
    oled.text(text1, 24, 0)
    oled.show()

    # Start positions for text2 and text3
    text2_pos = 130  # Start from the right for text2 (left to right)
    text3_pos = -130  # Start from the left for text3 (right to left)

    # Run both animations in the same loop until they align at x = 0
    while text2_pos > 0 or text3_pos < 0:
        # Clear the previous text at line 15 and line 25
        oled.fill_rect(0, 15, oled_width, 10, 0)  # Clear line 15
        oled.fill_rect(0, 25, oled_width, 10, 0)  # Clear line 25

        # Update text2 (line 15) if still animating
        if text2_pos > 0:
            oled.text(text2, text2_pos, 15)
            text2_pos -= 1  # Move left (left to right)

        # Update text3 (line 25) if still animating
        if text3_pos < 0:
            oled.text(text3, text3_pos, 25)
            text3_pos += 1  # Move right (right to left)

        # Show updated screen
        oled.show()
        sleep(0.01)  # Adjust speed if needed

    # After the loop, align both texts at x = 0
    oled.fill_rect(0, 15, oled_width, 10, 0)  # Clear line 15
    oled.fill_rect(0, 25, oled_width, 10, 0)  # Clear line 25

    oled.text(text2, 0, 15)  # Align text2 at x = 0
    oled.text(text3, 0, 25)  # Align text3 at x = 0
    oled.show()
    sleep(3)
    
if __name__ == "__main__":
    animate_text()

