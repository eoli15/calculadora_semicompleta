"""
Módulo de determinantes.

Este módulo implementa funciones para calcular el determinante de una matriz.

Funciones principales:
- analizar_independencia: Analiza la independencia lineal de un conjunto de vectores
- formar_matriz_desde_vectores: Forma una matriz usando vectores como columnas
- calcular_rango: Calcula el rango de una matriz usando eliminación gaussiana
- validar_vectores: Valida un conjunto de vectores
"""
from typing import List, Optional, Tuple
import copy

class DeterminantesError(Exception):
    """Excepción personalizada para errores de determinantes."""
    pass

class PasoDeterminante:
    """Clase para registrar cada paso de la reducción de la matriz."""
    def __init__(self, operacion: str, matriz_resultado: List[List[float]], factor_determinante: float, row_swaps: int):
        self.operacion = operacion
        self.matriz_resultado = copy.deepcopy(matriz_resultado)
        self.factor_determinante = factor_determinante
        self.row_swaps = row_swaps
        
def matrix_to_string(matrix: List[List[float]], precision: int = 4) -> str:
    """Convierte una matriz a una representación de cadena formateada."""
    if not matrix:
        return "Matriz vacía"
    
    lines = []
    max_width = 0
    # Calcular el ancho máximo de columna para alinear
    for row in matrix:
        for val in row:
            max_width = max(max_width, len(f"{val:.{precision}f}"))

    # Aplicar formato
    for row in matrix:
        formatted_row = [f"{val:>{max_width + 1}.{precision}f}" for val in row]
        lines.append("[ " + " ".join(formatted_row) + " ]")
    
    return "\n".join(lines)


def determinante_con_pasos(matriz: List[List[float]]) -> Tuple[float, List[PasoDeterminante]]:
    """
    Calcula el determinante de una matriz cuadrada registrando todos los pasos.
    
    Returns:
        Tupla de (valor del determinante, lista de PasoDeterminante).
    """
    rows = len(matriz)
    if rows == 0:
        raise DeterminantesError("La matriz está vacía.")
        
    cols = len(matriz[0])
    if rows != cols:
        raise DeterminantesError("El determinante solo puede calcularse para matrices cuadradas.")
        
    A = copy.deepcopy(matriz)
    n = rows
    determinant_val = 1.0
    row_swaps = 0
    pasos = []
    
    # Paso inicial
    pasos.append(PasoDeterminante("Matriz Inicial", A, determinant_val, row_swaps))
    
    # Eliminación hacia adelante (hacer la matriz triangular superior)
    for i in range(n):
        # Encontrar el pivote (para estabilidad numérica)
        pivot_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[pivot_row][i]):
                pivot_row = k
        
        # Intercambiar filas si es necesario
        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            row_swaps += 1 
            
            # Registrar el paso de intercambio
            pasos.append(PasoDeterminante(
                operacion=f"Intercambio: R{i+1} <-> R{pivot_row+1}. Det factor: (-1)", 
                matriz_resultado=A, 
                factor_determinante=determinant_val,
                row_swaps=row_swaps
            ))
        
        # Si el pivote es (cercano a) cero, el determinante es 0
        if abs(A[i][i]) < 1e-10:
            determinant_val = 0.0
            break 
            
        # Eliminación (crear ceros debajo del pivote)
        for k in range(i + 1, n):
            if abs(A[k][i]) < 1e-10: continue
            
            factor = A[k][i] / A[i][i]
            
            # Operación de fila: Rk -> Rk - factor * Ri (no cambia el determinante)
            operacion_str = f"R{k+1} -> R{k+1} - ({factor:.4f})R{i+1}"
            
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
                
            # Registrar el paso de eliminación
            pasos.append(PasoDeterminante(
                operacion=operacion_str, 
                matriz_resultado=A, 
                factor_determinante=determinant_val,
                row_swaps=row_swaps
            ))
            
    # 2. Calcular el determinante final (producto de la diagonal)
    if determinant_val != 0.0:
        for i in range(n):
            determinant_val *= A[i][i]
            
        # 3. Ajustar el signo por los intercambios de filas
        if row_swaps % 2 != 0:
            determinant_val *= -1
            
    # Redondear y devolver
    if abs(determinant_val) < 1e-10:
        return 0.0, pasos
    if abs(determinant_val - round(determinant_val)) < 1e-8:
        return round(determinant_val), pasos
        
    return determinant_val, pasos

# NOTA: Debes cambiar el nombre de la función principal "determinante"
# para que simplemente llame a la nueva función con pasos:

def determinante(matriz: List[List[float]]) -> float:
    """Función de fachada para obtener solo el valor del determinante."""
    val, _ = determinante_con_pasos(matriz)
    return val

# ... (resto de tu logica/determinantes.py)

def determinante(matriz: List[List[float]]) -> float:
    """
    Calcula el determinante de una matriz cuadrada utilizando eliminación Gaussiana 
    (para matrices N x N).
    
    Args:
        matrix: Una matriz cuadrada [A].
        
    Returns:
        El valor del determinante (float).
        
    Raises:
        DeterminantesError: Si la matriz no es cuadrada o está vacía.
    """
    rows = len(matriz)
    if rows == 0:
        raise DeterminantesError("La matriz está vacía.")
        
    cols = len(matriz[0])
    
    if rows != cols:
        raise DeterminantesError("El determinante solo puede calcularse para matrices cuadradas.")
        
    # Crear una copia profunda para no modificar la matriz original
    A = copy.deepcopy(matriz)
    n = rows
    determinant_val = 1.0
    row_swaps = 0
    
    # 1. Eliminación hacia adelante (hacer la matriz triangular superior)
    for i in range(n):
        # Encontrar el pivote (para estabilidad numérica)
        pivot_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[pivot_row][i]):
                pivot_row = k
        
        # Intercambiar filas si es necesario
        if pivot_row != i:
            A[i], A[pivot_row] = A[pivot_row], A[i]
            row_swaps += 1 # Contar el intercambio para el signo
        
        # Si el pivote es (cercano a) cero, el determinante es cero
        if abs(A[i][i]) < 1e-10:
            return 0.0 # Determinante es 0

        # Eliminación (crear ceros debajo del pivote)
        for k in range(i + 1, n):
            if abs(A[k][i]) < 1e-10: continue
            factor = A[k][i] / A[i][i]
            # Iterar sobre las columnas restantes
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
                    
    # 2. Calcular el determinante
    # El determinante de una matriz triangular es el producto de su diagonal.
    for i in range(n):
        determinant_val *= A[i][i]
        
    # 3. Ajustar el signo por los intercambios de filas
    if row_swaps % 2 != 0:
        determinant_val *= -1
        
    # Redondear valores muy cercanos a cero o enteros
    if abs(determinant_val) < 1e-10:
        return 0.0
    if abs(determinant_val - round(determinant_val)) < 1e-8:
        return round(determinant_val)
        
    return determinant_val

def get_matrix_dims(matriz: List[List[float]]) -> str:
    """Devuelve las dimensiones de la matriz como string (ej: '3x3')."""
    if not matriz or not matriz[0]:
        return "0x0"
    rows = len(matriz)
    cols = len(matriz[0])
    return f"{rows}x{cols}"

