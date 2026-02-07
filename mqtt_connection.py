import config
from mqtt_client import MQTTManager


def connect_mqtt():
    try:
        mqtt = MQTTManager(
            config.MQTT_CLIENT_ID,
            config.MQTT_BROKER,
            config.MQTT_PORT,
            config.MQTT_STATE_TOPIC,
            config.MQTT_AVAIL_TOPIC,
            username=config.MQTT_USERNAME,
            password=config.MQTT_PASSWORD,
        )
        mqtt.connect()
        return mqtt
    except Exception as e:
        print("[WARN] MQTT connect failed:", e)
        return None


def mqtt_status(mqtt):
    """Returns mqtt if alive, otherwise None"""
    if not mqtt or not mqtt.connected:
        return None

    try:
        mqtt.client.ping()
        return mqtt
    except Exception as e:
        print("[WARN] MQTT ping failed:", e)
        try:
            mqtt.disconnect()
        except:
            pass
        return None
