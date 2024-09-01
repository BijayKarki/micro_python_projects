# Indoor temperature and humidity

Outdoor weather info is easily available via various apps and online weather data portabls but how about indoor weather conditions?

My desire to know the room temperature inspired me to take on this project. For simplicity and ease a display was added to read through the data. This is a very basic project where data is read from the sensor and the corresponding reading is displayed on the screen.

## Components used

1. RaspberryPi Pico Zero
2. DHT11 (temperature and humidity) sensor
3. 1.3 inch OLED display

## Future updates

1. Real time tracking (but requires different micro controller or a hardware setup)
2. Time based features (turning display off during night)
3. 12 hour display (a line/bar chart )
4. Various LED indicators for running the setup independently.
5. Enhancing battery efficiency.

## Aditional info

Normal ssd1306 library does not support 1.3 inch OLED display. Hence, sh1106 library was used instead. The following documentation was used as a reference.

    https://github.com/robert-hh/SH1106/blob/master/readme.md


#
![IMG_5573](https://github.com/user-attachments/assets/03bca2ae-bb8f-4d51-a7ea-0c895c9da09b)
