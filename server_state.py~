#!/usr/bin/python

import time
from brewery.models import BrewSettings, Temperature, State, CoilEnum
from datetime import datetime

MAX_POWER = 128


def Log(message):
  print("{0} - {1}".format(datetime.now().time(), message))


class ServerState:

  def ResetToDefaults(self):
    state = State.GetDefault()
    state.save()

  def SetTemp(self, mash=None, boil=None, stream=None):

    if boil is None and mash is None and stream is None:
      return
    temp = Temperature.GetLatest()
    temp.date_time = int(time.time())
    if boil is not None:
      temp.boil_temp = boil
    if mash is not None:
      temp.mash_temp = mash
    if stream is not None:
      temp.stream_temp = stream
    temp.save()

  def GetCoilPower(self):
    latest_state = State.GetLatest()
    return latest_state.coil_power

  def SetCoilPower(self, coil_power):
    latest_setting = BrewSettings.GetLatest()
    latest_state = State.GetLatest()

    if not latest_setting.system_on:
      latest_state.coil_on = 0
      latest_state.coil_power = 0
      latest_state.save()
      return 0

    if coil_power == latest_state.coil_power:
      return coil_power
    if(coil_power >= 0 and coil_power <= 128):
      latest_state.coil_on = coil_power
      latest_state.coil_power = coil_power
      latest_state.save()
      return coil_power
    latest_state.coil_on = 0
    latest_state.coil_power = 0
    latest_state.save()
    return 0

  def ManageCoil(self):
    latest_settings = BrewSettings.GetLatest()
    temps = Temperature.GetLatest()
    # Handle system off
    if not latest_settings.system_on:
      Log('System Off')
      return self.SetCoilPower(0)
    # Use manual coil control
    if latest_settings.control_mode == CoilEnum.manual:
      Log('Manual {0}'.format(latest_settings.coil_power))
      return self.SetCoilPower(latest_settings.coil_power)

    if latest_settings.control_mode == CoilEnum.auto_mash:
      desired_temp = latest_settings.mash_temp
      Log('Auto Mash - Mash {0} Stream {1} Boil {2} Desired {3}'
        .format(temps.mash_temp, 
                temps.stream_temp, 
                temps.boil_temp,
                desired_temp))

      # Close or too high
      if(desired_temp - temps.mash_temp < 0.5):
        Log('Mash at Temp or above (off)')
        return self.SetCoilPower(0)

      if(temps.boil_temp < desired_temp):
        Log('HLT too low (on)')
        return self.SetCoilPower(MAX_POWER)

      if(temps.stream_temp < desired_temp):
        Log('Stream too low (on)')
        return self.SetCoilPower(MAX_POWER)
      
      # Close, allow to equalize.
      if(desired_temp - temps.mash_temp <= 5
         and temps.stream_temp - desired_temp >= 5):
        Log('Mash is close, stream is high (off)')
        return self.SetCoilPower(0)

    Log('Auto Boil - Actual {0} / Desired {1}'
        .format(temps.boil_temp, latest_settings.boil_temp));
    # Manage the kettle rather than the mash.
    if(latest_settings.boil_temp > temps.boil_temp):
      return self.SetCoilPower(MAX_POWER)

    return self.SetCoilPower(0);




