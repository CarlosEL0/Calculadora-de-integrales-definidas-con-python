# ui/components/keyboard_layouts.py
"""
Este archivo contiene exclusivamente la configuración y el diseño
de los botones del teclado virtual.
"""

# Se define un diccionario donde cada clave es el nombre de la pestaña.
# Cada valor es una lista de filas, donde cada fila es una lista de botones.
KEYBOARD_LAYOUT = {
    "Números": {
        "layout": [
            ['7', '8', '9', '/', '('],
            ['4', '5', '6', '*', ')'],
            ['1', '2', '3', '-', '^'],
            ['0', '.', 'x', '+', 'Borrar']
        ],
        "tooltips": {} # No se necesitan tooltips para números
    },
    "Funciones": {
        "layout": [
            ['ln(', 'log('],
            ['exp(', 'sqrt('],
            ['abs(', 'factorial(']
        ],
        "tooltips": {
            'ln(': 'Logaritmo natural, ej: ln(x)',
            'log(': 'Logaritmo base 10, ej: log(x)',
            'exp(': 'Función exponencial e^x, ej: exp(x)',
            'sqrt(': 'Raíz cuadrada',
            'abs(': 'Valor absoluto, ej: abs(x)',
            'factorial(': 'Factorial, ej: factorial(x)'
        }
    },
    "Trigonométricas": {
        "layout": [
            ['sin(', 'cos(', 'tan('],
            ['csc(', 'sec(', 'cot('],
            ['asin(', 'acos(', 'atan('],
            ['acsc(', 'asec(', 'acot(']
        ],
        "tooltips": {
            'asin(': 'Arcoseno', 'acos(': 'Arcocoseno', 'atan(': 'Arcotangente',
        }
    },
    "Constantes": {
        "layout": [
            ['pi', 'e', 'oo'],
            ['k,', 'a,', 'b,', 'm,']
        ],
        "tooltips": {
            'pi': 'Constante Pi (3.1415...)',
            'e': 'Constante de Euler (2.7182...)',
            'oo': 'Infinito simbólico',
            'k,': 'Inserta la constante "k," (lista para la siguiente)'
        }
    }
}