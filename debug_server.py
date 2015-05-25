#!/usr/bin/python
import serial
from time import sleep




def main():
  output = '100\r'
  com_serial = serial.Serial('/dev/ttyUSB0', 9600)
  while True:
    com_serial.flush()
    com_serial.write(output)

    sleep(2)


if  __name__ == '__main__':main()



