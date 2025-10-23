"""
Módulo de operaciones matriciales básicas.

Este módulo implementa las operaciones fundamentales con matrices:
suma, resta, multiplicación, transpuesta y producto por escalar,
con validación de compatibilidad y seguimiento detallado de pasos.

Funciones principales:
- sumar_matrices: Suma de dos matrices A + B
- restar_matrices: Resta de dos matrices A - B
- multiplicar_matrices: Multiplicación de matrices A × B
- transponer_matriz: Transpuesta de una matriz A^T
- escalar_por_matriz: Producto de escalar por matriz k × A
"""

from .gauss import formatear_matriz

def validar_dimensiones_iguales(A, B):
    """
    Valida que dos matrices tengan las mismas dimensiones.
    
    Args:
        A (list): Primera matriz
        B (list): Segunda matriz
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not A or not B:
        return False, "Una o ambas matrices están vacías"
    
    if len(A) != len(B):
        return False, f"Número de filas diferente: A tiene {len(A)} filas, B tiene {len(B)} filas"
    
    if not A[0] or not B[0]:
        return False, "Una o ambas matrices tienen filas vacías"
    
    if len(A[0]) != len(B[0]):
        return False, f"Número de columnas diferente: A tiene {len(A[0])} columnas, B tiene {len(B[0])} columnas"
    
    # Verificar que todas las filas tengan el mismo número de columnas
    for i, fila in enumerate(A):
        if len(fila) != len(A[0]):
            return False, f"Matriz A: fila {i + 1} tiene {len(fila)} elementos, esperado {len(A[0])}"
    
    for i, fila in enumerate(B):
        if len(fila) != len(B[0]):
            return False, f"Matriz B: fila {i + 1} tiene {len(fila)} elementos, esperado {len(B[0])}"
    
    return True, ""

def validar_multiplicacion(A, B):
    """
    Valida que dos matrices sean compatibles para multiplicación A × B.
    
    Args:
        A (list): Primera matriz (m×n)
        B (list): Segunda matriz (p×q)
    
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not A or not B or not A[0] or not B[0]:
        return False, "Una o ambas matrices están vacías"
    
    # Verificar consistencia interna de cada matriz
    for i, fila in enumerate(A):
        if len(fila) != len(A[0]):
            return False, f"Matriz A: fila {i + 1} tiene {len(fila)} elementos, esperado {len(A[0])}"
    
    for i, fila in enumerate(B):
        if len(fila) != len(B[0]):
            return False, f"Matriz B: fila {i + 1} tiene {len(fila)} elementos, esperado {len(B[0])}"
    
    # Verificar compatibilidad para multiplicación
    columnas_A = len(A[0])
    filas_B = len(B)
    
    if columnas_A != filas_B:
        return False, f"Incompatible para multiplicación: A es {len(A)}×{columnas_A}, B es {filas_B}×{len(B[0])}"
    
    return True, ""

def sumar_matrices(A, B):
    """
    Suma dos matrices A + B.
    
    Args:
        A (list): Primera matriz
        B (list): Segunda matriz
    
    Returns:
        tuple: (resultado, pasos)
            - resultado: Matriz resultado o None si hay error
            - pasos: Lista de strings describiendo el proceso
    
    Ejemplo:
        >>> A = [[1, 2], [3, 4]]
        >>> B = [[5, 6], [7, 8]]
        >>> resultado, pasos = sumar_matrices(A, B)
        >>> # resultado = [[6, 8], [10, 12]]
    """
    pasos = ["=== SUMA DE MATRICES ==="]
    
    # Validar dimensiones
    es_valido, error = validar_dimensiones_iguales(A, B)
    if not es_valido:
        pasos.append(f"Error: {error}")
        return None, pasos
    
    filas = len(A)
    columnas = len(A[0])
    
    pasos.append(f"Sumando matrices de dimensión {filas}×{columnas}")
    pasos.append("Matriz A:")
    pasos.append(formatear_matriz(A))
    pasos.append("Matriz B:")
    pasos.append(formatear_matriz(B))
    pasos.append("")
    pasos.append("Cálculo: C = A + B")
    pasos.append("C[i][j] = A[i][j] + B[i][j] para cada posición")
    pasos.append("")
    
    # Realizar la suma
    resultado = []
    for i in range(filas):
        fila_resultado = []
        elementos_fila = []
        
        for j in range(columnas):
            try:
                suma = float(A[i][j]) + float(B[i][j])
                fila_resultado.append(suma)
                elementos_fila.append(f"C[{i+1}][{j+1}] = {A[i][j]:.3f} + {B[i][j]:.3f} = {suma:.3f}")
            except (ValueError, TypeError) as e:
                pasos.append(f"Error en posición ({i+1}, {j+1}): {e}")
                return None, pasos
        
        resultado.append(fila_resultado)
        pasos.append(f"Fila {i + 1}: " + ", ".join(elementos_fila))
    
    pasos.append("")
    pasos.append("Resultado C = A + B:")
    pasos.append(formatear_matriz(resultado))
    
    return resultado, pasos

