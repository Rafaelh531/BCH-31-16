# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 22:23:49 2022

@author: RHR
"""


import numpy as np
import pandas as pd
import math

#Função que transforma numero binário em polinomio
def bin_to_poly(x):
  y = bin_to_list(x)
  poly = np.poly1d(y)
  return poly


#Função que transforma polinimio em numero binário
def poly_to_bin(x):
    list_ = poly_to_list(x)
    return list_to_bin(list_)

   
# Função que transforma polinomio em lista
def poly_to_list(x):
    bin_ = x.coef
    bin_ = bin_.astype(int)
    return bin_.tolist()

# Função que transforma binário em lista
def bin_to_list(x):
    return [int(d) for d in str(bin(x))[2:]]  

def list_to_bin(x):
    num = 0
    for b in x:
        num = 2 * num + b
    return num

def list_to_poly(x):
    return np.poly1d(x)

#primitive = 0b100101
primitive = [1,0,0,1,0,1]

#cria o field de 32 elementos
x = [0]
field = []
field.append([0,0,0,0,0])
field.append([0,0,0,0,1])

p2 = 0b10
for i in range(30): #MUDAR ESSE 30 PRA UM VALOR GENERICO
    quotient, remainder = np.polydiv(bin_to_poly(p2), list_to_poly(primitive))
    lst = poly_to_list(remainder)
    lst = [1 if x % 2 == 1 else 0 for x in lst]
    while len(lst) != 5:
        lst.insert(0,0)
    field.append(lst)
    p2 = p2 << 1
   
   

# CODIFICAÇÃO
m1 = [1,0,0,1,0,1]
m3 = [1,1,1,1,0,1]
m5 = [1,1,0,1,1,1]

gx_temp = np.polymul(list_to_poly(m1),list_to_poly(m3))
gx_temp = np.polymul(gx_temp,list_to_poly(m5))
gx = poly_to_list(gx_temp)
gx = [1 if x % 2 == 1 else 0 for x in gx]
#print(gx)


word = 0b1000001

information = bin_to_list(word)


while len(information) != 16:
    information.insert(0,0)

word_filed = information.copy()
for i in range(len(gx)-1):
    word_filed.append(0)
   
#quotient, remainder = np.polydiv(list_to_poly(word_filed), list_to_poly(gx))
#print(gx)
#while len(gx) != len(word_filed)-word_filed.index(1):
#    gx.append(0)

#print(gx)
#print(gx)
tmp_gx = gx.copy()
#print(gx)
checkbits = word_filed.copy()

while(list_to_bin(checkbits)>list_to_bin(gx)):
     while(len(tmp_gx) != len(checkbits) - checkbits.index(1)):
         tmp_gx.append(0)
     #print(tmp_gx)
     checkbits = bin_to_list(list_to_bin(checkbits)^list_to_bin(tmp_gx))
     tmp_gx = gx.copy()
     
     

# =============================================================================
# print("INFORMATION = ") 
# print(information) 
# print("CHECKBITS = ")
# print(checkbits) 
# 
# =============================================================================

#DECODIFICAÇÃO

m2 = m4 = m1
m6 = m3


#vx = information + checkbits
t = 0b0001000011000001100100000100010
vx = bin_to_list(t)


quotient, remainder = np.polydiv(list_to_poly(vx), list_to_poly(m1))
s1x = poly_to_list(remainder)
s1x = [1 if x % 2 == 1 else 0 for x in s1x]
s2x = s1x.copy()
s4x = s1x.copy()

quotient, remainder = np.polydiv(list_to_poly(vx), list_to_poly(m3))
s3x = poly_to_list(remainder)
s3x = [1 if x % 2 == 1 else 0 for x in s3x]
s6x = s3x.copy()

quotient, remainder = np.polydiv(list_to_poly(vx), list_to_poly(m5))
s5x = poly_to_list(remainder)
s5x = [1 if x % 2 == 1 else 0 for x in s5x]

tmp = s3x.copy()
s3a = [0,0,0,0,0]
for i in range(len(tmp)-1):
    tmp[i] = s3x[i]*3* (len(tmp)-i-1)
    print(tmp[i])
    print(field[tmp[i]+1])
    #print(s3a)
    if(tmp[i] != 0):
        s3a = [sum(value) for value in zip(s3a, field[tmp[i]+1])]
if(s3x[len(s3x)-1]==1):
    s3a[len(s3x)-1] = 1        
s3a = [1 if x % 2 == 1 else 0 for x in s3a]



