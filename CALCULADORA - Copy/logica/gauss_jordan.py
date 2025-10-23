"""
Módulo de eliminación de Gauss-Jordan para resolver sistemas de ecuaciones lineales.

Este módulo implementa el método de eliminación de Gauss-Jordan (forma escalonada 
reducida por filas - RREF) para resolver sistemas de ecuaciones de la forma Ax = b,
con seguimiento detallado de todos los pasos del proceso.

Funciones principales:
- gauss_jordan_resolver: Resuelve un sistema completo Ax = b
- gauss_jordan_rref: Convierte una matriz a su forma escalonada reducida
- normalizar_pivotes: Normaliza los pivotes a 1
"""

from .gauss import es_cero, formatear_matriz, encontrar_pivote

def normalizar_pivote(matriz, fila, col_pivote, pasos):
    """
    Normaliza un pivote dividiendo toda la fila por el valor del pivote.
    
    Args:
        matriz (list): Matriz a modificar
        fila (int): Índice de la fila del pivote
        col_pivote (int): Índice de la columna del pivote
        pasos (list): Lista para registrar pasos
    """
    pivote = matriz[fila][col_pivote]
    
    if es_cero(pivote):
        pasos.append(f"Error: Pivote en ({fila + 1}, {col_pivote + 1}) es cero")
        return
    
    if abs(pivote - 1.0) > 1e-10:  # Solo normalizar si el pivote no es 1
        pasos.append(f"Normalizar fila {fila + 1}: F{fila + 1} = F{fila + 1} / {pivote:.3f}")
        
        for j in range(len(matriz[fila])):
            matriz[fila][j] = matriz[fila][j] / pivote
    else:
        pasos.append(f"Pivote en ({fila + 1}, {col_pivote + 1}) ya es 1.000")

def eliminar_columna_completa(matriz, fila_pivote, col_pivote, pasos):
    """
    Elimina todos los elementos de una columna excepto el pivote (tanto arriba como abajo).
    
    Args:
        matriz (list): Matriz a modificar
        fila_pivote (int): Índice de la fila del pivote
        col_pivote (int): Índice de la columna del pivote
        pasos (list): Lista para registrar pasos
    """
    filas = len(matriz)
    
    # Eliminar elementos arriba del pivote
    for i in range(fila_pivote):
        if es_cero(matriz[i][col_pivote]):
            continue
            
        factor = matriz[i][col_pivote]
        pasos.append(f"Eliminar posición ({i + 1}, {col_pivote + 1}): F{i + 1} = F{i + 1} - ({factor:.3f}) * F{fila_pivote + 1}")
        
        for j in range(len(matriz[i])):
            matriz[i][j] = matriz[i][j] - factor * matriz[fila_pivote][j]
    
    # Eliminar elementos debajo del pivote
    for i in range(fila_pivote + 1, filas):
        if es_cero(matriz[i][col_pivote]):
            continue
            
        factor = matriz[i][col_pivote]
        pasos.append(f"Eliminar posición ({i + 1}, {col_pivote + 1}): F{i + 1} = F{i + 1} - ({factor:.3f}) * F{fila_pivote + 1}")
        
        for j in range(len(matriz[i])):
            matriz[i][j] = matriz[i][j] - factor * matriz[fila_pivote][j]

