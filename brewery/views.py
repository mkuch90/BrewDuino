import time
from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader
from brewery.models import BrewSettings, Temperature, State, CoilEnum

CHECKED = 'checked'


class ControlMode():
  def __init__(self, mode=CoilEnum.off):
    self.off = ''
    self.manual = ''
    self.autohlt = ''
    self.automash = ''

    if mode == CoilEnum.off:
      self.off = CHECKED

    if mode == CoilEnum.manual:
      self.manual = CHECKED

    if mode == CoilEnum.auto_boil:
      self.autohlt = CHECKED

    if mode == CoilEnum.auto_mash:
      self.automash = CHECKED

class Settings():

  def __init__(self):
    latest_entry = BrewSettings.objects.all().order_by('-date_time')[0]
    self.control_mode = ControlMode(latest_entry.control_mode)

    latest_temp = Temperature.GetLatest()
    self.temperature = CurrentTemperature(latest_temp)

    # Default action is safest
    self.main_power = ''
    if latest_entry.system_on:
      self.main_power = CHECKED


    self.mash_temp = latest_entry.mash_temp
    self.hlt_temp = latest_entry.boil_temp
    self.power_level = latest_entry.coil_power

class CurrentTemperature():
  def __init__(self, latest=None):

    self.mash = 0
    self.boil = 0
    self.stream = 0

    if latest is not None:
      self.boil = latest.boil_temp
      self.mash = latest.mash_temp
      self.stream = latest.stream_temp

class State():
  def __init__(self):
    self.kettle_power = 0

def index(request):

  if request.method == 'POST':
    print(request.POST)
    brew_settings = BrewSettings()
    brew_settings.date_time = int(time.time())
    brew_settings.system_on = request.POST.has_key('main_power')
    brew_settings.control_mode = int(request.POST['control_mode'])
    brew_settings.boil_temp = int(request.POST['hlt_temp'])
    brew_settings.mash_temp = int(request.POST['mash_temp'])
    brew_settings.coil_power = int(request.POST['coil_power'])
    brew_settings.save()

    settings = Settings()
    context = {
        'brewery_name': 'BrewDuino Meister Control',
        'settings':settings,
    }

    return render(request, 'brewery/index.html', RequestContext(
        request,
        context))

  settings = Settings()
  context = {
      'brewery_name': 'BrewDuino Meister Control',
      'settings':settings,
  }
  return render(request, 'brewery/index.html', context)
