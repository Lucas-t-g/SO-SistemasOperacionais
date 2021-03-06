import threading
from unicodedata import normalize
from os import walk, chdir, mkdir
import glob
import sys
from time import sleep
from random import choice
import argparse
import threading

class Process():# classe do objeto processo.
    def __init__(self, L):
        if len(L) == 6:
            self.name = L[0]
            self.PID = int(L[1])
            self.clock = int(L[2])
            self.priority = int(L[3])
            self.UID = int(L[4])
            self.mem = int(L[5])
    
    def show(self): # função que mostra na tela todos os dados de um processo.
        print("processo: {:>15}|{:>5}|{:>5}|{:>10}|{:>5}|{:>5}".format(self.name, self.PID, 
                    self.clock, self.priority, self.UID, self.mem))

    def show_is_in_CPU(self, _str = ""): # função que mostra na tela apenas os dados do processo  que está na CPU pedidos no enunciado.
        print(_str+"Processo na CPU->  PID: {:>5} - Nome: {:>15} - Clocks restantes: {:>5}".format(self.PID, self.name, self.clock))

class ProcessManager(): # classe que ira conter tduo sobre os processos.
    def __init__(self, path):
        arq = open(path, "r").read()
        arq = arq.split("\n")
        arq[0] = arq[0].split("|")
        self.algorithm = arq[0][0]  # qual algoritmo será utilizado na hora de escalonar.
        self.CPU_fraction = int(arq[0][1])  # quantos clocks um processo pdoe ficar na cpu.
        self.process_list = []  # lista com pos processos .
        for i in range(1, len(arq)):
            arq[i] =  arq[i].split("|")
            if arq[i] == ['']: continue
            self.process_list.append(Process(arq[i]))
        self.n_process = len(self.process_list) # quantidade de processos para serem processados.
        self.finished_process = [] # lista para armazenar os processos ja terminados.
        self.n_finished_process = 0 # número de processos terminados.
        self.n_clock = 0 # seracontaddo quantos clocks se passaram no total.
        self.access = False # quando a thread que adiciona novos processos tem um novo processo para adicionar ela muda para 'True'
        self.accessGranted = False # a thread de processamento muda o valor para 'True' para sinalizar que a thread de imput pode acesar a lista de processos
        self.stop = False

    def add_process(self, data): # adiciona um novo processo a lista.
        data = data.split("|")
        self.process_list.append(Process(data))
        self.update()
    
    def new_process(self):# função que fica esperando receber a entrada de um novo processo.
        while True:
            entrada = input()
            if entrada == 'exit':
                self.stop = True
                exit()
            self.AccessRequest()
            self.add_process(entrada)
            self.endAccess()
            # self.show()

    def endAccess(self): #avisa que o acesso a lista de processos acabou.
        if show : print("acesso terminado")
        if show : sleep(delay/4)
        self.access = False
    
    def AccessRequest(self): # esta função solicita o acesso a lista de processos.
        if show : print("solicitando acesso")
        if show : sleep(delay/4)
        self.access = True
        while not self.accessGranted: # só retorna pro escopo superior quando o acesso for atendido.
            continue
        if show : print("recebeu acesso")
        if show : sleep(delay/4)
        return True

    def show(self):  # função que mostra algumas informações e a lista de processos.
        print("\n{:-^62}\nalgoritmo: {:>21}\nfração de CPU: {:>5}\nprocessos: {:>5}\nprocessos prontos: {:>5}\nclocks passados: {:>5}\n{:^62}\nProcesso| {:>15}|{:>5}|{:>5}|{:>10}|{:>5}|{:>5}"
                .format("", self.algorithm, self.CPU_fraction, self.n_process, self.n_finished_process, self.n_clock, "Processos não terminados", "Nome", "PID", "Tempo", "Prioridade", "UID", "Memória"))
        for process in self.process_list:
            process.show()
        print("\n{:^62}\nProcesso| {:>15}|{:>5}|{:>5}|{:>10}|{:>5}|{:>5}".format("Processos terminados", "Nome", "PID", "Tempo", "Prioridade", "UID", "Memória"))
        for process in self.finished_process:
            process.show()
        print("{:-^62}\n".format("-"))

    def update(self): # função que atualiza a quantidade de processos feitos, e a quantidade de processos a fazer.
        self.n_process = len(self.process_list)
        self.n_finished_process = len(self.finished_process)

    def find(self, PID): # função que encontra um processo buscando pelo PID e o retorna se o encontrar.
        for elem in self.process_list:
            if elem.PID == PID:
                return elem
        return False
    
    def change_to_done(self, aux): # função que termina um processo(normalmente quando utiliza todos os clocks que ele pedia), 
                                    # removendo da lista de processos a fazer e adicionando na lista de processos feitos.
        if aux != False and aux.clock == 0:
            self.finished_process.append(aux)
            self.process_list.remove(aux)
            return True
        else:
            return False
    
    def put_at_the_end(self, aux): # função coloca um processo a fazer no final da lista (usada no round-robin por exemplo).
        if aux != False:
            self.process_list.append(aux)
            self.process_list.remove(aux)
            return True
        else:
            return False

    def choice_algorithm(self): # função que determina qual algoritmo será utilizado para escalonar.
        if self.algorithm == "alternanciaCircular":
            self.Round_robin()
        if self.algorithm == "prioridade":
            self.priority()
        if self.algorithm == "loteria":
            self.lottery()

    def the_highest_priority(self): # função que ve qual o processo tem maior prioridade
                                     # e o retorna (para o escalonamento por prioridade).
        if self.n_process > 0:
            aux = self.process_list[0]
            if self.n_process > 1:
                for elem in self.process_list[1:]:
                    if elem.priority > aux.priority: aux = elem
            return aux.PID
        else:
            return False

    def priority(self): # função que faz o escalonamento por prioridade.
        PID = self.the_highest_priority()
        # print("test", PID)
        if type(PID) == int:
            aux = self.to_process(PID)
            self.put_at_the_end(aux)

    def Round_robin(self): # função que faz o escalonamento por round-robin.
        PID = self.process_list[0].PID
        aux = self.to_process(PID)
        self.put_at_the_end(aux)

    def raffle(self): # função que gera uma lista com os PID de todos os processos, porem repetidos 
                       # para o número de prioridade, se por exemplo o processo de PID = 3 tiver prioridade 
                       # igual a 10, será adicionado o 3 dez vezes na listae então sorteia um PID da lista para escalonar.
        raffle_list = []
        for elem in self. process_list:
            raffle_list += [elem.PID]*elem.priority
        return choice(raffle_list)

    def lottery(self): # função que faz o escalonamento por loteria.
        PID = self.raffle()
        self.to_process(PID)

    def to_process(self, PID): # função que faz um processo ser 'processado', reduz o númeromde clocks que ele necessita 
                                # com base no número de clocks que ele pode ficar na CPU, 
                                # se chegar a 0 ele é transferido para lista de processos feitos.
        self.update()
        aux = self.find(PID)
        if aux != False: 
            aux.clock -= self.CPU_fraction
            temp = 0
            if aux.clock < 0:
                temp = abs(aux.clock)
                aux.clock = 0
            if aux.clock <= 0: # se o processo chegou ao fim,
                self.change_to_done(aux) # é movido para a lista de processos ja concluidos.
                
            self.n_clock += self.CPU_fraction - temp # atualiza a variável que define quantos clocks se passaram na simulação.
            aux.show_is_in_CPU() # mostra qual processo está na CPU.
        self.update()
        return aux
    
    def checkAccessRequest(self): # confere se a thread de input solicita acesso a lista de processos, e concede.
        if self.access:
            if show : print("concede acesso")
            if show : sleep(delay/4)
            self.accessGranted = True
            while self.access: # não deixa voltar a processar em quanto a thread de input não termiar a adição do novo processo a lista.
                continue
            if show : print("voltando a processar")
            self.accessGranted = False
            if show : sleep(delay/4)
        else:
            if show : print("sem solicitação de acesso, processando...")
    
    def processing(self): # função que mantem o processamento rodando.
        while not self.stop :
            sleep(delay)
            self.checkAccessRequest()
            if self.n_process > 0:
                self.choice_algorithm()
                # self.show()
            else:
                print("aguardando mais processos...")