def gauss_jordan_rref(matriz_aumentada):
    """
    Convierte una matriz aumentada a su forma escalonada reducida (RREF).
    
    Args:
        matriz_aumentada (list): Matriz aumentada [A|b]
    
    Returns:
        tuple: (matriz_rref, pasos, rango)
            - matriz_rref: Matriz en forma escalonada reducida
            - pasos: Lista de strings describiendo cada paso
            - rango: Rango de la matriz A (sin la columna aumentada)
    
    Ejemplo:
        >>> matriz = [[1, 2, 3, 7], [4, 5, 6, 8], [2, 1, 0, 9]]
        >>> resultado, pasos, rango = gauss_jordan_rref(matriz)
    """
    if not matriz_aumentada or not matriz_aumentada[0]:
        return [], ["Error: Matriz vacía"], 0
    
    # Copiar matriz para no modificar la original
    matriz = [fila[:] for fila in matriz_aumentada]
    pasos = ["=== ELIMINACIÓN DE GAUSS-JORDAN (RREF) ==="]
    pasos.append("Matriz aumentada inicial:")
    pasos.append(formatear_matriz(matriz))
    pasos.append("")
    
    filas = len(matriz)
    columnas = len(matriz[0]) - 1  # Excluir la columna aumentada
    rango = 0
    
    # Fase 1: Eliminación hacia adelante (igual que Gauss normal)
    pasos.append("=== FASE 1: Eliminación hacia adelante ===")
    
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
        
        # Normalizar pivote a 1
        normalizar_pivote(matriz, rango, col, pasos)
        
        pivote = matriz[rango][col]
        pasos.append(f"Pivote normalizado: {pivote:.3f} en posición ({rango + 1}, {col + 1})")
        
        # Eliminar elementos debajo del pivote
        elementos_eliminados = False
        for fila in range(rango + 1, filas):
            if not es_cero(matriz[fila][col]):
                elementos_eliminados = True
                factor = matriz[fila][col]
                pasos.append(f"Eliminar posición ({fila + 1}, {col + 1}): F{fila + 1} = F{fila + 1} - ({factor:.3f}) * F{rango + 1}")
                
                for j in range(len(matriz[fila])):
                    matriz[fila][j] = matriz[fila][j] - factor * matriz[rango][j]
        
        if elementos_eliminados or pasos[-2].startswith("Normalizar"):
            pasos.append("Matriz después de este paso:")
            pasos.append(formatear_matriz(matriz))
        
        rango += 1
        pasos.append("")
    
    # Fase 2: Eliminación hacia atrás para obtener RREF
    pasos.append("=== FASE 2: Eliminación hacia atrás (para RREF) ===")
    
    pivotes_procesados = []
    
    # Encontrar las posiciones de los pivotes
    for fila in range(min(rango, filas)):
        for col in range(columnas):
            if not es_cero(matriz[fila][col]):
                pivotes_procesados.append((fila, col))
                break
    
    # Procesar pivotes desde abajo hacia arriba
    for i in range(len(pivotes_procesados) - 1, -1, -1):
        fila_pivote, col_pivote = pivotes_procesados[i]
        
        pasos.append(f"--- Eliminar elementos arriba del pivote en ({fila_pivote + 1}, {col_pivote + 1}) ---")
        
        elementos_eliminados = False
        for fila in range(fila_pivote):
            if not es_cero(matriz[fila][col_pivote]):
                elementos_eliminados = True
                factor = matriz[fila][col_pivote]
                pasos.append(f"Eliminar posición ({fila + 1}, {col_pivote + 1}): F{fila + 1} = F{fila + 1} - ({factor:.3f}) * F{fila_pivote + 1}")
                
                for j in range(len(matriz[fila])):
                    matriz[fila][j] = matriz[fila][j] - factor * matriz[fila_pivote][j]
        
        if elementos_eliminados:
            pasos.append("Matriz después de eliminar arriba del pivote:")
            pasos.append(formatear_matriz(matriz))
        else:
            pasos.append("No hay elementos que eliminar arriba de este pivote")
        
        pasos.append("")
    
    pasos.append(f"RREF completada. Rango de la matriz: {rango}")
    pasos.append("Matriz en forma escalonada reducida:")
    pasos.append(formatear_matriz(matriz))
    
    return matriz, pasos, rango

