# -- coding: utf-8 --
"""
Created on Thu Jun  2 22:23:49 2022

@author: RHR
"""

import numpy as np


def bin_to_poly(x):
    # Função que transforma numero binário em polinomio
    y = bin_to_list(x)
    poly = np.poly1d(y)
    return poly


def poly_to_bin(x):
    # Função que transforma polinimio em numero binário
    list_ = poly_to_list(x)
    return list_to_bin(list_)


def poly_to_list(x):
    # Função que transforma polinomio em lista
    bin_ = x.coef
    bin_ = bin_.astype(int)
    return bin_.tolist()


def bin_to_list(x):
    # Função que transforma binário em lista
    return [int(d) for d in str(bin(x))[2:]]


def list_to_bin(x):
    # Função que transforma lista em binário
    num = 0
    for b in x:
        num = 2 * num + b
    return num


def list_to_poly(x):
    # Função que transforma lista em polinomio
    return np.poly1d(x)


def field_multiplication(lst1, lst2, primitive):
    # Função que faz multiplicação em campos finitos
    tmp = poly_to_list(np.polymul(list_to_poly(lst1), list_to_poly(lst2)))
    tmp = [1 if x % 2 == 1 else 0 for x in tmp]
    checkbits = tmp.copy()
    tmp_gx = primitive.copy()
    while(len(checkbits) >= len(primitive)):
        while(len(tmp_gx) != len(checkbits) - checkbits.index(1)):
            tmp_gx.append(0)
        checkbits = bin_to_list(list_to_bin(checkbits) ^ list_to_bin(tmp_gx))
        tmp_gx = primitive.copy()
    #print(checkbits)
    return checkbits

def field_mod(lst1,lst2):
     # Função que faz multiplicação em campos finitos
     #tmp = poly_to_list(np.polymul(list_to_poly(lst1), list_to_poly(lst2)))
     #tmp = [1 if x % 2 == 1 else 0 for x in tmp]
     checkbits = lst1.copy()
     tmp_gx = lst2.copy()
     while(len(checkbits) >= len(lst2)):
         while(len(tmp_gx) != len(checkbits) - checkbits.index(1)):
             tmp_gx.append(0)
         checkbits = bin_to_list(list_to_bin(checkbits) ^ list_to_bin(tmp_gx))
         tmp_gx = lst2.copy()
     #print(checkbits)
     return checkbits

def field_addiction(lst1, lst2):
    # Função que faz adição em campos finitos
    tmp = bin_to_list(list_to_bin(lst1) ^ list_to_bin(lst2))
    tmp = [1 if x % 2 == 1 else 0 for x in tmp]
    while(len(tmp) != 5):
        tmp.insert(0, 0)
    return (tmp)


def field_inverse(lst1):
    # Função que calcula inverso em campos finitos
    for i in range(1, 32):
        r = field_multiplication(lst1, field[i], primitive)
        if r == [1]:
            return field[i]


def find_exp(lst1):
    # Função que retorna o expoente de alpha a partir de uma lista
    while(len(lst1) != 5):
        lst1.insert(0, 0)
    for i in range(1, 32):
        if lst1 == field[i]:
            return i-1


def lst_by_alpha(x):
    # Função que retorna a lista correspondente ao expoente de alph
    return field[x+1]


def create_field(field):
    # Cria o field de 32 elementos
    field = []
    field.append([0, 0, 0, 0, 0])
    field.append([0, 0, 0, 0, 1])

    p2 = 0b10
    for i in range(30):   # MUDAR ESSE 30 PRA UM VALOR GENERICO
        quotient, remainder = np.polydiv(
            bin_to_poly(p2), list_to_poly(primitive))
        lst = poly_to_list(remainder)
        lst = [1 if x % 2 == 1 else 0 for x in lst]
        while len(lst) != 5:
            lst.insert(0, 0)
        field.append(lst)
        p2 = p2 << 1
    return field


