# 🔢 Matriz Inversa - Nueva Funcionalidad

## 📋 Descripción General

La calculadora ahora incluye una funcionalidad completa para calcular matrices inversas y verificar la invertibilidad de matrices cuadradas, con explicaciones educativas detalladas.

## ✨ Características Principales

### 1. **Cálculo de Matriz Inversa**
- **Método**: Eliminación de Gauss-Jordan con matriz aumentada [A|I] → [I|A⁻¹]
- **Soporte**: Matrices cuadradas de 2×2 hasta 6×6
- **Verificación automática**: A × A⁻¹ = I al final del proceso

### 2. **Verificación de Invertibilidad**
- **Opción separada**: Solo verificar si es invertible sin calcular la inversa
- **Cálculo de determinante**: Por expansión de cofactores
- **Explicaciones detalladas**: Por qué una matriz es o no invertible

### 3. **Análisis Educativo Completo**
- **Teoría**: Condiciones para que una matriz sea invertible
- **Pasos detallados**: Cada operación elemental explicada
- **Casos especiales**: Matrices singulares y sus características

## 🎯 Cómo Usar

### Interfaz Gráfica
1. **Abrir la pestaña "Matriz Inversa"**
2. **Configurar dimensión**: Seleccionar tamaño n×n (2 a 6)
3. **Generar campos**: Hacer clic en "Generar Campos"
4. **Ingresar matriz**: Llenar todos los campos numéricos
5. **Elegir operación**:
   - **"Calcular Inversa"**: Proceso completo con matriz inversa
   - **"Solo Verificar Invertibilidad"**: Solo análisis de invertibilidad

### Ejemplos de Uso

#### Matriz Invertible 2×2
```
Entrada:
[2  1]
[1  1]

Resultado:
Inversa: [1  -1]
         [-1  2]

Verificación: A × A⁻¹ = I ✅
```

#### Matriz No Invertible 2×2  
```
Entrada:
[1  2]
[2  4]

Resultado:
❌ La matriz NO es invertible
Razón: det(A) = 0
Explicación: Segunda fila es múltiplo de la primera
```

## 🧠 Conceptos Teóricos Implementados

### Condiciones de Invertibilidad
Una matriz cuadrada A es invertible si y solo si:
1. **det(A) ≠ 0** (determinante diferente de cero)
2. **Filas linealmente independientes**
3. **Columnas linealmente independientes** 
4. **Rango completo** (rango = dimensión)

### Método de Cálculo
1. **Matriz aumentada**: Formar [A|I]
2. **Eliminación hacia adelante**: Triangular superior
3. **Eliminación hacia atrás**: Forma escalonada reducida
4. **Resultado**: [I|A⁻¹]
5. **Verificación**: A × A⁻¹ = I

### Cálculo de Determinante
- **1×1**: det(A) = a₁₁
- **2×2**: det(A) = a₁₁a₂₂ - a₁₂a₂₁
- **n×n**: Expansión por cofactores (primera fila)

## 🛠️ Aspectos Técnicos

### Archivos Modificados/Creados
- **`logica/matriz_inversa.py`** ✨ NUEVO
  - `calcular_matriz_inversa()`
  - `verificar_invertibilidad()`
  - `calcular_determinante_por_expansion()`
- **`interfaz_principal.py`** 🔄 ACTUALIZADO
  - Nueva pestaña "Matriz Inversa"
  - Métodos de interfaz correspondientes
- **`pruebas/pruebas_basicas.py`** 🔄 ACTUALIZADO
  - 4 nuevas pruebas unitarias

### Validaciones Implementadas
- **Solo matrices cuadradas**: Verificación automática
- **Campos numéricos**: Validación de entrada
- **Dimensión limitada**: Máximo 6×6 para rendimiento
- **Tolerancia numérica**: 1e-10 para comparaciones con cero

### Manejo de Errores
- **Matriz no cuadrada**: Error claro y explicativo
- **Determinante cero**: Explicación de no invertibilidad
- **Campos vacíos**: Solicitud de completar datos
- **Errores numéricos**: Advertencias de precisión

## 🎓 Valor Educativo

### Para Estudiantes
- **Comprensión conceptual**: Por qué existe la inversa
- **Proceso paso a paso**: Cada operación explicada
- **Conexión con teoría**: Determinante, rango, independencia lineal
- **Verificación práctica**: Comprobación A × A⁻¹ = I

### Para Profesores
- **Herramienta didáctica**: Mostrar casos específicos
- **Ejemplos variados**: Matrices invertibles y no invertibles
- **Explicaciones detalladas**: Listas para presentar en clase
- **Exportación de resultados**: Para tareas y exámenes

## 📊 Ejemplos Avanzados

### Matriz Identidad 3×3
```
Entrada: I₃ = [1 0 0]
              [0 1 0]  
              [0 0 1]

Resultado: I₃⁻¹ = I₃ (la identidad es su propia inversa)
```

### Matriz Singular 3×3
```
Entrada: [1  2  3]
         [2  4  6]  (segunda fila = 2 × primera fila)
         [1  1  1]

Resultado: det(A) = 0 → No invertible
Explicación: Filas linealmente dependientes
```

## ⚡ Rendimiento

- **Matrices pequeñas** (2×2, 3×3): Instantáneo
- **Matrices medianas** (4×4, 5×5): < 1 segundo  
- **Matrices grandes** (6×6): 1-2 segundos
- **Límite recomendado**: 6×6 por precisión numérica

## 🔮 Futuras Mejoras Posibles

1. **Soporte para matrices más grandes** (con advertencias de precisión)
2. **Diferentes métodos de cálculo** (Adjunta, LU, etc.)
3. **Aritmética de fracciones** para resultados exactos
4. **Visualización gráfica** del proceso de eliminación
5. **Más ejemplos predefinidos** para práctica

---

## 🎉 ¡La matriz inversa ya está disponible!

Esta nueva funcionalidad convierte la calculadora en una herramienta aún más completa para el aprendizaje y práctica del álgebra lineal. 

**Próximos pasos recomendados**:
1. Probar con matrices simples 2×2
2. Experimentar con matrices no invertibles  
3. Usar la función "Solo Verificar" para análisis rápidos
4. Exportar resultados para estudiar los pasos detalladamente
