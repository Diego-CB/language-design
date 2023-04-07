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

- **`Renders`**: Dentro de esta carpeta se encuentran las imagenes resultantes de los AF y el arbol de syntaxis

- **`Examples`**: Dentro de esta carpeta se encuentran ejemplos de archivos yalex.

- `main.py`: Programa principal (Driver Program).

## 🕹️ Getting Started

- Ejecute el archivo `main.py` escribiendo como argumento el path al archivo yalex a leer.
    > Ejemplo: py main.py <<Archivo.yal>>

## 🤓 Autor

Diego Cordova - 20212
