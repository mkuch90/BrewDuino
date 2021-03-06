#!/usr/bin/python
import serial
import os
import threading
import signal
import sys
import time
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

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# settings.configure(
#   DATABASE_ENGINE='django.db.backends.sqlite3',
#   DATABASE_HOST="localhost",
#   DATABASE_NAME=os.path.join(BASE_DIR, "brewmaster.db"),
#   DATABASE_USER="kuchenbecker",
#   DATABASE_PASSWORD="brewmeister",
#   DATABASE_PORT="5432",
#   INSTALLED_APPS="brewery",
# )
settings.configure(
    DATABASES={ 'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "brewmaster.db"),
        'USER': 'kuchenbecker',
        'PASSWORD': 'brewmeister',
        'HOST': '',
        'PORT': '',
        }, },
    TIME_ZONE='Europe/Luxembourg'
)

from server_state import ServerState


def Log(message):
  print("{0} - {1}".format(datetime.now().time(), message))

POWER_INTERVAL = 2
MAX_POWER = 128.0

sig_server = None
sig_ssr = None



class Handler:


  def __init__(self):
    
    self.running = True
    signal.signal(signal.SIGINT, self.Shutdown)
    self._server_state = ServerState()
    self._server_state.ResetToDefaults()
    self.ssr = ssr_controller.SSRController()
    self.HandlePower()
    self.sensor = temperature_sensor.TemperatureSensor()  
    
    
  def SampleTemperature(self):
      stream = self.sensor.TemperatureStream()
      boil = self.sensor.TemperatureBoil()
      mash = self.sensor.TemperatureMash()
      Log("Boil ({0}) Mash ({1}) Stream ({2})".format(boil,mash,stream))
      self._server_state.SetTemp(mash, boil, stream)

  def GetPower(self):
    return self._server_state.ManageCoil()

  def Shutdown(self, signal, frame):
    self.ssr.SSROff()
    self.running = False
    self.ssr = None  # Set to none so SSR does not turn on again.
    Log('Shutting Down')
    sys.exit(0)

  def PowerOffInterrupt(self):
    self.ssr.SSROff()

  def HandlePower (self):
    if not self.running:
      return
    power = self.GetPower()
    if(power > 0):
      Log("Power {0}".format(power))
      self.ssr.SSROn()
    else:
      Log("Power Off")
      self.ssr.SSROff()
    if(power > 0 and power < MAX_POWER):
      delay = power * POWER_INTERVAL / MAX_POWER
      timer = Timer(delay, self.PowerOffInterrupt)
      timer.start()
      Log("Delay Until Off: {0}".format(delay))
      Log(delay)

    threading.Timer(POWER_INTERVAL, self.HandlePower).start()



def main():
  handler = Handler()
  
  while True:
    handler.SampleTemperature()
    time.sleep(2)
  
  
  





if  __name__ == '__main__':main()



