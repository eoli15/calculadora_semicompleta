"""
Módulo de eliminación gaussiana para resolver sistemas de ecuaciones lineales.

Este módulo implementa el método de eliminación gaussiana con pivoteo parcial
para resolver sistemas de ecuaciones de la forma Ax = b, con seguimiento
detallado de todos los pasos del proceso.

Funciones principales:
- gauss_resolver: Resuelve un sistema completo Ax = b
- gauss_eliminar: Realiza solo la eliminación hacia adelante
- sustitucion_hacia_atras: Realiza la sustitución hacia atrás
"""

def es_cero(valor, tolerancia=1e-10):
    """
    Verifica si un valor es prácticamente cero dentro de una tolerancia.
    
    Args:
        valor (float): Valor a verificar
        tolerancia (float): Tolerancia para la comparación
    
    Returns:
        bool: True si el valor es prácticamente cero
    """
    return abs(valor) < tolerancia

def encontrar_pivote(matriz, fila_inicio, columna, pasos):
    """
    Encuentra el mejor pivote en una columna (pivoteo parcial).
    
    Args:
        matriz (list): Matrix aumentada
        fila_inicio (int): Fila desde donde buscar
        columna (int): Columna donde buscar el pivote
        pasos (list): Lista para registrar pasos
    
    Returns:
        int: Índice de la fila con el mejor pivote, o -1 si no hay pivote
    """
    mejor_fila = -1
    mejor_valor = 0
    
    for i in range(fila_inicio, len(matriz)):
        valor_abs = abs(matriz[i][columna])
        if valor_abs > mejor_valor and not es_cero(valor_abs):
            mejor_valor = valor_abs
            mejor_fila = i
    
    if mejor_fila != -1 and mejor_fila != fila_inicio:
        pasos.append(f"Intercambiar fila {fila_inicio + 1} con fila {mejor_fila + 1} (pivoteo)")
        # Intercambiar filas
        matriz[fila_inicio], matriz[mejor_fila] = matriz[mejor_fila], matriz[fila_inicio]
    
    return mejor_fila if mejor_fila != -1 else fila_inicio

def formatear_matriz(matriz, precision=3):
    """
    Formatea una matriz para mostrarla de forma legible.
    
    Args:
        matriz (list): Matriz a formatear
        precision (int): Número de decimales a mostrar
    
    Returns:
        str: Representación formateada de la matriz
    """
    if not matriz:
        return "[]"
    
    # Encontrar el ancho máximo necesario
    max_width = 0
    for fila in matriz:
        for elemento in fila:
            str_elemento = f"{elemento:.{precision}f}"
            max_width = max(max_width, len(str_elemento))
    
    resultado = []
    for fila in matriz:
        fila_str = "  [" + ", ".join(f"{elemento:>{max_width}.{precision}f}" for elemento in fila) + "]"
        resultado.append(fila_str)
    
    return "[\n" + "\n".join(resultado) + "\n]"