def extraer_solucion_rref(matriz_rref, rango):
    """
    Extrae la solución de una matriz en forma escalonada reducida.
    
    Args:
        matriz_rref (list): Matriz en forma escalonada reducida
        rango (int): Rango de la matriz
    
    Returns:
        tuple: (solucion, pasos)
            - solucion: Vector solución, "infinitas", o None
            - pasos: Lista de strings describiendo el proceso
    """
    pasos = ["=== EXTRACCIÓN DE LA SOLUCIÓN ==="]
    
    if not matriz_rref:
        return None, pasos + ["Error: Matriz vacía"]
    
    filas = len(matriz_rref)
    columnas = len(matriz_rref[0]) - 1
    
    # Verificar consistencia del sistema
    for i in range(rango, filas):
        if not es_cero(matriz_rref[i][-1]):  # Última columna (b) no es cero
            pasos.append(f"Sistema inconsistente: fila {i + 1} tiene la forma 0 = {matriz_rref[i][-1]:.3f}")
            return None, pasos
    
    if rango < columnas:
        pasos.append(f"Sistema tiene infinitas soluciones (rango {rango} < {columnas} variables)")
        pasos.append("Variables libres presentes.")
        return "infinitas", pasos
    
    # Sistema tiene solución única - leer directamente de RREF
    solucion = [0.0] * columnas
    pasos.append("Sistema tiene solución única. Leyendo solución de RREF:")
    
    # En RREF, cada fila con pivote tiene la forma [0...0 1 * * * | valor]
    # donde el 1 está en la posición del pivote
    for i in range(min(rango, columnas)):
        # Encontrar la columna del pivote en esta fila
        col_pivote = -1
        for j in range(columnas):
            if not es_cero(matriz_rref[i][j]):
                col_pivote = j
                break
        
        if col_pivote != -1 and abs(matriz_rref[i][col_pivote] - 1.0) < 1e-10:
            solucion[col_pivote] = matriz_rref[i][-1]
            pasos.append(f"x{col_pivote + 1} = {solucion[col_pivote]:.3f}")
    
    return solucion, pasos

def gauss_jordan_resolver(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando eliminación de Gauss-Jordan.
    
    Args:
        A (list): Matriz de coeficientes (lista de listas)
        b (list): Vector de términos independientes
    
    Returns:
        tuple: (estado, solucion, pasos)
            - estado: "unica", "infinitas", "inconsistente", o "error"
            - solucion: Vector solución, "infinitas", o None
            - pasos: Lista de strings con todos los pasos del proceso
    
    Ejemplo:
        >>> A = [[2, 1], [1, 3]]
        >>> b = [5, 4]
        >>> estado, solucion, pasos = gauss_jordan_resolver(A, b)
        >>> print(estado)  # "unica"
        >>> print(solucion)  # [1.0, 3.0] (aproximadamente)
    """
    pasos_totales = ["=== RESOLUCIÓN POR ELIMINACIÓN DE GAUSS-JORDAN ===", ""]
    
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
    
    # Gauss-Jordan (RREF)
    matriz_rref, pasos_rref, rango = gauss_jordan_rref(matriz_aumentada)
    pasos_totales.extend(pasos_rref)
    pasos_totales.append("")
    
    # Extraer solución
    solucion, pasos_solucion = extraer_solucion_rref(matriz_rref, rango)
    pasos_totales.extend(pasos_solucion)
    
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
    estado, solucion, pasos = gauss_jordan_resolver(A1, b1)
    for paso in pasos[-10:]:  # Mostrar los últimos 10 pasos
        print(paso)
    
    print("\n" + "="*50 + "\n")
    
    # Ejemplo 2: Sistema más grande
    print("=== EJEMPLO 2: Sistema 3x3 ===")
    A2 = [[1, 2, 1], [3, 8, 1], [0, 4, 1]]
    b2 = [2, 12, 2]
    estado, solucion, pasos = gauss_jordan_resolver(A2, b2)
    print(f"Estado: {estado}")
    if solucion not in [None, "infinitas"]:
        print(f"Solución: {[round(x, 3) for x in solucion]}")
