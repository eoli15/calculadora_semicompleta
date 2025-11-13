import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
from sympy import sympify, E, log, exp, sin, cos, tan, sqrt, Abs, Symbol
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# --- Funciones Auxiliares ---

GLOBAL_MATH_FUNCTIONS = {
    "e": math.e, "pi": math.pi, "exp": math.exp, "log": math.log,
    "log10": math.log10, "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "sqrt": math.sqrt, "abs": abs, "pow": math.pow,
}

def f(equation, x_val):
    """Evalúa la ecuación usando un entorno seguro con funciones de math."""
    ecuacion_limpia = equation.lower()
    
    replacements = {
        'ln(': 'log(', 'sen(': 'sin(', 'tg(': 'tan(', 'raiz(': 'sqrt(',
    }
    for key, value in replacements.items():
        ecuacion_limpia = ecuacion_limpia.replace(key, value)
        
    scope = {"x": x_val}
    scope.update(GLOBAL_MATH_FUNCTIONS)

    try:
        # Usa None para globals y scope para locals para un entorno controlado
        return eval(ecuacion_limpia, {"__builtins__": None}, scope)
    except Exception as e:
        # print(f"Error de evaluación: {e}") # Para depuración
        return None

def ensamblar_ecuacion(lado_izq, lado_der):
    """Ensambla la función de prueba f(x) = LI - LD."""
    return f"({lado_izq}) - ({lado_der})"

# --- Lógica de Graficación ---

def graficar_funcion():
    """
    Función llamada desde la GUI para graficar solo con la ecuación y un rango inicial
    para ayudar al usuario a definir el intervalo [a, b].
    """
    lado_izq_str = entry_left.get()
    lado_der_str = entry_right.get()
    ecuacion_str = ensamblar_ecuacion(lado_izq_str, lado_der_str)
    
    # Intenta obtener un rango inicial para graficar; si falla, usa un default.
    try:
        a_test = float(entry_a.get()) if entry_a.get() else -5.0
        b_test = float(entry_b.get()) if entry_b.get() else 5.0
    except ValueError:
        a_test = -5.0
        b_test = 5.0
        
    if a_test >= b_test:
        a_test = -5.0
        b_test = 5.0
        
    try:
        x = np.linspace(a_test, b_test, 500)
        y = np.array([f(ecuacion_str, val) for val in x])
        
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.plot(x, y, label=f'f(x) = {ecuacion_str}', color='blue')
        ax.axhline(0, color='black', linewidth=0.8)
        
        # Resaltar el rango tentativo del usuario
        ax.axvline(a_test, color='gray', linestyle=':', linewidth=0.7, label='Rango Tentativo')
        ax.axvline(b_test, color='gray', linestyle=':', linewidth=0.7)
        
        ax.set_title('Gráfica para Definir Intervalo [a, b]')
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

# --- Método de Falsa Posición (Regla Falsi) ---

def calcular_falsa_posicion():
    """
    Implementa el Método de Falsa Posición, mostrando solo la tabla resumen 
    y los valores finales.
    """
    resultados_text.delete(1.0, tk.END)

    try:
        # Obtener entradas
        lado_izq_str = entry_left.get()
        lado_der_str = entry_right.get()
        a_initial = float(entry_a.get())
        b_initial = float(entry_b.get())
        a = a_initial
        b = b_initial
        tolerancia = float(entry_tolerancia.get())
    except ValueError:
        messagebox.showerror("Error de Entrada", "Asegúrese de que a, b, y la precisión son números válidos.")
        return

    ecuacion_str = ensamblar_ecuacion(lado_izq_str, lado_der_str)
    
    # --- Verificación Inicial ---
    fa = f(ecuacion_str, a)
    fb = f(ecuacion_str, b)

    if fa is None or fb is None:
        messagebox.showerror("Error de Función", "Revise la sintaxis de la ecuación y el intervalo.")
        return
    
    if fa * fb >= 0:
        resultados_text.insert(tk.END, "❌ Error: f(a) * f(b) >= 0. No hay garantía de raíz en este intervalo.\n")
        return

    # --- Algoritmo de Falsa Posición ---
    c = 0.0
    c_anterior = 0.0
    iteraciones = 0
    max_iter = 100
    tabla_data = []

    resultados_text.insert(tk.END, f"\n--- MÉTODO DE FALSA POSICIÓN (REGULA FALSI) ---\n")
    resultados_text.insert(tk.END, f"Ecuación: {lado_izq_str} = {lado_der_str} (f(x) = {ecuacion_str})\n")
    resultados_text.insert(tk.END, f"Intervalo Inicial: [{a_initial}, {b_initial}]\n")
    resultados_text.insert(tk.END, f"Tolerancia (E): {tolerancia:.6e}\n")
    resultados_text.insert(tk.END, "\n" + "="*50 + "\n")

    while iteraciones < max_iter:
        iteraciones += 1
        
        c_anterior = c 
        a_previo = a
        b_previo = b
        
        fa_previo = f(ecuacion_str, a_previo)
        fb_previo = f(ecuacion_str, b_previo)
        
        # ⭐ CÁLCULO DE FALSA POSICIÓN
        try:
            c = b_previo - fb_previo * (a_previo - b_previo) / (fa_previo - fb_previo)
        except ZeroDivisionError:
            messagebox.showerror("Error", "División por cero (f(a) = f(b)). El método falla.")
            return
            
        fc = f(ecuacion_str, c)
        
        # Cálculo de Errores
        error_relativo_frac_str = "---"
        error_relativo_porc_str = "---"
        error_relativo_float = 0.0
        is_exact_root = False
        is_tolerance_met = False
        
        if iteraciones > 1 and c != 0:
            error_relativo_float = abs((c - c_anterior) / c)
            error_relativo_porc_float = error_relativo_float * 100
            
            error_relativo_frac_str = f"{error_relativo_float:.6e}"
            error_relativo_porc_str = f"{error_relativo_porc_float:.8f}"
            
            if error_relativo_float < tolerancia:
                is_tolerance_met = True

        if abs(fc) < 1e-9:
             is_exact_root = True

        # ⭐ CAPTURAR LA DATA EN CADA ITERACIÓN
        tabla_data.append([iteraciones, a_previo, b_previo, c, fc, error_relativo_float, error_relativo_frac_str, error_relativo_porc_str])


        # Criterio de Parada y Decisión
        if is_exact_root or is_tolerance_met: 
            break

        if fa_previo * fc < 0:
            b = c
        else: # f(b) * f(c) < 0
            a = c
        
    # --- Resultados Finales y Tabla ---

    # Mensaje de resultado
    if is_exact_root:
        final_status = "¡RAÍZ EXACTA ENCONTRADA!"
    elif is_tolerance_met:
        final_status = f"¡PRECISIÓN ALCANZADA! Error ({error_relativo_float:.6e}) < Tolerancia ({tolerancia:.6e})."
    elif iteraciones >= max_iter:
        final_status = "⚠️ Advertencia: Máximo de iteraciones alcanzado (100)."
    else:
        final_status = "Cálculo completado." # Caso por defecto

    resultados_text.insert(tk.END, f"STATUS FINAL: {final_status}\n")
    resultados_text.insert(tk.END, f"Iteraciones: {iteraciones}\n")
    resultados_text.insert(tk.END, f"✅ Raíz aproximada: **{c:.9f}**\n")
    
    # Tabla resumen
    resultados_text.insert(tk.END, "\n*** TABLA RESUMEN DE ITERACIONES ***\n")
    resultados_text.insert(tk.END, "| Iter. |     a     |     b     |     c     |    f(c)   | Error Fraccional | Error (%) |\n")
    resultados_text.insert(tk.END, "|-------|-----------|-----------|-----------|-----------|------------------|-----------|\n")
    
    for row in tabla_data:
        iter_num, a_val, b_val, c_val, fc_val, error_float, error_relativo_frac_str, error_relativo_porc_str = row
        
        # Formateo
        error_frac = error_relativo_frac_str if iter_num > 1 else "---"
        error_porc = error_relativo_porc_str if iter_num > 1 else "---"
             
        porcentaje_final_str = error_porc + ('%' if error_porc != '---' else '')
        
        linea = (f"| {iter_num:5} | {a_val:9.6f} | {b_val:9.6f} | {c_val:9.6f} | {fc_val:9.6e} "
                 f"| {error_frac:16} | {porcentaje_final_str:9} |\n")
        resultados_text.insert(tk.END, linea)