def restar_matrices(A, B):
    """
    Resta dos matrices A - B.
    
    Args:
        A (list): Primera matriz (minuendo)
        B (list): Segunda matriz (sustraendo)
    
    Returns:
        tuple: (resultado, pasos)
            - resultado: Matriz resultado o None si hay error
            - pasos: Lista de strings describiendo el proceso
    """
    pasos = ["=== RESTA DE MATRICES ==="]
    
    # Validar dimensiones
    es_valido, error = validar_dimensiones_iguales(A, B)
    if not es_valido:
        pasos.append(f"Error: {error}")
        return None, pasos
    
    filas = len(A)
    columnas = len(A[0])
    
    pasos.append(f"Restando matrices de dimensión {filas}×{columnas}")
    pasos.append("Matriz A (minuendo):")
    pasos.append(formatear_matriz(A))
    pasos.append("Matriz B (sustraendo):")
    pasos.append(formatear_matriz(B))
    pasos.append("")
    pasos.append("Cálculo: C = A - B")
    pasos.append("C[i][j] = A[i][j] - B[i][j] para cada posición")
    pasos.append("")
    
    # Realizar la resta
    resultado = []
    for i in range(filas):
        fila_resultado = []
        elementos_fila = []
        
        for j in range(columnas):
            try:
                resta = float(A[i][j]) - float(B[i][j])
                fila_resultado.append(resta)
                elementos_fila.append(f"C[{i+1}][{j+1}] = {A[i][j]:.3f} - {B[i][j]:.3f} = {resta:.3f}")
            except (ValueError, TypeError) as e:
                pasos.append(f"Error en posición ({i+1}, {j+1}): {e}")
                return None, pasos
        
        resultado.append(fila_resultado)
        pasos.append(f"Fila {i + 1}: " + ", ".join(elementos_fila))
    
    pasos.append("")
    pasos.append("Resultado C = A - B:")
    pasos.append(formatear_matriz(resultado))
    
    return resultado, pasos

def multiplicar_matrices(A, B):
    """
    Multiplica dos matrices A × B.
    
    Args:
        A (list): Primera matriz (m×n)
        B (list): Segunda matriz (n×p)
    
    Returns:
        tuple: (resultado, pasos)
            - resultado: Matriz resultado (m×p) o None si hay error
            - pasos: Lista de strings describiendo el proceso
    
    Ejemplo:
        >>> A = [[1, 2], [3, 4]]
        >>> B = [[5, 6], [7, 8]]
        >>> resultado, pasos = multiplicar_matrices(A, B)
        >>> # resultado = [[19, 22], [43, 50]]
    """
    pasos = ["=== MULTIPLICACIÓN DE MATRICES ==="]
    
    # Validar compatibilidad
    es_valido, error = validar_multiplicacion(A, B)
    if not es_valido:
        pasos.append(f"Error: {error}")
        return None, pasos
    
    filas_A = len(A)
    columnas_A = len(A[0])
    filas_B = len(B)
    columnas_B = len(B[0])
    
    pasos.append(f"Multiplicando A({filas_A}×{columnas_A}) × B({filas_B}×{columnas_B})")
    pasos.append(f"Resultado será de dimensión {filas_A}×{columnas_B}")
    pasos.append("")
    pasos.append("Matriz A:")
    pasos.append(formatear_matriz(A))
    pasos.append("Matriz B:")
    pasos.append(formatear_matriz(B))
    pasos.append("")
    pasos.append("Cálculo: C = A × B")
    pasos.append("C[i][j] = Σ(A[i][k] × B[k][j]) para k = 1 hasta n")
    pasos.append("")
    
    # Realizar la multiplicación
    resultado = []
    for i in range(filas_A):
        fila_resultado = []
        
        for j in range(columnas_B):
            # Calcular el elemento C[i][j]
            suma = 0.0
            terminos = []
            
            pasos.append(f"Calculando C[{i+1}][{j+1}]:")
            
            for k in range(columnas_A):
                try:
                    producto = float(A[i][k]) * float(B[k][j])
                    suma += producto
                    terminos.append(f"{A[i][k]:.3f} × {B[k][j]:.3f}")
                except (ValueError, TypeError) as e:
                    pasos.append(f"Error en multiplicación A[{i+1}][{k+1}] × B[{k+1}][{j+1}]: {e}")
                    return None, pasos
            
            fila_resultado.append(suma)
            pasos.append(f"  C[{i+1}][{j+1}] = {' + '.join(terminos)} = {suma:.3f}")
        
        resultado.append(fila_resultado)
        pasos.append("")
    
    pasos.append("Resultado C = A × B:")
    pasos.append(formatear_matriz(resultado))
    
    return resultado, pasos

