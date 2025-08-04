#core/expression_preprocessor.py

import re

class ExpressionPreprocessor:
    """
    Preprocesa expresiones matemáticas para manejar casos especiales
    antes de pasarlos al parser de SymPy.
    """
    @staticmethod
    def preprocess(expression: str) -> str:
        """
        Preprocesa una expresión matemática para manejar casos especiales.
        """
        if not expression.strip():
            return expression

        # 1. Eliminar espacios en blanco
        expr = expression.replace(" ", "")

        # 2. Patrones para multiplicación implícita
        patterns = [
            # Número seguido de x: 2x -> 2*x
            (r'(\d+)([x])', r'\1*\2'),
            # Número seguido de función trigonométrica: 2sin -> 2*sin
            (r'(\d+)(sin|cos|tan|exp|ln|sqrt)', r'\1*\2'),
            # Número seguido de constante: 2pi -> 2*pi
            (r'(\d+)(pi|e)', r'\1*\2'),
            # Número seguido de paréntesis: 2(x) -> 2*(x)
            (r'(\d+)(\()', r'\1*\2'),
            # Paréntesis seguido de número o variable: (2)x -> (2)*x
            (r'(\))(\d+|x|sin|cos|tan|exp|ln|sqrt|pi|e)', r'\1*\2')
        ]

        # Aplicar cada patrón de reemplazo
        for pattern, replacement in patterns:
            expr = re.sub(pattern, replacement, expr)

        return expr