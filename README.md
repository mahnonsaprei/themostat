uPython-ESP8266-Thermostat 
==========================

From Naish21:
I presented the data received from a DHT22 (Temperature-Humidity Sensor) connected to a ESP12 Nodemcu in a OLED 128x64 Screen via I2C (SSD1306) and also send the data to a Mosquitto (MQTT) Server in a Linux machine that is running OpenHab. I can send ON/OFF commands via MQTT from the OpenHab to start/stop the Boiler (in the prototype is just a led that I turn on/off).

You can see all the details of the project here: https://hackaday.io/project/12979-thermostat-with-esp8266-mqtt-openhab-micropython

 ssd1306.py -> Library for the oled 128x64 screen. It's been trimmed to include only I2C functions. Original from: https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

 umqtt.py -> MQTT library for ESP8266. Original from: https://github.com/micropython/micropython-lib/tree/master/umqtt.simple

  main.py -> Main program, all the functionality here.
 
  Modified by Marcello Colangelo:
  ==================================
  The code is tested with 1.9.2 version of micropython with esp8266 and ssd1206. 
  Main scope of this fork is to connect with my home assistant.
  
  You need to import only umqtt.simple from here: https://github.com/micropython/micropython-lib/tree/master/umqtt.simple/umqtt
  No matter from ssd1306 library you don't need to import, just this line: "from ssd1306 import SSD1306_I2C"
  Post google plus: https://plus.google.com/104340292881255677295/posts/eQ2Ey7Q81Mm?hl=it
  
