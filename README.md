# Lab E: YAPar

## 📡 Tecnologias Utilizadas

- Python 🐍: Modern syntax, Interpreted Languaje
  > Python 10.0 or higher needed

## ✅ Rúbrica

- [ ] Correcta interpretación de un archivo de especificación YAPar.
- [ ] Validación de tokens provistos en archivo de especificación de YAPar con el
output generado por YALex.
- [ ] Cálculo de funciones asociadas sobre la gramática provista: FIRST, FOLLOW
y CLOSURE.
- [ ] Generación de elementos de nodos de autómata LR(0) y construcción del
autómata LR(0).

## 🗃️ Estructura de Archivos

- ***`src`***

  - `Automata.py`: Objectos Automatas y funcionalidades de los mismos
  - `drivers.py`: implemetaciones de pipelines (API)

  - ***`Lexer`***
    - `postfix.py`: Implementación del algoritmo shunting yard para conversion de infix a postfix para regex.
    - `util.py`: funcinones auxiliares
    - `Tree.py`: Implementación de arbol de sintaxis y followpos.
    - `Thompson.py`: Implementación de algoritmo de Thompson para construccion de AFN's.
    - `Subconjuntos.py`: Implementación de algoritmo de construccion de subconjuntos.
    - `DirectCons.py`: Implementación de algoritmo de construccion directa de AFD.
    - `Min.py`: Implementación de algoritmo de minimizacion de AFD.
    - `YalexScanner.py`: Lectura de archivos .yal

  - ***`Parser`***
    - `YaparProcessor.py`: Procesa los tokens de los archivos yapar
    - `YaparReader.py`: Lector de archivos *Yapl*

- ***`out`***: Dentro de esta carpeta se encuentran los archivos resultantes de las ejecuciones.
  - `AFD.png`: Grafo de AFD resultante para el Lexer.
  - `tokens.txt`: Tokens leidos por le scanner

- ***`Examples`***: 
  - ***`input`***: Ejemplos de archivos de entrada para el Scanner.
  - ***`yalex`***: Ejemplos de archivos yalex para lectura.
  - ***`yapar`***: Ejemplos de archivos yapar para lectura.

- `main.py`: Programa principal (Driver Program).

## 🕹️ Getting Started

1. Instale las dependencias del projecto ejecutando `pip install -r requirements.txt`
2. Ejecute el archivo `main.py` escribiendo como argumento el path al archivo yalex a leer.
    > Ejemplo: py main.py *Archivo.yal*

3. Se crearan varias carpetas `__pycache__` con compilados del codigo.
4. Se crearan los siguientes archivos con el autput de la lectura del archivo YALex:
     - `./out/steps.txt`
     - `./out/tree.txt`
     - `./out/AFD.png`
     - `./Scanner.py`

5. Ejecute el archivo `Scanner.py` escribiendo como argumento el path al archivo *input* a leer.
    > Ejemplo: py Scanner.py *./Examples/input/ejemplo.txt*

6. Se desplegará el listado de ***Tokens*** y/o ***Errores Lexicos*** encontrados en el archivo *input*

## 🤓 Autor

Diego Cordova - 20212
