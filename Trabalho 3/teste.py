import threading
import time

processos = []

def leProcessos():
    proc = ''
    while proc != 'exit':
        p = input()
        processos.append(p)

def escalona():
    while True:
        print('Processo executando...')
        time.sleep(2)
        print(len(processos), "processos na tabela")
        print(processos)
        if "exit" in processos:
            break


if __name__ == "__main__":

    t1 = threading.Thread(target=escalona)
    t1.start()
    time.sleep(0.5)
    t2 = threading.Thread(target=leProcessos)
    t2.start()

    t1.join()
    t2.join()

    exit()