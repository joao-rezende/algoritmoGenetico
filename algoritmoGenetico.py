import random

taxa_crossover = 70
taxa_mutacao = 1

class Individuo():
    def __init__(self, valor, aptidao):
        self.valor = valor
        self.aptidao = aptidao

    def __str__(self):
        aptidao_formatada = "      " + str(self.aptidao)
        return "    " + self.valor + " | " + aptidao_formatada[-7::]

    def __repr__(self):
        aptidao_formatada = "      " + str(self.aptidao)
        return "\n" + "    " + str(binario_decimal(self.valor)) + " | " + aptidao_formatada[-7::] + "\n"

def bin_formatado(i, tamanho):
    s = bin(i)
    return s[2:].zfill(tamanho)

def gerar_populacao_inicial(populacao, qtd_individuos):
    pop_inicial = []
    while len(pop_inicial) != qtd_individuos:
        indice_sorteado = int(random.random() * 21)
        individuo = populacao[indice_sorteado]
        pop_inicial.append(Individuo(individuo, aptidao(individuo)))

    return pop_inicial

def binario_decimal(binary):
    decimal, i, n = 0, 0, 0
    binary = int(binary)
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal - 10


def aptidao(n):
    n = binario_decimal(n)
    return n*n - 3*n + 4


def crossover(individuo1, individuo2):
    limite_corte = len(individuo1.valor) - 1
    ponto_corte = int(random.random() * (limite_corte - 1) + 1)
    print("Ponto de corte = " + str(ponto_corte))

    valor1 = individuo1.valor[0:(len(individuo1.valor) - ponto_corte)] + individuo2.valor[-ponto_corte::]
    valor2 = individuo2.valor[0:(len(individuo2.valor) - ponto_corte)] + individuo1.valor[-ponto_corte::]
    filho1 = Individuo(valor1, aptidao(valor1))
    filho2 = Individuo(valor2, aptidao(valor2))

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
        for bit in individuo.valor:
            fazMutacao = random.random() * 100 < taxa_mutacao
            if(fazMutacao and bit == '0'):
                novoValor += '1'
            elif(fazMutacao and bit == '1'):
                novoValor += '0'
            else:
                novoValor += bit
        individuo.valor = novoValor

def selecaoTorneio(populacao):
    primeiroIndividuo = populacao[random.randrange(0,4)]
    segundoIndividuo = populacao[random.randrange(0,4)]

    return primeiroIndividuo if primeiroIndividuo.aptidao > segundoIndividuo.aptidao else segundoIndividuo 

x = []

for y in range(0, 21):
    x.append(bin_formatado(y, 5))

populacao = gerar_populacao_inicial(x, 30)

melhor_individuo = None
segundo_melhor_individuo = None
melhor = None
segundo_melhor = None

print("População inicial")
print("Indíviduo | Aptidão")
for individuo in populacao:
    print(individuo)

for i in range(20):
    geracao = []
    while len(geracao) < 30:
        individuo = selecaoTorneio(populacao)
        individuo_ = selecaoTorneio(populacao)
        
        geracao += gerar_individuos(individuo, individuo_)
    print('-- Geração ' + str(i+1) + ' --' )
    print(geracao)

# print(x[20])
