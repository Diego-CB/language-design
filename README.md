# Lab A: Construccion de Thomson

## 📡 Tecnologias Utilizadas
- Python 🐍: Modern syntax, Interpreted Languaje
  > Python 10.0 or higher needed

## ✅ Rúbrica:

  - [x] Validación de errores para expresión regular y balanceo de 𝑟
  - [x] Conversión de de infix a postfix para producción de 𝑟' en postfix
  - [ ] Implementación del algoritmo de Construcción de Thompson con base en 𝑟'    
  - [ ] Mostrar en pantalla el listado solicitado de descripciones sobre los AFN generados
  - [x] Ejercicios Pre-Laboratorio

## 🗃️ Estructura de Archivos

- **`src`**

  - `alfabeto.py`: Definicion de alfabeto para regex.
  - `postfix.py`: Implementación del algoritmo shunting yard para conversion de infix a postfix para regex.
  - `Tree.py`: Implementación de arbol de sintaxis para regex.

- **`Renders`**: Dentro de esta carpeta se encuentran las imagenes resultantes de los AFN

- `main.py`: Programa principal (Driver Program).

## 🕹️ Getting Started

1. Ejecute el archivo `main.py`.
2. Ingrese una regex valida
3. Si no existen errores en ejecución, se escribirá un achivo `AFN_(regex).png` con la imagen resultante en la carpeta **`Renders`**.
  > path de la imagen: `./Renders/AFN_(regex).png`
  > Si existen errores en la regex de entrada se desplegara un error con la descripcion

## 🤓 Autor

Diego Cordova - 20212
