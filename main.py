import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
from sympy import sympify, E, log, exp, sin, cos, tan, sqrt, Abs
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Función de Evaluación (f(x)) Mejorada ---

def f(equation, x_val):
    """
    Evalúa la ecuación ensamblada (LI - LD) en un punto x_val.
    Pre-procesa la ecuación para aceptar notación matemática común.
    """
    
    replacements = {
        'e': 'E',           # Constante de Euler
        'ln': 'log',        # Logaritmo natural
        'sen': 'sin',       # Seno
        'tg': 'tan',        # Tangente
        'abs': 'Abs',       # Valor absoluto
        'raiz': 'sqrt'      # Raíz cuadrada
    }

    ecuacion_limpia = equation.lower()

    # Reemplazar funciones completas
    for key, value in replacements.items():
        ecuacion_limpia = re.sub(r'\b' + key + r'\b', value, ecuacion_limpia)

    try:
        expr = sympify(ecuacion_limpia)
        # Sustitución y evaluación numérica
        return float(expr.subs('x', x_val))
    except Exception as e:
        return None

# --- Funciones de Graficación ---

def mostrar_grafica(ecuacion_str, a_inicial, b_inicial, c_final, f_eval):
    """
    Crea una nueva ventana para mostrar la gráfica de la función.
    """
    try:
        # Generar puntos X
        x_min = a_inicial - 0.1 * abs(b_inicial - a_inicial)
        x_max = b_inicial + 0.1 * abs(b_inicial - a_inicial)
        x = np.linspace(x_min, x_max, 500)
        
        # Generar puntos Y evaluando la función
        y = np.array([f_eval(ecuacion_str, val) for val in x])
        
        # Crear la figura de Matplotlib
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(x, y, label=f'f(x) = {ecuacion_str}', color='blue')
        
        # Añadir eje X (y=0)
        ax.axhline(0, color='black', linewidth=0.8)
        
        # Marcar la raíz encontrada (c_final)
        ax.plot(c_final, f_eval(ecuacion_str, c_final), 'ro', label=f'Raíz (c={c_final:.6f})')
        ax.axvline(c_final, color='red', linestyle='--', linewidth=0.7)
        
        # Marcar el intervalo inicial
        ax.axvline(a_inicial, color='green', linestyle=':', linewidth=0.7, label=f'Intervalo [{a_inicial}, {b_inicial}]')
        ax.axvline(b_inicial, color='green', linestyle=':', linewidth=0.7)
        
        ax.set_title('Gráfica del Método de Bisección')
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y (f(x))')
        ax.grid(True)
        ax.legend()
        
        # Mostrar la gráfica en una nueva ventana de Tkinter
        graph_window = tk.Toplevel(root)
        graph_window.title("Gráfica de la Ecuación")
        
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()
        
    except Exception as e:
        messagebox.showerror("Error de Gráfico", f"No se pudo graficar la función. Revise el intervalo.\nError: {e}")

# --- Función Principal de Cálculo ---

# ... (El código de importaciones, f(equation, x_val) y mostrar_grafica permanecen iguales) ...

