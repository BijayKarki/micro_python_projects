from time import sleep
from set_time import get_Finnish_time

# Text constants
TEXT1 = "WELCOME TO"
TEXT2 = "Project: Weather"
TEXT3 = ""

def scene_first(oled, oled_width):
    """Display startup welcome animation"""
    oled.text(TEXT1, 24, 0)
    oled.show()

    text2_pos = 130
    text3_pos = -130

    while text2_pos > 0 or text3_pos < 0:
        oled.fill_rect(0, 15, oled_width, 10, 0)
        oled.fill_rect(0, 25, oled_width, 10, 0)

        if text2_pos > 0:
            oled.text(TEXT2, text2_pos, 15)
            text2_pos -= 1

        if text3_pos < 0:
            oled.text(TEXT3, text3_pos, 25)
            text3_pos += 1

        oled.show()
        sleep(0.01)

    oled.fill_rect(0, 15, oled_width, 10, 0)
    oled.fill_rect(0, 25, oled_width, 10, 0)
    oled.text(TEXT2, 0, 15)
    oled.text(TEXT3, 0, 25)
    oled.show()
    sleep(3)

def scene_second(oled):
    """Simple startup message animation"""
    oled.fill(0)
    oled.text("Measurement", 0, 0)
    oled.text("Starting", 0, 15)
    oled.show()

    for i in range(10):
        oled.text(".", 65 + i*7, 15)
        oled.show()
        sleep(0.2)
    oled.fill(0)

def scene_interrupt(oled):
    oled.fill(0)
    oled.text("Terminating", 0, 0)
    oled.text("See you again!", 0, 20)
    oled.show()
    sleep(2)
    oled.fill(0)

def clear_line(oled, y, length):
    """Clear a line of text at specific y-coordinate"""
    oled.fill_rect(0, y, length, 8, 0)

def draw_table(oled, oled_width):
    """Draw table lines for weather data"""
    h_line = 12
    oled.hline(0, 0, oled_width, 1)
    oled.hline(0, h_line, oled_width, 1)
    oled.hline(0, h_line*2, oled_width, 1)
    oled.hline(0, h_line*3, oled_width, 1)
    oled.hline(0, h_line*4, oled_width, 1)

    v1, v2, v3 = 0, 35, 73
    oled.vline(v1, 0,h_line*4, 1)
    oled.vline(v2, 0, h_line*4, 1)
    oled.vline(v3, 0, h_line*4, 1)

def display_weather(oled, oled_width, room_temp, room_humidity, out_temp, out_humidity, wind_speed, weekday):
    """Display weather data in table"""
    oled.fill(0)
    oled.text(weekday, 2, 3)
    oled.text("Room", 37, 3)
    oled.text("Outdoor", 75, 3)

    clear_line(oled, 16, oled_width)
    oled.text("Temp", 2, 15)
    oled.text(f"{room_temp} C", 40, 15)
    oled.text(f"{out_temp} C", 80, 15)

    clear_line(oled, 27, oled_width)
    oled.text("RH", 2, 27)
    oled.text(f"{room_humidity}%", 40, 27)
    oled.text(f"{out_humidity}%", 80, 27)

    clear_line(oled, 39, oled_width)
    oled.text("Wind", 2, 39)
    oled.text("--", 40, 39)
    oled.text(f"{wind_speed} km/h", 80, 39)

    draw_table(oled, oled_width)
    oled.show()

def display_weather_n_time(oled, oled_width, room_temp, room_humidity, out_temp, out_humidity, wind_speed):
    """Display weather data along with current time and date"""
    current_time = get_Finnish_time()
    hour, minute = current_time[3:5]
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][current_time[6]]
    time_str = "{:02d}:{:02d}".format(hour, minute)
    date_str = "{:04d}.{:02d}.{:02d}".format(current_time[0], current_time[1], current_time[2])

    oled.fill(0)
    display_weather(oled, oled_width, room_temp, room_humidity, out_temp, out_humidity, wind_speed, weekday)
    oled.text(f"{time_str},{date_str}", 0, 54)
    oled.show()

