# -*- coding:utf-8 -*-
import socket
from contextlib import closing

import os
import commands
import time

def soraSend(hostName,portNumber,payload): 
    soracom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(soracom):    # サーバを指定
        soracom.connect((hostName, portNumber))
    # サーバにメッセージを送る
        soracom.sendall(payload)
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
        ret=soracom.recv(1024)
    return ret 
    #print(soracom.recv(1024))



hostName='harvest.soracom.io'
portNumber=8514

interval = 18
while True:
    temp = commands.getoutput("vcgencmd measure_temp").split('=')[1].split('\'')[0]

    payload="{\"temperature\":"+temp+"}"
    print time.time(), payload
    
    print soraSend(hostName,portNumber,payload)


    time.sleep(interval)

