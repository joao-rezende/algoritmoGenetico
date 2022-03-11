import random

taxa_crossover = 70
taxa_mutacao = 1


def bin_formatado(i, tamanho):
    s = bin(i)
    return s[2:].zfill(tamanho)


def gerar_populacao_inicial(populacao, qtd_individuos):
    pop_inicial = []
    while len(pop_inicial) != qtd_individuos:
        indice_sorteado = int(random.random() * 21)

        existe = False
        for ind in pop_inicial:
            if (populacao[indice_sorteado] == ind):
                existe = True

        if(not existe):
            pop_inicial.append(populacao[indice_sorteado])

    return pop_inicial


def binario_decimal(binary):
    decimal, i, n = 0, 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal


def aptidao(n):
    n = binario_decimal(int(n))
    n -= 10
    return n*n - 3*n + 4


def crossover(individuo1, individuo2):
    limite_corte = len(individuo1) - 1
    ponto_corte = int(random.random() * (limite_corte - 1) + 1)
    print("Ponto de corte = " + str(ponto_corte))

    filho1 = individuo1[0:(len(individuo1) - ponto_corte)] + individuo2[-ponto_corte::]
    filho2 = individuo2[0:(len(individuo2) - ponto_corte)] + individuo1[-ponto_corte::]

    return [filho1, filho2]


def evoluir(individuo1, individuo2):
    if(random.random() * 100 < taxa_crossover):
        filhos = crossover(individuo1, individuo2)
    else:
        filhos = [individuo1, individuo2]
    
    return filhos


x = []

for y in range(0, 21):
    x.append(bin_formatado(y, 5))


populacao_inicial = gerar_populacao_inicial(x, 4)

melhor_individuo = None
segundo_melhor_individuo = None
melhor = None
segundo_melhor = None

print("População inicial")
print("Indíviduo | Aptidão")
for individuo in populacao_inicial:
    aptidao_individuo = aptidao(individuo)

    if (melhor == None or melhor < aptidao_individuo):
        segundo_melhor_individuo = melhor_individuo
        segundo_melhor = melhor
        melhor_individuo = individuo
        melhor = aptidao_individuo
    elif (segundo_melhor == None or segundo_melhor < aptidao_individuo):
        segundo_melhor_individuo = individuo
        segundo_melhor = aptidao_individuo

    aptidao_formatada = "      " + str(aptidao_individuo)
    print("    " + individuo + " | " + aptidao_formatada[-7::])

print("\nOs melhores indíviduos desta geração")
print("Melhor = " + melhor_individuo)
print("Segundo melhor = " + segundo_melhor_individuo)

[filho1, filho2] = evoluir(melhor_individuo, segundo_melhor_individuo)
print(filho1, filho2)

# print(x[20])
