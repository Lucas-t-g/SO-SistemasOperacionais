import logging
import threading
from time import sleep
import numpy as np
from random import randint

class Conta: # nomes das funções das classes ja são bem autoexplicativos
    def __init__(self, IDconta, saldo = 0):
        self.IDconta = IDconta
        self.saldo = saldo
    
    def credito(self, valor):
        self.saldo += valor
    
    def debito(self, valor):
        self.saldo -= valor

    def show(self):
        print("Conta n: {:<10}; saldo: {:>16}".format(self.IDconta, self.saldo))

class Banco:
    def __init__(self, numero_de_contas, saldo = []):
        self.qtdContas = numero_de_contas
        self.contas = []
        for i in range(numero_de_contas):
            saldo_temp = 0
            if( len(saldo) > i ):
                saldo_temp = saldo[i]
            self.contas.append( Conta(IDconta=i, saldo=saldo_temp) )
    
    def show(self):
        print('{0:-<45}'.format('-'))
        for conta in self.contas:
            conta.show()
        print('{0:-<45}'.format('-'))
    
    def consulta(self, IDconta):
        for conta in self.contas:
            if conta.IDconta == IDconta:
                return conta.saldo
    
    def credito(self, IDconta, valor):
        for conta in self.contas:
            if conta.IDconta == IDconta:
                conta.credito(valor)
                break
    
    def debito(self, IDconta, valor):
        for conta in self.contas:
            if conta.IDconta == IDconta:
                conta.debito(valor)
                break

def threads_are_working(ThreadsList): #função que verifica se ainda tem threads trabalhando
    for thread in ThreadsList:
        if ( thread.is_alive() ):
            #print("thread viva")
            return True
    print("todas as threads mortas")
    return False

def printgerencia(gerencia): #esta função apenas printa de forma mais organizada o conteudo do vetor 'gerencia'
    global num_thread
    aux = ["Threads", "requisição", "atendido", "operacao"]
    aux2 = [list(range(num_thread))]+gerencia
    for linha in aux2:
        _str = "{:>10}: ".format(aux.pop(0))
        for elem in linha:
            if type(elem) == bool and elem == False: elem  = "False"
            if type(elem) == int and elem == 0: elem  = "0"
            _str += "{:^7}".format(elem)
        print(_str)
    # print(gerencia)
    print("\n")

def gerente(): # define qual thread pode fazer operações sobre sobre cada conta, mexendo na segunda linha do array 'gerencia'
                    #apenas o gerente mexe nessa linha de 'gerencia', as outras são para as threads fazerem suas requisições
    global gerencia, ThreasList, lista_de_eventos, delay
    while True:
        if not threads_are_working(ThreadsList): return 0 # se as threads que fazem requsições ja tiverem terminado esta fecha.
        # print(lista_de_eventos)
        printgerencia(gerencia) # mostra o array de requisições antes da iteração do gerente
        for i in range(len(gerencia[0])): # percorre as solicitações de acesso
            if gerencia[0][i] != False: # verifica se acesso foi solicitado
                if gerencia[2][i] in ['d', 'c']:
                    ocupada = False
                    for j in range(len(gerencia[0])): # verifica se acesso solicitado está ocupado
                        if gerencia[1][j] == gerencia[0][i]: # testa se a conta solicitada está ocupada
                            ocupada = True
                            break
                    if not ocupada:
                        gerencia[1][i] = gerencia[0][i] # atende a requisição
                        # lista_de_eventos[i].set() # não funcionou


                if gerencia[2][i] == 'l': # procedimento para leitura do saldo é diferente das outras operaçoes, só preciso ver se 
                    ocupada = False          # nenhuma outra thread esta fazendo uam operação que não seja leitura na mesma conta
                    for j in range(len(gerencia[0])): # verifica se acesso solicitado está ocupado
                        if gerencia[1][j] == gerencia[0][i] and gerencia[2][j] != 'l': # testa se a conta solicitada está ocupada
                            ocupada = True
                            break
                    if not ocupada:
                        gerencia[1][i] = gerencia[0][i] # atende a requisição
                        # lista_de_eventos[i].set() # não funcionou
            else:
                gerencia[1][i] = False # se a thread requisitora sinaliza que ja terminou, tira a licença da thread

        printgerencia(gerencia) # mostra o array de requisições depois da iteração do gerente
        sleep(delay) # para a simuação não ficar muito rápida

def posso_acessar(ThreadID, contaID, operacao): # função que a thread chama para saber se pode acessar determinada conta
    global gerencia,lista_de_eventos
    if operacao not in ['l', 'd', 'c']: return False
    gerencia[0][ThreadID] = contaID # deixa sua requisição no array de requisições
    gerencia[2][ThreadID] = operacao # especifica a operação requisitada
    while True:
        if gerencia[0][ThreadID] == gerencia[1][ThreadID]: # verifica se a solicitação foi atendida para efetuar a operação
            return True             # serve como o as funções wait e set que não funcionaram, não encontrei as funções sleep e wakeup.
    # lista_de_eventos[ThreadID].clear() # não funciou
    # lista_de_eventos[ThreadID].wait() # não funcionou

