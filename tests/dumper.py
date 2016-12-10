#!/usr/bin/env python3
from pylibftdi import Driver
from pylibftdi import SerialDevice
import time

class MCMD(object):
  def __init__(self):
    self.__driver = Driver()
    self.__device = None
    self.connect()

  def connected_devices(self):
    connected = self.__driver.list_devices()
    if len(connected) == 0:
      print('No devices connected')
    else:
      print('Connected devices:', len(connected))
      print(connected)
      print('Using first device:', connected[0])

  def connect(self):
    if (len(self.__driver.list_devices()) == 0):
      raise Exception('No FT232R-device connected')
    else:
      try:
        self.__device = SerialDevice()
        self.__device.baudrate = 600
        self.__device.dtr = 0
        time.sleep(1)
      except:
        raise Exception('Error while opening Serial Device')
    print('Device connected')

  def getready(self, tries = 5):
    print('Trying to get device ready in max.', tries, 'tries')
    i = 1
    success = False

    self.reset()

    while (i <= 5):
      print('Try #', i)
      self.__device.read(100)
      retry = False
      wakereply = self.wake()
      self.pair()

      if wakereply != 'A':
        retry = True
        self.checksum()
        self.checksum()

      i += 1

      if (retry == False):
        success = True
        break;
      else:
        self.sleep()

    if (success == True):
      print('Got device ready successfully')
    else:
      print('Device did not get ready')

    return success

  def reset(self):
    print('Resetting device')
    self.__device.dtr = 1
    time.sleep(1)
    self.__device.dtr = 0
    time.sleep(1)

  def wake(self):
    print('Waking up device')
    self.__device.write('g')
    time.sleep(1)
    reply = self.__device.read(1).decode()
    print('Wake-up-reply:', reply)
    return reply

  def sleep(self):
    print('Sending device to sleep')
    self.__device.write('s')
    time.sleep(1)

  def pair(self):
    print('Pairing to escrow')
    self.__device.write('l')
    time.sleep(1)

  def checksum(self):
    print('Recalculating checkum')
    self.__device.write('k')
    time.sleep(3)

  def getROMversion(self):
    print('Getting ROM version')
    self.__device.write('q')
    time.sleep(0.1)
    self.__device.write('\x01')
    time.sleep(0.1)
    self.__device.write('\xFC')
    time.sleep(0.1)
    self.__device.write('q')
    time.sleep(0.1)
    self.__device.write('\x01')
    time.sleep(0.1)
    self.__device.write('\xFD')
    time.sleep(1)
    ROMversion = self.__device.read(2).decode()
    print('ROM version:', ROMversion)
    return ROMversion

  def getConfigID(self):
    print('Getting Config ID')
    self.__device.write('q')
    time.sleep(0.1)
    self.__device.write('\x01')
    time.sleep(0.1)
    self.__device.write('\xFE')
    time.sleep(0.1)
    self.__device.write('q')
    time.sleep(0.1)
    self.__device.write('\x01')
    time.sleep(0.1)
    self.__device.write('\xFF')
    time.sleep(0.1)
    configID = self.__device.read(2).decode()
    print('Config ID:', configID)
    return configID

  def dumpEEPROM(self):
    print('Dumping EEPROM - this may take some time')
    EEPROM = []
    for i in range(0, 256):
      if (i%8 == 7):
        print('|', end="", flush=True)
      else:
        print('.', end="", flush=True)
      self.__device.write('q')
      time.sleep(0.1)
      self.__device.write('\x01')
      time.sleep(0.1)
      self.__device.write(chr(i))
      time.sleep(0.1)
      EEPROM.append("{:02x}".format(ord(self.__device.read(2))))
      time.sleep(0.1)
    print()
    print('Dump finished')
    return EEPROM

if __name__ == '__main__':
  print('Millennium Coinmech Dumper')
  print()
  mcmd = MCMD()
  mcmd.connected_devices()
  if (mcmd.getready() != False):
    mcmd.getROMversion()
    mcmd.getConfigID()
    EEPROM = mcmd.dumpEEPROM()
    print(len(EEPROM))
    print(EEPROM)
  mcmd.sleep()
