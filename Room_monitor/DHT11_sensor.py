from machine import Pin
from dht import DHT11


def get_data (pin_no):
    """
    Returns a dictionary data type for humidtity(%) and temperature(°C) from the DHT11 sensor
    """
    # create DHT11 object
    sensor = DHT11(Pin(int(pin_no)))
    
    try:
        # read sensor data
        sensor.measure()

        # get humidity and temperature
        hum = sensor.humidity()
        temp = sensor.temperature()
        
        return{"humidity":hum, "temperature":temp}

    except Exception as e:
        return(f"Failed to read from sensor: {e}", False)