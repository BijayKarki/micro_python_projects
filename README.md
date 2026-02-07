# Mini weather station

This is the fourth iteration of the project.
This implementation continues the use of ESP32-S3 board (MicroPython) along with AHT21 sensor instead of DHT11.
The WiFi connection capability of the board features real time tracker and API call for outdoor weather information.
The data gathered is pushed to ThingSpeak for visualization and further acccess.

## Components used

1. ESP32-S3 board
2. AHT21 (temp and humidity) sensor
3. 1.3 inch OLED display
4. Breadboard and Jumper wires
5. A toggle switch (to turn the OLED display ON/OFF)

## Tech stack:

1. ntptime
2. <a href="https://github.com/robert-hh/SH1106/blob/master/readme.md"> SH1106 </a> (For 1.3" OLED display)
3. <a href="https://thingspeak.mathworks.com/"> ThingSpeak </a>
4. <a href="https://mqtt.org/"> MQTT </a>

## Features

1. Real time tracker
2. Outdoor weather information
3. ThingSpeak <a href=https://thingspeak.mathworks.com/channels/3024639> dashboard </a>
4. Data integration to Home Assistant dashboard
   - Via Thingspeak (yaml config; platform: rest, every 15 mins)
   - MQTT (sensor data every 30 secs)
5. The OLED display set to automatically turn OFF during the night hours (22:00 - 06:00)
   - The button press will revive the screen for 10 sec (by default) before turning OFF.
   - The button can also be used to manually turn OFF before 10 sec interval

## Problems encountered

| Sn. | Problem                                   | Cause                                           | Solution opted                                        |
| --- | :---------------------------------------- | :---------------------------------------------- | :---------------------------------------------------- |
| 1   | The switch does not respond sometimes     | Basic setup: just an internal pull up resistor  | Interrupt handler switch implemented                  |
| 2   | Outdoor data is not updated instantly     | Algorithm needs some minor revisions            | Algorithm changed to update the new data accordingly  |
| 3   | Conflict between I2C bus (OLED and AHT21) | Earlier programming logic for only 1 I2C device | Edited the code and logic for both I2C initialization |
| 4   | MQTT does not reconnect once dropped      | `mqtt` value was true even after disconnected| Added a module to handle reconnection when nedded     |

## Future work

1. 1 line I2C bus (unlike current implementation)
2. ~~MQTT for data exchange between other devices in LAN~~.
3. More GUI options for the OLED ?

## Aditional info for ESP32 setup

- `ssd1306` library does not support 1.3 inch OLED display. This <a href="https://github.com/robert-hh/SH1106/blob/master/readme.md"> documentation </a> offers the solution.

- <a href="https://docs.micropython.org/en/latest/esp32/tutorial/intro.html"> Documentation </a> for flashing MicroPython firmware to ESP32 boards.

- Note: If the board is a clone, please flash at "0x00" not "0x10000".
  <a href="https://github.com/orgs/micropython/discussions/10206"> Discussion </a>

- Unlike RPi PICO, ESP32 board offers I2C (sda, scl) in most of the GPIOs.

## Functional Setup

<p align="center"> <img align="center" height = 500, src="./docs/ESP32-S3-AHT21.jpeg"/> </p>
