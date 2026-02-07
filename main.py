from time import sleep, time, localtime
import gc
from machine import I2C, Pin, WDT

import config
from connect_wifi import connect_wifi, is_connected
from set_time import sync_time
from aht21_sensor import AHT21B
from mqtt_connection import connect_mqtt, mqtt_status

from oled_init import init_oled
from Intro_text import (scene_first, scene_second, scene_interrupt, display_weather_n_time)
from open_weather_api import fetch_weather_data
from thingspeak import upload_to_thingspeak
from screen_control import get_screen_status


# Initialization
def initialize_system():
    
    """Initialize WiFi, time, watchdog, I2C, OLED, sensor and mqtt."""
    
    connect_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
    sleep(2)
    sync_time()

    # I2C buses
    i2c_oled = I2C(1, scl=Pin(8), sda=Pin(3))
    i2c_sensor = I2C(0, scl=Pin(5), sda=Pin(4))

    # Devices
    oled, OLED_W, OLED_H = init_oled(i2c_oled)
    sensor = AHT21B(i2c_sensor)

    print("OLED bus scan:", [hex(a) for a in i2c_oled.scan()])
    print("AHT21 bus scan:", [hex(a) for a in i2c_sensor.scan()])
    
    # MQTT
    mqtt = None
    mqtt = connect_mqtt()
        
    # Watch dog moved here to avoid any conflict with mqtt initialization 
    wdt = WDT(timeout=60000)

    return wdt, oled, OLED_W, OLED_H, sensor, mqtt
    
    
# Main loop
def main_loop():
    wdt, oled, OLED_W, OLED_H, sensor, mqtt = initialize_system()

    # Startup animation
    if get_screen_status():
        scene_first(oled, OLED_W)
        sleep(2)
        scene_second(oled)
    else:
        oled.fill(0)
        oled.show()

    # Data state
    room_temp, room_humidity = None, None
    out_temp, out_humidity, wind_speed = None, None, None

    # Timing
    last_sensor_update = 0
    last_weather_update = 0
    last_mqtt_publish = 0
    last_mqtt_attempt = 0
    last_mqtt_ping = 0

    # Screen state
    screen_was_on = True
    weather_updated = False

    while True:
        try:
            now = time()

            # Screen control (interrupt driven)
            screen_is_on = get_screen_status()

            # Sensor update (every 20 seconds)
            sensor_due = (
                last_sensor_update == 0
                or now - last_sensor_update >= 20
            )

            if sensor_due:
                try:
                    room_temp, room_humidity = sensor.read()
                    last_sensor_update = now
                except Exception as e:
                    print("[ERROR] AHT21 read failed:", e)
            
            # check MQTT every 15 secs
            if mqtt and now - last_mqtt_ping >= 15:
                mqtt = mqtt_status(mqtt)
                last_mqtt_ping = now
                
                
            # connect MQTT if connection dropped    
            if mqtt is None and is_connected() and now - last_mqtt_attempt >= 30:
                mqtt = connect_mqtt()
                last_mqtt_attempt = now
            
            
            # MQTT publish (local data if connected)
            if (
                mqtt
                and mqtt.connected
                and room_temp is not None
                and room_humidity is not None
                and (last_mqtt_publish == 0 or now - last_mqtt_publish >= config.MQTT_PUBLISH_INTERVAL)
            ):
                try:
                    mqtt.publish_state({
                        "temperature": room_temp,
                        "humidity": room_humidity,
                        "free_mem": gc.mem_free(),
                        "uptime": now
                    })
                    last_mqtt_publish = now
                except Exception as e:
                    print("[ERROR] MQTT publish failed:", e)
                    

            # Weather API update
            if last_weather_update == 0:
                # First fetch
                try:
                    if is_connected():
                        out_temp, out_humidity, wind_speed = fetch_weather_data()
                        weather_updated = True
                        #print(f"[{now}] Initial weather fetched")
                except Exception as e:
                    print("[ERROR] Initial weather fetch failed:", e)
                last_weather_update = now
            
            elif now - last_weather_update >= 900:
                # Every 15 minutes
                try:
                    if is_connected():
                        out_temp, out_humidity, wind_speed = fetch_weather_data()
                        weather_updated = True

                        upload_to_thingspeak(
                            config.THINGSPEAK_API_KEY,
                            room_temp,
                            room_humidity,
                            out_temp,
                            out_humidity,
                            wind_speed,
                            gc.mem_free()
                        )
                        print(f"[{now}] Weather update pushed to ThingSpeak")
                except Exception as e:
                    print("[ERROR] Weather/ThingSpeak failed:", e)
                last_weather_update = now
            

            # Screen refresh logic
            screen_needs_refresh = (
                screen_is_on != screen_was_on
                or (screen_is_on and sensor_due)
                or (screen_is_on and weather_updated)
            )

            if screen_is_on and screen_needs_refresh:
                display_weather_n_time(
                    oled,
                    OLED_W,
                    room_temp,
                    room_humidity,
                    out_temp,
                    out_humidity,
                    wind_speed
                )
                weather_updated = False

            elif not screen_is_on:
                oled.fill(0)
                oled.show()

            screen_was_on = screen_is_on


            # Housekeeping
            if now % 900 < 2:
                gc.collect()
                # print(f"[{now}] GC forced, free mem: {gc.mem_free()}")

            wdt.feed()
            sleep(0.05)

        except KeyboardInterrupt:
            scene_interrupt(oled)
            break


# Entry point
if __name__ == "__main__":
    main_loop()