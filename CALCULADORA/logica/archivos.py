"""
Módulo de manejo de archivos para la Calculadora de Álgebra Lineal.

Este módulo implementa funciones para guardar y cargar matrices,
exportar pasos de cálculo y manejar archivos de texto y CSV,
con validación de formato y manejo de errores.

Funciones principales:
- guardar_matriz: Guarda una matriz en archivo de texto
- cargar_matriz: Carga una matriz desde archivo de texto o CSV
- exportar_pasos: Exporta pasos de cálculo a archivo de texto
- exportar_resultado_completo: Exporta matriz, pasos y resultado
"""

import os
from datetime import datetime
import csv

def validar_ruta_archivo(ruta):
    """
    Valida que la ruta de archivo sea válida y el directorio exista.
    
    Args:
        ruta (str): Ruta del archivo
    
    Returns:
        tuple: (es_valida, mensaje_error)
    """
    if not ruta:
        return False, "Ruta de archivo vacía"
    
    # Verificar que el directorio padre exista
    directorio = os.path.dirname(ruta)
    if directorio and not os.path.exists(directorio):
        try:
            os.makedirs(directorio, exist_ok=True)
        except (OSError, PermissionError) as e:
            return False, f"No se puede crear el directorio: {e}"
    
    # Verificar permisos de escritura en el directorio
    directorio_escritura = directorio if directorio else "."
    if not os.access(directorio_escritura, os.W_OK):
        return False, f"Sin permisos de escritura en: {directorio_escritura}"
    
    return True, ""

def formatear_matriz_para_archivo(matriz, precision=6):
    """
    Formatea una matriz para guardarla en archivo de texto.
    
    Args:
        matriz (list): Matriz a formatear
        precision (int): Número de decimales
    
    Returns:
        str: Representación de la matriz para archivo
    """
    if not matriz:
        return "[]"
    
    lineas = []
    for fila in matriz:
        elementos = [f"{float(elemento):.{precision}f}" for elemento in fila]
        lineas.append("\t".join(elementos))
    
    return "\n".join(lineas)

def parsear_matriz_desde_texto(texto):
    """
    Parsea una matriz desde texto.
    
    Args:
        texto (str): Texto conteniendo la matriz
    
    Returns:
        tuple: (matriz, error)
            - matriz: Matriz parseada o None si hay error
            - error: Mensaje de error si hay problemas
    """
    if not texto.strip():
        return None, "Texto vacío"
    
    lineas = texto.strip().split('\n')
    matriz = []
    columnas_esperadas = None
    
    for i, linea in enumerate(lineas):
        linea = linea.strip()
        if not linea:
            continue
        
        # Intentar separar por diferentes delimitadores
        if '\t' in linea:
            elementos_str = linea.split('\t')
        elif ',' in linea:
            elementos_str = linea.split(',')
        elif ';' in linea:
            elementos_str = linea.split(';')
        else:
            elementos_str = linea.split()
        
        # Filtrar elementos vacíos
        elementos_str = [e.strip() for e in elementos_str if e.strip()]
        
        if not elementos_str:
            continue
        
        # Validar número de columnas
        if columnas_esperadas is None:
            columnas_esperadas = len(elementos_str)
        elif len(elementos_str) != columnas_esperadas:
            return None, f"Fila {i + 1}: esperado {columnas_esperadas} elementos, encontrado {len(elementos_str)}"
        
        # Convertir a números
        fila = []
        for j, elemento_str in enumerate(elementos_str):
            try:
                numero = float(elemento_str)
                fila.append(numero)
            except ValueError:
                return None, f"Fila {i + 1}, columna {j + 1}: '{elemento_str}' no es un número válido"
        
        matriz.append(fila)
    
    if not matriz:
        return None, "No se encontraron datos válidos de matriz"
    
    return matriz, ""

def guardar_matriz(matriz, ruta_archivo, titulo="Matriz", incluir_timestamp=True):
    """
    Guarda una matriz en un archivo de texto.
    
    Args:
        matriz (list): Matriz a guardar
        ruta_archivo (str): Ruta del archivo donde guardar
        titulo (str): Título descriptivo para el archivo
        incluir_timestamp (bool): Si incluir marca temporal
    
    Returns:
        tuple: (exito, mensaje)
            - exito: True si se guardó correctamente
            - mensaje: Mensaje de éxito o error
    """
    # Validar matriz
    if not matriz:
        return False, "Matriz vacía"
    
    if not matriz[0]:
        return False, "Matriz con filas vacías"
    
    # Validar ruta
    es_valida, error_ruta = validar_ruta_archivo(ruta_archivo)
    if not es_valida:
        return False, error_ruta
    
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            # Escribir encabezado
            if incluir_timestamp:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                archivo.write(f"# {titulo}\n")
                archivo.write(f"# Guardado el: {timestamp}\n")
                archivo.write(f"# Dimensiones: {len(matriz)}×{len(matriz[0])}\n")
                archivo.write("#\n")
            
            # Escribir matriz
            contenido_matriz = formatear_matriz_para_archivo(matriz)
            archivo.write(contenido_matriz)
            archivo.write("\n")
        
        return True, f"Matriz guardada correctamente en: {ruta_archivo}"
    
    except (IOError, OSError, PermissionError) as e:
        return False, f"Error al guardar archivo: {e}"

