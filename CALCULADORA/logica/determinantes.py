"""
Módulo de determinantes.

Este módulo implementa funciones para calcular el determinante de una matriz.

Funciones principales:
- analizar_independencia: Analiza la independencia lineal de un conjunto de vectores
- formar_matriz_desde_vectores: Forma una matriz usando vectores como columnas
- calcular_rango: Calcula el rango de una matriz usando eliminación gaussiana
- validar_vectores: Valida un conjunto de vectores
"""

from typing import List
import copy

class DeterminantesError(Exception):
    """Excepción personalizada para errores de determinantes."""
    pass

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

