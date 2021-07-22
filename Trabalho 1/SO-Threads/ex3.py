import threading
from unicodedata import normalize
from os import walk, chdir, mkdir
import glob

def threads_are_working(ThreadsList): #função que verifica se aainda tem threads trabalhando
    for thread in ThreadsList:
        if ( thread.is_alive() ):
            #print("thread viva")
            return True
    print("todas as threads mortas")
    return  False

def most_frequent(List): 
    return max(set(List), key = List.count)

def estatisticas(ThreadID, arquivo):
    _strOut = ""
    arq = open(arquivo, "r").read()
    maiusculo = arq.upper()
    arqM = open("Maiusculas/"+arquivo, 'w')
    arqM.write(maiusculo)
    arqM.close()
    arq = arq.lower() # coloca tudo em minusculo pra contagem de palavras não ser Case-sensitive
    arq = arq.replace("\n", " ") # remove terminos de linha
    arq = arq.replace(",", " ") # remove virgulas
    arq = arq.replace(".", " ") # remove pontos
    arq = arq.replace("  ", " ") #remove espaços duplicados pelas anteriores
    # print(arq)
    arq = normalize('NFKD', arq).encode('ASCII', 'ignore').decode('ASCII') #remove acentuação
    # print(arq)
    arq = arq.split(" ")

    palavras = []
    vogais = []
    consoantes = []

    arq.remove("")
    for palavra in arq:
        if palavra not in palavras :
            palavras.append(palavra)
        for letra in palavra:
            if letra == "a" or letra == "e" or letra == "i" or letra == "o" or letra == "u":
                vogais.append(letra)
            else:
                consoantes.append(letra)
    _strOut += "Thread {:^4}: começou".format(ThreadID) + "\n"
    _strOut += "nome do arquivo: " + arquivo + "\n"
    _strOut += "número de palavras no arquivo: " + str(len(arq)) + "\n"
    _strOut += "número de palavras, sem repetir, no arquivo: " + str(len(palavras)) + "\n"
    _strOut += "número de vogais: " + str(len(vogais)) + "\n"
    _strOut += "número de consoantes: " + str(len(consoantes)) + "\n"
    _strOut += "palavra que mais apareceu no arquivo: " + str(most_frequent(arq)) + "\n"
    _strOut += "vogal que mais apareceu no arquivo: " + str(most_frequent(vogais)) + "\n"
    _strOut += "consoante que mais apareceu no arquivo: "+ str(most_frequent(consoantes)) + "\n"
    print(_strOut)


def criaPasta(path):
    try:
        mkdir(path)
        return True
    except:
        return False

def ex3():
    # files = []
    # path = 'test'
    path = input("informe o diretorio: ")
    criaPasta(path + "/Maiusculas")

    chdir(path)
    ThreadsList = []
    i = 0
    for file in glob.glob("*.txt"):
        x = threading.Thread(target=estatisticas, args=(i, file))
        x.start()
        ThreadsList.append(x)
        i += 1

    u=0
    while (threads_are_working(ThreadsList)): #para o escopo principal seguir só quando as threads terminarem sua execução
        u+=1
ex3()