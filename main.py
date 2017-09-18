# https://github.com/Naish21/themostat
'''
 * The MIT License (MIT)
 *
 * Copyright (c) 2016 Jorge Aranda Moro
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.

'''
#---Modified by Marcello Colangelo---

#This part is to connect to the WiFi
#In this case: SSID:  & PASS:

WIFISSID='INSERT_YOUR_SSD_HERE'
WIFIPASS='INSERT_YOUR_WIFI_PASSWOR_HERE'

from network import WLAN

def do_connect():
    from network import WLAN
    sta_if = WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFISSID, WIFIPASS)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

#---End Wifi Config---

from machine import Pin

led = Pin(14, Pin.OUT, value=1)

#---MQTT Sending---
from time import sleep_ms
from ubinascii import hexlify
from machine import unique_id
from simple import MQTTClient #Import umqtt.simple https://github.com/micropython/micropython-lib/tree/master/umqtt.simple/umqtt

SERVER = "192.168.1.8"
CLIENT_ID = hexlify(unique_id())
TOPIC1 = "sensor1/tem" #Topic for temperature in home assistant
TOPIC2 = "sensor1/hum" #Topic for Humidity in home assistant
TOPIC3 = b"sensor1/led" #Topic to command state of led

def envioMQTT(server=SERVER, topic="/foo", dato=None):
    try:
        c = MQTTClient(CLIENT_ID, server)
        c.connect()
        c.publish(topic, dato)
        sleep_ms(200)
        c.disconnect()
        #led.value(1)
    except Exception as e:
        pass
        #led.value(0)

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == b"on":
        led.value(1)
        state = 1
    elif msg == b"off":
        led.value(0)
        state = 0

state = 0

def recepcionMQTT(server=SERVER, topic=TOPIC3):
    c = MQTTClient(CLIENT_ID, server)
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(topic)
    print("Connected to %s, subscribed to %s topic" % (server, topic))
    try:
        c.wait_msg()
    finally:
        c.disconnect()
    sleep_ms(100)




#---DHT22---
from dht import DHT22

ds = DHT22(Pin(16)) #DHT22 connected to GPIO16

def medirTemHum():
    try:
        ds.measure()
        tem = ds.temperature()
        hum = ds.humidity()
        #ed.value(1)
        return (tem,hum)
    except Exception as e:
        #led.value(0)
        return (-1,-1)

#---End DHT22---

#---OLED 128x64---
from ssd1306 import SSD1306_I2C
from machine import I2C

i2c = I2C(sda = Pin(4), scl = Pin(5))
display = SSD1306_I2C(128, 64, i2c)

#---RECEIVE WEATHERUNDERGROUND---
import urequests

def weather():
    import urequests
    r = urequests.get("http://api.wunderground.com/api/INSERT_YOUR_API_HERE/conditions/q/IT/Naples.json").json() #Request json to recevie weather info
    temperature = r['current_observation']['temp_c']
    humidityInt = r['current_observation']['relative_humidity']
    return (temperature, humidityInt) # Ritorna il valore della variabile da passare alla funzione
    print(temperature, humidityInt)

#---END RECEIVE WEATHER---

def displaytem(tem,hum,temperature,humidityInt): #import Variables in definition function
    display.fill(0)
    temperatura = 'Tem int: ' + str(tem)[:5] + 'C'
    humedad = 'Hum int: ' + str(hum)[:5] + '%'
    weatherNapoli = 'Tem ext: ' + str(temperature)[:5] + 'C' #Assign weather variableNapoli the value of temperature
    weatherNapoliHumidity = 'Hum ext: ' + str(humidityInt)[:5] + ''
    ip = str(sta_if.ifconfig())
    display.text(temperatura,2,2,1)
    display.text(humedad,2,14,1)
    display.text(ip,2,30,1)
    display.text(weatherNapoli,2,40,1) #Show on lcd value of temp
    display.text(weatherNapoliHumidity,2,50,1) #Show on lcd value of Hum
    display.show()


sleep_ms(3000)

while True:
    (temperature,humidityInt) = weather()
    (tem,hum) = medirTemHum()
    displaytem(tem,hum,temperature,humidityInt)
    envioMQTT(SERVER,TOPIC1,str(tem))
    envioMQTT(SERVER,TOPIC2,str(hum))
    recepcionMQTT()
    sleep_ms(300000)

#---END Main Program---
