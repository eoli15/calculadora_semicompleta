# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a comprehensive Linear Algebra Calculator built in Python with a Tkinter GUI. The application solves linear equation systems, performs matrix operations, and analyzes linear independence of vectors - all implemented from scratch without external mathematical libraries like NumPy or SymPy.

## Commands

### Running the Application
```powershell
python interfaz_principal.py
```

### Running Tests
```powershell
# Run the custom test suite (no external testing framework)
python -m pruebas.pruebas_basicas

# Alternative way to run tests
python pruebas/pruebas_basicas.py
```

### Testing Individual Modules
```powershell
# Test Gaussian elimination
python -c "from logica.gauss import gauss_resolver; print(gauss_resolver([[2,1],[1,3]], [5,4]))"

# Test matrix operations
python -c "from logica.operaciones_matrices import sumar_matrices; print(sumar_matrices([[1,2],[3,4]], [[5,6],[7,8]]))"

# Test vector independence
python -c "from logica.vectores import analizar_independencia; print(analizar_independencia([[1,0],[0,1]]))"

# Test matrix inverse
python -c "from logica.matriz_inversa import calcular_matriz_inversa; print(calcular_matriz_inversa([[2,1],[1,1]])[0])"
```

### Development Environment Setup
```powershell
# Check Python version (requires 3.8+)
python --version

# Verify Tkinter is available
python -c "import tkinter; print('Tkinter available')"

# Run a quick smoke test
python -c "import sys; sys.path.insert(0, '.'); from logica import gauss, operaciones_matrices, vectores; print('All modules imported successfully')"
```

## Architecture

### Module Structure

The application follows a clear separation between GUI and mathematical logic:

```
calculadora-algebra-lineal/
├── interfaz_principal.py          # Main GUI application (entry point)
└── logica/                        # Mathematical computation modules
    ├── gauss.py                   # Gaussian elimination
    ├── gauss_jordan.py            # Gauss-Jordan elimination
    ├── operaciones_matrices.py    # Matrix operations
    ├── vectores.py                # Vector analysis and linear independence
    ├── matriz_inversa.py          # Matrix inverse calculation
    └── archivos.py                # File I/O operations
```

### Key Design Patterns

**1. Function-Based Architecture**
- Each mathematical operation returns `(result, steps)` tuples
- `result` contains the mathematical result or None if error
- `steps` contains detailed step-by-step explanations for educational purposes

**2. Numerical Precision Strategy**
- All calculations use Python's built-in `float` type
- Results displayed rounded to 3 decimal places for readability
- Zero comparisons use tolerance of 1e-10 (`es_cero()` function)

**3. Error Handling Pattern**
- Input validation occurs at the GUI layer using `validar_matriz()` and `validar_vector()`
- Mathematical modules assume valid input and focus on algorithm implementation
- Errors are propagated through return values, not exceptions

### Core Mathematical Algorithms

**Gaussian Elimination (`gauss.py`)**
- Implements partial pivoting for numerical stability
- Returns system state: "unica" (unique), "infinitas" (infinite), "inconsistente" (inconsistent)
- Tracks matrix rank and performs back-substitution

**Matrix Operations (`operaciones_matrices.py`)**
- Validates dimension compatibility before operations
- Supports: sum, subtraction, multiplication, transpose, scalar multiplication
- Each operation includes detailed mathematical step tracking

**Vector Analysis (`vectores.py`)**
- Forms matrices from vector sets (as columns)
- Determines linear independence by comparing rank to number of vectors
- Uses Gaussian elimination to calculate matrix rank

**Matrix Inverse (`matriz_inversa.py`)**
- Calculates matrix inverse using Gauss-Jordan elimination method
- Verifies invertibility by computing determinant
- Provides detailed explanations of why matrices are/aren't invertible
- Includes verification that A × A⁻¹ = I

### GUI Architecture (`interfaz_principal.py`)

**Tabbed Interface Structure**
- Each mathematical operation has its own tab (6 tabs total)
- Dynamic field generation based on user-specified dimensions
- Consistent workflow: Configure → Generate Fields → Input Data → Calculate → View Results
- Special "Matrix Inverse" tab with invertibility verification option

**State Management**
- Application maintains `ultimo_resultado`, `ultimos_pasos`, `ultimos_datos_entrada` for file export
- Each tab manages its own entry widgets and result display areas
- Status bar provides real-time feedback on operation progress

### File I/O System (`archivos.py`)

**Export Functionality**
- Generates timestamped filenames automatically
- Exports complete calculation records including: input data, step-by-step process, final results
- Uses plain text format for maximum compatibility

## Development Guidelines

### Code Style and Patterns

**Function Signatures**
- Mathematical functions return `(result, pasos)` tuples consistently
- GUI methods follow naming convention: `generar_campos_*`, `resolver_*`, `limpiar_*`
- Validation functions return `(is_valid, error_message)` tuples

**Mathematical Precision**
- Use `es_cero(valor, tolerancia=1e-10)` for all zero comparisons
- Format display values to 3 decimal places using `formatear_matriz()`
- Preserve full precision in intermediate calculations

**Error Handling**
- GUI layer handles user input validation and displays error messages
- Mathematical modules focus on algorithm correctness, assuming valid input
- File operations return success/failure status with descriptive messages

### Testing Approach

The project uses a custom testing framework (`PruebaTester` class) instead of external libraries:

**Test Categories Covered**
- Gaussian elimination (unique, inconsistent, infinite solutions)
- Matrix operations (sum, multiplication, transpose, scalar)
- Vector independence analysis
- Matrix inverse calculation (2x2, 3x3, invertible/non-invertible)
- Invertibility verification and determinant calculation
- Input validation and error cases
- File I/O operations

**Running Comprehensive Tests**
```powershell
python -m pruebas.pruebas_basicas
```

### Adding New Features

**For New Mathematical Operations:**
1. Implement core algorithm in appropriate `/logica/` module
2. Follow `(result, pasos)` return pattern
3. Add input validation (see `matriz_inversa.py` for square matrix validation example)
4. Create corresponding GUI tab in `interfaz_principal.py`
5. Add test cases to `pruebas_basicas.py`
6. Import new functions in interface and test files

**For GUI Enhancements:**
1. Modify `interfaz_principal.py` following existing tab patterns
2. Implement: `generar_campos_*`, calculation method, `limpiar_*` methods
3. Update `guardar_resultado()` if new data types need export support

## Important Implementation Notes

**No External Mathematical Dependencies**
- The entire mathematical engine is implemented from scratch
- This is intentional for educational purposes
- Do not add NumPy, SciPy, or similar dependencies

**Tkinter GUI Limitations**
- Uses basic Tkinter widgets only
- Dynamic field generation based on spinbox values
- ScrolledText widgets for displaying detailed calculation steps

**Educational Focus**
- All operations show complete step-by-step solutions
- Mathematical notation and terminology in Spanish
- Detailed explanations suitable for students learning linear algebra
- Matrix inverse includes comprehensive invertibility theory explanations
- Determinant calculation with expansion by cofactors for educational clarity

**Windows Compatibility**
- Uses Windows-style path separators in some places
- Designed to run on Windows PowerShell environment
- File dialogs use Windows-native conventions
