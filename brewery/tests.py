from django.test import TestCase

#!/usr/bin/python

import time

from server_state import ServerState

from brewery.models import BrewSettings, Temperature, State, CoilEnum



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


  def testCoilPower(self):
    self._server_state = ServerState()
    SetUp()
    settings = BrewSettings.GetDefault()
    settings.system_on = True
    settings.coil_mode = CoilEnum.manual
    settings.save()
    assert self._server_state.SetCoilPower(50) == 50
    assert self._server_state.SetCoilPower(120) == 120
    assert self._server_state.SetCoilPower(130) == 0
    assert self._server_state.SetCoilPower(-5) == 0
    TearDown()

  def testManageCoil(self):
    self._server_state = ServerState()
    SetUp()
    
    settings = BrewSettings.GetDefault()
    settings.system_on = False
    settings.control_mode = CoilEnum.off
    settings.save()
    
    assert self._server_state.ManageCoil() == 0
    
    
    settings.system_on = True
    settings.control_mode = CoilEnum.manual
    settings.coil_power = 50
    settings.save()
    
    assert self._server_state.ManageCoil() == 50
    
    settings.system_on = True
    settings.control_mode = CoilEnum.auto_boil
    settings.boil_temp = 50
    settings.save()
    
    assert self._server_state.ManageCoil() == 128
    
    temp = Temperature.GetDefault()
    temp.boil_temp = 100
    temp.save()
    
    
    assert self._server_state.ManageCoil() == 0
    
    settings.system_on = True
    settings.control_mode = CoilEnum.auto_mash
    settings.mash_temp = 50
    settings.save()
    temp = Temperature.GetDefault()
    temp.boil_temp = 100
    temp.save()
    
    assert self._server_state.ManageCoil() == 128
    
    
    settings.system_on = True
    settings.control_mode = CoilEnum.auto_mash
    settings.mash_temp = 50
    settings.save()
    
    
    temp = Temperature.GetDefault()
    temp.mash_temp = 100
    temp.boil_temp = 0
    temp.stream_temp = 0
    temp.save()
    
    assert self._server_state.ManageCoil() == 0
    
    
    settings.system_on = True
    settings.control_mode = CoilEnum.auto_mash
    settings.mash_temp = 50
    settings.save()
    
    
    temp = Temperature.GetDefault()
    temp.mash_temp = 45
    temp.boil_temp = 0
    temp.stream_temp = 0
    temp.save()
    
    
    assert self._server_state.ManageCoil() == 128
    
    settings.system_on = True
    settings.control_mode = CoilEnum.auto_mash
    settings.mash_temp = 50
    settings.save()
    
    
    temp = Temperature.GetDefault()
    temp.mash_temp = 46
    temp.boil_temp = 58
    temp.stream_temp = 56
    temp.save()
    
    print(self._server_state.ManageCoil())
    assert self._server_state.ManageCoil() == 0
    
    
    
    

    TearDown()