# ----------------------------------------------------
# Configuración de la Interfaz Gráfica con Tkinter
# ----------------------------------------------------

root = tk.Tk()
root.title("Método de Falsa Posición y Graficación")
root.state('zoomed') 

input_frame = tk.LabelFrame(root, text="Parámetros de Ecuación y Falsa Posición", padx=10, pady=10)
input_frame.pack(padx=20, pady=10, fill="x")

# --- Campos de Entrada para la Ecuación ---
tk.Label(input_frame, text="Ecuación: Lado Izquierdo (ej: sin(x)):").grid(row=0, column=0, sticky="w", pady=5)
entry_left = tk.Entry(input_frame, width=40)
entry_left.insert(0, "x**3 - x - 1") 
entry_left.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Ecuación: Lado Derecho (ej: exp(-x)):").grid(row=1, column=0, sticky="w", pady=5)
entry_right = tk.Entry(input_frame, width=40)
entry_right.insert(0, "0") 
entry_right.grid(row=1, column=1, padx=5, pady=5)

# --- Campos de Intervalo y Tolerancia ---
tk.Label(input_frame, text="Límite inferior 'a':").grid(row=2, column=0, sticky="w", pady=5)
entry_a = tk.Entry(input_frame, width=15)
entry_a.insert(0, "")
entry_a.grid(row=2, column=1, sticky="w", padx=5, pady=5)

tk.Label(input_frame, text="Límite superior 'b':").grid(row=3, column=0, sticky="w", pady=5)
entry_b = tk.Entry(input_frame, width=15)
entry_b.insert(0, "")
entry_b.grid(row=3, column=1, sticky="w", padx=5, pady=5)

tk.Label(input_frame, text="Precisión (Tolerancia E):").grid(row=4, column=0, sticky="w", pady=5)
entry_tolerancia = tk.Entry(input_frame, width=15)
entry_tolerancia.insert(0, "0.0001")
entry_tolerancia.grid(row=4, column=1, sticky="w", padx=5, pady=5)

# 4. Botones Separados
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

boton_graficar = tk.Button(button_frame, text="GRAFICAR FUNCIÓN", command=graficar_funcion, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white")
boton_graficar.pack(side=tk.LEFT, padx=10)

boton_calcular = tk.Button(button_frame, text="CALCULAR RAÍZ", command=calcular_falsa_posicion, font=("Arial", 10, "bold"), bg="#2196F3", fg="white")
boton_calcular.pack(side=tk.LEFT, padx=10)

# 5. Área de Resultados (Detalles y Tabla)
tk.Label(root, text="Resultados Detallados y Tabla Resumen:").pack(pady=(5, 0))
resultados_text = scrolledtext.ScrolledText(root, width=120, height=20, font=("Courier", 10))
resultados_text.pack(padx=20, pady=(0, 20), fill="both", expand=True)

# 6. Iniciar el bucle principal de la GUI
root.mainloop()