def cargar_matriz(ruta_archivo):
    """
    Carga una matriz desde un archivo de texto o CSV.
    
    Args:
        ruta_archivo (str): Ruta del archivo a cargar
    
    Returns:
        tuple: (matriz, mensaje)
            - matriz: Matriz cargada o None si hay error
            - mensaje: Mensaje de éxito o error
    """
    # Verificar que el archivo exista
    if not os.path.exists(ruta_archivo):
        return None, f"Archivo no encontrado: {ruta_archivo}"
    
    if not os.path.isfile(ruta_archivo):
        return None, f"La ruta no es un archivo: {ruta_archivo}"
    
    try:
        # Leer el archivo
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        
        # Filtrar comentarios (líneas que empiecen con #)
        lineas_filtradas = []
        for linea in contenido.split('\n'):
            linea_limpia = linea.strip()
            if linea_limpia and not linea_limpia.startswith('#'):
                lineas_filtradas.append(linea_limpia)
        
        contenido_limpio = '\n'.join(lineas_filtradas)
        
        # Parsear matriz
        matriz, error = parsear_matriz_desde_texto(contenido_limpio)
        if error:
            return None, f"Error al parsear matriz: {error}"
        
        return matriz, f"Matriz cargada correctamente desde: {ruta_archivo} (dimensión {len(matriz)}×{len(matriz[0])})"
    
    except (IOError, OSError, UnicodeDecodeError) as e:
        return None, f"Error al leer archivo: {e}"

def exportar_pasos(pasos, ruta_archivo, titulo="Cálculo", incluir_timestamp=True):
    """
    Exporta una lista de pasos de cálculo a un archivo de texto.
    
    Args:
        pasos (list): Lista de strings con los pasos
        ruta_archivo (str): Ruta del archivo donde guardar
        titulo (str): Título para el archivo
        incluir_timestamp (bool): Si incluir marca temporal
    
    Returns:
        tuple: (exito, mensaje)
            - exito: True si se exportó correctamente
            - mensaje: Mensaje de éxito o error
    """
    if not pasos:
        return False, "Lista de pasos vacía"
    
    # Validar ruta
    es_valida, error_ruta = validar_ruta_archivo(ruta_archivo)
    if not es_valida:
        return False, error_ruta
    
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            # Escribir encabezado
            if incluir_timestamp:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                archivo.write(f"# {titulo}\n")
                archivo.write(f"# Exportado el: {timestamp}\n")
                archivo.write(f"# Total de pasos: {len(pasos)}\n")
                archivo.write("#" + "="*60 + "\n\n")
            
            # Escribir pasos
            for i, paso in enumerate(pasos):
                archivo.write(f"{paso}\n")
            
            archivo.write(f"\n# Fin del cálculo\n")
        
        return True, f"Pasos exportados correctamente a: {ruta_archivo}"
    
    except (IOError, OSError, PermissionError) as e:
        return False, f"Error al exportar pasos: {e}"

def exportar_resultado_completo(datos_entrada, pasos, resultado, ruta_archivo, tipo_calculo="Cálculo"):
    """
    Exporta un resultado completo incluyendo datos de entrada, pasos y resultado.
    
    Args:
        datos_entrada (dict): Diccionario con los datos de entrada
        pasos (list): Lista de pasos del cálculo
        resultado (any): Resultado del cálculo
        ruta_archivo (str): Ruta del archivo donde guardar
        tipo_calculo (str): Tipo de cálculo realizado
    
    Returns:
        tuple: (exito, mensaje)
            - exito: True si se exportó correctamente
            - mensaje: Mensaje de éxito o error
    """
    # Validar ruta
    es_valida, error_ruta = validar_ruta_archivo(ruta_archivo)
    if not es_valida:
        return False, error_ruta
    
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            # Encabezado
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"# CALCULADORA DE ÁLGEBRA LINEAL\n")
            archivo.write(f"# Tipo de cálculo: {tipo_calculo}\n")
            archivo.write(f"# Fecha y hora: {timestamp}\n")
            archivo.write("#" + "="*70 + "\n\n")
            
            # Datos de entrada
            archivo.write("DATOS DE ENTRADA:\n")
            archivo.write("-" * 20 + "\n")
            for clave, valor in datos_entrada.items():
                archivo.write(f"{clave}:\n")
                if isinstance(valor, list) and valor and isinstance(valor[0], list):
                    # Es una matriz
                    archivo.write(formatear_matriz_para_archivo(valor))
                elif isinstance(valor, list):
                    # Es un vector
                    archivo.write(f"{[round(float(x), 6) for x in valor]}")
                else:
                    archivo.write(f"{valor}")
                archivo.write("\n\n")
            
            # Pasos del cálculo
            archivo.write("PROCESO DE CÁLCULO:\n")
            archivo.write("-" * 25 + "\n")
            for paso in pasos:
                archivo.write(f"{paso}\n")
            archivo.write("\n")
            
            # Resultado
            archivo.write("RESULTADO FINAL:\n")
            archivo.write("-" * 20 + "\n")
            if isinstance(resultado, list) and resultado and isinstance(resultado[0], list):
                # Es una matriz
                archivo.write(formatear_matriz_para_archivo(resultado))
            elif isinstance(resultado, list):
                # Es un vector
                archivo.write(f"{[round(float(x), 3) for x in resultado]}")
            elif isinstance(resultado, dict):
                # Es un diccionario (como resultado de independencia)
                for clave, valor in resultado.items():
                    archivo.write(f"{clave}: {valor}\n")
            else:
                archivo.write(f"{resultado}")
            archivo.write("\n\n")
            
            archivo.write("# Fin del reporte\n")
        
        return True, f"Resultado completo exportado a: {ruta_archivo}"
    
    except (IOError, OSError, PermissionError) as e:
        return False, f"Error al exportar resultado completo: {e}"

