import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
from sympy import sympify, Symbol, lambdify # SymPy solo para evaluación y ensamblaje
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# --- Funciones de Evaluación ---

GLOBAL_MATH_FUNCTIONS = {
    "e": math.e, "pi": math.pi, "exp": math.exp, "log": math.log,
    "log10": math.log10, "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "sqrt": math.sqrt, "abs": abs, "pow": math.pow,
}

def preprocesar_ecuacion(equation):
    """Aplica reemplazos de notación común (ln -> log, sen -> sin)."""
    ecuacion_limpia = equation.lower()
    replacements = {
        'ln': 'log', 'sen': 'sin', 'tg': 'tan', 'raiz': 'sqrt',
    }
    for key, value in replacements.items():
        ecuacion_limpia = re.sub(r'\b' + key + r'\b', value, ecuacion_limpia)
    return ecuacion_limpia

def ensamblar_ecuacion(lado_izq, lado_der):
    """Ensambla la función de prueba f(x) = LI - LD."""
    return f"({lado_izq}) - ({lado_der})"

def f_eval(ecuacion_str, x_val):
    """Evalúa la función f(x) en x_val usando SymPy y lambdify."""
    try:
        expr = sympify(preprocesar_ecuacion(ecuacion_str))
        x = Symbol('x')
        f_num = lambdify(x, expr, 'numpy') 
        return f_num(x_val)
    except Exception:
        return None

# --- Lógica de Graficación ---

def graficar_funcion():
    """Grafica la función para definir los puntos iniciales."""
    lado_izq_str = entry_left.get()
    lado_der_str = entry_right.get()
    ecuacion_str = ensamblar_ecuacion(lado_izq_str, lado_der_str)
    
    try:
        # Usar los puntos iniciales como centro de un rango si son válidos
        xi = float(entry_xi.get())
        xi_minus_1 = float(entry_xi_minus_1.get())
        
        x_min = min(xi, xi_minus_1) - 1.0
        x_max = max(xi, xi_minus_1) + 1.0
    except ValueError:
        x_min = -2.0
        x_max = 2.0
        
    try:
        x = np.linspace(x_min, x_max, 500)
        y = np.array([f_eval(ecuacion_str, val) for val in x])
        
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.plot(x, y, label=f'f(x) = {ecuacion_str}', color='blue')
        ax.axhline(0, color='black', linewidth=0.8)
        
        ax.set_title('Gráfica para Elegir Puntos Iniciales ($x_{i-1}, x_i$)')
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y (f(x))')
        ax.grid(True)
        ax.legend()
        
        graph_window = tk.Toplevel(root)
        graph_window.title("Visualización de la Función")
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()
        
    except Exception as e:
        messagebox.showerror("Error de Gráfico", f"No se pudo graficar la función. Revise la sintaxis.\nError: {e}")

# --- Método de la Secante ---

def calcular_secante():
    """
    Implementa el Método de la Secante con robustez contra la división por cero.
    """
    resultados_text.delete(1.0, tk.END)

    try:
        # Obtener los dos puntos iniciales
        xi = float(entry_xi.get())
        xi_minus_1 = float(entry_xi_minus_1.get()) 
        tolerancia = float(entry_tolerancia.get())
    except ValueError:
        messagebox.showerror("Error de Entrada", "Asegúrese de que los puntos iniciales y la precisión son números válidos.")
        return

    ecuacion_str = ensamblar_ecuacion(lado_izq_str.get(), lado_der_str.get())
    
    # --- Algoritmo de la Secante ---
    xi_actual = xi
    xi_anterior = xi_minus_1
    iteraciones = 0
    max_iter = 100
    tabla_data = []
    
    # Encabezado
    resultados_text.insert(tk.END, f"\n--- MÉTODO DE LA SECANTE ---\n")
    resultados_text.insert(tk.END, f"Puntos Iniciales: x_{{i-1}} = {xi_anterior}, x_i = {xi_actual}\n")
    resultados_text.insert(tk.END, f"Tolerancia (E): {tolerancia:.6e}\n")
    resultados_text.insert(tk.END, "\n*** TABLA RESUMEN DE ITERACIONES ***\n")
    resultados_text.insert(tk.END, "| Iter. |    x_{i-1}  |     x_i    |   f(x_i)   | Error Fraccional | Error (%) |\n")
    resultados_text.insert(tk.END, "|-------|-------------|------------|------------|------------------|-----------|\n")

    # Incluir el punto inicial en la tabla (Iteración 0)
    tabla_data.append([0, xi_anterior, xi_actual, f_eval(ecuacion_str, xi_actual), 0.0, "---", "---"])
    
    while iteraciones < max_iter:
        iteraciones += 1
        
        f_xi_actual = f_eval(ecuacion_str, xi_actual)
        f_xi_anterior = f_eval(ecuacion_str, xi_anterior)
        
        # ⭐ CHEQUEO DE ROBUSTEZ: Denominador Cero (f(xi) = f(xi-1))
        if abs(f_xi_actual - f_xi_anterior) < 1e-9:
            resultados_text.insert(tk.END, "\n ERROR: Denominador muy cercano a cero ($f(x_i) \approx f(x_{i-1})$). El método diverge. Elija otros puntos iniciales.\n")
            break

        # CÁLCULO DE LA SECANTE
        xi_plus_1 = xi_actual - (f_xi_actual * (xi_actual - xi_anterior) / (f_xi_actual - f_xi_anterior))
        
        # Cálculo de Errores
        error_relativo_float = 0.0
        error_relativo_frac_str = "---"
        error_relativo_porc_str = "---"
        
        if iteraciones > 0 and abs(xi_plus_1) > 1e-9: # Evita división por cero si xi+1 es 0
            error_relativo_float = abs((xi_plus_1 - xi_actual) / xi_plus_1)
            error_relativo_porc_float = error_relativo_float * 100
            
            error_relativo_frac_str = f"{error_relativo_float:.6e}"
            error_relativo_porc_str = f"{error_relativo_porc_float:.8f}"
            
            # ⭐ PARADA POR TOLERANCIA
            if error_relativo_float < tolerancia:
                tabla_data.append([iteraciones, xi_actual, xi_plus_1, f_eval(ecuacion_str, xi_plus_1), error_relativo_float, error_relativo_frac_str, error_relativo_porc_str])
                xi_actual = xi_plus_1
                break
        
        # Capturar la data para la tabla
        tabla_data.append([iteraciones, xi_anterior, xi_actual, f_xi_actual, error_relativo_float, error_relativo_frac_str, error_relativo_porc_str])
        
        # Actualizar variables para la siguiente iteración
        xi_anterior = xi_actual
        xi_actual = xi_plus_1
        
    # --- Impresión de la Tabla ---
    
    for row in tabla_data:
        iter_num, x_ant, x_act, f_x_act, error_float, error_relativo_frac_str, error_relativo_porc_str = row
        
        # Lógica de formato (solo error real a partir de la Iteración 1)
        error_frac = error_relativo_frac_str if iter_num > 0 else "---"
        error_porc = error_relativo_porc_str if iter_num > 0 else "---"
        
        porcentaje_final_str = error_porc + ('%' if error_porc != '---' else '')
        
        linea = (f"| {iter_num:5} | {x_ant:10.6f} | {x_act:10.6f} | {f_x_act:10.4e} "
                 f"| {error_frac:16} | {porcentaje_final_str:9} |\n")
        resultados_text.insert(tk.END, linea)

    # --- Resultados Finales ---
    x_final = xi_actual
    
    resultados_text.insert(tk.END, "\n" + "="*50 + "\n")
    if iteraciones >= max_iter:
        resultados_text.insert(tk.END, " Advertencia: Máximo de iteraciones alcanzado (100).\n")

    resultados_text.insert(tk.END, f" Raíz aproximada: **{x_final:.9f}** en {iteraciones} iteraciones.\n")

