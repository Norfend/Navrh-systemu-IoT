from binascii import hexlify

import machine
import dht
import time
import network
import ntptime
from umqtt.robust2 import MQTTClient

# Setup global variables
keepalive = 60
message_timeout = keepalive * 2
TIMEZONE_OFFSET = 2
sensor = dht.DHT22(machine.Pin(15))

# Setup WiFi
ssid = 'WIFI_SSID'
password = 'WIFI_PASSWORD'

# Setup MQTT client
mqtt_broker = 'BROKER_IP'
mqtt_port = 'BROKER_PORT'
mqtt_topic = 'sensor/temperature'

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(5)
print('Connected to Wi-Fi')

def get_timestamp(offset_hours):
    t = time.localtime(time.time() + offset_hours * 3600)
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )

def mqtt_connect():
    mqtt_client = MQTTClient(hexlify(machine.unique_id()).decode('ascii'), mqtt_broker, mqtt_port, keepalive=keepalive,
                             message_timeout=message_timeout)
    mqtt_client.DEBUG = True
    mqtt_client.connect()
    return mqtt_client

def mqtt_reconnect():
    print('Could not connect to MQTT broker, reconnecting: ' + str(mqtt_client.conn_issue))
    mqtt_client.reconnect()

try:
    mqtt_client = mqtt_connect()
    ntptime.settime()
    print('MQTT Connected')
except OSError as e:
    print('Error connecting to MQTT, retrying...')
    mqtt_reconnect()

while True:
    if mqtt_client.is_conn_issue():
        while mqtt_client.is_conn_issue():
            mqtt_reconnect()
    else:
        for i in range(20):
            measurement_time = get_timestamp(TIMEZONE_OFFSET)
            sensor.measure()
            temp = sensor.temperature()
            sending_time = get_timestamp(TIMEZONE_OFFSET)
            payload = ("Measurement Time: {}, Sending Time: {}, Temperature: {:.1f}"
                       .format(measurement_time, sending_time, temp))
            mqtt_client.publish(mqtt_topic, payload, qos=1)
            print("Message was sent")

        for _ in range(500):
            mqtt_client.check_msg()
            mqtt_client.send_queue()
            if not mqtt_client.things_to_do():
                break
            time.sleep_ms(1)
        time.sleep_ms(keepalive // 2)