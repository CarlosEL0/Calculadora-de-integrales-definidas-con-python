# core/calculator.py
import sympy
from sympy import symbols, lambdify, integrate, latex, Symbol

from .parser import InputParser


class CalculatorEngine:
    def __init__(self):
        self.history = []
        # Definimos el único símbolo 'variable' que la calculadora usa. Todo lo demás es una constante.
        self.variable = symbols('x')
        # Símbolos matemáticos fijos
        self.known_symbols = {
            'pi': sympy.pi, 'e': sympy.E, 'sin': sympy.sin, 'cos': sympy.cos,
            'tan': sympy.tan, 'exp': sympy.exp, 'ln': lambda x: sympy.log(x, sympy.E), 'log': lambda x: sympy.log(x, 10),
            'sqrt': sympy.sqrt, 'abs': sympy.Abs, 'factorial': sympy.factorial, 'oo': sympy.oo,

            # NUEVAS Funciones trigonométricas y sus inversas
            'csc': sympy.csc, 'sec': sympy.sec, 'cot': sympy.cot,
            'asin': sympy.asin, 'acos': sympy.acos, 'atan': sympy.atan,
            'acsc': sympy.acsc, 'asec': sympy.asec, 'acot': sympy.acot, 'x': self.variable
        }

    def _prepare_local_symbols(self, constants_str: str) -> dict:
        user_symbols = {}
        if constants_str:
            constant_names = [s.strip() for s in constants_str.split(',') if s.strip()]
            for name in constant_names:
                # Evitar que el usuario redefina símbolos base
                if name and name not in self.known_symbols and name != str(self.variable):
                    user_symbols[name] = Symbol(name)

        # Combinar todos los símbolos y AÑADIR LA VARIABLE DE INTEGRACIÓN 'x'
        local_symbols = {**self.known_symbols, **user_symbols}
        local_symbols[str(self.variable)] = self.variable
        return local_symbols

    def calculate_integral(self, func_str: str, lower_limit_str: str, upper_limit_str: str, constants_str: str = ""):
        try:
            # 1. Crear el entorno de símbolos completo
            local_symbols = self._prepare_local_symbols(constants_str)

            # 2. Parsear las expresiones
            func_expr = InputParser.parse(func_str, local_symbols)
            a_expr = InputParser.parse(lower_limit_str, local_symbols)
            b_expr = InputParser.parse(upper_limit_str, local_symbols)

            # --- 3. Lógica de Graficación ---
            can_plot_function = not func_expr.free_symbols - {self.variable}

            can_fill_area = can_plot_function and a_expr.is_number and b_expr.is_number

            numeric_func = None
            if can_plot_function:
                numeric_func = lambdify(self.variable, func_expr, modules=['numpy', {'ln': sympy.log}])

            # --- 4. Integración ---
            integral_def = integrate(func_expr, (self.variable, a_expr, b_expr))
            integral_indef = integrate(func_expr, self.variable)

            defined_result_eval = integral_def.evalf(n=10) if integral_def.is_Number else integral_def

            self.add_to_history(func_str, str(a_expr), str(b_expr), defined_result_eval, constants_str)

            return {
                "success": True, "func_expr": func_expr, "numeric_func": numeric_func,
                "a": float(a_expr) if a_expr.is_number else 0,
                "b": float(b_expr) if b_expr.is_number else 0,
                "can_fill_area": can_fill_area,
                "defined_integral": defined_result_eval,
                "indefinite_integral": integral_indef
            }

        except Exception as e:
            return {"success": False, "error_message": str(e)}

    def add_to_history(self, func_str, a, b, result, constants):
        # Usar LaTeX para un formato más bonito
        result_str = str(latex(result))
        self.history.append({
            "function": func_str, "lower_limit": a, "upper_limit": b,
            "constants": constants, "result": result_str})

    def get_history(self):
        return self.history