def cargar_matriz_csv(ruta_archivo, delimitador=','):
    """
    Carga una matriz específicamente desde un archivo CSV.
    
    Args:
        ruta_archivo (str): Ruta del archivo CSV
        delimitador (str): Delimitador usado en el CSV
    
    Returns:
        tuple: (matriz, mensaje)
            - matriz: Matriz cargada o None si hay error
            - mensaje: Mensaje de éxito o error
    """
    if not os.path.exists(ruta_archivo):
        return None, f"Archivo no encontrado: {ruta_archivo}"
    
    try:
        matriz = []
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            lector_csv = csv.reader(archivo, delimiter=delimitador)
            
            columnas_esperadas = None
            for i, fila in enumerate(lector_csv):
                # Filtrar elementos vacíos
                elementos = [elem.strip() for elem in fila if elem.strip()]
                
                if not elementos:
                    continue
                
                # Validar número de columnas
                if columnas_esperadas is None:
                    columnas_esperadas = len(elementos)
                elif len(elementos) != columnas_esperadas:
                    return None, f"Fila {i + 1}: esperado {columnas_esperadas} elementos, encontrado {len(elementos)}"
                
                # Convertir a números
                fila_numerica = []
                for j, elemento in enumerate(elementos):
                    try:
                        numero = float(elemento)
                        fila_numerica.append(numero)
                    except ValueError:
                        return None, f"Fila {i + 1}, columna {j + 1}: '{elemento}' no es un número válido"
                
                matriz.append(fila_numerica)
        
        if not matriz:
            return None, "No se encontraron datos válidos en el CSV"
        
        return matriz, f"Matriz CSV cargada correctamente (dimensión {len(matriz)}×{len(matriz[0])})"
    
    except (IOError, OSError, UnicodeDecodeError) as e:
        return None, f"Error al leer archivo CSV: {e}"

def generar_nombre_archivo(base="calculo", extension="txt", incluir_timestamp=True):
    """
    Genera un nombre de archivo único con timestamp opcional.
    
    Args:
        base (str): Nombre base del archivo
        extension (str): Extensión del archivo (sin punto)
        incluir_timestamp (bool): Si incluir timestamp en el nombre
    
    Returns:
        str: Nombre de archivo generado
    """
    if incluir_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base}_{timestamp}.{extension}"
    else:
        return f"{base}.{extension}"

# Ejemplo de uso para pruebas
if __name__ == "__main__":
    # Ejemplo de guardado y carga de matriz
    print("=== PRUEBA DE GUARDADO Y CARGA ===")
    
    # Matriz de prueba
    matriz_test = [[1.5, 2.7, 3.1], [4.2, 5.8, 6.3], [7.9, 8.4, 9.6]]
    
    # Generar nombre único
    nombre_archivo = generar_nombre_archivo("matriz_test", "txt")
    print(f"Archivo a usar: {nombre_archivo}")
    
    # Guardar matriz
    exito, mensaje = guardar_matriz(matriz_test, nombre_archivo, "Matriz de Prueba")
    print(f"Guardado: {mensaje}")
    
    if exito:
        # Cargar matriz
        matriz_cargada, mensaje_carga = cargar_matriz(nombre_archivo)
        print(f"Carga: {mensaje_carga}")
        
        if matriz_cargada:
            print(f"Matriz original:  {matriz_test}")
            print(f"Matriz cargada:   {matriz_cargada}")
            print(f"Son iguales: {matriz_test == matriz_cargada}")
    
    print("\n=== PRUEBA DE EXPORTACIÓN DE PASOS ===")
    
    # Pasos de ejemplo
    pasos_test = [
        "=== SUMA DE MATRICES ===",
        "Matriz A: [[1, 2], [3, 4]]",
        "Matriz B: [[5, 6], [7, 8]]",
        "Resultado: [[6, 8], [10, 12]]"
    ]
    
    nombre_pasos = generar_nombre_archivo("pasos_test", "txt")
    exito_pasos, mensaje_pasos = exportar_pasos(pasos_test, nombre_pasos, "Prueba de Pasos")
    print(f"Exportación: {mensaje_pasos}")
