import RPi.GPIO as GPIO
from temperature_sensor import TemperatureSensor

#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)


temp_sensor = TemperatureSensor()

while True:
  print(temp_sensor.ReadTemperature(temp_sensor.TEMPERATURE_ADDRESS_1))
  print(temp_sensor.ReadTemperature(temp_sensor.TEMPERATURE_ADDRESS_2))
  print(temp_sensor.ReadTemperature(temp_sensor.TEMPERATURE_ADDRESS_3))



GPIO.cleanup()