def gauss_eliminar(matriz_aumentada):
    """
    Realiza la eliminación gaussiana hacia adelante en una matriz aumentada.
    
    Args:
        matriz_aumentada (list): Matriz aumentada [A|b]
    
    Returns:
        tuple: (matriz_escalonada, pasos, rango)
            - matriz_escalonada: Matriz después de la eliminación
            - pasos: Lista de strings describiendo cada paso
            - rango: Rango de la matriz A (sin la columna aumentada)
    
    Ejemplo:
        >>> matriz = [[1, 2, 3, 7], [4, 5, 6, 8], [2, 1, 0, 9]]
        >>> resultado, pasos, rango = gauss_eliminar(matriz)
    """
    if not matriz_aumentada or not matriz_aumentada[0]:
        return [], ["Error: Matriz vacía"], 0
    
    # Copiar matriz para no modificar la original
    matriz = [fila[:] for fila in matriz_aumentada]
    pasos = ["=== ELIMINACIÓN GAUSSIANA ==="]
    pasos.append("Matriz aumentada inicial:")
    pasos.append(formatear_matriz(matriz))
    pasos.append("")
    
    filas = len(matriz)
    columnas = len(matriz[0]) - 1  # Excluir la columna aumentada
    rango = 0
    
    for col in range(min(filas, columnas)):
        pasos.append(f"--- Paso {col + 1}: Procesar columna {col + 1} ---")
        
        # Encontrar pivote
        fila_pivote = encontrar_pivote(matriz, rango, col, pasos)
        
        if es_cero(matriz[rango][col]):
            pasos.append(f"No hay pivote válido en columna {col + 1}, continuar con siguiente columna")
            continue
        
        # Mostrar matriz después del posible intercambio
        if pasos[-1].startswith("Intercambiar"):
            pasos.append("Matriz después del intercambio:")
            pasos.append(formatear_matriz(matriz))
        
        pivote = matriz[rango][col]
        pasos.append(f"Pivote: {pivote:.3f} en posición ({rango + 1}, {col + 1})")
        
        # Eliminar elementos debajo del pivote
        for fila in range(rango + 1, filas):
            if es_cero(matriz[fila][col]):
                continue
            
            factor = matriz[fila][col] / pivote
            pasos.append(f"Eliminar posición ({fila + 1}, {col + 1}): F{fila + 1} = F{fila + 1} - ({factor:.3f}) * F{rango + 1}")
            
            for j in range(len(matriz[fila])):
                matriz[fila][j] = matriz[fila][j] - factor * matriz[rango][j]
        
        rango += 1
        pasos.append("Matriz después de la eliminación:")
        pasos.append(formatear_matriz(matriz))
        pasos.append("")
    
    pasos.append(f"Eliminación completada. Rango de la matriz: {rango}")
    return matriz, pasos, rango

def sustitucion_hacia_atras(matriz_escalonada, rango):
    """
    Realiza la sustitución hacia atrás para encontrar la solución.
    
    Args:
        matriz_escalonada (list): Matriz en forma escalonada
        rango (int): Rango de la matriz
    
    Returns:
        tuple: (solucion, pasos)
            - solucion: Vector solución o None si no existe
            - pasos: Lista de strings describiendo cada paso
    """
    pasos = ["=== SUSTITUCIÓN HACIA ATRÁS ==="]
    
    if not matriz_escalonada:
        return None, pasos + ["Error: Matriz vacía"]
    
    filas = len(matriz_escalonada)
    columnas = len(matriz_escalonada[0]) - 1
    
    # Verificar consistencia del sistema
    for i in range(rango, filas):
        if not es_cero(matriz_escalonada[i][-1]):  # Última columna (b) no es cero
            pasos.append(f"Sistema inconsistente: fila {i + 1} tiene la forma 0 = {matriz_escalonada[i][-1]:.3f}")
            return None, pasos
    
    if rango < columnas:
        pasos.append(f"Sistema tiene infinitas soluciones (rango {rango} < {columnas} variables)")
        pasos.append("El sistema es subdeterminado.")
        return "infinitas", pasos
    
    # Sistema tiene solución única
    solucion = [0.0] * columnas
    pasos.append("Sistema tiene solución única. Iniciando sustitución hacia atrás:")
    
    for i in range(rango - 1, -1, -1):
        # Encontrar la columna pivote en esta fila
        col_pivote = -1
        for j in range(columnas):
            if not es_cero(matriz_escalonada[i][j]):
                col_pivote = j
                break
        
        if col_pivote == -1:
            continue
        
        # Calcular el valor de la variable
        suma = matriz_escalonada[i][-1]  # Término independiente
        terminos = [f"{matriz_escalonada[i][-1]:.3f}"]
        
        for j in range(col_pivote + 1, columnas):
            if not es_cero(matriz_escalonada[i][j]):
                suma -= matriz_escalonada[i][j] * solucion[j]
                terminos.append(f"- ({matriz_escalonada[i][j]:.3f}) * ({solucion[j]:.3f})")
        
        solucion[col_pivote] = suma / matriz_escalonada[i][col_pivote]
        
        pasos.append(f"x{col_pivote + 1} = ({' '.join(terminos)}) / {matriz_escalonada[i][col_pivote]:.3f} = {solucion[col_pivote]:.3f}")
    
    return solucion, pasos

