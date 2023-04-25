# Lab D: Lexer

## 📡 Tecnologias Utilizadas

- Python 🐍: Modern syntax, Interpreted Languaje
  > Python 10.0 or higher needed

## ✅ Rúbrica

- [x] Procesamiento de Archivo de Entrada [identificación de errores].
- [ ] Generación y correcta compilación [interpretación] de Analizador Léxico.
- [ ] Generación de Scanner e identificación de Tokens [ 4 archivos .yal].

## 🗃️ Estructura de Archivos

- ***`src`***

  - `alfabeto.py`: Definicion de alfabeto para regex.
  - `postfix.py`: Implementación del algoritmo shunting yard para conversion de infix a postfix para regex.
  - `drivers.py`: implemetaciones de pipelines (API)

  - ***`Lexer`***
    - `util.py`: funcinones auxiliares
    - `Tree.py`: Implementación de arbol de sintaxis y followpos.
    - `Automata.py`: Objectos Automatas y funcionalidades de los mismos
    - `Thompson.py`: Implementación de algoritmo de Thompson para construccion de AFN's.
    - `Subconjuntos.py`: Implementación de algoritmo de construccion de subconjuntos.
    - `DirectCons.py`: Implementación de algoritmo de construccion directa de AFD.
    - `Min.py`: Implementación de algoritmo de minimizacion de AFD.
    - `YalexScanner.py`: Lectura de archivos .yal

- ***`out`***: Dentro de esta carpeta se encuentran los archivos resultantes de las ejecuciones.
  - `stepts.txt`: Descripcion del proceso de lectura YAlex
  - `Tree.png`: Arbol de expresion resultante
  - `AFD.png`: Grafo de AFD resultante para el Lexer.
  - `Scanner.py`: Código del

- ***`Examples`***: 
  - ***`input`***: Ejemplos de archivos de entrada para el Scanner.
  - ***`yalex`***: Ejemplos de archivos yalex para lectura.

- `main.py`: Programa principal (Driver Program).

## 🕹️ Getting Started

- Ejecute el archivo `main.py` escribiendo como argumento el path al archivo yalex a leer.
    > Ejemplo: py main.py <<Archivo.yal>>

1. Se crearan varias carpetas `__pycache__` con compilados del codigo.
2. Se crearan los siguientes archivos con el autput de la lectura del archivo YALex:
     - `./out/steps.txt`
     - `./out/tree.txt`
     - `./out/AFD.png`
     - `./out/Scanner.py`

3. Ejecute el archivo `Scanner.py` escribiendo como argumento el path al archivo *input* a leer.
    > Ejemplo: py Scanner.py <<./Examples/input/ejemplo.txt>>

## 🤓 Autor

Diego Cordova - 20212
