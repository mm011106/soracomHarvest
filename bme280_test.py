#coding: utf-8


import bme280

# bme280.setup()
# bme280.get_calib_param()


if __name__ == '__main__':
	try:
		bme280.readData()
	except KeyboardInterrupt:
		pass