def fim_acesso(ThreadID, contaID): # aqui a thread chama para sinalizar que terminou sua operação
    global gerencia
    gerencia[0][ThreadID] = False # retira as flags de requisição
    gerencia[2][ThreadID] = False
    while True:
        if False == gerencia[1][ThreadID]:  # verifica se a esta liberado pra seguir pra proxima operação
            return True           # serve como o as funções wait e set que não funcionaram, não encontrei as funções sleep e wakeup.
    # lista_de_eventos[ThreadID].clear() # não funciou
    # lista_de_eventos[ThreadID].wait() # não funcionou


def ThreadOperador(ThreadID, NuBank): # thread que opera sobre as contas,fazendo requisições de operação
    global historico, delay, num_op
    nops = 0
    while True :
        nops += 1
        if nops -1== num_op: break # para parar apos algumas operações realizadas
        operacao = randint(0, 2) # sorteia qual operação será feita, 0 = credito, 1 = debito, 2 = consulta do saldo
        operacaostr = ['c', 'd', 'l'][operacao]
        contaID = randint(0, len(NuBank.contas)-1) # sorteia em qual conta vai fazer operação
        valor = randint(1, 100) # sorteia o valor caso seja operação de credito ou debito
        
        if operacao == 2 and posso_acessar(ThreadID, contaID, operacaostr): # CONSULTA
            historico[ThreadID].append([contaID, "consulta", NuBank.consulta(contaID)]) # adiciona direto no seu histórico a consulta
    
        elif operacao in [0, 1] and posso_acessar(ThreadID, contaID, operacaostr):
            if operacao == 0: # CREDITO
                NuBank.credito(contaID, valor) # faz a alteração na conta
                historico[ThreadID].append([contaID, "credito", valor]) # salva no histórico a operação feita

            elif operacao == 1: #DEBITO
                NuBank.debito(contaID, valor) # faz a alteração na conta
                historico[ThreadID].append([contaID, "debito", valor]) # salva no histórico a operação feita

        sleep(delay/2) # dorme para a 'simulação nao ser tão rapida
        fim_acesso(ThreadID, contaID) # remove a requisição do array de requisições
        sleep(delay/2)
    return

# __DEFINIÇÃO DE VARIAVEIS GLOBAIS__

num_op = 3 # quantas operações cada thread deve fazer, -1 para operações infinitas
delay = 2 # valor utilizado em sleep(delay) pra 'simulação' não ser tão rapida, pode ser float.
num_thread = 6 # número de threads a ser usado na 'simulação', precisa ser um inteiro
num_contas = 5 # número de contas no banco a ser usado na 'simulação', precisa ser um inteiro
saldo_inicial = [4000, 4000, 4000, 4000, 4000] # saldo inicial para as contas do banco, 
                            # não precisa ter um saldo para cada conta, caso crie 10 contas e a lista tenha 5 saldos,
                            # as 5 primeiras contas teram os saldos da lista, o resto teral saldo inicial igual a 0
                            # pode estar vazia tambem, ai todasiniciam zeradas.
num_op = int(input("quantas operações cada thread deve fazer, -1 para operações infinitas: "))
delay = float(input("valor utilizado em sleep(delay) pra 'simulação' não ser tão rapida, pode ser float: "))
num_thread = int(input("número de threads a ser usado na 'simulação', precisa ser um inteiro: "))
num_contas = int(input("número de contas no banco a ser usado na 'simulação', precisa ser um inteiro: "))


gerencia = []
for i in range(3): # cada coluna é uma thread, a primeira linha é qual conta a thread quer acessar,
    gerencia.append([])     # a segunda linha é se ela pode acessar a terceira linha é a operação, 
    for j in range(num_thread): gerencia[i].append(False) #'l' para leitura e 'd' para debito e 'c' para credito.
        
historico = [] # cada operação feita pelas threads adicionada neste vetor, que é printado no final da 'simulação'.
for i in range(num_thread): historico.append([]) # o vetor historico tem o tamanho igual au número de threads, 
                                    # cada elemento é outro vetor onde cada thread adiciona seu histórico na posição corespondente
ThreadsList = []
lista_de_eventos = []
for i in range(num_thread):
    lista_de_eventos.append(threading.Event())

def main():
    NuBank = Banco(num_contas, saldo_inicial) # cria um banco com 5 contas e 4000 de saldo em cada uma
    # NuBank.show()
    # print(gerencia)
    i = 0
    for i in range(num_thread):
        x = threading.Thread(target=ThreadOperador, args=(i, NuBank))
        x.start()
        ThreadsList.append(x)
        i += 1

    gerente()
    NuBank.show()
    i = 0
    for threadhist in historico: # mostra o historico de cada thread
        print("Thread: ", i)
        for op in threadhist:
            print(op)
        print("\n")
        i += 1

main()