# Define o polinomio primitivo
primitive = [1, 0, 0, 1, 0, 1]

# Inicia e preenche o campo finito GF(32)
field = []
field = create_field(field)


# CODIFICAÇÃO
# Polinomios minimos (tabelados)
m1 = [1, 0, 0, 1, 0, 1]
m3 = [1, 1, 1, 1, 0, 1]
m5 = [1, 1, 0, 1, 1, 1]

# g(x) é o polinomio gerador, feito da multiplicação dos polinomios minimos
gx_temp = np.polymul(list_to_poly(m1), list_to_poly(m3))
gx_temp = np.polymul(gx_temp, list_to_poly(m5))
gx = poly_to_list(gx_temp)
# As potencias de g(x) que tem valor par são zeradas
gx = [1 if x % 2 == 1 else 0 for x in gx]



# Informação a ser enviada
word = 0b1000001
print("Palavra a ser enviada:")
print(bin(word))
information = bin_to_list(word)

gerador = ""
for i in range(len(gx)):
    if(gx[i] == 1):
        gerador += "x^" + str(len(gx)- i-1)
        gerador += " "

print("-------------------------------------")
print("Polinomio gerador:")
print(gerador)
print("-------------------------------------")

# Preenche a informação até ficar do tamanho do pacote de 16 bits
while len(information) != 16:
    information.insert(0, 0)

# Preenche o pacote com o numero de zeros
# equivalente ao grau do polinomio gerador
word_filed = information.copy()
for i in range(len(gx)-1):
    word_filed.append(0)

# Realiza divisão usando artimética binária, dividindo o pacote preenchido
# pelo polinomio gerador
# Os checkbits que são enviados com a mensagem são o resto da divisão

tmp_gx = gx.copy()
checkbits = word_filed.copy()

while(list_to_bin(checkbits) > list_to_bin(gx)):
    while(len(tmp_gx) != len(checkbits) - checkbits.index(1)):
        tmp_gx.append(0)
    checkbits = bin_to_list(list_to_bin(checkbits) ^ list_to_bin(tmp_gx))
    tmp_gx = gx.copy()

# msg é a mensagem codificada
print("Pacote envido:")
msg = information + checkbits
print(bin(list_to_bin(msg))[2:].zfill(31))
print("-------------------------------------")

# DECODIFICAÇÃO

# ****************************************************************************
# bits que mudaram seu estado durante o envio
# (Esquerda para direita)
changed_bits = [4, 9, 22]

# ****************************************************************************


recebido = msg.copy()

for element in changed_bits:
    if recebido[element-1] == 1:
        recebido[element-1] = 0
    else:
        recebido[element-1] = 1
recebido = list_to_bin(recebido)

# Vx é a mensagem recebida
vx = bin_to_list(recebido)
vb = vx.copy()
print("Pacote recebido:")
print(bin(list_to_bin(vx))[2:].zfill(31))

mostrador = ""
for i in range(31):
    flag = 0
    for element in changed_bits:
        if i+1 == element:
            mostrador += "^"
            flag = 1
    if(flag == 0):
        mostrador += " "
    else:
        flag = 0
print(mostrador)
print("-------------------------------------")

# Polinomios minimos (tabelados)
minimal_polys = []
minimal_polys.append(m1)
minimal_polys.append(m1)
minimal_polys.append(m3)
minimal_polys.append(m1)
minimal_polys.append(m5)
minimal_polys.append(m3)

# Calcula as 6 expressoes das sindromes em função de x são obtidas atraves
# da divisão polinomial de v(x) (mensagem recebida) pelo polinomio minimo
# respectivo
sindromes_x = []
for i in range(6):

    #quotient, remainder = np.polydiv(list_to_poly(vx),
    #                                 list_to_poly(minimal_polys[i]))
    #s1x = poly_to_list(remainder)
    s1x = field_mod(vx,minimal_polys[i])
    s1x = [1 if x % 2 == 1 else 0 for x in s1x]
    while(len(s1x) <5):
        s1x.insert(0,0)
    sindromes_x.append(s1x)

