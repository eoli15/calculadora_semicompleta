"""
Módulo para calcular la matriz inversa de una matriz cuadrada sin usar determinantes ni librerías externas.

Este módulo implementa el método de eliminación de Gauss-Jordan
para verificar si una matriz es invertible y calcular su inversa.
Proporciona explicaciones paso a paso del proceso.
"""

# ==========================================
#  VERIFICAR SI ES CUADRADA
# ==========================================
def es_matriz_cuadrada(matriz):
    if not matriz or not matriz[0]:
        return False, "Matriz vacía o con filas vacías", 0

    filas = len(matriz)
    columnas = len(matriz[0])

    for i, fila in enumerate(matriz):
        if len(fila) != columnas:
            return False, f"Fila {i+1} tiene diferente longitud", 0

    if filas != columnas:
        return False, f"La matriz no es cuadrada ({filas}x{columnas})", 0

    return True, "", filas

# ==========================================
#  VERIFICAR INVERTIBILIDAD (SIN DETERMINANTE)
# ==========================================
def verificar_invertibilidad(matriz):
    n = len(matriz)
    A = [fila[:] for fila in matriz]  # copia profunda

    for i in range(n):
        # Buscar pivote distinto de cero en o debajo de la fila actual
        pivote = None
        for r in range(i, n):
            if abs(A[r][i]) > 1e-12:  # considerar tolerancia numérica
                pivote = r
                break

        if pivote is None:
            return False, f"La matriz no es invertible: columna {i+1} sin pivote."

        # Intercambiar filas si es necesario
        if pivote != i:
            A[i], A[pivote] = A[pivote], A[i]

        # Eliminar elementos debajo del pivote
        piv = A[i][i]
        for r in range(i+1, n):
            factor = A[r][i] / piv
            for c in range(i, n):
                A[r][c] -= factor * A[i][c]

    return True, "La matriz es invertible: tiene un pivote en cada columna (rango completo)."

# ==========================================
#  CALCULAR MATRIZ INVERSA (GAUSS-JORDAN)
# ==========================================
def calcular_matriz_inversa(matriz):
    pasos = ["=== CÁLCULO DE MATRIZ INVERSA ==="]

    es_invertible, razon = verificar_invertibilidad(matriz)
    pasos.append(razon)

    if not es_invertible:
        pasos.append("❌ No se puede calcular la inversa de una matriz no invertible.")
        return None, pasos

    n = len(matriz)
    A = [fila[:] for fila in matriz]

    # Crear matriz aumentada [A | I]
    identidad = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    aumentada = [A[i] + identidad[i] for i in range(n)]
    pasos.append("Matriz aumentada inicial [A | I]:")
    pasos.append(formatear_matriz_aumentada(aumentada, n))

    # Gauss-Jordan
    for i in range(n):
        # Buscar pivote
        pivote = i
        for r in range(i, n):
            if abs(aumentada[r][i]) > abs(aumentada[pivote][i]):
                pivote = r

        if pivote != i:
            pasos.append(f"🔁 Intercambiar fila {i+1} con fila {pivote+1}")
            aumentada[i], aumentada[pivote] = aumentada[pivote], aumentada[i]
            pasos.append(formatear_matriz_aumentada(aumentada, n))

        piv = aumentada[i][i]
        if abs(piv) < 1e-12:
            pasos.append(f"❌ Pivote en columna {i+1} es cero. No se puede continuar.")
            return None, pasos

        # Normalizar fila
        pasos.append(f"Dividir fila {i+1} por {piv:.6f}")
        for j in range(2*n):
            aumentada[i][j] /= piv
        pasos.append(formatear_matriz_aumentada(aumentada, n))

        # Hacer ceros arriba y abajo
        for r in range(n):
            if r != i:
                factor = aumentada[r][i]
                if abs(factor) > 1e-12:
                    pasos.append(f"F{r+1} = F{r+1} - ({factor:.6f}) × F{i+1}")
                    for j in range(2*n):
                        aumentada[r][j] -= factor * aumentada[i][j]
                    pasos.append(formatear_matriz_aumentada(aumentada, n))

    # Extraer inversa
    inversa = [fila[n:] for fila in aumentada]
    pasos.append("✅ Matriz inversa encontrada:")
    pasos.append(formatear_matriz(inversa))

    return inversa, pasos

# ==========================================
#  FUNCIONES AUXILIARES
# ==========================================
def formatear_matriz_aumentada(matriz, n):
    maxw = max(len(f"{x:.6f}") for fila in matriz for x in fila)
    texto = []
    for fila in matriz:
        a = " ".join(f"{x:>{maxw}.6f}" for x in fila[:n])
        b = " ".join(f"{x:>{maxw}.6f}" for x in fila[n:])
        texto.append(f"[ {a} | {b} ]")
    return "\n".join(texto)

def formatear_matriz(M):
    maxw = max(len(f"{x:.6f}") for fila in M for x in fila)
    return "\n".join(" ".join(f"{x:>{maxw}.6f}" for x in fila) for fila in M)
