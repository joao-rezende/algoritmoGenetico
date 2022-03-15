'''
Algoritmo Genético para econtrar valor máximo da função f(x) = x*x - 3x + 4, dentro de determinado limite. [-10, 10]
Desenvolvido por:
    João Vitor Soares Rezende
    Pedro Henrique de Menezes

OBS: Para executar o algoritmo é necessário a instalação das libs importadas
'''
import random
import matplotlib.pyplot as plt
import numpy as np

taxa_crossover = 70
taxa_mutacao = 1
qtd_individuos = 4
qtd_geracoes = 5
qtd_bits = 10
qtd_binarios = (2 ** qtd_bits) - 1
usar_eletismo = True

class Individuo():
    def __init__(self, binario, x, aptidao):
        self.binario = binario
        self.x = x
        self.aptidao = aptidao

    def __str__(self):
        return "    " + self.binario + " | " + str(round(self.x, 2)) + " | " + str(round(self.aptidao, 2))

    def __repr__(self):
        return "\n" + "    " + str(self.binario) + " | " + str(round(self.x, 2)) + " | " + str(round(self.aptidao, 2)) + "\n"

def bin_formatado(i, tamanho):
    s = bin(i)
    return s[2:].zfill(tamanho)

def binario_decimal(binario):
    decimal, i = 0, 0
    binario = int(binario)
    while(binario != 0):
        dec = binario % 10
        decimal = decimal + dec * pow(2, i)
        binario = binario//10
        i += 1
    return -10 + 20 * decimal / (2 ** qtd_bits - 1)

def gerar_populacao_inicial(populacao, qtd_individuos):
    pop_inicial = []
    while len(pop_inicial) != qtd_individuos:
        indice_sorteado = int(random.random() * qtd_binarios)
        individuo = populacao[indice_sorteado]
        pop_inicial.append(Individuo(individuo, binario_decimal(individuo), aptidao(individuo)))

    return pop_inicial

def selecao_torneio(populacao):
    primeiroIndividuo = populacao[random.randrange(0, qtd_individuos)]
    segundoIndividuo = populacao[random.randrange(0, qtd_individuos)]

    return primeiroIndividuo if primeiroIndividuo.aptidao > segundoIndividuo.aptidao else segundoIndividuo 

def aptidao(n):
    n = binario_decimal(n)
    return n*n - 3*n + 4

def crossover(individuo1, individuo2):
    limite_corte = len(individuo1.binario) - 1
    ponto_corte = int(random.random() * (limite_corte - 1) + 1)

    binario1 = individuo1.binario[0:(len(individuo1.binario) - ponto_corte)] + individuo2.binario[-ponto_corte::]
    binario2 = individuo2.binario[0:(len(individuo2.binario) - ponto_corte)] + individuo1.binario[-ponto_corte::]
    filho1 = Individuo(binario1, binario_decimal(binario1), aptidao(binario1))
    filho2 = Individuo(binario2, binario_decimal(binario2), aptidao(binario2))

    return [filho1, filho2]

def mutacao(filhos):
    for individuo in filhos:
        novoValor = ''
        for bit in individuo.binario:
            fazMutacao = random.random() * 100 < taxa_mutacao
            if(fazMutacao and bit == '0'):
                novoValor += '1'
            elif(fazMutacao and bit == '1'):
                novoValor += '0'
            else:
                novoValor += bit
        individuo.binario = novoValor

def gerar_individuos(individuo1, individuo2):
    if(random.random() * 100 < taxa_crossover):
        filhos = crossover(individuo1, individuo2)
    else:
        filhos = [individuo1, individuo2]
    
    mutacao(filhos)
    return filhos

def retorna_melhor(populacao):
    melhor = None
    for individuo in populacao:
        if (melhor == None or melhor.aptidao < individuo.aptidao):
            melhor = individuo
    
    return melhor

def elitismo(populacao, geracao):
    melhor = retorna_melhor(populacao)

    indice_pior = None
    for i in range(len(geracao)):
        individuo = geracao[i]
        if (indice_pior == None or geracao[indice_pior].aptidao > individuo.aptidao):
            indice_pior = i

    geracao[indice_pior] = melhor

    return geracao

#Todos os cromossomos existente para a população
todos_cromossomos = [] 
for y in range(0, qtd_binarios):
    todos_cromossomos.append(bin_formatado(y, qtd_bits))

#Gera a população inicial a partir de um array com todos os cromossomos possível para aquele indíviduo
populacao = gerar_populacao_inicial(todos_cromossomos, qtd_individuos)

print("Indíviduo |       X |   Aptidão ")

print("População inicial")
for individuo in populacao:
    print(individuo)

#Repetição com a quantidade de gerações que for definido para ser gerado
for i in range(qtd_geracoes):
    geracao = []
    #Gerando uma nova geração com a quantidade de indivíduos informada
    while len(geracao) < qtd_individuos:
        individuo = selecao_torneio(populacao)
        individuo_ = selecao_torneio(populacao)
        
        geracao += gerar_individuos(individuo, individuo_)

    #Verificando se será feito o uso do elitismo
    if usar_eletismo:
        populacao = elitismo(populacao, geracao)
    else:
        populacao = geracao

    print('\n-- Geração  ' + str(i+1) + ' --' )
    for individuo in populacao:
        print(individuo)

#Exibindo o gráfico
x = np.linspace(-10, 10, 1000)
y = x**2 - 3*x + 4  
plt.plot(x, y, color='red')

melhor = retorna_melhor(populacao)
plt.title("Valor máximo - f(x) = x² - 3x + 4")
plt.annotate(u'Valor máximo encontrado f(' + str(round(melhor.x, 2)) + ') = ' + str(round(melhor.aptidao, 2)), xy=(melhor.x, melhor.aptidao), xytext=(melhor.x, melhor.aptidao), arrowprops=dict(facecolor='blue',shrink=0.05)) 
plt.show()