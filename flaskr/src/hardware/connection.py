from binascii import hexlify

import threading
import machine
import dht
import time
import network
import ntptime
from machine import Timer
from umqtt.robust2 import MQTTClient

# Setup global variables
keepalive = 120
message_timeout = keepalive * 2
measurement_enabled = False
blinking_enabled = False
measurement_interval = 1
led_timer = Timer()
blinking = False

# Setup sensors
sensor = dht.DHT22(machine.Pin(15))
measuring_LED = machine.Pin(16, machine.Pin.OUT)
blinking_LED = machine.Pin(14, machine.Pin.OUT)

# Setup WiFi
ssid = 'WIFI_SSID'
password = 'WIFI_PASSWORD'

# Setup MQTT client
mqtt_broker = 'BROKER_IP'
mqtt_port = 'BROKER_PORT'
mqtt_topic = 'sensor/temperature'
mqtt_led = b'control/led'
mqtt_measurement = b'control/measurement'
mqtt_interval = b'control/interval'

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(5)
print('Connected to Wi-Fi')

def toggle_led(timer):
    blinking_LED.value(not blinking_LED.value())

def start_blinking():
    global blinking
    if not blinking:
        led_timer.init(freq=1, mode=Timer.PERIODIC, callback=toggle_led)
        blinking = True

def stop_blinking():
    global blinking
    if blinking:
        led_timer.deinit()
        blinking_LED.value(0)
        blinking = False

def get_timestamp():
    offset_hours = 2
    t = time.localtime(time.time() + offset_hours * 3600)
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )

def led_flash():
    global flashing_thread_running
    flashing_thread_running = True
    while flashing_thread_running:
        blinking_LED.value(1)
        time.sleep(1)
        blinking_LED.value(0)
        time.sleep(1)

def mqtt_callback(topic, msg, retained, dup):
    global blinking_enabled, measurement_enabled, measurement_interval
    if topic == mqtt_led:
        blinking_enabled = (msg == b'on')
    elif topic == mqtt_measurement:
        if msg == b'on':
            measuring_LED.value(1)
            measurement_enabled = True
        else:
            measuring_LED.value(0)
            measurement_enabled = False
    elif topic == mqtt_interval:
        try:
            val = int(msg)
            if 1 <= val <= 3600:
                measurement_interval = val
        except:
            pass

def mqtt_connect():
    mqtt_client = MQTTClient(hexlify(machine.unique_id()).decode('ascii'), mqtt_broker, mqtt_port, keepalive=keepalive,
                             message_timeout=message_timeout)
    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.connect()
    mqtt_client.subscribe(mqtt_led)
    mqtt_client.subscribe(mqtt_measurement)
    mqtt_client.subscribe(mqtt_interval)
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
        mqtt_client.check_msg()
        
        if blinking_enabled:
            start_blinking()
        else:
            stop_blinking()
        
        if measurement_enabled:
            measurement_time = get_timestamp()
            try:
                sensor.measure()
            except e:
                print(e);
            temp = sensor.temperature()
            sending_time = get_timestamp()
            payload = ("{},{},{:.1f}".format(measurement_time, sending_time, temp))
            mqtt_client.publish(mqtt_topic, payload, qos=1)
            print("Message was sent")
            time.sleep(measurement_interval)