import logging
import threading
from time import sleep
import datetime
import numpy as np
from random import randint

def threads_are_working(ThreadsList): #função que verifica se aainda tem threads trabalhando
    for thread in ThreadsList:
        if ( thread.is_alive() ):
            #print("thread viva")
            return True
    print("todas as threads mortas")
    return  False

def ThreadMultiplicaMAtriz(ThreadID, A, B, C, M, N, P, start, end):
    print("Thread {:^4}: começou. Inicio: {:^4} ,Fim: {:^4}".format(ThreadID, start, end))
    for k in range(start, end):
        i = int(k/P)
        j = k%P
        elem  = 0
        for l in range(N):
            elem += A[i,l]*B[l,j]
        C[i][j] = elem
        # print(C)

def ex2():
    print("matrizes A(MxN) e B(NxP)")
    M = int(input("M: "))
    N = int(input("N: "))
    P = int(input("P: "))
    num_thread = int(input("numero de threads: "))
    A = np.random.randint(20, size=(M,N))
    B = np.random.randint(5, size=(N,P))

    # M = 2
    # N = 2
    # P = 2
    # A = np.matrix([[2, 1], [0, 0]])
    # B = np.matrix([[0, 1], [0, -2]])
    # print("resposta:\n", np.dot(A, B))

    C = np.zeros((M,P))
    n = M*P
    print("A:\n", A)
    print("B:\n", B)
    gap = int(n/num_thread)
    start = 0
    end = gap + n%num_thread # caso o tamnho do vetor seja uma divisão exata pelo numero de threads o excedente (resto da divisão) é colocado na primeira iteração

    ThreadsList = []

    for i in range(num_thread):
        x = threading.Thread(target=ThreadMultiplicaMAtriz, args=(i, A, B, C, M, N, P, start, end))
        x.start()
        ThreadsList.append(x)
        start = end
        end += gap
    u = 0
    while (threads_are_working(ThreadsList)): #para o escopo principal seguir só quando as threads terminarem sua execução
        u+=1

    print("C:\n", C)
    print("resultado(usando a multiplicação de matriz da biblioteca numpy):\n", np.dot(A, B))

ex2()