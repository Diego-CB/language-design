'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

util.py
- funciones auxiliares

Autor: Diego Cordova - 20212
*************************************************
'''

def toFileName(filename:str) -> str:
  '''Fromatea una regex para nombre de un archivo'''
  filename = filename.replace('*', '_kleen_')
  filename = filename.replace('+', '_kleen_')
  filename = filename.replace('?', '_kleen_')
  filename = filename.replace('|', '_or_')

  return filename