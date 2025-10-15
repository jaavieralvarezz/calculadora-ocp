
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

# ============================================
# SOLID: Principio Abierto-Cerrado (OCP)
# - Abierto a extensión: podemos añadir operaciones nuevas.
# - Cerrado a modificación: no cambiamos el código de Calculator.
# ============================================

class Operation(ABC):
    @property
    @abstractmethod
    def symbol(self) -> str:
        "Símbolo textual de la operación (p.ej., '+', 'pow')."
        raise NotImplementedError

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        "Ejecuta la operación sobre a y b."
        raise NotImplementedError

# ----- Operaciones básicas -----

@dataclass(frozen=True)
class Add(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b
    @property
    def symbol(self) -> str:
        return "+"

@dataclass(frozen=True)
class Subtract(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b
    @property
    def symbol(self) -> str:
        return "-"

@dataclass(frozen=True)
class Multiply(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b
    @property
    def symbol(self) -> str:
        return "*"

@dataclass(frozen=True)
class Divide(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("No se puede dividir entre cero")
        return a / b
    @property
    def symbol(self) -> str:
        return "/"

# ----- Calculadora OCP -----

class Calculator:
    def __init__(self) -> None:
        self._ops: Dict[str, Operation] = {}

    def register(self, operation: Operation) -> None:
        """Registrar/inyectar una operación nueva SIN modificar la clase."""
        self._ops[operation.symbol] = operation

    def available(self) -> Dict[str, Operation]:
        return dict(self._ops)

    def compute(self, a: float, op_symbol: str, b: float) -> float:
        if op_symbol not in self._ops:
            raise ValueError(f"Operación no soportada: {op_symbol}. Disponibles: {list(self._ops)}")
        return self._ops[op_symbol].execute(a, b)

# ----- Quinta operación añadida SIN tocar Calculator -----

@dataclass(frozen=True)
class Power(Operation):
    def execute(self, a: float, b: float) -> float:
        return a ** b
    @property
    def symbol(self) -> str:
        return "pow"

# ----- Demo y pruebas rápidas -----

def demo() -> None:
    calc = Calculator()

    # 1) Registrar operaciones "plug-in":
    calc.register(Add())
    calc.register(Subtract())
    calc.register(Multiply())
    calc.register(Divide())

    print("=== DEMO OCP: Operaciones básicas ===")
    print("2 + 3 =", calc.compute(2, "+", 3))
    print("10 - 4 =", calc.compute(10, "-", 4))
    print("6 * 7 =", calc.compute(6, "*", 7))
    print("9 / 3 =", calc.compute(9, "/", 3))

    # 2) Añadir una nueva operación SIN modificar Calculator:
    calc.register(Power())

    print("\n=== DEMO OCP: Nueva operación añadida (Power) ===")
    print("2 pow 5 =", calc.compute(2, "pow", 5))

def _tests() -> None:
    calc = Calculator()
    calc.register(Add())
    calc.register(Subtract())
    calc.register(Multiply())
    calc.register(Divide())
    calc.register(Power())  # añadida sin tocar Calculator

    # Asserts básicos
    assert calc.compute(2, "+", 3) == 5
    assert calc.compute(10, "-", 4) == 6
    assert calc.compute(6, "*", 7) == 42
    assert calc.compute(9, "/", 3) == 3
    assert calc.compute(2, "pow", 5) == 32

    # División por cero
    try:
        calc.compute(1, "/", 0)
        raise AssertionError("Se esperaba ZeroDivisionError")
    except ZeroDivisionError:
        pass

    # Operación no existente
    try:
        calc.compute(1, "%", 2)
        raise AssertionError("Se esperaba ValueError por operación no soportada")
    except ValueError:
        pass

    print("Pruebas OK")

if __name__ == "__main__":
    demo()
    _tests()
