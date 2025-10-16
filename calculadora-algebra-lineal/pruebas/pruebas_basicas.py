"""
Pruebas básicas para la Calculadora de Álgebra Lineal.

Este módulo contiene pruebas unitarias básicas para verificar el correcto
funcionamiento de todos los módulos de lógica matemática sin usar
librerías externas como pytest o unittest.

Funciones de prueba:
- Eliminación gaussiana (sistemas consistentes e inconsistentes)
- Eliminación de Gauss-Jordan
- Operaciones matriciales básicas
- Análisis de independencia lineal
- Cálculo de rango y transpuesta
- Manejo de archivos
"""

import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logica.gauss import gauss_resolver
from logica.gauss_jordan import gauss_jordan_resolver
from logica.operaciones_matrices import (
    sumar_matrices, restar_matrices, multiplicar_matrices,
    transponer_matriz, escalar_por_matriz
)
from logica.vectores import analizar_independencia
from logica.matriz_inversa import calcular_matriz_inversa, verificar_invertibilidad
from logica.archivos import guardar_matriz, cargar_matriz, generar_nombre_archivo

class PruebaTester:
    """Clase simple para ejecutar pruebas sin librerías externas."""
    
    def __init__(self):
        self.pruebas_ejecutadas = 0
        self.pruebas_exitosas = 0
        self.errores = []
    
    def assert_equal(self, esperado, obtenido, mensaje=""):
        """Verifica que dos valores sean iguales."""
        self.pruebas_ejecutadas += 1
        if esperado == obtenido:
            self.pruebas_exitosas += 1
            return True
        else:
            error = f"Esperado: {esperado}, Obtenido: {obtenido}"
            if mensaje:
                error = f"{mensaje} - {error}"
            self.errores.append(error)
            return False
    
    def assert_almost_equal(self, esperado, obtenido, tolerancia=1e-6, mensaje=""):
        """Verifica que dos valores float sean aproximadamente iguales."""
        self.pruebas_ejecutadas += 1
        if abs(esperado - obtenido) < tolerancia:
            self.pruebas_exitosas += 1
            return True
        else:
            error = f"Esperado: {esperado}, Obtenido: {obtenido} (diferencia: {abs(esperado - obtenido)})"
            if mensaje:
                error = f"{mensaje} - {error}"
            self.errores.append(error)
            return False
    
    def assert_matriz_almost_equal(self, esperada, obtenida, tolerancia=1e-6, mensaje=""):
        """Verifica que dos matrices sean aproximadamente iguales."""
        self.pruebas_ejecutadas += 1
        
        if not esperada and not obtenida:
            self.pruebas_exitosas += 1
            return True
        
        if not esperada or not obtenida:
            error = f"Una matriz es None - Esperada: {esperada is not None}, Obtenida: {obtenida is not None}"
            if mensaje:
                error = f"{mensaje} - {error}"
            self.errores.append(error)
            return False
        
        if len(esperada) != len(obtenida):
            error = f"Diferente número de filas - Esperado: {len(esperada)}, Obtenido: {len(obtenida)}"
            if mensaje:
                error = f"{mensaje} - {error}"
            self.errores.append(error)
            return False
        
        for i in range(len(esperada)):
            if len(esperada[i]) != len(obtenida[i]):
                error = f"Diferente número de columnas en fila {i} - Esperado: {len(esperada[i])}, Obtenido: {len(obtenida[i])}"
                if mensaje:
                    error = f"{mensaje} - {error}"
                self.errores.append(error)
                return False
            
            for j in range(len(esperada[i])):
                if abs(esperada[i][j] - obtenida[i][j]) > tolerancia:
                    error = f"Diferencia en posición [{i}][{j}] - Esperado: {esperada[i][j]}, Obtenido: {obtenida[i][j]}"
                    if mensaje:
                        error = f"{mensaje} - {error}"
                    self.errores.append(error)
                    return False
        
        self.pruebas_exitosas += 1
        return True
    
    def assert_true(self, condicion, mensaje=""):
        """Verifica que una condición sea verdadera."""
        self.pruebas_ejecutadas += 1
        if condicion:
            self.pruebas_exitosas += 1
            return True
        else:
            error = f"Se esperaba True, pero fue False"
            if mensaje:
                error = f"{mensaje} - {error}"
            self.errores.append(error)
            return False
    
    def imprimir_resumen(self):
        """Imprime el resumen de las pruebas."""
        print(f"\n{'='*60}")
        print(f"RESUMEN DE PRUEBAS")
        print(f"{'='*60}")
        print(f"Pruebas ejecutadas: {self.pruebas_ejecutadas}")
        print(f"Pruebas exitosas: {self.pruebas_exitosas}")
        print(f"Pruebas fallidas: {len(self.errores)}")
        
        if self.errores:
            print(f"\nERRORES ENCONTRADOS:")
            for i, error in enumerate(self.errores, 1):
                print(f"{i}. {error}")
        else:
            print(f"\n✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        
        print(f"{'='*60}")

def prueba_gauss_sistema_solucion_unica():
    """Prueba eliminación gaussiana con sistema de solución única."""
    print("Prueba: Sistema con solución única (Gauss)")
    
    tester = PruebaTester()
    
    # Sistema: 2x + y = 5, x + 3y = 4
    # Solución: x = 11/5 = 2.2, y = 5 - 2(2.2) = 0.6
    A = [[2, 1], [1, 3]]
    b = [5, 4]
    
    estado, solucion, pasos = gauss_resolver(A, b)
    
    tester.assert_equal("unica", estado, "Estado del sistema")
    tester.assert_true(solucion is not None, "Solución no debe ser None")
    
    if solucion:
        tester.assert_almost_equal(2.2, solucion[0], 0.01, "Primera variable")
        tester.assert_almost_equal(0.6, solucion[1], 0.01, "Segunda variable")
    
    tester.assert_true(len(pasos) > 10, "Debe haber pasos detallados")
    
    return tester

def prueba_gauss_sistema_inconsistente():
    """Prueba eliminación gaussiana con sistema inconsistente."""
    print("Prueba: Sistema inconsistente (Gauss)")
    
    tester = PruebaTester()
    
    # Sistema inconsistente
    A = [[1, 2, 3], [4, 5, 6], [2, 1, 0]]
    b = [7, 8, 9]
    
    estado, solucion, pasos = gauss_resolver(A, b)
    
    tester.assert_equal("inconsistente", estado, "Estado del sistema")
    tester.assert_equal(None, solucion, "Solución debe ser None para sistema inconsistente")
    tester.assert_true(len(pasos) > 5, "Debe haber pasos detallados")
    
    return tester

def prueba_gauss_jordan_sistema_unico():
    """Prueba eliminación de Gauss-Jordan con sistema de solución única."""
    print("Prueba: Sistema con solución única (Gauss-Jordan)")
    
    tester = PruebaTester()
    
    # Sistema: 2x + y = 5, x + 3y = 4
    A = [[2, 1], [1, 3]]
    b = [5, 4]
    
    estado, solucion, pasos = gauss_jordan_resolver(A, b)
    
    tester.assert_equal("unica", estado, "Estado del sistema")
    tester.assert_true(solucion is not None, "Solución no debe ser None")
    
    if solucion:
        tester.assert_almost_equal(2.2, solucion[0], 0.01, "Primera variable")
        tester.assert_almost_equal(0.6, solucion[1], 0.01, "Segunda variable")
    
    tester.assert_true(len(pasos) > 15, "Gauss-Jordan debe tener más pasos que Gauss normal")
    
    return tester

def prueba_suma_matrices():
    """Prueba suma de matrices."""
    print("Prueba: Suma de matrices")
    
    tester = PruebaTester()
    
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    esperado = [[6, 8], [10, 12]]
    
    resultado, pasos = sumar_matrices(A, B)
    
    tester.assert_matriz_almost_equal(esperado, resultado, mensaje="Resultado de suma")
    tester.assert_true(len(pasos) > 5, "Debe haber pasos detallados")
    
    return tester

def prueba_multiplicacion_matrices():
    """Prueba multiplicación de matrices."""
    print("Prueba: Multiplicación de matrices")
    
    tester = PruebaTester()
    
    A = [[1, 2], [3, 4]]
    B = [[2, 0], [1, 2]]
    esperado = [[4, 4], [10, 8]]  # Resultado de A × B
    
    resultado, pasos = multiplicar_matrices(A, B)
    
    tester.assert_matriz_almost_equal(esperado, resultado, mensaje="Resultado de multiplicación")
    tester.assert_true(len(pasos) > 8, "Debe haber pasos detallados de multiplicación")
    
    return tester

def prueba_transpuesta_matriz():
    """Prueba transpuesta de matriz."""
    print("Prueba: Transpuesta de matriz")
    
    tester = PruebaTester()
    
    A = [[1, 2, 3], [4, 5, 6]]
    esperado = [[1, 4], [2, 5], [3, 6]]
    
    resultado, pasos = transponer_matriz(A)
    
    tester.assert_matriz_almost_equal(esperado, resultado, mensaje="Resultado de transpuesta")
    tester.assert_true(len(pasos) > 3, "Debe haber pasos detallados")
    
    return tester

def prueba_producto_escalar():
    """Prueba producto de matriz por escalar."""
    print("Prueba: Producto por escalar")
    
    tester = PruebaTester()
    
    k = 2.5
    A = [[1, 2], [3, 4]]
    esperado = [[2.5, 5.0], [7.5, 10.0]]
    
    resultado, pasos = escalar_por_matriz(k, A)
    
    tester.assert_matriz_almost_equal(esperado, resultado, mensaje="Resultado de producto por escalar")
    tester.assert_true(len(pasos) > 4, "Debe haber pasos detallados")
    
    return tester

def prueba_vectores_independientes():
    """Prueba análisis de independencia lineal - vectores independientes."""
    print("Prueba: Vectores linealmente independientes")
    
    tester = PruebaTester()
    
    # Vectores canónicos 2D - linealmente independientes
    vectores = [[1, 0], [0, 1]]
    
    resultado, pasos = analizar_independencia(vectores)
    
    tester.assert_equal(True, resultado['independientes'], "Vectores deben ser independientes")
    tester.assert_equal(2, resultado['rango'], "Rango debe ser 2")
    tester.assert_equal(2, resultado['num_vectores'], "Número de vectores debe ser 2")
    tester.assert_true(len(pasos) > 10, "Debe haber análisis detallado")
    
    return tester

def prueba_vectores_dependientes():
    """Prueba análisis de independencia lineal - vectores dependientes."""
    print("Prueba: Vectores linealmente dependientes")
    
    tester = PruebaTester()
    
    # El tercer vector es suma de los primeros dos
    vectores = [[1, 0], [0, 1], [1, 1]]
    
    resultado, pasos = analizar_independencia(vectores)
    
    tester.assert_equal(False, resultado['independientes'], "Vectores deben ser dependientes")
    tester.assert_equal(2, resultado['rango'], "Rango debe ser 2")
    tester.assert_equal(3, resultado['num_vectores'], "Número de vectores debe ser 3")
    tester.assert_true(len(pasos) > 10, "Debe haber análisis detallado")
    
    return tester

def prueba_validacion_errores():
    """Prueba manejo de errores en validaciones."""
    print("Prueba: Validación de errores")
    
    tester = PruebaTester()
    
    # Matriz vacía
    estado, solucion, pasos = gauss_resolver([], [])
    tester.assert_equal("error", estado, "Matriz vacía debe dar error")
    
    # Dimensiones incompatibles para suma
    A = [[1, 2]]
    B = [[1], [2]]
    resultado, pasos = sumar_matrices(A, B)
    tester.assert_equal(None, resultado, "Suma con dimensiones incompatibles debe dar None")
    
    # Dimensiones incompatibles para multiplicación
    A = [[1, 2]]  # 1x2
    B = [[1], [2], [3]]  # 3x1
    resultado, pasos = multiplicar_matrices(A, B)
    tester.assert_equal(None, resultado, "Multiplicación incompatible debe dar None")
    
    return tester

def prueba_archivos_basica():
    """Prueba básica de guardado y carga de archivos."""
    print("Prueba: Guardado y carga de archivos")
    
    tester = PruebaTester()
    
    # Crear matriz de prueba
    matriz_original = [[1.5, 2.3], [4.7, 5.1]]
    nombre_archivo = generar_nombre_archivo("prueba_matriz", "txt")
    
    # Guardar matriz
    exito, mensaje = guardar_matriz(matriz_original, nombre_archivo, "Matriz de Prueba")
    tester.assert_equal(True, exito, "Guardado debe ser exitoso")
    
    # Cargar matriz
    matriz_cargada, mensaje_carga = cargar_matriz(nombre_archivo)
    
    if matriz_cargada:
        tester.assert_matriz_almost_equal(matriz_original, matriz_cargada, mensaje="Matriz cargada debe ser igual a la original")
    else:
        tester.assert_true(False, "Carga de matriz falló")
    
    # Limpiar archivo de prueba
    try:
        os.remove(nombre_archivo)
    except:
        pass  # No importa si no se puede eliminar
    
    return tester

def prueba_matriz_inversa_2x2():
    """Prueba cálculo de matriz inversa 2x2."""
    print("Prueba: Matriz inversa 2x2")
    
    tester = PruebaTester()
    
    # Matriz 2x2 invertible
    A = [[2, 1], [1, 1]]
    # Su inversa debería ser [[1, -1], [-1, 2]]
    esperada = [[1, -1], [-1, 2]]
    
    matriz_inversa, pasos = calcular_matriz_inversa(A)
    
    tester.assert_true(matriz_inversa is not None, "Matriz inversa no debe ser None")
    
    if matriz_inversa:
        tester.assert_matriz_almost_equal(esperada, matriz_inversa, tolerancia=0.01, mensaje="Matriz inversa 2x2")
    
    tester.assert_true(len(pasos) > 20, "Debe haber pasos detallados")
    
    return tester

def prueba_matriz_no_invertible():
    """Prueba matriz no invertible (determinante cero)."""
    print("Prueba: Matriz no invertible")
    
    tester = PruebaTester()
    
    # Matriz singular (no invertible)
    A = [[1, 2], [2, 4]]  # Segunda fila es múltiplo de la primera
    
    matriz_inversa, pasos = calcular_matriz_inversa(A)
    
    tester.assert_equal(None, matriz_inversa, "Matriz no invertible debe retornar None")
    tester.assert_true(len(pasos) > 10, "Debe explicar por qué no es invertible")
    
    return tester

def prueba_verificacion_invertibilidad():
    """Prueba verificación de invertibilidad sin calcular inversa."""
    print("Prueba: Verificación de invertibilidad")
    
    tester = PruebaTester()
    
    # Matriz invertible
    A = [[3, 1], [2, 1]]
    
    es_invertible, razon, det, pasos = verificar_invertibilidad(A)
    
    tester.assert_equal(True, es_invertible, "Matriz debe ser invertible")
    tester.assert_true(abs(det - 1.0) < 0.01, f"Determinante esperado ~1.0, obtenido {det}")
    tester.assert_true(len(pasos) > 8, "Debe haber explicación detallada")
    
    # Matriz no invertible
    B = [[1, 2], [2, 4]]
    
    es_invertible2, razon2, det2, pasos2 = verificar_invertibilidad(B)
    
    tester.assert_equal(False, es_invertible2, "Matriz debe ser no invertible")
    tester.assert_true(abs(det2) < 0.01, f"Determinante esperado ~0, obtenido {det2}")
    tester.assert_true(len(pasos2) > 8, "Debe explicar por qué no es invertible")
    
    return tester

def prueba_matriz_inversa_3x3():
    """Prueba matriz inversa 3x3."""
    print("Prueba: Matriz inversa 3x3")
    
    tester = PruebaTester()
    
    # Matriz 3x3 identidad (su inversa es ella misma)
    A = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    
    matriz_inversa, pasos = calcular_matriz_inversa(A)
    
    tester.assert_true(matriz_inversa is not None, "Matriz identidad debe ser invertible")
    
    if matriz_inversa:
        tester.assert_matriz_almost_equal(A, matriz_inversa, tolerancia=0.01, mensaje="Inversa de identidad es identidad")
    
    tester.assert_true(len(pasos) > 15, "Debe haber pasos detallados")
    
    return tester

def ejecutar_todas_las_pruebas():
    """Ejecuta todas las pruebas y muestra el resumen."""
    print("INICIANDO PRUEBAS BÁSICAS DE LA CALCULADORA DE ÁLGEBRA LINEAL")
    print("=" * 70)
    
    # Lista de todas las funciones de prueba
    pruebas = [
        prueba_gauss_sistema_solucion_unica,
        prueba_gauss_sistema_inconsistente,
        prueba_gauss_jordan_sistema_unico,
        prueba_suma_matrices,
        prueba_multiplicacion_matrices,
        prueba_transpuesta_matriz,
        prueba_producto_escalar,
        prueba_vectores_independientes,
        prueba_vectores_dependientes,
        prueba_validacion_errores,
        prueba_archivos_basica,
        prueba_matriz_inversa_2x2,
        prueba_matriz_no_invertible,
        prueba_verificacion_invertibilidad,
        prueba_matriz_inversa_3x3
    ]
    
    # Tester principal para acumular todos los resultados
    tester_principal = PruebaTester()
    
    # Ejecutar cada prueba
    for i, prueba in enumerate(pruebas, 1):
        print(f"\n{i}. ", end="")
        try:
            resultado_tester = prueba()
            
            # Acumular resultados
            tester_principal.pruebas_ejecutadas += resultado_tester.pruebas_ejecutadas
            tester_principal.pruebas_exitosas += resultado_tester.pruebas_exitosas
            tester_principal.errores.extend(resultado_tester.errores)
            
            # Mostrar resultado individual
            if len(resultado_tester.errores) == 0:
                print(" ✅ PASÓ")
            else:
                print(" ❌ FALLÓ")
                for error in resultado_tester.errores:
                    print(f"   - {error}")
        
        except Exception as e:
            print(f" ❌ ERROR CRÍTICO: {str(e)}")
            tester_principal.pruebas_ejecutadas += 1
            tester_principal.errores.append(f"Error crítico en {prueba.__name__}: {str(e)}")
    
    # Mostrar resumen final
    tester_principal.imprimir_resumen()
    
    # Determinar si todas las pruebas pasaron
    if len(tester_principal.errores) == 0:
        print("\n🎉 ¡TODAS LAS PRUEBAS BÁSICAS FUNCIONAN CORRECTAMENTE!")
        return True
    else:
        print(f"\n⚠️  Hay {len(tester_principal.errores)} errores que corregir.")
        return False

def main():
    """Función principal para ejecutar las pruebas."""
    try:
        exito = ejecutar_todas_las_pruebas()
        
        if exito:
            print("\nLa calculadora está lista para usar.")
        else:
            print("\nRevisa los errores antes de usar la calculadora.")
            
    except Exception as e:
        print(f"\nError crítico al ejecutar las pruebas: {e}")
        
    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