def calcular_biseccion():
    """
    Función que aplica el Método de Bisección y muestra los cálculos detallados,
    y la tabla de iteraciones, mostrando el Error Porcentual en formato decimal estándar.
    """
    resultados_text.delete(1.0, tk.END)

    try:
        # 1. Obtener entradas de la GUI
        lado_izq_str = entry_left.get()
        lado_der_str = entry_right.get()
        a_initial = float(entry_a.get())
        b_initial = float(entry_b.get())
        a = a_initial
        b = b_initial
        tolerancia = float(entry_tolerancia.get())
    except ValueError:
        messagebox.showerror("Error de Entrada", "Asegúrese de que a, b, y la precisión sean números válidos.")
        return

    # 2. Ensamblar la función de prueba f(x) = LI - LD
    ecuacion_str = f"({lado_izq_str}) - ({lado_der_str})"
    
    # --- Verificación Inicial ---
    fa = f(ecuacion_str, a)
    fb = f(ecuacion_str, b)

    if fa is None or fb is None:
        messagebox.showerror("Error de Función", "Revise la sintaxis de la ecuación.")
        return

    if fa * fb >= 0:
        resultados_text.insert(tk.END, "❌ Error: f(a) * f(b) >= 0.\n")
        resultados_text.insert(tk.END, f"f({a}) = {fa:.6f}, f({b}) = {fb:.6f}\n")
        resultados_text.insert(tk.END, "La raíz no está garantizada en este intervalo.\n")
        return

    # --- Algoritmo de Bisección ---
    c = 0.0
    c_anterior = 0.0
    iteraciones = 0
    max_iter = 100
    tabla_data = [] # Lista para almacenar los datos de la tabla

    # --- ENCABEZADO Y DETALLES INICIALES ---
    resultados_text.insert(tk.END, f"\n--- RESOLVIENDO: f(x) = {ecuacion_str} ---\n")
    resultados_text.insert(tk.END, f"Intervalo Inicial: [{a_initial}, {b_initial}]\n")
    resultados_text.insert(tk.END, f"Tolerancia: {tolerancia}\n")

    # --- INICIO DE DETALLES DE CÁLCULO (Paso a Paso) ---
    resultados_text.insert(tk.END, "\n*** DETALLES DE CÁLCULO POR ITERACIÓN ***\n")

    while (b - a) >= tolerancia and iteraciones < max_iter:
        iteraciones += 1
        
        # Guardar valores previos
        c_anterior = c 
        a_previo = a
        b_previo = b
        
        # CÁLCULO 1: Punto Medio
        c = (a + b) / 2
        fc = f(ecuacion_str, c)
        
        # EVALUACIONES (para el criterio)
        fa = f(ecuacion_str, a) 
        fb = f(ecuacion_str, b)
        
        # CÁLCULO 2: Error Relativo (Fraccional y Porcentual)
        error_relativo_frac_str = "---"
        error_relativo_porc_str = "---"
        error_relativo_float = 0.0
        
        if iteraciones > 1 and c != 0:
            error_relativo_float = abs((c - c_anterior) / c)           # ERROR FRACCIONAL
            error_relativo_porc_float = error_relativo_float * 100     # ERROR PORCENTUAL
            
            error_relativo_frac_str = f"{error_relativo_float:.6e}"     # Fraccional en notación científica
            
            # ⭐ CORRECCIÓN AQUÍ: Usamos el formato 'f' para decimal estándar
            error_relativo_porc_str = f"{error_relativo_porc_float:.8f}" # Porcentual en formato decimal (.8f)
        
        
        # --- MOSTRAR DETALLES DE ESTA ITERACIÓN EN EL ÁREA DE TEXTO ---
        resultados_text.insert(tk.END, "\n-----------------------------------------------------\n")
        resultados_text.insert(tk.END, f"ITERACIÓN {iteraciones}:\n")
        resultados_text.insert(tk.END, f"1. Cálculo de c: c = ({a_previo:.6f} + {b_previo:.6f}) / 2 = {c:.6f}\n")
        resultados_text.insert(tk.END, f"2. f(c): f({c:.6f}) = {fc:.6e}\n")
        
        # Guardar datos para la tabla
        tabla_data.append([iteraciones, a_previo, b_previo, c, fc, error_relativo_float, error_relativo_frac_str, error_relativo_porc_str])
        
        # Criterio de Bolzano (Decisión)
        if abs(fc) < 1e-9: 
            resultados_text.insert(tk.END, "   -> ¡RAÍZ EXACTA ENCONTRADA! Terminado.\n")
            break

        if fa * fc < 0:
            b = c
            resultados_text.insert(tk.END, f"3. Criterio: f(a) * f(c) = ({fa:.3e}) * ({fc:.3e}) < 0.  ")
            resultados_text.insert(tk.END, f"-> Nuevo intervalo: [a, c] = [{a:.6f}, {b:.6f}]\n")
        else: # f(b) * f(c) < 0
            a = c
            resultados_text.insert(tk.END, f"3. Criterio: f(b) * f(c) = ({fb:.3e}) * ({fc:.3e}) < 0.  ")
            resultados_text.insert(tk.END, f"-> Nuevo intervalo: [c, b] = [{a:.6f}, {b:.6f}]\n")

        resultados_text.insert(tk.END, f"4. Error Relativo (Fraccional): {error_relativo_frac_str}\n")
        # Mostrar el error porcentual sin notación científica y con el símbolo %
        resultados_text.insert(tk.END, f"5. Error Relativo (Porcentual): {error_relativo_porc_str}%\n") 
        
    # --- FIN DE DETALLES DE CÁLCULO ---
    
    # --- INICIO DE LA TABLA ESTRUCTURADA ---
    resultados_text.insert(tk.END, "\n\n*** TABLA RESUMEN DE ITERACIONES ***\n")
    
    # Encabezado de la tabla con ambas columnas de error
    resultados_text.insert(tk.END, "| Iter. |     a     |     b     |     c     |    f(c)   | Error Fraccional | Error (%) |\n")
    resultados_text.insert(tk.END, "|-------|-----------|-----------|-----------|-----------|------------------|-----------|\n")
    
    # Imprimir filas de la tabla
    for row in tabla_data:
        # Desempaquetar los datos guardados
        iter_num, a_val, b_val, c_val, fc_val, error_float, error_relativo_frac_str, error_relativo_porc_str = row
        
        # Lógica para la raíz exacta
        if abs(fc_val) < 1e-9:
             error_relativo_frac_str = "RAÍZ EXACTA"
             error_relativo_porc_str = "RAÍZ EXACTA"
             
        # Construir la línea de la tabla: Usamos un ancho fijo de 10 para el porcentaje
        porcentaje_final_str = error_relativo_porc_str + ('%' if error_relativo_porc_str != 'RAÍZ EXACTA' else '')
        
        linea = (f"| {iter_num:5} | {a_val:9.6f} | {b_val:9.6f} | {c_val:9.6f} | {fc_val:9.6e} "
                 f"| {error_relativo_frac_str:16} | {porcentaje_final_str:9} |\n")
        resultados_text.insert(tk.END, linea)

    # --- Resultados Finales ---
    # ... (El resto del código permanece igual) ...
    resultados_text.insert(tk.END, "\n" + "="*50 + "\n")
    
    if iteraciones >= max_iter:
        resultados_text.insert(tk.END, " Advertencia: Máximo de iteraciones alcanzado.\n")

    resultados_text.insert(tk.END, f" Raíz aproximada: **{c:.6f}** en {iteraciones} iteraciones.\n")
    resultados_text.insert(tk.END, f"   Longitud de intervalo final: {b - a:.6e}\n")
    
    # Mostrar Gráfica
    if c != 0.0:
        mostrar_grafica(ecuacion_str, a_initial, b_initial, c, f)