# Calcula as 6 expressoes das sindromes em função de alpha são obtidas
# substituindo alpha^n na sindrome(x) encontrada anteriormente
sindromes_a = []
for index, sindrome in enumerate(sindromes_x):
    tmp = sindrome.copy()
    s = [0, 0, 0, 0, 0]
    for i in range(len(tmp)-1):
        tmp[i] = sindromes_x[index][i] * (index+1) * (len(tmp)-i-1)
        if(tmp[i] != 0):
            s = [sum(value) for value in zip(s, field[tmp[i]+1])]
    if(sindromes_x[index][len(s1x)-1] == 1):
        s[len(sindromes_x[index])-1] = 1
    s = [1 if x % 2 == 1 else 0 for x in s]
    sindromes_a.append(s)


# COMEÇA A PREENCHER A TABELA DE DECODIFICAÇÃO

# Coeficientes de alpha da equação final de localização de erros
sigma = [0, 0, 0, 0]


# PARA U = 0
sigma[2] = find_exp(sindromes_a[0])
sigma[3] = 1

d_up1 = field_addiction(sindromes_a[2],
                        field_multiplication(
                            sindromes_a[0], sindromes_a[1],
                            primitive))

# PARA U = 1

sigma[1] = find_exp(field_multiplication(d_up1,
                                         field_inverse(sindromes_a[0]),
                                         primitive))

d_up2 = field_addiction(sindromes_a[4],
                        field_multiplication(
                            lst_by_alpha(sigma[2]), sindromes_a[3],
                            primitive))
d_up2 = field_addiction(d_up2,
                        field_multiplication(
                            lst_by_alpha(sigma[1]), sindromes_a[2],
                            primitive))

# PARA U = 2
tmp = field_multiplication(d_up2, field_inverse(d_up1), primitive)  # alpha25

sigma[0] =  find_exp(
    field_multiplication(tmp, lst_by_alpha(sigma[2]), primitive))

sigma[1] = find_exp(field_addiction(lst_by_alpha(sigma[1]), tmp))

print("Polinomio localizador de erros:")
pol = ""
for i in range(len(sigma)):
    pol += "α^" + str(sigma[i])
    pol += " * x^" + str(3-i)
    if(i != len(sigma)-1):
        pol += " + "

print(pol)
print("-------------------------------------")

roots = []

# Calcula as raizes do polinomio localizador de erros
for i in range(0, 30):
    r = field_multiplication(lst_by_alpha(i), lst_by_alpha(i), primitive)
    rr = field_multiplication(r, lst_by_alpha(i), primitive)
    rrr = field_multiplication(rr, lst_by_alpha(sigma[0]), primitive)
    s = field_multiplication(r, lst_by_alpha(sigma[1]), primitive)
    t = field_multiplication(lst_by_alpha(sigma[2]),
                             lst_by_alpha(i), primitive)
    u = field_addiction(rrr, s)
    u = field_addiction(u, t)
    u = field_addiction(u, [1])
    if(u == [0, 0, 0, 0, 0]):
        roots.append(i)

print("Raizes do polinomio:")

raizes = ""
for i in range(len(roots)):
    raizes += "α^" + str(roots[i])
    raizes += ", "

print(raizes)
print("-------------------------------------")

while(len(vx) != 31):
    vx.insert(0, 0)

# Corrige a mensagem de acordo com as raizes do polinomio localizador de
# erros
for i in range(len(roots)):
    if vx[roots[i]-1] == 1:
        vx[roots[i]-1] = 0
    else:
        vx[roots[i]-1] = 1

print("Mensagem corrigida:")
print(bin(list_to_bin(vx))[2:].zfill(31))
print(mostrador)