def transponer_matriz(A):
    """
    Calcula la transpuesta de una matriz A^T.
    
    Args:
        A (list): Matriz a transponer
    
    Returns:
        tuple: (resultado, pasos)
            - resultado: Matriz transpuesta o None si hay error
            - pasos: Lista de strings describiendo el proceso
    
    Ejemplo:
        >>> A = [[1, 2, 3], [4, 5, 6]]
        >>> resultado, pasos = transponer_matriz(A)
        >>> # resultado = [[1, 4], [2, 5], [3, 6]]
    """
    pasos = ["=== TRANSPUESTA DE MATRIZ ==="]
    
    # Validar matriz
    if not A:
        pasos.append("Error: Matriz vacía")
        return None, pasos
    
    if not A[0]:
        pasos.append("Error: Matriz con filas vacías")
        return None, pasos
    
    # Verificar consistencia de la matriz
    columnas = len(A[0])
    for i, fila in enumerate(A):
        if len(fila) != columnas:
            pasos.append(f"Error: Fila {i + 1} tiene {len(fila)} elementos, esperado {columnas}")
            return None, pasos
    
    filas = len(A)
    
    pasos.append(f"Transponiendo matriz de dimensión {filas}×{columnas}")
    pasos.append("Matriz original A:")
    pasos.append(formatear_matriz(A))
    pasos.append("")
    pasos.append("Cálculo: B = A^T")
    pasos.append("B[i][j] = A[j][i] (intercambiar filas y columnas)")
    pasos.append("")
    
    # Realizar la transposición
    resultado = []
    for j in range(columnas):
        fila_transpuesta = []
        elementos_fila = []
        
        for i in range(filas):
            try:
                valor = float(A[i][j])
                fila_transpuesta.append(valor)
                elementos_fila.append(f"B[{j+1}][{i+1}] = A[{i+1}][{j+1}] = {valor:.3f}")
            except (ValueError, TypeError) as e:
                pasos.append(f"Error en posición A[{i+1}][{j+1}]: {e}")
                return None, pasos
        
        resultado.append(fila_transpuesta)
        pasos.append(f"Fila {j + 1} de A^T: " + ", ".join(elementos_fila))
    
    pasos.append("")
    pasos.append(f"Resultado A^T (dimensión {columnas}×{filas}):")
    pasos.append(formatear_matriz(resultado))
    
    return resultado, pasos

