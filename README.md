# Lab E: YAPar

## 📡 Tecnologias Utilizadas

- Python 🐍: Modern syntax, Interpreted Languaje
  > Python 10.0 or higher needed

## ✅ Rúbrica

- [x] Correcta interpretación de un archivo de especificación YAPar.
- [x] Validación de tokens provistos en archivo de especificación de YAPar con el
output generado por YALex.
- [x] Cálculo de funciones asociadas sobre la gramática provista: FIRST, FOLLOW
y CLOSURE.
- [x] Generación de elementos de nodos de autómata LR(0) y construcción del
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
    - `WriteScanner.py`: Escritor de Scanner

  - ***`Parser`***
    - `YaparProcessor.py`: Procesa los tokens de los archivos yapar
    - `YaparReader.py`: Lector de archivos *Yalp*
    - `util.py`: Objetos y funciones utiles
    - `LR0.py`: Objeto Automata LR0
    - `LR_Constructor.py`: Construccion de Automata LR0

- ***`out`***: Dentro de esta carpeta se encuentran los archivos resultantes de las ejecuciones.
      - `./out/AFD.png`: Con el AFD generado por el Yalex
     - `./out/LR0.png`: Con el Automata LR0 generado a partir del YAPar
     - `./out/Scanner.txt`: Con el Analizador lexico generado en base al yalex de entrada
     - `./out/tokens.txt`: Con los tokens leidos por el Scanner generado
     - `./out/yapar_tokens.txt`: Con los tokens leidos por el scanner de YAPar

- ***`Examples`***: Ejemplos de ejecuciones para powershell de windows
- ***`input`***: Ejemplos de archivos de entrada para el Scanner.
- ***`yalex`***: Ejemplos de archivos yalex para lectura.
- ***`yapar`***: Ejemplos de archivos yapar para lectura.

- `main.py`: Programa principal (Driver Program).

## 🕹️ Getting Started

1. Instale las **dependencias** del projecto ejecutando `pip install -r requirements.txt`
2. Ejecute el archivo `main.py` escribiendo como argumentos:
   1. El arhivo *YALex* con la definicíon del analizador lexico.
   2. El arhivo *YAPar* con la definicíon del analizador sintactico.
   3. Un archivo de entrada para ambos generadores.
    > Ejemplo: py main.py *Archivo.yal* *Archivo.yalp* *Archivo.txt*

3. O ejecute alguno de los ejemplos predefinidos en la carpeta ***`Examples`***
   > Ejemplo: *./Examples/1*

4. Se crearan varias carpetas `__pycache__` con compilados del codigo.
5. Se crearan los siguientes archivos con el autput de la lectura del archivo YALex:
     - `./out/AFD.png`: Con el AFD generado por el Yalex
     - `./out/LR0.png`: Con el Automata LR0 generado a partir del YAPar
     - `./out/Scanner.txt`: Con el Analizador lexico generado en base al yalex de entrada
     - `./out/tokens.txt`: Con los tokens leidos por el Scanner generado
     - `./out/yapar_tokens.txt`: Con los tokens leidos por el scanner de YAPar

6. En consola se imprimera una prueba del funcionamiento de las funciones ***FOLLOW*** y ***FIRST***

## 🤓 Autor

Diego Cordova - 20212
