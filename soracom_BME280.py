#coding: utf-8
#/usr/bin/python

import bme280

import socket
from contextlib import closing

import os
import commands
import time

# logger setup
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# create a file handler
handler = logging.FileHandler('soracom_BME280.log')
handler.setLevel(logging.WARNING)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

def soraSend(hostName,portNumber,payload):
    soracom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(soracom):    # サーバを指定
        soracom.connect((hostName, portNumber))
    # サーバにメッセージを送る
        soracom.sendall(payload)
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
        ret=soracom.recv(1024)
        logger.info('sent data')
    return ret

hostName='harvest.soracom.io'
portNumber=8514
resultSend=''

if __name__ == '__main__':
    bmeRead=[0.00 , 0.00, 0.00]
    interval = 18
    while True:
        bmeRead = bme280.readData()
        # print bmeRead
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
        # print payload
        logger.debug('%f - %s', time.time(),payload)

        try:
            resultSend = soraSend(hostName,portNumber,payload)
            logger.info('Result: %s', resultSend)
        except socket.gaierror as msg:
#            print("send error !")
            logger.warning('Error on sending data: %s',msg)
        except :
            logger.warning('unexpected errror occurred.')

        time.sleep(interval)