def gauss_resolver(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando eliminación gaussiana.
    
    Args:
        A (list): Matriz de coeficientes (lista de listas)
        b (list): Vector de términos independientes
    
    Returns:
        tuple: (estado, solucion, pasos)
            - estado: "unica", "infinitas", "inconsistente", o "error"
            - solucion: Vector solución, "infinitas", o None
            - pasos: Lista de strings con todos los pasos del proceso
    
    Ejemplo:
        >>> A = [[1, 2, 3], [4, 5, 6], [2, 1, 0]]
        >>> b = [7, 8, 9]
        >>> estado, solucion, pasos = gauss_resolver(A, b)
        >>> print(estado)  # "inconsistente"
    """
    pasos_totales = ["=== RESOLUCIÓN POR ELIMINACIÓN GAUSSIANA ===", ""]
    
    # Validaciones básicas
    if not A or not A[0] or not b:
        return "error", None, pasos_totales + ["Error: Matriz o vector vacío"]
    
    if len(A) != len(b):
        return "error", None, pasos_totales + [f"Error: Incompatibilidad de dimensiones - A tiene {len(A)} filas, b tiene {len(b)} elementos"]
    
    for i, fila in enumerate(A):
        if len(fila) != len(A[0]):
            return "error", None, pasos_totales + [f"Error: Fila {i + 1} tiene {len(fila)} elementos, esperado {len(A[0])}"]
    
    pasos_totales.append(f"Sistema: {len(A)} ecuaciones, {len(A[0])} variables")
    pasos_totales.append("Matriz A:")
    pasos_totales.append(formatear_matriz(A))
    pasos_totales.append(f"Vector b: {[round(x, 3) for x in b]}")
    pasos_totales.append("")
    
    # Construir matriz aumentada [A|b]
    try:
        matriz_aumentada = []
        for i in range(len(A)):
            fila_aumentada = A[i][:] + [float(b[i])]
            matriz_aumentada.append(fila_aumentada)
    except (ValueError, TypeError) as e:
        return "error", None, pasos_totales + [f"Error al construir matriz aumentada: {e}"]
    
    # Eliminación gaussiana
    matriz_escalonada, pasos_eliminacion, rango = gauss_eliminar(matriz_aumentada)
    pasos_totales.extend(pasos_eliminacion)
    pasos_totales.append("")
    
    # Sustitución hacia atrás
    solucion, pasos_sustitucion = sustitucion_hacia_atras(matriz_escalonada, rango)
    pasos_totales.extend(pasos_sustitucion)
    
    # Determinar el estado del sistema
    if solucion is None:
        estado = "inconsistente"
        pasos_totales.append("")
        pasos_totales.append("RESULTADO: Sistema inconsistente (no tiene solución)")
    elif solucion == "infinitas":
        estado = "infinitas"
        pasos_totales.append("")
        pasos_totales.append("RESULTADO: Sistema tiene infinitas soluciones")
    else:
        estado = "unica"
        pasos_totales.append("")
        pasos_totales.append("RESULTADO: Solución única encontrada")
        pasos_totales.append(f"Solución: {[round(x, 3) for x in solucion]}")
    
    return estado, solucion, pasos_totales

# Ejemplo de uso para pruebas
if __name__ == "__main__":
    # Ejemplo 1: Sistema con solución única
    print("=== EJEMPLO 1: Sistema con solución única ===")
    A1 = [[2, 1], [1, 3]]
    b1 = [5, 4]
    estado, solucion, pasos = gauss_resolver(A1, b1)
    for paso in pasos:
        print(paso)
    
    print("\n" + "="*50 + "\n")
    
    # Ejemplo 2: Sistema inconsistente
    print("=== EJEMPLO 2: Sistema inconsistente ===")
    A2 = [[1, 2, 3], [4, 5, 6], [2, 1, 0]]
    b2 = [7, 8, 9]
    estado, solucion, pasos = gauss_resolver(A2, b2)
    for paso in pasos[-5:]:  # Mostrar solo los últimos pasos
        print(paso)
