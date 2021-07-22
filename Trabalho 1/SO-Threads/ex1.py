import logging
import threading
from time import sleep
import datetime
import numpy as np
from random import randint

def ThreadInvVector(ThreadID, vet1, vet2, n, start, end):
    print("Thread {:^4}: começou. Inicio: {:^4} ,Fim: {:^4}".format(ThreadID, start, end))
    for i in range(start, end):
        vet2[n-1-i] = vet1[i]

def threads_are_working(ThreadsList): #função que verifica se aainda tem threads trabalhando
    for thread in ThreadsList:
        if ( thread.is_alive() ):
            #print("thread viva")
            return True
    print("todas as threads mortas")
    return  False

def ex1():
    n  = int(input("tamanho da vetor: "))
    num_thread = int(input("numero de threads: "))
    vet1 = []
    for i in range(n):
        vet1.append(randint(0, 1000)) # gera valor aleatório entre 0 e 1000
    print("vetor original: ", vet1)
    vet2 = vet1.copy()
    gap = int(n/num_thread)
    start = 0
    end = gap + n%num_thread # caso o tamnho do vetor seja uma divisão exata pelo numero de threads o excedente (resto da divisão) é colocado na primeira iteração

    ThreadsList = []

    for i in range(num_thread):
        x = threading.Thread(target=ThreadInvVector, args=(i, vet1, vet2, n, start, end))
        x.start()
        ThreadsList.append(x)
        start = end
        end += gap
    u = 0
    while (threads_are_working(ThreadsList)): #para o escopo principal seguir só quando as threads terminarem sua execução
        u+=1

    print("vetor invertido: ", vet2)
ex1()