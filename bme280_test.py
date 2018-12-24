#coding: utf-8

from smbus import SMBus
import time

import bme280

bus_number  = 1
i2c_address = 0x76

bus = SMBus(bus_number)

digT = []
digP = []
digH = []

t_fine = 0.0

bme280.setup()
bme280.get_calib_param()


if __name__ == '__main__':
	try:
		readData()
	except KeyboardInterrupt:
		pass
