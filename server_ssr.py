#!/usr/bin/python
import serial
import os
import threading
import signal
import sys
from threading import Timer
from datetime import datetime

from django.conf import settings

try:
  from GPIO import ssr_controller
except ImportError:
  from FakeGPIO import fake_ssr_controller as ssr_controller

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

POWER_INTERVAL = 5.0
MAX_POWER = 128.0

class SSRServer:
  """The server uses timers and interrupts to read from the database the state
  of the server and control the SSR accordingly"""


  def __init__(self):
    self._running = True
    self._server_state = ServerState()
    self._server_state.ResetToDefaults()

  def ProcessInput(self, lines):
    # do something with the lines
    mash_temp, boil_temp, stream_temp = None, None, None
    for line in lines:
      line.strip()
      keyval = line.split(':')
      if(len(keyval) != 2):
        continue
      key, value = keyval
      if (key == 'mash'):
        mash_temp = int(value)
      if (key == 'boil'):
        boil_temp = int(value)
      if (key == 'stream'):
        stream_temp = int(value)
      if mash_temp is not None and boil_temp  is not None and stream_temp  is not None:  # case where they are set multiple times
        break
    print(lines)
    self._server_state.SetTemp(mash_temp, boil_temp, stream_temp)
    return

  def GetPower(self):
    return self._server_state.ManageStateViaSettingsAndTemperature()

  def GetPump(self):
    return self._server_state.IsPumpOn()




sig_server = None
sig_ssr = None



class Handler:


  def __init__(self):

    signal.signal(signal.SIGINT, self.Shutdown)
    self.server = SSRServer()
    self.ssr = ssr_controller.SSRController()
    self.HandlePower()
    self.HandlePump()


  def Shutdown(self, signal, frame):
    self.server._running = False
    self.ssr.PumpOff()
    self.ssr.SSROff()
    self.ssr = None  # Set to none so SSR does not turn on again.
    Log('Shutting Down')
    sys.exit(0)

  def HandlePump (self):
    if not self.server._running:
      return
    if(self.server.GetPump()):
      self.ssr.PumpOn()
    else:
      self.ssr.PumpOff()

    timer = Timer(1, self.HandlePump)
    timer.start()

  def PowerOffInterrupt(self):
    self.ssr.SSROff()

  def HandlePower (self):
    if not self.server._running:
      return
    power = self.server.GetPower()
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
    pass
  
  





if  __name__ == '__main__':main()



