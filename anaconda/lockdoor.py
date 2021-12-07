import pyfirmata
from time import sleep

port = 'COM5'
board = pyfirmata.Arduino(port)
LOCKDOOR = board.get_pin('d:7:o')
ledHijau = board.get_pin('d:9:o')
ledMerah = board.get_pin('d:10:o')

def terbuka():
  print("halo")

def salah():
  print("salah")