#core/parser.py

import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from .expression_preprocessor import ExpressionPreprocessor

class InputParser:
    """
    Su única responsabilidad es el PARSEO de la entrada.
    Es un traductor de 'texto de usuario' a 'expresión matemática'.
    """
    @staticmethod
    def parse(expression_str: str, local_symbols: dict) -> sympy.Expr:
        """
        Analiza una cadena y la convierte en una expresión SymPy.
        Aplica transformaciones para sintaxis común (ej: '2x' -> '2*x').
        """
        if not expression_str.strip():
            return sympy.S.Zero # Devuelve un cero simbólico para entradas vacías

        # 1. Preprocesar la expresión
        preprocessed_str = ExpressionPreprocessor.preprocess(expression_str)

        # 2. Reemplazar la potencia '^' por el '**' de Python
        parsed_str = preprocessed_str.replace('^', '**')

        try:
            # 3. Definir que la multiplicación implícita se procese PRIMERO
            transformations = (implicit_multiplication_application,) + standard_transformations

            # 4. Usar el parser AVANZADO de SymPy, que acepta transformaciones
            return parse_expr(parsed_str, local_dict=local_symbols, transformations=transformations)
        except Exception as e:
            raise ValueError(f"Error al parsear la expresión '{expression_str}': {str(e)}")