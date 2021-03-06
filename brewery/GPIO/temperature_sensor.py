import RPi.GPIO as GPIO


class TemperatureSensor:  
  TEMPERATURE_ADDRESS_1 = "28-000004bf40cd"  #boil
  TEMPERATURE_ADDRESS_2 = "28-000004bf8d1f"  #stream
  TEMPERATURE_ADDRESS_3 = "28-000004c068a7"  #mash
  FILE_PATH = "/sys/bus/w1/devices/{0}/w1_slave"

  def ReadTemperature(self,address):
    path = self.FILE_PATH.format(address)
    tempfile = open(path)
    text = tempfile.read()
    tempfile.close()
    tempdata = text.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:])
    temperature = temperature / 1000
    return temperature

  def __init__(self):
    x = 1
