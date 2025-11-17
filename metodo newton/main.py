import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
from sympy import sympify, Symbol, diff, lambdify # Importaciones clave para la derivada
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# --- Funciones de Evaluación y Derivada ---

# Diccionario de funciones seguras para uso opcional, aunque lambdify es preferido.
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
        # Usamos re.sub con r'\b' para asegurar que solo se reemplace la palabra completa
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
        # lambdify crea una función de Python para una evaluación numérica rápida
        f_num = lambdify(x, expr, 'numpy') 
        return f_num(x_val)
    except Exception:
        return None

def f_derivada_eval(ecuacion_str, x_val):
    """Calcula y evalúa la primera derivada f'(x) en x_val usando SymPy."""
    try:
        expr = sympify(preprocesar_ecuacion(ecuacion_str))
        x = Symbol('x')
        # Calcula la derivada simbólica
        derivada = diff(expr, x)
        # Crea una función numérica a partir de la derivada
        f_prima_num = lambdify(x, derivada, 'numpy')
        return f_prima_num(x_val)
    except Exception:
        return None

# --- Lógica de Graficación ---

def graficar_funcion():
    """Grafica la función y su derivada (opcional) para definir el punto inicial."""
    # ... (Lógica de graficación similar, pero usando un rango amplio o definido por el usuario) ...
    lado_izq_str = entry_left.get()
    lado_der_str = entry_right.get()
    ecuacion_str = ensamblar_ecuacion(lado_izq_str, lado_der_str)
    
    try:
        # Intenta usar el punto inicial como centro para graficar un rango
        x0 = float(entry_x0.get())
        rango = 2
        x_min = x0 - rango
        x_max = x0 + rango
    except ValueError:
        x_min = -2.0
        x_max = 2.0
        
    try:
        x = np.linspace(x_min, x_max, 500)
        y = np.array([f_eval(ecuacion_str, val) for val in x])
        
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.plot(x, y, label=f'f(x) = {ecuacion_str}', color='blue')
        ax.axhline(0, color='black', linewidth=0.8)
        
        # Opcionalmente, graficar la derivada para referencia visual
        # y_prima = np.array([f_derivada_eval(ecuacion_str, val) for val in x])
        # ax.plot(x, y_prima, label=f'f\'(x)', color='orange', linestyle='--')
        
        ax.set_title('Gráfica para Elegir Punto Inicial ($x_0$)')
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

# --- Método de Newton-Raphson ---

def calcular_newton_raphson():
    """
    Implementa el Método de Newton-Raphson, mostrando el error completo
    en la tabla resumen hasta la última iteración.
    """
    resultados_text.delete(1.0, tk.END)

    try:
        # Obtener entradas
        lado_izq_str = entry_left.get()
        lado_der_str = entry_right.get()
        x_i = float(entry_x0.get()) # Punto inicial (x_i)
        tolerancia = float(entry_tolerancia.get())
    except ValueError:
        messagebox.showerror("Error de Entrada", "Asegúrese de que x0 y la precisión son números válidos.")
        return

    ecuacion_str = ensamblar_ecuacion(lado_izq_str, lado_der_str)
    
    # --- Verificación Inicial ---
    f_x_i = f_eval(ecuacion_str, x_i)
    f_prima_x_i = f_derivada_eval(ecuacion_str, x_i)

    if f_x_i is None or f_prima_x_i is None:
        messagebox.showerror("Error", "No se pudo evaluar la función o su derivada. Revise la sintaxis.")
        return
    
    # --- Algoritmo de Newton-Raphson ---
    x_i_plus_1 = 0.0
    x_anterior = x_i
    iteraciones = 0
    max_iter = 100
    tabla_data = []

    resultados_text.insert(tk.END, f"\n--- MÉTODO DE NEWTON-RAPHSON ---\n")
    resultados_text.insert(tk.END, f"Punto Inicial ($x_0$): {x_i}\n")
    resultados_text.insert(tk.END, f"Tolerancia (E): {tolerancia:.6e}\n")
    resultados_text.insert(tk.END, "\n*** TABLA RESUMEN DE ITERACIONES ***\n")
    resultados_text.insert(tk.END, "| Iter. |    $x_i$    |   $f(x_i)$   |  $f'(x_i)$   | Error Fraccional | Error (%) |\n")
    resultados_text.insert(tk.END, "|-------|------------|------------|------------|------------------|-----------|\n")

    # Incluir el punto inicial como iteración 0 para la tabla
    tabla_data.append([0, x_i, f_x_i, f_derivada_eval(ecuacion_str, x_i), 0.0, "---", "---"])
    
    while iteraciones < max_iter:
        iteraciones += 1
        
        f_x_i = f_eval(ecuacion_str, x_i)
        f_prima_x_i = f_derivada_eval(ecuacion_str, x_i)
        
        # 1. Chequeo de división por cero (derivada = 0)
        if abs(f_prima_x_i) < 1e-9:
            resultados_text.insert(tk.END, "\n❌ Error: La derivada ($f'(x_i)$) es cero. El método diverge.\n")
            break

        # ⭐ FÓRMULA CLAVE: CÁLCULO DE NEWTON-RAPHSON
        x_i_plus_1 = x_i - (f_x_i / f_prima_x_i)
        
        # Cálculo de Errores
        error_relativo_float = abs((x_i_plus_1 - x_i) / x_i_plus_1)
        error_relativo_porc_float = error_relativo_float * 100
        
        error_relativo_frac_str = f"{error_relativo_float:.6e}"
        error_relativo_porc_str = f"{error_relativo_porc_float:.8f}"
        
        # Capturar la data para la tabla (siempre, incluyendo la última)
        tabla_data.append([iteraciones, x_i_plus_1, f_eval(ecuacion_str, x_i_plus_1), f_derivada_eval(ecuacion_str, x_i_plus_1), error_relativo_float, error_relativo_frac_str, error_relativo_porc_str])
        
        # ⭐ PARADA POR TOLERANCIA
        if error_relativo_float < tolerancia:
            x_i = x_i_plus_1
            break
            
        # Actualizar x_i para la siguiente iteración
        x_i = x_i_plus_1
        
    # --- Impresión de la Tabla ---
    
    # Imprimir filas de la tabla
    for row in tabla_data:
        iter_num, x_val, f_x, f_prima_x, error_float, error_relativo_frac_str, error_relativo_porc_str = row
        
        # Lógica de formato: Solo la iteración 0 tiene "---"
        error_frac = error_relativo_frac_str if iter_num > 0 else "---"
        error_porc = error_relativo_porc_str if iter_num > 0 else "---"
        
        porcentaje_final_str = error_porc + ('%' if error_porc != '---' else '')
        
        linea = (f"| {iter_num:5} | {x_val:10.6f} | {f_x:10.4e} | {f_prima_x:10.4e} "
                 f"| {error_frac:16} | {porcentaje_final_str:9} |\n")
        resultados_text.insert(tk.END, linea)

    # --- Resultados Finales ---
    x_final = x_i_plus_1 if iteraciones > 0 else x_i
    
    resultados_text.insert(tk.END, "\n" + "="*50 + "\n")
    if iteraciones >= max_iter:
        resultados_text.insert(tk.END, "⚠️ Advertencia: Máximo de iteraciones alcanzado (100).\n")

    resultados_text.insert(tk.END, f"✅ Raíz aproximada: **{x_final:.9f}** en {iteraciones} iteraciones.\n")

