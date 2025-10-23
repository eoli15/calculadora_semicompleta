"""
Módulo de análisis de vectores e independencia lineal.

Este módulo implementa funciones para analizar conjuntos de vectores,
determinar su independencia lineal y calcular el rango de matrices
formadas por vectores, con seguimiento detallado de todos los pasos.

Funciones principales:
- analizar_independencia: Analiza la independencia lineal de un conjunto de vectores
- formar_matriz_desde_vectores: Forma una matriz usando vectores como columnas
- calcular_rango: Calcula el rango de una matriz usando eliminación gaussiana
- validar_vectores: Valida un conjunto de vectores
"""

from .gauss import gauss_eliminar, formatear_matriz, es_cero

def validar_vectores(vectores):
    """
    Valida que un conjunto de vectores sea consistente.
    
    Args:
        vectores (list): Lista de vectores (cada vector es una lista)
    
    Returns:
        tuple: (es_valido, mensaje_error, dimension)
            - es_valido: True si los vectores son válidos
            - mensaje_error: Descripción del error si es_valido es False
            - dimension: Dimensión de los vectores si son válidos
    """
    if not vectores:
        return False, "Lista de vectores vacía", 0
    
    if len(vectores) == 0:
        return False, "No se proporcionaron vectores", 0
    
    # Verificar que el primer vector no esté vacío
    if not vectores[0]:
        return False, "El primer vector está vacío", 0
    
    dimension = len(vectores[0])
    
    if dimension == 0:
        return False, "Los vectores tienen dimensión 0", 0
    
    # Verificar que todos los vectores tengan la misma dimensión
    for i, vector in enumerate(vectores):
        if not vector:
            return False, f"Vector {i + 1} está vacío", 0
        
        if len(vector) != dimension:
            return False, f"Vector {i + 1} tiene dimensión {len(vector)}, esperado {dimension}", 0
        
        # Verificar que todos los elementos sean numéricos
        for j, elemento in enumerate(vector):
            try:
                float(elemento)
            except (ValueError, TypeError):
                return False, f"Vector {i + 1}, posición {j + 1}: '{elemento}' no es un número", 0
    
    return True, "", dimension

def formar_matriz_desde_vectores(vectores, como_columnas=True):
    """
    Forma una matriz usando los vectores dados como columnas o filas.
    
    Args:
        vectores (list): Lista de vectores
        como_columnas (bool): Si True, los vectores forman las columnas; si False, las filas
    
    Returns:
        tuple: (matriz, pasos)
            - matriz: Matriz formada o None si hay error
            - pasos: Lista de strings describiendo el proceso
    """
    pasos = ["=== FORMAR MATRIZ DESDE VECTORES ==="]
    
    # Validar vectores
    es_valido, error, dimension = validar_vectores(vectores)
    if not es_valido:
        pasos.append(f"Error: {error}")
        return None, pasos
    
    num_vectores = len(vectores)
    
    if como_columnas:
        pasos.append(f"Formando matriz usando {num_vectores} vectores de dimensión {dimension} como COLUMNAS")
        pasos.append(f"Matriz resultante será de dimensión {dimension}×{num_vectores}")
    else:
        pasos.append(f"Formando matriz usando {num_vectores} vectores de dimensión {dimension} como FILAS")
        pasos.append(f"Matriz resultante será de dimensión {num_vectores}×{dimension}")
    
    pasos.append("")
    pasos.append("Vectores de entrada:")
    for i, vector in enumerate(vectores):
        pasos.append(f"v{i + 1} = {[round(float(x), 3) for x in vector]}")
    
    pasos.append("")
    
    try:
        if como_columnas:
            # Los vectores forman las columnas
            matriz = []
            for i in range(dimension):
                fila = []
                for j in range(num_vectores):
                    fila.append(float(vectores[j][i]))
                matriz.append(fila)
            
            pasos.append("Formando matriz por columnas:")
            pasos.append("M[i][j] = vⱼ[i] (fila i, columna j = elemento i del vector j)")
        else:
            # Los vectores forman las filas
            matriz = []
            for i in range(num_vectores):
                fila = []
                for j in range(dimension):
                    fila.append(float(vectores[i][j]))
                matriz.append(fila)
            
            pasos.append("Formando matriz por filas:")
            pasos.append("M[i][j] = vᵢ[j] (fila i, columna j = elemento j del vector i)")
        
    except (ValueError, TypeError) as e:
        pasos.append(f"Error al convertir elementos a números: {e}")
        return None, pasos
    
    pasos.append("")
    pasos.append("Matriz formada:")
    pasos.append(formatear_matriz(matriz))
    
    return matriz, pasos

