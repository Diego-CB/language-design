# Lab C: Yalex

## 📡 Tecnologias Utilizadas

- Python 🐍: Modern syntax, Interpreted Languaje
  > Python 10.0 or higher needed

## ✅ Rúbrica

- [x] Correcta interpretación de Expresiones Regulares en Definición Regular.
- [x] Generación de Árbol de Expresión, representando cada Expresión Regular dentro de la Definición Regular.
- [x] Generación de un único árbol de Expresión.

## 🗃️ Estructura de Archivos

- **`src`**

  - `alfabeto.py`: Definicion de alfabeto para regex.
  - `postfix.py`: Implementación del algoritmo shunting yard para conversion de infix a postfix para regex.
  - `drivers.py`: implemetaciones de pipelines (API)

  - **`Lexer`**
    - `util.py`: funcinones auxiliares
    - `Tree.py`: Implementación de arbol de sintaxis y followpos.
    - `Automata.py`: Objectos Automatas y funcionalidades de los mismos
    - `Thompson.py`: Implementación de algoritmo de Thompson para construccion de AFN's.
    - `Subconjuntos.py`: Implementación de algoritmo de construccion de subconjuntos.
    - `DirectCons.py`: Implementación de algoritmo de construccion directa de AFD.
    - `Min.py`: Implementación de algoritmo de minimizacion de AFD.
    - `YalexScanner.py`: Lectura de archivos .yal

- **`out`**: Dentro de esta carpeta se encuentran los archivos resultantes de las ejecuciones.
  - `stepts.txt`: Descripcion del proceso de lectura YAlex
  - `Tree.png`: Arbol de expresion resultante

- **`Examples`**: Dentro de esta carpeta se encuentran ejemplos de archivos yalex.

- `main.py`: Programa principal (Driver Program).

## 🕹️ Getting Started

- Ejecute el archivo `main.py` escribiendo como argumento el path al archivo yalex a leer.
    > Ejemplo: py main.py <<Archivo.yal>>

1. Se crearan varias carpetas `__pycache__` con compilados del codigo.
2. Se crearan dos archivos `./out/steps.txt` y `./out/tree.txt` con el autput de la lectura del archivo YALex.

## 🤓 Autor

Diego Cordova - 20212
