# Lab B: Varios Algoritmos de Automatas

## 📡 Tecnologias Utilizadas
- Python 🐍: Modern syntax, Interpreted Languaje
  > Python 10.0 or higher needed

## ✅ Rúbrica:

  - [x] Implementación del algoritmo de Construcción de Subconjuntos para transformar los AFN generados a AFD, con su implementación de funciones necesarias para cerraduras y similares.
  - [x] Implementación del algoritmo de Construcción directa de AFD (DFA) para construir a partir de r.
  - [x] Implementación del algoritmo de Minimización de AFD (DFA) para minimizar los AFD generados en los incisos anteriores.
  - [x] Implementación de la simulación de un AFN para determinar si .𝑤 ∈ 𝐿(𝑟).
  - [x] Implementación de la simulación de un AFD para determinar si .𝑤 ∈ 𝐿(𝑟).
  - [x] Ejercicios de pre laboratorio.

## 🗃️ Estructura de Archivos

- **`src`**

  - `alfabeto.py`: Definicion de alfabeto para regex.
  - `postfix.py`: Implementación del algoritmo shunting yard para conversion de infix a postfix para regex.

  - **`Lexer`**
    - `util.py`: funcinones auxiliares
    - `Tree.py`: Implementación de arbol de sintaxis y followpos.
    - `Automata.py`: Objectos Automatas y funcionalidades de los mismos
    - `Thompson.py`: Implementación de algoritmo de Thompson para construccion de AFN's.
    - `Subconjuntos.py`: Implementación de algoritmo de construccion de subconjuntos.
    - `DirectCons.py`: Implementación de algoritmo de construccion directa de AFD.
    - `Min.py`: Implementación de algoritmo de minimizacion de AFD.

- **`Renders`**: Dentro de esta carpeta se encuentran las imagenes resultantes de los AF y el arbol de syntaxis

- `drivers.py`: implemetaciones de pipelines (API)
- `main.py`: Programa principal (Driver Program).

## 🕹️ Getting Started

- Ejecute el archivo `main.py`.

- Si selecciona: Crear un AFN:
  1. Ingrese una regex valida
  2. Se generaran varios archivos dentro de la carpeta **`Renders`** con las representaciones graficas de los Automatas generados.
    > path de la imagen: `./Renders/Automatas.png`
  3. Ingrese una cadena para simular en los automatas.
  4. Se indicara si la cadena fue aceptada por los distintos automatas.

## 🤓 Autor

Diego Cordova - 20212