# ----------------------------------------------------
# Configuración de la Interfaz Gráfica con Tkinter
# ----------------------------------------------------

root = tk.Tk()
root.title("Método de Bisección (Flexible y Gráfico)")
root.state('zoomed') 

input_frame = tk.LabelFrame(root, text="Parámetros de Ecuación y Bisección", padx=10, pady=10)
input_frame.pack(padx=20, pady=10, fill="x")

# --- Campos de Entrada para la Ecuación ---
tk.Label(input_frame, text="Ecuación: Lado Izquierdo (ej: cos(x) o x**3):").grid(row=0, column=0, sticky="w", pady=5)
entry_left = tk.Entry(input_frame, width=40)
entry_left.insert(0, "cos(x)") 
entry_left.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Ecuación: Lado Derecho (ej: x o 0):").grid(row=1, column=0, sticky="w", pady=5)
entry_right = tk.Entry(input_frame, width=40)
entry_right.insert(0, "x") 
entry_right.grid(row=1, column=1, padx=5, pady=5)

# --- Campos de Bisección ---
tk.Label(input_frame, text="Límite inferior 'a':").grid(row=2, column=0, sticky="w", pady=5)
entry_a = tk.Entry(input_frame, width=15)
entry_a.insert(0, "0")
entry_a.grid(row=2, column=1, sticky="w", padx=5, pady=5)

tk.Label(input_frame, text="Límite superior 'b':").grid(row=3, column=0, sticky="w", pady=5)
entry_b = tk.Entry(input_frame, width=15)
entry_b.insert(0, "1")
entry_b.grid(row=3, column=1, sticky="w", padx=5, pady=5)

tk.Label(input_frame, text="Precisión (Tolerancia E):").grid(row=4, column=0, sticky="w", pady=5)
entry_tolerancia = tk.Entry(input_frame, width=15)
entry_tolerancia.insert(0, "0.0001")
entry_tolerancia.grid(row=4, column=1, sticky="w", padx=5, pady=5)

# 4. Botón de Calcular
boton_calcular = tk.Button(root, text="CALCULAR RAÍZ Y GRAFICAR", command=calcular_biseccion, font=("Arial", 10, "bold"))
boton_calcular.pack(pady=10)

# 5. Área de Resultados (Detalles y Tabla)
tk.Label(root, text="Resultados Detallados y Tabla Resumen:").pack(pady=(5, 0))
resultados_text = scrolledtext.ScrolledText(root, width=120, height=20, font=("Courier", 10))
resultados_text.pack(padx=20, pady=(0, 20), fill="both", expand=True)

# 6. Iniciar el bucle principal de la GUI
root.mainloop()