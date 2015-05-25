import serial
import os
import threading
import signal
import time
import sys
from threading import Timer
from datetime import datetime

from django.conf import settings

try:
  from GPIO import ssr_controller
except ImportError:
  from FakeGPIO import fake_ssr_controller as ssr_controller



try:
  from GPIO import temperature_sensor
except ImportError:
  from FakeGPIO import fake_temperature_sensor as temperature_sensor



def Log(message):
  print("{0} - {1}".format(datetime.now().time(), message))

POWER_INTERVAL = 5.0
MAX_POWER = 100

def PowerOffInterrupt(ssr):
  ssr.SSROff()

def HandlePower (power, ssr):
  if(power > 0):
    Log("Power {0}".format(power))
    ssr.SSROn()
  else:
    Log("Power Off")
    ssr.SSROff()
  if(power > 0 and power < MAX_POWER):
    delay = power * POWER_INTERVAL / MAX_POWER
    timer = Timer(delay, PowerOffInterrupt, [ssr])
    timer.start()
    Log("Delay Until Off: {0}".format(delay))

  threading.Timer(POWER_INTERVAL, HandlePower, [power, ssr]).start()


def main():
  ssr = ssr_controller.SSRController()
  sensor = temperature_sensor.TemperatureSensor()
  ssr.SSROff()
  power = 40
  HandlePower(power, ssr)



  while True:
    Log("Temp: {0}".format(sensor.TemperatureStream()))
    time.sleep(2)









if  __name__ == '__main__':main()