# ----------------------------------------------------
# Configuración de la Interfaz Gráfica con Tkinter
# ----------------------------------------------------

root = tk.Tk()
root.title("Método de Newton-Raphson y Graficación")
root.state('zoomed') 

input_frame = tk.LabelFrame(root, text="Parámetros de Ecuación y Newton-Raphson", padx=10, pady=10)
input_frame.pack(padx=20, pady=10, fill="x")

# --- Campos de Entrada para la Ecuación ---
tk.Label(input_frame, text="Ecuación: Lado Izquierdo (ej: x**3 - x - 1):").grid(row=0, column=0, sticky="w", pady=5)
entry_left = tk.Entry(input_frame, width=40)
entry_left.insert(0, "x**3 - x - 1") 
entry_left.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Ecuación: Lado Derecho (ej: 0):").grid(row=1, column=0, sticky="w", pady=5)
entry_right = tk.Entry(input_frame, width=40)
entry_right.insert(0, "0") 
entry_right.grid(row=1, column=1, padx=5, pady=5)

# --- Campos de Punto Inicial y Tolerancia ---
tk.Label(input_frame, text="Punto Inicial ($x_0$):").grid(row=2, column=0, sticky="w", pady=5)
entry_x0 = tk.Entry(input_frame, width=15)
entry_x0.insert(0, "1.5")
entry_x0.grid(row=2, column=1, sticky="w", padx=5, pady=5)

# Campo b (intervalo superior) eliminado
# El campo 'a' se ha renombrado internamente para ser el punto inicial (x0)

tk.Label(input_frame, text="Precisión (Tolerancia E):").grid(row=3, column=0, sticky="w", pady=5)
entry_tolerancia = tk.Entry(input_frame, width=15)
entry_tolerancia.insert(0, "0.0001")
entry_tolerancia.grid(row=3, column=1, sticky="w", padx=5, pady=5)

# 4. Botones Separados
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

boton_graficar = tk.Button(button_frame, text="1. GRAFICAR FUNCIÓN", command=graficar_funcion, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white")
boton_graficar.pack(side=tk.LEFT, padx=10)

boton_calcular = tk.Button(button_frame, text="2. CALCULAR RAÍZ (Newton-Raphson)", command=calcular_newton_raphson, font=("Arial", 10, "bold"), bg="#2196F3", fg="white")
boton_calcular.pack(side=tk.LEFT, padx=10)

# 5. Área de Resultados (Detalles y Tabla)
tk.Label(root, text="Resultados Detallados y Tabla Resumen:").pack(pady=(5, 0))
resultados_text = scrolledtext.ScrolledText(root, width=120, height=20, font=("Courier", 10))
resultados_text.pack(padx=20, pady=(0, 20), fill="both", expand=True)

# 6. Iniciar el bucle principal de la GUI
root.mainloop()