def calcular_rango_matriz_simple(matriz):
    """
    Calcula el rango de una matriz regular (no aumentada) usando eliminación gaussiana.
    
    Args:
        matriz (list): Matriz para calcular el rango
    
    Returns:
        tuple: (rango, pasos)
            - rango: Rango de la matriz
            - pasos: Lista de strings describiendo el proceso
    """
    pasos = ["=== CÁLCULO DE RANGO DE MATRIZ ==="]
    
    if not matriz:
        pasos.append("Error: Matriz vacía")
        return 0, pasos
    
    if not matriz[0]:
        pasos.append("Error: Matriz con filas vacías")
        return 0, pasos
    
    # Copiar matriz para no modificar la original
    matriz_copia = [fila[:] for fila in matriz]
    filas = len(matriz_copia)
    columnas = len(matriz_copia[0])
    
    pasos.append(f"Calculando rango de matriz de dimensión {filas}×{columnas}")
    pasos.append("Matriz original:")
    pasos.append(formatear_matriz(matriz_copia))
    pasos.append("")
    pasos.append("Aplicando eliminación gaussiana...")
    pasos.append("")
    
    rango = 0
    
    for col in range(min(filas, columnas)):
        pasos.append(f"--- Procesar columna {col + 1} ---")
        
        # Encontrar el mejor pivote en esta columna
        mejor_fila = -1
        mejor_valor = 0
        
        for i in range(rango, filas):
            valor_abs = abs(matriz_copia[i][col])
            if valor_abs > mejor_valor and not es_cero(valor_abs):
                mejor_valor = valor_abs
                mejor_fila = i
        
        if mejor_fila == -1 or es_cero(matriz_copia[mejor_fila][col]):
            pasos.append(f"No hay pivote válido en columna {col + 1}")
            continue
        
        # Intercambiar filas si es necesario
        if mejor_fila != rango:
            pasos.append(f"Intercambiar fila {rango + 1} con fila {mejor_fila + 1}")
            matriz_copia[rango], matriz_copia[mejor_fila] = matriz_copia[mejor_fila], matriz_copia[rango]
        
        pivote = matriz_copia[rango][col]
        pasos.append(f"Pivote: {pivote:.3f} en posición ({rango + 1}, {col + 1})")
        
        # Eliminar elementos debajo del pivote
        for fila in range(rango + 1, filas):
            if es_cero(matriz_copia[fila][col]):
                continue
            
            factor = matriz_copia[fila][col] / pivote
            pasos.append(f"F{fila + 1} = F{fila + 1} - ({factor:.3f}) * F{rango + 1}")
            
            for j in range(columnas):
                matriz_copia[fila][j] = matriz_copia[fila][j] - factor * matriz_copia[rango][j]
        
        rango += 1
        pasos.append("Matriz después de este paso:")
        pasos.append(formatear_matriz(matriz_copia))
        pasos.append("")
    
    pasos.append(f"Rango de la matriz: {rango}")
    return rango, pasos

def calcular_rango(matriz):
    """
    Calcula el rango de una matriz usando eliminación gaussiana.
    Función de compatibilidad que llama a calcular_rango_matriz_simple.
    """
    return calcular_rango_matriz_simple(matriz)

def analizar_independencia(vectores, como_columnas=True):
    """
    Analiza la independencia lineal de un conjunto de vectores.
    
    Args:
        vectores (list): Lista de vectores a analizar
        como_columnas (bool): Si True, analiza vectores como columnas; si False, como filas
    
    Returns:
        tuple: (resultado, pasos)
            - resultado: Dict con 'independientes' (bool), 'rango' (int), 'num_vectores' (int)
            - pasos: Lista de strings con todos los pasos del análisis
    
    Ejemplo:
        >>> vectores = [[1, 2, 3], [4, 5, 6], [2, 1, 0]]
        >>> resultado, pasos = analizar_independencia(vectores)
        >>> print(resultado['independientes'])  # False (porque rango < num_vectores)
    """
    pasos_totales = ["=== ANÁLISIS DE INDEPENDENCIA LINEAL ==="]
    
    # Validar vectores
    es_valido, error, dimension = validar_vectores(vectores)
    if not es_valido:
        pasos_totales.append(f"Error: {error}")
        return {"independientes": None, "rango": 0, "num_vectores": 0}, pasos_totales
    
    num_vectores = len(vectores)
    
    pasos_totales.append(f"Analizando {num_vectores} vectores de dimensión {dimension}")
    pasos_totales.append("Vectores:")
    for i, vector in enumerate(vectores):
        pasos_totales.append(f"  v{i + 1} = {[round(float(x), 3) for x in vector]}")
    
    pasos_totales.append("")
    pasos_totales.append("MÉTODO: Formar matriz con los vectores y calcular su rango")
    pasos_totales.append("- Si rango = número de vectores → independientes")
    pasos_totales.append("- Si rango < número de vectores → dependientes")
    pasos_totales.append("")
    
    # Formar matriz
    matriz, pasos_matriz = formar_matriz_desde_vectores(vectores, como_columnas)
    pasos_totales.extend(pasos_matriz)
    
    if matriz is None:
        return {"independientes": None, "rango": 0, "num_vectores": num_vectores}, pasos_totales
    
    pasos_totales.append("")
    
    # Calcular rango
    rango, pasos_rango = calcular_rango(matriz)
    pasos_totales.extend(pasos_rango)
    
    # Determinar independencia
    independientes = rango == num_vectores
    
    pasos_totales.append("")
    pasos_totales.append("=== ANÁLISIS DE RESULTADOS ===")
    pasos_totales.append(f"Número de vectores: {num_vectores}")
    pasos_totales.append(f"Rango de la matriz: {rango}")
    pasos_totales.append(f"Dimensión del espacio: {dimension}")
    pasos_totales.append("")
    
    if independientes:
        pasos_totales.append("CONCLUSIÓN: Los vectores son LINEALMENTE INDEPENDIENTES")
        pasos_totales.append(f"Razón: rango ({rango}) = número de vectores ({num_vectores})")
    else:
        pasos_totales.append("CONCLUSIÓN: Los vectores son LINEALMENTE DEPENDIENTES")
        pasos_totales.append(f"Razón: rango ({rango}) < número de vectores ({num_vectores})")
        
        if rango < num_vectores:
            vectores_redundantes = num_vectores - rango
            pasos_totales.append(f"Hay {vectores_redundantes} vector(es) que puede(n) expresarse como combinación lineal de los otros")
    
    # Información adicional sobre la máxima independencia posible
    if dimension < num_vectores:
        pasos_totales.append("")
        pasos_totales.append("NOTA ADICIONAL:")
        pasos_totales.append(f"En un espacio de dimensión {dimension}, máximo {dimension} vectores pueden ser independientes")
        pasos_totales.append(f"Se tienen {num_vectores} vectores, por lo que necesariamente hay dependencia lineal")
    
    resultado = {
        "independientes": independientes,
        "rango": rango,
        "num_vectores": num_vectores,
        "dimension": dimension
    }
    
    return resultado, pasos_totales