def escalar_por_matriz(k, A):
    """
    Multiplica una matriz por un escalar k × A.
    
    Args:
        k (float): Escalar
        A (list): Matriz
    
    Returns:
        tuple: (resultado, pasos)
            - resultado: Matriz resultado o None si hay error
            - pasos: Lista de strings describiendo el proceso
    
    Ejemplo:
        >>> k = 2
        >>> A = [[1, 2], [3, 4]]
        >>> resultado, pasos = escalar_por_matriz(k, A)
        >>> # resultado = [[2, 4], [6, 8]]
    """
    pasos = ["=== PRODUCTO DE ESCALAR POR MATRIZ ==="]
    
    # Validar escalar
    try:
        escalar = float(k)
    except (ValueError, TypeError):
        pasos.append(f"Error: El escalar '{k}' no es un número válido")
        return None, pasos
    
    # Validar matriz
    if not A:
        pasos.append("Error: Matriz vacía")
        return None, pasos
    
    if not A[0]:
        pasos.append("Error: Matriz con filas vacías")
        return None, pasos
    
    # Verificar consistencia de la matriz
    columnas = len(A[0])
    for i, fila in enumerate(A):
        if len(fila) != columnas:
            pasos.append(f"Error: Fila {i + 1} tiene {len(fila)} elementos, esperado {columnas}")
            return None, pasos
    
    filas = len(A)
    
    pasos.append(f"Multiplicando matriz de dimensión {filas}×{columnas} por escalar k = {escalar:.3f}")
    pasos.append("Matriz A:")
    pasos.append(formatear_matriz(A))
    pasos.append("")
    pasos.append(f"Cálculo: B = {escalar:.3f} × A")
    pasos.append("B[i][j] = k × A[i][j] para cada posición")
    pasos.append("")
    
    # Realizar la multiplicación escalar
    resultado = []
    for i in range(filas):
        fila_resultado = []
        elementos_fila = []
        
        for j in range(columnas):
            try:
                valor_original = float(A[i][j])
                producto = escalar * valor_original
                fila_resultado.append(producto)
                elementos_fila.append(f"B[{i+1}][{j+1}] = {escalar:.3f} × {valor_original:.3f} = {producto:.3f}")
            except (ValueError, TypeError) as e:
                pasos.append(f"Error en posición A[{i+1}][{j+1}]: {e}")
                return None, pasos
        
        resultado.append(fila_resultado)
        pasos.append(f"Fila {i + 1}: " + ", ".join(elementos_fila))
    
    pasos.append("")
    pasos.append(f"Resultado B = {escalar:.3f} × A:")
    pasos.append(formatear_matriz(resultado))
    
    return resultado, pasos

def obtener_dimensiones(matriz):
    """
    Obtiene las dimensiones de una matriz.
    
    Args:
        matriz (list): Matriz a analizar
    
    Returns:
        tuple: (filas, columnas) o (0, 0) si hay error
    """
    if not matriz:
        return 0, 0
    
    if not matriz[0]:
        return len(matriz), 0
    
    return len(matriz), len(matriz[0])

# Ejemplo de uso para pruebas
if __name__ == "__main__":
    # Ejemplo de suma
    print("=== SUMA DE MATRICES ===")
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    resultado, pasos = sumar_matrices(A, B)
    for paso in pasos[-5:]:
        print(paso)
    
    print("\n" + "="*30 + "\n")
    
    # Ejemplo de multiplicación
    print("=== MULTIPLICACIÓN DE MATRICES ===")
    C = [[1, 2], [3, 4]]
    D = [[2, 0], [1, 2]]
    resultado, pasos = multiplicar_matrices(C, D)
    for paso in pasos[-8:]:
        print(paso)
    
    print("\n" + "="*30 + "\n")
    
    # Ejemplo de transpuesta
    print("=== TRANSPUESTA ===")
    E = [[1, 2, 3], [4, 5, 6]]
    resultado, pasos = transponer_matriz(E)
    for paso in pasos[-3:]:
        print(paso)

def obtener_menor(matriz, i, j):
    """
    Retorna la submatriz resultante de eliminar la fila i y la columna j.
    """
    return [fila[:j] + fila[j+1:] for k, fila in enumerate(matriz) if k != i]       
    
def determinante(matriz):
    """
    Calcula el determinante de una matriz cuadrada.
    """
    # Validación básica
    n = len(matriz)
    if n == 0 or any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada para calcular el determinante.")

    # Caso base: matriz 1x1
    if n == 1:
        return matriz[0][0]

    # Caso base: matriz 2x2
    if n == 2:
        return (matriz[0][0] * matriz[1][1]) - (matriz[0][1] * matriz[1][0])

    # Caso recursivo: Expansión por cofactores (usando la primera fila)
    det = 0
    for j in range(n):
        signo = (-1) ** j
        menor = obtener_menor(matriz, 0, j)
        det += signo * matriz[0][j] * determinante(menor)
    
    return det