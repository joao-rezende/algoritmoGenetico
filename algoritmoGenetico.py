from contextlib import nullcontext
from logging import NullHandler
import random
def bin_formatado(i, tamanho):
    s = bin(i)
    return s[2:].zfill(tamanho)

def gerar_populacao_inicial(populacao, qtd_individuos):
    pop_inicial = []
    for i in range(0, qtd_individuos):
        indice_sorteado = int(random.random() * 21)

        existe = False
        for ind in pop_inicial:
            if (populacao[indice_sorteado] == ind):
                existe = True

        if(not existe):
            pop_inicial.append(populacao[indice_sorteado])
        else:
            i = i - 1

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


x = []

for y in range(0, 21):
    x.append(bin_formatado(y, 5))


populacao_inicial = gerar_populacao_inicial(x, 4)

pai = None
mae = None
melhor = None
segundo_melhor = None

print("População inicial")
print("Indíviduo | Aptidão")
for individuo in populacao_inicial:
    aptidao_individuo = aptidao(individuo)

    if (melhor == None or melhor < aptidao_individuo):
        mae = pai
        segundo_melhor = melhor
        pai = individuo
        melhor = aptidao_individuo
    elif (segundo_melhor == None or segundo_melhor < aptidao_individuo):
        mae = individuo
        segundo_melhor = aptidao_individuo

    aptidao_formatada = "      " + str(aptidao_individuo)
    print("    " + individuo + " | " +  aptidao_formatada[-7::])

print(pai)
print(mae)

# print(x[20])