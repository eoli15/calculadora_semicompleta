# En logica/cramer.py

# Importamos la función de determinante desde el otro módulo
try:
    
    from .operaciones_matrices import determinante
except ImportError:
  
    from operaciones_matrices import determinante

def resolver_por_cramer(matriz_A, vector_b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando la Regla de Cramer.
    
    :param matriz_A: Matriz de coeficientes (lista de listas).
    :param vector_b: Vector de términos independientes (lista).
    :return: Una lista con las soluciones [x1, x2, ..., xn] o None si no hay solución única.
    """
    
    # --- Validaciones ---
    n = len(matriz_A)
    if any(len(fila) != n for fila in matriz_A):
        raise ValueError("La matriz de coeficientes (A) debe ser cuadrada.")
    if len(vector_b) != n:
        raise ValueError("El número de constantes (b) debe coincidir con el tamaño de la matriz (A).")

    
    D_principal = determinante(matriz_A)

    
    if D_principal == 0:
        
        print("Error: El determinante principal es 0. El sistema no tiene solución única.")
        return None 

    soluciones = []
    
    # 3. Calcular la solución para cada variable xi
    for j in range(n):
        # Crear la matriz A_i reemplazando la columna 'j' con el vector 'b'
        matriz_Ai = []
        for i in range(n):
            fila_nueva = list(matriz_A[i])  # Copiar la fila original
            fila_nueva[j] = vector_b[i]     # Reemplazar el elemento de la columna j
            matriz_Ai.append(fila_nueva)
        
        # Calcular el determinante de esta nueva matriz
        D_i = determinante(matriz_Ai)
        
        # 4. Calcular la solución x_i = D_i / D
        x_i = D_i / D_principal
        soluciones.append(x_i)

    return soluciones