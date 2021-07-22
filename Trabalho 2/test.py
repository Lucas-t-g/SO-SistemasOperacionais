# -*- coding: utf-8 -*-
import threading
from time import sleep
acordar_dormir_produtor = threading.Event()
acordar_dormir_consumidor = threading.Event()
bufer = 0
bufer_max = 10


def consumidor():
    global acordar_dormir_produtor
    global acordar_dormir_consumidor
    global bufer
    global bufer_max
    while True:
        if bufer == 0:
            print ("consumidor dormindo")
            acordar_dormir_produtor.clear()
            acordar_dormir_consumidor.wait()
            print ("consumidor acordou")
        bufer = bufer - 1
        if bufer == (bufer_max - 1):
            print ("distracando produtor")
            acordar_dormir_produtor.set()
        print ("consumidor",bufer)
        sleep(1)


def produtor():
    global acordar_dormir_produtor
    global acordar_dormir_consumidor
    global bufer
    global bufer_max
    while True:
        if bufer == bufer_max:
            print ("produtor dormindo")
            acordar_dormir_produtor.clear()
            acordar_dormir_produtor.wait()
            print ("produtor acordou")
        bufer = bufer + 1
        if bufer == 1:
            print ("distracando consumidor")
            acordar_dormir_consumidor.set()
        print ("produtor ",bufer)
        sleep(1)

print (bufer)
b = threading.Thread(target=produtor)
a = threading.Thread(target=consumidor)
a.start()
b.start()
#while True:
   # time.sleep(3)
   # print (bufer)