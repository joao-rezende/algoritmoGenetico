import random

taxa_crossover = 70
taxa_mutacao = 1

class Individuo():
    def __init__(self, binario, x, aptidao):
        self.binario = binario
        self.x = x
        self.aptidao = aptidao

    def __str__(self):
        aptidao_formatada = "      " + str(self.aptidao)
        x_formatado = "      " + str(self.x)
        return "    " + self.binario + " | " + x_formatado[-7::] + " | " + aptidao_formatada[-9::]

    def __repr__(self):
        aptidao_formatada = "      " + str(self.aptidao)
        x_formatado = "      " + str(self.x)
        return "\n" + "    " + str(self.binario) + " | " + x_formatado[-7::] + " | " + aptidao_formatada[-7::] + "\n"

def bin_formatado(i, tamanho):
    s = bin(i)
    return s[2:].zfill(tamanho)

def gerar_populacao_inicial(populacao, qtd_individuos):
    pop_inicial = []
    while len(pop_inicial) != qtd_individuos:
        indice_sorteado = int(random.random() * 21)
        individuo = populacao[indice_sorteado]
        pop_inicial.append(Individuo(individuo, binario_decimal(individuo), aptidao(individuo)))

    return pop_inicial

def binario_decimal(binario):
    decimal, i = 0, 0
    binario = int(binario)
    while(binario != 0):
        dec = binario % 10
        decimal = decimal + dec * pow(2, i)
        binario = binario//10
        i += 1
    return round(-10 + 20 * decimal / 31, 4)


def aptidao(n):
    n = binario_decimal(n)
    return round(n*n - 3*n + 4, 4)


def crossover(individuo1, individuo2):
    limite_corte = len(individuo1.binario) - 1
    ponto_corte = int(random.random() * (limite_corte - 1) + 1)
    # print("Ponto de corte = " + str(ponto_corte))

    binario1 = individuo1.binario[0:(len(individuo1.binario) - ponto_corte)] + individuo2.binario[-ponto_corte::]
    binario2 = individuo2.binario[0:(len(individuo2.binario) - ponto_corte)] + individuo1.binario[-ponto_corte::]
    filho1 = Individuo(binario1, binario_decimal(binario1), aptidao(binario1))
    filho2 = Individuo(binario2, binario_decimal(binario2), aptidao(binario2))

    return [filho1, filho2]


def gerar_individuos(individuo1, individuo2):
    if(random.random() * 100 < taxa_crossover):
        filhos = crossover(individuo1, individuo2)
    else:
        filhos = [individuo1, individuo2]
    
    mutacao(filhos)
    return filhos

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

def selecaoTorneio(populacao):
    primeiroIndividuo = populacao[random.randrange(0,4)]
    segundoIndividuo = populacao[random.randrange(0,4)]

    return primeiroIndividuo if primeiroIndividuo.aptidao > segundoIndividuo.aptidao else segundoIndividuo 

def elitismo(populacao):
    melhor = None
    for individuo in populacao:
        if (melhor == None or melhor.aptidao < individuo.aptidao):
            melhor = individuo
    
    return melhor
x = []

for y in range(0, 21):
    x.append(bin_formatado(y, 5))

populacao = gerar_populacao_inicial(x, 30)

melhor_individuo = None
segundo_melhor_individuo = None
melhor = None
segundo_melhor = None

print("Indíviduo |       X |   Aptidão ")

print("População inicial")
for individuo in populacao:
    print(individuo)

for i in range(20):
    geracao = []
    while len(geracao) < 29:
        individuo = selecaoTorneio(populacao)
        individuo_ = selecaoTorneio(populacao)
        
        geracao += gerar_individuos(individuo, individuo_)
    
    print('\n-- Geração ' + str(i+1) + ' --' )
    for individuo in geracao:
        print(individuo)

    geracao.append(elitismo(populacao))
    
    populacao = geracao
