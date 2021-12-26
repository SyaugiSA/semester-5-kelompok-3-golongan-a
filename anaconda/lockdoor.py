import pyfirmata
from time import sleep

port = 'COM3'
board = pyfirmata.Arduino(port)
ledHijau = 9
ledMerah = 10
lockDoor = 7

def reset():
  for i in range(2,13):
    board.digital[i].write(1)

def terbuka():
  board.digital[ledHijau].write(0)
  board.digital[lockDoor].write(0)
  sleep(5)

def tidakTerbuka():
  board.digital[ledMerah].write(0)
  sleep(1)