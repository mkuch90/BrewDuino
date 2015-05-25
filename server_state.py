#!/usr/bin/python

import time
from brewery.models import BrewSettings, Temperature, State, CoilEnum, PumpEnum



class ServerState:

  def ResetToDefaults(self):
    state = State.GetDefault()
    state.save()


  def SetPumpOn(self, is_on):
    latest_state = State.GetLatest()
    latest_state.date_time = int(time.time())
    latest_state.pump_on = is_on
    latest_setting = BrewSettings.GetLatest()
    if not is_on:
      latest_state.save()
      return
    if not latest_setting.pump_unlocked and latest_setting.system_on:
      return
    latest_state.save()

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


  def SetPumpUnlocked(self, unlocked):
    latest_setting = BrewSettings.GetLatest()
    # Safety on, turn pump off
    if not unlocked:
      self.SetPumpOn(False)


    if unlocked == latest_setting.pump_unlocked:
      return

    latest_setting.pump_unlocked = unlocked
    latest_setting.date_time = int(time.time())
    latest_setting.save()

  def IsPumpOn(self):
    latest_state = State.GetLatest()
    latest_setting = BrewSettings.GetLatest()
    if not latest_setting.pump_unlocked:
      latest_state.pump_on = False
      latest_state.save()
      return 0;
    if latest_setting.pump_setting == PumpEnum.off:
      latest_state.pump_on = False
      latest_state.save()
      return 0;

    return latest_state.pump_on


  def GetCoilPower(self):
    latest_state = State.GetLatest()
    return latest_state.coil_power



  def SetCoilPower(self, coil_power):
    latest_setting = BrewSettings.GetLatest()
    latest_state = State.GetLatest()

    if not latest_setting.coil_unlocked or not latest_setting.system_on:
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


  def ManageKettlePower(self, desired_kettle_temp):

    temp = Temperature.GetLatest()
    boil_temp = temp.boil_temp
    kettle_temp_diff = boil_temp - desired_kettle_temp
    if kettle_temp_diff == 0:
      return self.SetCoilPower(0)

    if kettle_temp_diff > 1:  # Don't let kettle get too hot
      return self.SetCoilPower(0)
    if kettle_temp_diff < -1:
      return self.SetCoilPower(128)

    return self.SetCoilPower(30)

  def ManageStateViaSettingsAndTemperature(self):
    latest_settings = BrewSettings.GetLatest()

    # Handle system off
    if not latest_settings.system_on:
      self.SetPumpOn(False)
      return self.SetCoilPower(0)


    if not (latest_settings.pump_setting == PumpEnum.auto):
      if latest_settings.pump_unlocked:
        self.SetPumpOn(latest_settings.pump_setting == PumpEnum.on)

    # Coil Locked
    if ((not latest_settings.coil_unlocked) or
        (latest_settings.control_mode == CoilEnum.off)):
      return self.SetCoilPower(0)

    # Use manual coil control
    if latest_settings.control_mode == CoilEnum.manual:
      return self.SetCoilPower(latest_settings.coil_power)

    if latest_settings.control_mode == CoilEnum.auto_mash:
      temps = Temperature.GetLatest()
      temp_goal = latest_settings.mash_temp - temps.mash_temp

      if temp_goal <= 0:  # Too high
        if latest_settings.pump_setting == PumpEnum.auto:
          self.SetPumpOn(False)
        return self.ManageKettlePower(latest_settings.mash_temp + 14)

      if latest_settings.pump_setting == PumpEnum.auto:
        self.SetPumpOn(True)
      # In mash mode, the kettle should be X degrees above mash goal

      return self.ManageKettlePower(latest_settings.mash_temp + 14)
    return self.ManageKettlePower(latest_settings.boil_temp)