def encontrar_base(vectores, como_columnas=True):
    """
    Encuentra una base a partir de un conjunto de vectores (funcionalidad adicional).
    
    Args:
        vectores (list): Lista de vectores
        como_columnas (bool): Si True, analiza vectores como columnas
    
    Returns:
        tuple: (indices_base, pasos)
            - indices_base: Lista de índices de vectores que forman una base
            - pasos: Lista de strings describiendo el proceso
    """
    pasos = ["=== ENCONTRAR BASE A PARTIR DE VECTORES ==="]
    
    # Validar vectores
    es_valido, error, dimension = validar_vectores(vectores)
    if not es_valido:
        pasos.append(f"Error: {error}")
        return [], pasos
    
    num_vectores = len(vectores)
    pasos.append(f"Buscando base entre {num_vectores} vectores de dimensión {dimension}")
    pasos.append("")
    
    # Formar matriz y aplicar eliminación gaussiana
    matriz, pasos_matriz = formar_matriz_desde_vectores(vectores, como_columnas)
    if matriz is None:
        return [], pasos + pasos_matriz
    
    pasos.extend(pasos_matriz[-3:])  # Solo incluir el resultado final
    pasos.append("")
    
    # Aplicar eliminación gaussiana para identificar columnas pivote
    matriz_copia = [fila[:] for fila in matriz]
    matriz_escalonada, pasos_eliminacion, rango = gauss_eliminar(matriz_copia)
    
    pasos.append("Aplicando eliminación gaussiana para identificar columnas pivote...")
    pasos.append(f"Rango encontrado: {rango}")
    pasos.append("")
    
    # Encontrar las columnas pivote
    indices_base = []
    for i in range(len(matriz_escalonada)):
        for j in range(len(matriz_escalonada[0])):
            if not es_cero(matriz_escalonada[i][j]):
                if j not in indices_base:
                    indices_base.append(j)
                break
    
    # Limitar a los primeros 'rango' indices
    indices_base = indices_base[:rango]
    
    pasos.append(f"Vectores que forman una base: {[f'v{i+1}' for i in indices_base]}")
    pasos.append(f"Índices: {[i+1 for i in indices_base]}")
    
    if indices_base:
        pasos.append("")
        pasos.append("Base encontrada:")
        for idx in indices_base:
            pasos.append(f"  v{idx + 1} = {[round(float(x), 3) for x in vectores[idx]]}")
    
    return indices_base, pasos

# Ejemplo de uso para pruebas
if __name__ == "__main__":
    # Ejemplo 1: Vectores dependientes
    print("=== EJEMPLO 1: Vectores linealmente dependientes ===")
    vectores1 = [[1, 2, 3], [4, 5, 6], [2, 1, 0]]
    resultado, pasos = analizar_independencia(vectores1)
    for paso in pasos[-8:]:
        print(paso)
    
    print("\n" + "="*50 + "\n")
    
    # Ejemplo 2: Vectores independientes
    print("=== EJEMPLO 2: Vectores linealmente independientes ===")
    vectores2 = [[1, 0], [0, 1]]
    resultado, pasos = analizar_independencia(vectores2)
    for paso in pasos[-6:]:
        print(paso)
    
    print("\n" + "="*50 + "\n")
    
    # Ejemplo 3: Más vectores que dimensión
    print("=== EJEMPLO 3: Más vectores que la dimensión del espacio ===")
    vectores3 = [[1, 0], [0, 1], [1, 1]]
    resultado, pasos = analizar_independencia(vectores3)
    for paso in pasos[-10:]:
        print(paso)
