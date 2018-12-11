# -*- coding:utf-8 -*-
import socket
from contextlib import closing

import os
import commands

hostName='harvest.soracom.io'
portNumber=8514

temp = commands.getoutput("vcgencmd measure_temp").split('=')[1].split('\'')[0]

payload="{\"temperature\":"+temp+"}"
print payload

soracom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with closing(soracom):    # サーバを指定
    soracom.connect((hostName, portNumber))
    # サーバにメッセージを送る
    soracom.sendall(payload)
    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
    #soracom.recv(1024)
    print(soracom.recv(1024))