def main():
    manager = ProcessManager(path) # cria a lista de processos.
    if show : manager.show()
    Thread_Inputs = threading.Thread(target=manager.new_process, args=())
    Thread_Inputs.start()
    manager.processing()
    if show : manager.show()

#__GLOBAL_ESCOPE__ aqui são definidos as configurações que se recebe por argumento quando executa o código.
print("em caso de duvidas, execute com 'python3 127367.py -h'")
parser = argparse.ArgumentParser(description = "Escalonador de Processos {:>>11} by: Lucas T. G.".format(''))
parser.add_argument('--arquivo', '-a', action = 'store', dest = 'path', 
                required=True, help = "Arquivo e/ou diretorio com os dados de entrada(este argumento é necessário).")
parser.add_argument('--delay', '-d', type=float, action = "store", dest="delay", 
                    required=False, default=0, help="Delay para deixar a simulação mais lenta, e visualizar em tempo real")
parser.add_argument('--show', '-s', type=str, action = "store", dest="show", 
                    required=False, default=False, help="'False': apenas mostra o processo na cpu em dado momento, falso é o valor default. 'True': mostra mais detalhes durante o processo, recomendo botar um valor de pelo menos alguns segundos no argumento delay para utilizar este como True")

args = parser.parse_args()
path = args.path
delay = float(args.delay)
show = args.show == "True" or args.show == 'T'

main()
