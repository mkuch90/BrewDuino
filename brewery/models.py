from django.db import models

import time

class BrewSettings(models.Model):
  date_time = models.FloatField(primary_key=True)
  system_on = models.IntegerField()
  coil_unlocked = models.IntegerField()
  pump_unlocked = models.IntegerField()
  control_mode = models.IntegerField()
  boil_temp = models.IntegerField()
  mash_temp = models.IntegerField()
  coil_power = models.IntegerField()
  pump_setting = models.IntegerField()

  @staticmethod
  def GetLatest():
    entries = BrewSettings.objects.all().order_by('-date_time')
    entry = None
    if len(entries) == 0:
      entry = BrewSettings.GetDefault()
      entry.save()
    else:
      entry = entries[0]

    return entry

  @staticmethod
  def GetDefault():
    settings = BrewSettings()
    settings.date_time = int(time.time())
    settings.system_on = False
    settings.coil_unlocked = False
    settings.pump_unlocked = False
    settings.control_mode = 0
    settings.boil_temp = 0
    settings.mash_temp = 0
    settings.coil_power = 0
    settings.pump_setting = 0
    return settings

class Temperature(models.Model):
  date_time = models.FloatField(primary_key=True)
  boil_temp = models.IntegerField()
  mash_temp = models.IntegerField()
  stream_temp = models.IntegerField()

  @staticmethod
  def GetLatest():
    entries = Temperature.objects.all().order_by('-date_time')
    entry = None
    if len(entries) == 0:
      entry = Temperature.GetDefault()
      entry.save()
    else:
      entry = entries[0]

    return entry


  @staticmethod
  def GetDefault():
    settings = Temperature()
    settings.date_time = int(time.time())
    settings.boil_temp = 0
    settings.mash_temp = 0
    settings.stream_temp = 0
    return settings



class State(models.Model):
  date_time = models.FloatField(primary_key=True)
  coil_on = models.IntegerField()
  pump_on = models.IntegerField()
  coil_power = models.IntegerField()

  @staticmethod
  def GetLatest():
    entries = State.objects.all().order_by('-date_time')
    entry = None
    if len(entries) == 0:
      entry = State.GetDefault()
      entry.save()
    else:
      entry = entries[0]

    return entry

  @staticmethod
  def GetDefault():
    settings = State()
    settings.date_time = int(time.time())
    settings.coil_on = 0
    settings.pump_on = 0
    settings.coil_power = 0
    return settings

class CoilEnum:
  manual = 3
  auto_boil = 1
  auto_mash = 2
  off = 0  # Default Action Safest

class PumpEnum:
  auto = 2
  on = 1
  off = 0  # Default Action safest
