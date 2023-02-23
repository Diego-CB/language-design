'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

alfabeto.py
- Definicion de alfabeto para regex

Autor: Diego Cordova - 20212
*************************************************
'''

lower = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z']
upper = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']
digits = ['0','1','2','3','4','5','6','7','8','9']
epsilon = '^'

ALPHABET = lower + upper + digits + [epsilon]
OPERATORS = ['.', '|', '*', '?', '+']