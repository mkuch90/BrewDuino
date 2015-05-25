from django.test import TestCase

#!/usr/bin/python

import time

from server_state import ServerState

from brewery.models import BrewSettings, Temperature, State, CoilEnum, PumpEnum



def SetUp():
  State.objects.all().delete()
  Temperature.objects.all().delete()
  BrewSettings.objects.all().delete()

  settings = State.GetDefault()
  settings.save()


  settings = Temperature.GetDefault()
  settings.save()


  settings = BrewSettings.GetDefault()
  settings.save()

def TearDown():
  State.objects.all().delete()
  Temperature.objects.all().delete()
  BrewSettings.objects.all().delete()


class ServerStateTest(TestCase):


  def testPumpOn(self):
    self._server_state = ServerState()
    SetUp()
    settings = BrewSettings.GetDefault()
    settings.system_on = True
    settings.save()
    self._server_state.SetPumpUnlocked(True)
    self._server_state.SetPumpOn(True)
    assert self._server_state.IsPumpOn()

    self._server_state.SetPumpOn(False)
    assert not self._server_state.IsPumpOn()

    self._server_state.SetPumpOn(True)
    # Should Turn the pump off
    assert self._server_state.IsPumpOn()
    self._server_state.SetPumpUnlocked(False)
    assert not self._server_state.IsPumpOn()

    # should not work with the safety on
    self._server_state.SetPumpOn(True)
    assert not self._server_state.IsPumpOn()

    # should work after the safety is turned off
    self._server_state.SetPumpUnlocked(True)
    assert not self._server_state.IsPumpOn()
    self._server_state.SetPumpOn(True)
    assert self._server_state.IsPumpOn()
    TearDown()

  def testCoilPower(self):
    self._server_state = ServerState()
    SetUp()
    settings = BrewSettings.GetDefault()
    settings.coil_unlocked = True
    settings.system_on = True
    settings.coil_mode = CoilEnum.manual
    settings.save()
    assert self._server_state.SetCoilPower(50) == 50
    assert self._server_state.SetCoilPower(120) == 0
    TearDown()

  def testManageKettlePower(self):
    self._server_state = ServerState()
    SetUp()
    settings = BrewSettings.GetDefault()
    settings.coil_unlocked = True
    settings.system_on = True
    settings.coil_mode = CoilEnum.auto_boil
    settings.save()


    self._server_state.SetTemp(0, 100, 0)
    assert self._server_state.ManageKettlePower(100) == 30
    assert self._server_state.ManageKettlePower(105) == 100
    assert self._server_state.ManageKettlePower(95) == 0
    TearDown()

  def testManageStateViaSettingsAndTemperature(self):
    self._server_state = ServerState()
    SetUp()
    settings = BrewSettings.GetDefault()
    settings.coil_unlocked = False
    settings.system_on = False
    settings.control_mode = CoilEnum.off
    settings.save()


    assert self._server_state.ManageStateViaSettingsAndTemperature() == 0

    settings.control_mode = CoilEnum.manual
    settings.coil_power = 50
    settings.save()
    assert self._server_state.ManageStateViaSettingsAndTemperature() == 0

    settings.system_on = True
    settings.save()
    assert self._server_state.ManageStateViaSettingsAndTemperature() == 0

    settings.coil_unlocked = True
    settings.save()
    assert self._server_state.ManageStateViaSettingsAndTemperature() == 50

    settings.control_mode = CoilEnum.auto_boil
    settings.boil_temp = 100
    settings.save()
    temp = Temperature.GetDefault()
    temp.boil_temp = 100
    temp.mash_temp = 100
    temp.save()
    assert self._server_state.ManageStateViaSettingsAndTemperature() == 30

    settings.control_mode = CoilEnum.auto_mash

    temp.boil_temp = 30
    temp.mash_temp = 100
    temp.save()
    settings.pump_unlocked = True
    settings.mash_temp = 100
    settings.pump_setting = PumpEnum.auto
    settings.save()
    assert self._server_state.ManageStateViaSettingsAndTemperature() == 100
    assert self._server_state.IsPumpOn()


    temp.boil_temp = 112
    temp.save()
    settings.mash_temp = 98  # In Target Range
    settings.pump_setting = PumpEnum.auto
    settings.save()
    assert self._server_state.ManageStateViaSettingsAndTemperature() == 0
    assert not self._server_state.IsPumpOn()



    settings.pump_setting = PumpEnum.off
    settings.save()
    self._server_state.ManageStateViaSettingsAndTemperature()
    assert not self._server_state.IsPumpOn()

    settings.pump_setting = PumpEnum.on
    settings.save()
    self._server_state.ManageStateViaSettingsAndTemperature()
    assert self._server_state.IsPumpOn()

    TearDown()








