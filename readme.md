# SoracomHavest用のデータ送信プログラム

## 何をするためのスクリプトか

- TCPプロトコルでsoracom Harvestにデータを送信する
- 20秒ごとに１回下記のデータを計測する。
  - 液面:level
  - 圧力:contPressure
  - 動作状況:status
  - 外気温:temp
  - 大気圧:atmPressure
  - 湿度:humid

## 実現されていること
- 約20秒ごとに繰り返しデータを送信する


## 実現されていないこと
- データが取れていない
- 送信周期が不正確
- 自動で立ち上がらない
- エラーのハンドリングができていない
  - サーバが見つからない
  - 論理的に　ネットワークに接続できない
  - 物理的に　ネットワークに接続できない（SIMが見つからないなど）
  
## 使い方
まだ自動化されていないので、手動でPPPインターフェイスを立ち上げる必要がある。

`sudo pon soracom_ak-020`

しばらくするとSIMドングルのLEDが点滅。その後、スクリプトを起動。

うまく動いていれば`201`が帰ってくる。


## 構成

![PINCONFIG](https://user-images.githubusercontent.com/9587359/49682538-37840600-faf9-11e8-9961-4d8529ed1cbd.png)


- ADC:MCP3208  SPI接続　　[Datasheet:MCP3208](http://ww1.microchip.com/downloads/en/DeviceDoc/21298e.pdf)
  - 2.5V FS / diff input
  - Input config
    - CH0,1 : level (液面)　0~10V -> 0~2V
    - CH2,3 : contPressure (コンテナ圧力) 1〜5V -> 0.2V〜1V
    - CH4,5 : NC
    - CH6,7 : NC
  - __RasPi PIN config__ :  19(MOSI),21(MISO),23(CLK),24(CE)


- 環境計測:BME280  I2C接続　　
[Datasheet:BME280(switch science )](https://www.switch-science.com/catalog/2236/)
  - __RasPi PIN config__ : 3(SD),5(SCK),1(V33),6(GND)


- ステータス:GPIO
  - どのIOを使うか未定。4bitぐらい。
    - 液面測定中　（液面センサがアクティブ）
    - 注液中　（バルブが閉じている）
    - リモコン状態（On:液面計動作/Off:液面系off=MEG計測中)
