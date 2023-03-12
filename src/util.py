'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

util.py
- funciones auxiliares

Autor: Diego Cordova - 20212
*************************************************
'''

def delete_duplicates(arr:list) -> list:
  ''' Elimina los elementos duplicados de un array'''
  newArr:list = []

  for n in arr:
    if n not in newArr:
      newArr.append(n)

  return newArr