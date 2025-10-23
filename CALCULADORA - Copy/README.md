# Calculadora de Álgebra Lineal

Una calculadora completa de álgebra lineal desarrollada en Python 3 con interfaz gráfica usando Tkinter. El proyecto implementa operaciones matriciales, resolución de sistemas de ecuaciones lineales y análisis de independencia lineal de vectores, todo sin usar librerías externas de álgebra como numpy o sympy.

## Características Principales

- **Resolución de sistemas de ecuaciones lineales** usando eliminación de Gauss y Gauss-Jordan
- **Operaciones matriciales** básicas: suma, resta, multiplicación, transpuesta, producto por escalar
- **Análisis de independencia lineal** de conjuntos de vectores
- **Interfaz gráfica intuitiva** con pestañas organizadas por funcionalidad
- **Registro detallado de pasos** para todos los cálculos
- **Exportación de resultados** a archivos de texto
- **Validación completa** de entrada de datos

## Estructura del Proyecto

```
calculadora-algebra-lineal/
│
├── README.md                      # Este archivo
├── interfaz_principal.py          # Archivo principal - ejecutar para iniciar la GUI
│
├── logica/                        # Módulos de lógica matemática
│   ├── __init__.py
│   ├── gauss.py                   # Eliminación gaussiana
│   ├── gauss_jordan.py            # Eliminación de Gauss-Jordan (RREF)
│   ├── operaciones_matrices.py    # Operaciones matriciales básicas
│   ├── vectores.py                # Análisis de vectores e independencia lineal
│   └── archivos.py                # Manejo de archivos (guardar/cargar)
│
└── pruebas/                       # Módulo de pruebas
    ├── __init__.py
    └── pruebas_basicas.py         # Pruebas unitarias básicas
```

## Instalación y Ejecución

### Requisitos
- Python 3.8 o superior
- Tkinter (incluido por defecto en Python)
- No se requieren librerías externas

### Ejecutar la aplicación
```bash
python interfaz_principal.py
```

### Ejecutar las pruebas
```bash
python -m pruebas.pruebas_basicas
```

## Funcionalidades

### 1. Resolver Sistemas de Ecuaciones (Gauss)
Resuelve sistemas de ecuaciones lineales Ax = b usando eliminación gaussiana.

**Ejemplo de entrada:**
```
Matriz A:
1  2  3
4  5  6
2  1  0

Vector b:
7
8
9
```

**Salida esperada:**
- Estado: "Sistema inconsistente" o "Solución única" o "Infinitas soluciones"
- Pasos detallados de la eliminación
- Solución (si existe)

### 2. Resolver Sistemas de Ecuaciones (Gauss-Jordan)
Resuelve sistemas usando el método de Gauss-Jordan (forma escalonada reducida).

### 3. Operaciones Matriciales
- **Suma/Resta:** A ± B (verifica compatibilidad de dimensiones)
- **Multiplicación:** A × B (verifica compatibilidad m×n y n×p)
- **Transpuesta:** A^T
- **Producto por escalar:** k × A

### 4. Independencia Lineal de Vectores
Determina si un conjunto de vectores es linealmente independiente.

**Ejemplo:**
```
Vector 1: [1, 2, 3]
Vector 2: [4, 5, 6]  
Vector 3: [2, 1, 0]
```

**Proceso:**
1. Forma matriz con vectores como columnas
2. Calcula el rango usando eliminación gaussiana
3. Compara el rango con el número de vectores
4. Muestra pasos detallados

### 5. Exportar Resultados
Todos los cálculos pueden exportarse a archivos de texto con marca temporal, incluyendo:
- Datos de entrada
- Pasos detallados del cálculo
- Resultados finales

## Uso de la Interfaz Gráfica

### Pestañas Principales
1. **Gauss:** Resolver sistemas con eliminación gaussiana
2. **Gauss-Jordan:** Resolver sistemas con método de Gauss-Jordan
3. **Operaciones:** Operaciones matriciales básicas
4. **Vectores:** Análisis de independencia lineal
5. **Transpuesta:** Cálculo de matriz transpuesta

### Flujo de Trabajo Típico
1. Seleccionar la pestaña correspondiente
2. Especificar dimensiones (botón "Generar campos")
3. Ingresar datos en los campos generados
4. Hacer clic en "Calcular"
5. Revisar pasos y resultados en el área de texto
6. Opcionalmente exportar resultados con "Guardar resultado"

### Validaciones
- Campos vacíos o no numéricos
- Dimensiones incompatibles para operaciones
- Matrices singulares donde sea relevante
- Mensajes de error claros y específicos

## Ejemplos de Uso

### Sistema de Ecuaciones
```python
# Sistema: x + 2y + 3z = 7
#         4x + 5y + 6z = 8  
#         2x + y = 9

A = [[1, 2, 3],
     [4, 5, 6], 
     [2, 1, 0]]
b = [7, 8, 9]

# Resultado: Sistema inconsistente
```

### Independencia Lineal
```python
# Vectores: v1=[1,2,3], v2=[4,5,6], v3=[2,1,0]
# Matriz formada: [[1,4,2], [2,5,1], [3,6,0]]
# Rango = 2 < 3 vectores → Linealmente dependientes
```

### Operaciones Matriciales
```python
# Transpuesta
A = [[1, 2],
     [3, 4],
     [5, 6]]
# A^T = [[1, 3, 5], [2, 4, 6]]
```

## Características Técnicas

### Precisión Numérica
- Cálculos internos en punto flotante (`float`)
- Salidas redondeadas a 3 decimales para legibilidad
- Tolerancia de 1e-10 para comparaciones con cero

### Manejo de Casos Especiales
- Sistemas inconsistentes
- Sistemas con infinitas soluciones (variables libres)
- Matrices no cuadradas
- Conjuntos vacíos de vectores

### Arquitectura Modular
- Separación clara entre lógica y presentación
- Funciones públicas bien documentadas
- Reutilización de código entre módulos
- Fácil extensión y mantenimiento

## Desarrollo y Pruebas

El proyecto incluye pruebas básicas que verifican:
- Cálculo de rango de matrices
- Operaciones matriciales básicas
- Resolución de sistemas consistentes e inconsistentes
- Análisis de independencia lineal
- Funciones de transposición

Para desarrolladores: cada módulo incluye docstrings detallados y ejemplos de uso en comentarios.

## Limitaciones

- No usa librerías optimizadas (numpy, scipy) por diseño
- Precisión limitada por aritmética de punto flotante estándar
- Interfaz gráfica básica con Tkinter
- Sin soporte para números complejos o racionales

## Autor

Proyecto educativo de calculadora de álgebra lineal implementada desde cero en Python.
