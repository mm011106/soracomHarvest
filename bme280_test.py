#coding: utf-8


import bme280

# bme280.setup()
# bme280.get_calib_param()

import socket
from contextlib import closing

import os
import commands
import time

# logger setup
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('soracom.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)



hostName='harvest.soracom.io'
portNumber=8514
resultSend=''

if __name__ == '__main__':
    bmeRead=[0.00 , 0.00, 0.00]
    interval = 18
    while True:
        #temp = commands.getoutput("vcgencmd measure_temp").split('=')[1].split('\'')[0]
        bmeRead = bme280.readData()
#        print bmeRead
        temp = bmeRead[0]
        humid = bmeRead[2]
        pres = bmeRead[1]
        payload =     "{" + "\"level\": 50.3"          + ", "
        payload = payload + "\"contPressure\": 500"    + ", "
        payload = payload + "\"status\": \"0xF\""          + ", "
        payload = payload + "\"temp\":" + format(temp)         + ", "
        payload = payload + "\"humid\":" + format(humid)          + ", "
        payload = payload + "\"atmPressure\":" + format(pres)
        payload = payload + "}"
        logger.debug('%f - %s', time.time(),payload)

        try:
            resultSend = soraSend(hostName,portNumber,payload)
            logger.info('Result: %s', resultSend)
        except socket.error as msg:
#            print("send error !")
            logger.warning('Error on sending data: %s',msg)
        except :
            logger.warning('unexpected errror occurred.')

        time.sleep(interval)