# ----------------------------------------------------
# Configuración de la Interfaz Gráfica con Tkinter
# ----------------------------------------------------

root = tk.Tk()
root.title("Método de la Secante y Graficación")
root.state('zoomed') 

input_frame = tk.LabelFrame(root, text="Parámetros de Ecuación y Secante", padx=10, pady=10)
input_frame.pack(padx=20, pady=10, fill="x")

# --- Variables Globales de la GUI (para ser accesibles por los botones)
lado_izq_str = tk.StringVar(value="x**3 - x - 1")
lado_der_str = tk.StringVar(value="0")

# --- Campos de Entrada para la Ecuación ---
tk.Label(input_frame, text="Ecuación: Lado Izquierdo (ej: x**3 - x - 1):").grid(row=0, column=0, sticky="w", pady=5)
entry_left = tk.Entry(input_frame, width=40, textvariable=lado_izq_str)
entry_left.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Ecuación: Lado Derecho (ej: 0):").grid(row=1, column=0, sticky="w", pady=5)
entry_right = tk.Entry(input_frame, width=40, textvariable=lado_der_str)
entry_right.grid(row=1, column=1, padx=5, pady=5)

# --- Campos de Puntos Iniciales y Tolerancia ---
tk.Label(input_frame, text="Punto Inicial x_i:").grid(row=2, column=0, sticky="w", pady=5)
entry_xi = tk.Entry(input_frame, width=15)
entry_xi.insert(0, "") # Punto inicial actual (xi)
entry_xi.grid(row=2, column=1, sticky="w", padx=5, pady=5)

tk.Label(input_frame, text="Punto Inicial x_{i-1}:").grid(row=3, column=0, sticky="w", pady=5)
entry_xi_minus_1 = tk.Entry(input_frame, width=15)
entry_xi_minus_1.insert(0, "") # Punto inicial anterior (xi-1)
entry_xi_minus_1.grid(row=3, column=1, sticky="w", padx=5, pady=5)


tk.Label(input_frame, text="Precisión (Tolerancia E):").grid(row=4, column=0, sticky="w", pady=5)
entry_tolerancia = tk.Entry(input_frame, width=15)
entry_tolerancia.insert(0, "0.0001")
entry_tolerancia.grid(row=4, column=1, sticky="w", padx=5, pady=5)

# 4. Botones Separados
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

boton_graficar = tk.Button(button_frame, text="1. GRAFICAR FUNCIÓN", command=graficar_funcion, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white")
boton_graficar.pack(side=tk.LEFT, padx=10)

boton_calcular = tk.Button(button_frame, text="2. CALCULAR RAÍZ (Secante)", command=calcular_secante, font=("Arial", 10, "bold"), bg="#2196F3", fg="white")
boton_calcular.pack(side=tk.LEFT, padx=10)

# 5. Área de Resultados (Detalles y Tabla)
tk.Label(root, text="Resultados Detallados y Tabla Resumen:").pack(pady=(5, 0))
resultados_text = scrolledtext.ScrolledText(root, width=120, height=20, font=("Courier", 10))
resultados_text.pack(padx=20, pady=(0, 20), fill="both", expand=True)

# 6. Iniciar el bucle principal de la GUI
root.mainloop()