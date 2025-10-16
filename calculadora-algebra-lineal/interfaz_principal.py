"""
Interfaz gráfica principal para la Calculadora de Álgebra Lineal - Versión Moderna.

Esta aplicación proporciona una interfaz gráfica completa y moderna usando Tkinter
con un diseño atractivo y funcionalidades avanzadas para todas las operaciones
de la calculadora: resolución de sistemas de ecuaciones, operaciones matriciales, 
análisis de independencia lineal y exportación de resultados.

Características:
- Interfaz moderna con pestañas y tema personalizado
- Validación completa de entrada de datos
- Campos dinámicos según las dimensiones especificadas
- Visualización detallada de pasos y resultados
- Exportación de resultados a archivos
- Diseño mejorado con colores y tipografías modernas
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, font
import sys
import os

# Agregar el directorio actual al path para importar los módulos de lógica
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logica.gauss import gauss_resolver
from logica.gauss_jordan import gauss_jordan_resolver
from logica.operaciones_matrices import (
    sumar_matrices, restar_matrices, multiplicar_matrices, 
    transponer_matriz, escalar_por_matriz
)
from logica.vectores import analizar_independencia
from logica.matriz_inversa import calcular_matriz_inversa, verificar_invertibilidad
from logica.archivos import exportar_resultado_completo, generar_nombre_archivo

class CalculadoraAlgebraLineal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculadora de Álgebra Lineal")
        self.root.geometry("900x750")
        self.root.minsize(800, 650)
        
        # Definir colores y estilo
        self.colors = {
            "primary": "#940707",   # Azul principal
            "secondary": "#670416", # Azul oscuro
            "accent": "#10ca22",    # Acento rojo
            "bg_dark": "#000000",   # Fondo oscuro
            "bg_light": "#ffffff",  # Fondo claro
            "text_light": "#ffffff", # Texto claro
            "text_dark": "#000000"   # Texto oscuro
        }
        
        # Configurar fuentes personalizadas
        self.fonts = {
            "heading": font.Font(family="Segoe UI", size=12, weight="bold"),
            "subheading": font.Font(family="Segoe UI", size=10, weight="bold"),
            "normal": font.Font(family="Segoe UI", size=9),
            "small": font.Font(family="Segoe UI", size=8)
        }
        
        # Configurar estilo personalizado
        self.configurar_estilo()
        
        # Variables para almacenar datos y resultados actuales
        self.ultimo_resultado = None
        self.ultimos_pasos = []
        self.ultimos_datos_entrada = {}
        self.ultimo_tipo_calculo = ""
        
        self.configurar_interfaz()
    
    def configurar_estilo(self):
        """Configura el estilo personalizado para la aplicación."""
        style = ttk.Style()
        
        # Configurar estilo general
        style.configure("TFrame", background=self.colors["bg_light"])
        style.configure("TLabel", background=self.colors["bg_light"], font=self.fonts["normal"])
        style.configure("TLabelframe", background=self.colors["bg_light"], font=self.fonts["normal"])
        style.configure("TLabelframe.Label", background=self.colors["bg_light"], foreground=self.colors["text_dark"], font=self.fonts["subheading"])
        style.configure("TNotebook", background=self.colors["bg_light"], tabmargins=[2, 5, 2, 0])
        style.configure("TNotebook.Tab", background=self.colors["bg_light"], foreground=self.colors["text_dark"], 
                        font=self.fonts["normal"], padding=[10, 4], focuscolor=self.colors["primary"])
        
        # Estilo para botones
        style.configure("TButton", background=self.colors["primary"], foreground=self.colors["text_dark"], 
                        font=self.fonts["normal"], padding=[10, 5], relief="flat")
        style.map("TButton", 
                  background=[("active", self.colors["secondary"]), ("!disabled", self.colors["primary"])],
                  foreground=[("!disabled", self.colors["text_dark"])])
        
        # Estilo para botones de acción principal
        style.configure("Action.TButton", background=self.colors["accent"], font=self.fonts["subheading"])
        style.map("Action.TButton", background=[("active", "#c0392b"), ("!disabled", self.colors["accent"])])
        
        # Estilo para campos de entrada
        style.configure("TEntry", padding=[5, 3])
        
        # Estilo para radio buttons
        style.configure("TRadiobutton", background=self.colors["bg_light"], font=self.fonts["normal"])
        
        # Estilo para scrolledtext
        style.configure("TScrollbar", background=self.colors["bg_light"], troughcolor=self.colors["bg_light"], 
                        relief="flat", arrowcolor=self.colors["text_dark"])
    
    def configurar_interfaz(self):
        """Configura la interfaz principal con pestañas."""
        # Configurar color de fondo principal
        self.root.configure(bg=self.colors["bg_light"])
        
        # Crear frame principal
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Crear título de la aplicación
        title_label = ttk.Label(main_frame, text="Calculadora de Álgebra Lineal", font=self.fonts["heading"])
        title_label.pack(pady=(0, 10))
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Crear pestañas
        self.crear_pestaña_gauss()
        self.crear_pestaña_gauss_jordan()
        self.crear_pestaña_operaciones()
        self.crear_pestaña_vectores()
        self.crear_pestaña_transpuesta()
        self.crear_pestaña_matriz_inversa()
        
        # Crear barra de estado
        self.status_bar = ttk.Label(self.root, text="Listo", relief="sunken", anchor="w", 
                                  background=self.colors["secondary"], foreground=self.colors["text_dark"])
        self.status_bar.pack(side="bottom", fill="x", padx=5, pady=(5, 0))
    
    def crear_pestaña_gauss(self):
        """Crea la pestaña para resolver sistemas con eliminación gaussiana."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Resolver Sistema (Gauss)")
        
        # Frame superior para configuración
        config_frame = ttk.LabelFrame(frame, text="Configuración del Sistema", padding=10)
        config_frame.pack(fill="x", padx=5, pady=5)
        
        # Dimensiones
        dim_frame = ttk.Frame(config_frame)
        dim_frame.pack(pady=10)
        
        ttk.Label(dim_frame, text="Ecuaciones:", font=self.fonts["normal"]).pack(side="left")
        self.gauss_filas = tk.Spinbox(dim_frame, from_=1, to=10, width=5, value=3, 
                                     font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                     buttonbackground=self.colors["primary"])
        self.gauss_filas.pack(side="left", padx=5)
        
        ttk.Label(dim_frame, text="Variables:", font=self.fonts["normal"]).pack(side="left")
        self.gauss_columnas = tk.Spinbox(dim_frame, from_=1, to=10, width=5, value=3, 
                                       font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                       buttonbackground=self.colors["primary"])
        self.gauss_columnas.pack(side="left", padx=5)
        
        ttk.Button(dim_frame, text="Generar Campos", style="TButton",
                  command=self.generar_campos_gauss).pack(side="left", padx=15)
        
        # Frame para matriz y vector
        entrada_frame = ttk.Frame(frame)
        entrada_frame.pack(fill="both", expand=True, padx=5, pady=10)
        
        # Frame para matriz A
        self.gauss_matriz_frame = ttk.LabelFrame(entrada_frame, text="Matriz A (coeficientes)", padding=8)
        self.gauss_matriz_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Frame para vector b
        self.gauss_vector_frame = ttk.LabelFrame(entrada_frame, text="Vector b (términos independientes)", padding=8)
        self.gauss_vector_frame.pack(side="right", fill="y", padx=5)
        
        # Botones de acción
        botones_frame = ttk.Frame(frame, padding=5)
        botones_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Button(botones_frame, text="Calcular", style="Action.TButton",
                  command=self.resolver_gauss).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Limpiar",
                  command=self.limpiar_gauss).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Guardar Resultado",
                  command=self.guardar_resultado).pack(side="left", padx=5)
        
        # Área de resultados
        resultado_frame = ttk.LabelFrame(frame, text="Pasos y Resultado", padding=8)
        resultado_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.gauss_resultado = scrolledtext.ScrolledText(resultado_frame, height=15, width=80, 
                                                     font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                                     fg=self.colors["text_dark"], padx=8, pady=8)
        self.gauss_resultado.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Inicializar campos
        self.generar_campos_gauss()
    
    def crear_pestaña_gauss_jordan(self):
        """Crea la pestaña para resolver sistemas con Gauss-Jordan."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Gauss-Jordan")
        
        # Configuración del sistema
        config_frame = ttk.LabelFrame(frame, text="Configuración del Sistema", padding=10)
        config_frame.pack(fill="x", padx=5, pady=5)
        
        dim_frame = ttk.Frame(config_frame)
        dim_frame.pack(pady=10)
        
        ttk.Label(dim_frame, text="Ecuaciones:", font=self.fonts["normal"]).pack(side="left")
        self.gj_filas = tk.Spinbox(dim_frame, from_=1, to=10, width=5, value=3, 
                                 font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                 buttonbackground=self.colors["primary"])
        self.gj_filas.pack(side="left", padx=5)
        
        ttk.Label(dim_frame, text="Variables:", font=self.fonts["normal"]).pack(side="left")
        self.gj_columnas = tk.Spinbox(dim_frame, from_=1, to=10, width=5, value=3, 
                                    font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                    buttonbackground=self.colors["primary"])
        self.gj_columnas.pack(side="left", padx=5)
        
        ttk.Button(dim_frame, text="Generar Campos", 
                  command=self.generar_campos_gauss_jordan).pack(side="left", padx=15)
        
        entrada_frame = ttk.Frame(frame)
        entrada_frame.pack(fill="both", expand=True, padx=5, pady=10)
        
        self.gj_matriz_frame = ttk.LabelFrame(entrada_frame, text="Matriz A (coeficientes)", padding=8)
        self.gj_matriz_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        self.gj_vector_frame = ttk.LabelFrame(entrada_frame, text="Vector b (términos independientes)", padding=8)
        self.gj_vector_frame.pack(side="right", fill="y", padx=5)
        
        botones_frame = ttk.Frame(frame, padding=5)
        botones_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Button(botones_frame, text="Calcular", style="Action.TButton",
                  command=self.resolver_gauss_jordan).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Limpiar", 
                  command=self.limpiar_gauss_jordan).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Guardar Resultado", 
                  command=self.guardar_resultado).pack(side="left", padx=5)
        
        resultado_frame = ttk.LabelFrame(frame, text="Pasos y Resultado", padding=8)
        resultado_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.gj_resultado = scrolledtext.ScrolledText(resultado_frame, height=15, width=80, 
                                                   font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                                   fg=self.colors["text_dark"], padx=8, pady=8)
        self.gj_resultado.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.generar_campos_gauss_jordan()
    
    def crear_pestaña_operaciones(self):
        """Crea la pestaña para operaciones matriciales."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Operaciones")
        
        # Configuración
        config_frame = ttk.LabelFrame(frame, text="Configuración de Operación", padding=10)
        config_frame.pack(fill="x", padx=5, pady=5)
        
        # Tipo de operación
        op_frame = ttk.Frame(config_frame)
        op_frame.pack(pady=10)
        
        ttk.Label(op_frame, text="Operación:", font=self.fonts["normal"]).pack(side="left")
        self.operacion_var = tk.StringVar(value="suma")
        operaciones = [("Suma A + B", "suma"), ("Resta A - B", "resta"), 
                      ("Multiplicación A × B", "multiplicacion"), ("Escalar k × A", "escalar")]
        
        for texto, valor in operaciones:
            ttk.Radiobutton(op_frame, text=texto, variable=self.operacion_var, style="TRadiobutton",
                           value=valor, command=self.cambiar_operacion).pack(side="left", padx=8)
        
        # Dimensiones
        dim_frame = ttk.Frame(config_frame)
        dim_frame.pack(pady=5)
        
        ttk.Label(dim_frame, text="Filas A:", font=self.fonts["normal"]).pack(side="left")
        self.op_filas_a = tk.Spinbox(dim_frame, from_=1, to=8, width=5, value=2, 
                                    font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                    buttonbackground=self.colors["primary"])
        self.op_filas_a.pack(side="left", padx=3)
        
        ttk.Label(dim_frame, text="Columnas A:", font=self.fonts["normal"]).pack(side="left")
        self.op_columnas_a = tk.Spinbox(dim_frame, from_=1, to=8, width=5, value=2, 
                                       font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                       buttonbackground=self.colors["primary"])
        self.op_columnas_a.pack(side="left", padx=3)
        
        ttk.Label(dim_frame, text="Filas B:", font=self.fonts["normal"]).pack(side="left")
        self.op_filas_b = tk.Spinbox(dim_frame, from_=1, to=8, width=5, value=2, 
                                    font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                    buttonbackground=self.colors["primary"])
        self.op_filas_b.pack(side="left", padx=3)
        
        ttk.Label(dim_frame, text="Columnas B:", font=self.fonts["normal"]).pack(side="left")
        self.op_columnas_b = tk.Spinbox(dim_frame, from_=1, to=8, width=5, value=2, 
                                       font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                       buttonbackground=self.colors["primary"])
        self.op_columnas_b.pack(side="left", padx=3)
        
        ttk.Button(dim_frame, text="Generar Campos", 
                  command=self.generar_campos_operaciones).pack(side="left", padx=15)
        
        # Entrada de datos
        entrada_frame = ttk.Frame(frame)
        entrada_frame.pack(fill="both", expand=True, padx=5, pady=10)
        
        self.op_matriz_a_frame = ttk.LabelFrame(entrada_frame, text="Matriz A", padding=8)
        self.op_matriz_a_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        self.op_matriz_b_frame = ttk.LabelFrame(entrada_frame, text="Matriz B / Escalar k", padding=8)
        self.op_matriz_b_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Botones
        botones_frame = ttk.Frame(frame, padding=5)
        botones_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Button(botones_frame, text="Calcular", style="Action.TButton",
                  command=self.ejecutar_operacion).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Limpiar", 
                  command=self.limpiar_operaciones).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Guardar Resultado", 
                  command=self.guardar_resultado).pack(side="left", padx=5)
        
        # Resultado
        resultado_frame = ttk.LabelFrame(frame, text="Pasos y Resultado", padding=8)
        resultado_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.op_resultado = scrolledtext.ScrolledText(resultado_frame, height=15, 
                                                     font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                                     fg=self.colors["text_dark"], padx=8, pady=8)
        self.op_resultado.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.generar_campos_operaciones()
    
    def crear_pestaña_vectores(self):
        """Crea la pestaña para análisis de independencia lineal."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Vectores")
        
        # Configuración
        config_frame = ttk.LabelFrame(frame, text="Configuración de Vectores", padding=10)
        config_frame.pack(fill="x", padx=5, pady=5)
        
        dim_frame = ttk.Frame(config_frame)
        dim_frame.pack(pady=10)
        
        ttk.Label(dim_frame, text="Número de vectores:", font=self.fonts["normal"]).pack(side="left")
        self.vec_cantidad = tk.Spinbox(dim_frame, from_=1, to=8, width=5, value=3, 
                                     font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                     buttonbackground=self.colors["primary"])
        self.vec_cantidad.pack(side="left", padx=5)
        
        ttk.Label(dim_frame, text="Dimensión de vectores:", font=self.fonts["normal"]).pack(side="left")
        self.vec_dimension = tk.Spinbox(dim_frame, from_=1, to=8, width=5, value=3, 
                                       font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                       buttonbackground=self.colors["primary"])
        self.vec_dimension.pack(side="left", padx=5)
        
        ttk.Button(dim_frame, text="Generar Campos", 
                  command=self.generar_campos_vectores).pack(side="left", padx=15)
        
        # Entrada de vectores
        self.vec_entrada_frame = ttk.LabelFrame(frame, text="Vectores", padding=8)
        self.vec_entrada_frame.pack(fill="x", padx=5, pady=10)
        
        # Botones
        botones_frame = ttk.Frame(frame, padding=5)
        botones_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Button(botones_frame, text="Analizar Independencia", style="Action.TButton",
                  command=self.analizar_vectores).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Limpiar", 
                  command=self.limpiar_vectores).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Guardar Resultado", 
                  command=self.guardar_resultado).pack(side="left", padx=5)
        
        # Resultado
        resultado_frame = ttk.LabelFrame(frame, text="Análisis y Resultado", padding=8)
        resultado_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.vec_resultado = scrolledtext.ScrolledText(resultado_frame, height=20, 
                                                      font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                                      fg=self.colors["text_dark"], padx=8, pady=8)
        self.vec_resultado.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.generar_campos_vectores()
    
    def crear_pestaña_transpuesta(self):
        """Crea la pestaña para calcular transpuesta de matrices."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Transpuesta")
        
        # Configuración
        config_frame = ttk.LabelFrame(frame, text="Configuración de la Matriz", padding=10)
        config_frame.pack(fill="x", padx=5, pady=5)
        
        dim_frame = ttk.Frame(config_frame)
        dim_frame.pack(pady=10)
        
        ttk.Label(dim_frame, text="Filas:", font=self.fonts["normal"]).pack(side="left")
        self.trans_filas = tk.Spinbox(dim_frame, from_=1, to=8, width=5, value=3, 
                                     font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                     buttonbackground=self.colors["primary"])
        self.trans_filas.pack(side="left", padx=5)
        
        ttk.Label(dim_frame, text="Columnas:", font=self.fonts["normal"]).pack(side="left")
        self.trans_columnas = tk.Spinbox(dim_frame, from_=1, to=8, width=5, value=2, 
                                       font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                       buttonbackground=self.colors["primary"])
        self.trans_columnas.pack(side="left", padx=5)
        
        ttk.Button(dim_frame, text="Generar Campos", 
                  command=self.generar_campos_transpuesta).pack(side="left", padx=15)
        
        # Entrada de matriz
        self.trans_entrada_frame = ttk.LabelFrame(frame, text="Matriz A", padding=8)
        self.trans_entrada_frame.pack(fill="x", padx=5, pady=10)
        
        # Botones
        botones_frame = ttk.Frame(frame, padding=5)
        botones_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Button(botones_frame, text="Calcular Transpuesta", style="Action.TButton",
                  command=self.calcular_transpuesta).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Limpiar", 
                  command=self.limpiar_transpuesta).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Guardar Resultado", 
                  command=self.guardar_resultado).pack(side="left", padx=5)
        
        # Resultado
        resultado_frame = ttk.LabelFrame(frame, text="Pasos y Resultado", padding=8)
        resultado_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.trans_resultado = scrolledtext.ScrolledText(resultado_frame, height=15, 
                                                        font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                                        fg=self.colors["text_dark"], padx=8, pady=8)
        self.trans_resultado.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.generar_campos_transpuesta()
    
    def crear_pestaña_matriz_inversa(self):
        """Crea la pestaña para calcular matriz inversa."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Matriz Inversa")
        
        # Configuración
        config_frame = ttk.LabelFrame(frame, text="Configuración de la Matriz", padding=10)
        config_frame.pack(fill="x", padx=5, pady=5)
        
        dim_frame = ttk.Frame(config_frame)
        dim_frame.pack(pady=10)
        
        ttk.Label(dim_frame, text="Dimensión (n×n):", font=self.fonts["normal"]).pack(side="left")
        self.inversa_dimension = tk.Spinbox(dim_frame, from_=2, to=6, width=5, value=3, 
                                          font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                          buttonbackground=self.colors["primary"])
        self.inversa_dimension.pack(side="left", padx=5)
        
        ttk.Label(dim_frame, text="(Solo matrices cuadradas)", font=self.fonts["small"]).pack(side="left", padx=10)
        
        ttk.Button(dim_frame, text="Generar Campos", 
                  command=self.generar_campos_matriz_inversa).pack(side="left", padx=15)
        
        # Entrada de matriz
        self.inversa_entrada_frame = ttk.LabelFrame(frame, text="Matriz A", padding=8)
        self.inversa_entrada_frame.pack(fill="x", padx=5, pady=10)
        
        # Botones
        botones_frame = ttk.Frame(frame, padding=5)
        botones_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Button(botones_frame, text="Calcular Inversa", style="Action.TButton",
                  command=self.calcular_matriz_inversa).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Verificar Invertibilidad",
                  command=self.solo_verificar_invertibilidad).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Limpiar", 
                  command=self.limpiar_matriz_inversa).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Guardar Resultado", 
                  command=self.guardar_resultado).pack(side="left", padx=5)
        
        # Resultado
        resultado_frame = ttk.LabelFrame(frame, text="Análisis y Resultado", padding=8)
        resultado_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.inversa_resultado = scrolledtext.ScrolledText(resultado_frame, height=18, 
                                                         font=self.fonts["normal"], bg=self.colors["bg_light"], 
                                                         fg=self.colors["text_dark"], padx=8, pady=8)
        self.inversa_resultado.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.generar_campos_matriz_inversa()
    
    def generar_campos_gauss(self):
        """Genera los campos de entrada para el sistema Gauss."""
        # Limpiar frames
        for widget in self.gauss_matriz_frame.winfo_children():
            widget.destroy()
        for widget in self.gauss_vector_frame.winfo_children():
            widget.destroy()
        
        filas = int(self.gauss_filas.get())
        columnas = int(self.gauss_columnas.get())
        
        # Campos para matriz A
        self.gauss_entries_matriz = []
        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                entry = tk.Entry(self.gauss_matriz_frame, width=8, font=self.fonts["normal"], 
                                 bg=self.colors["bg_light"], relief="solid", borderwidth=1)
                entry.grid(row=i, column=j, padx=4, pady=4, ipadx=3, ipady=3)
                fila_entries.append(entry)
            self.gauss_entries_matriz.append(fila_entries)
        
        # Campos para vector b
        self.gauss_entries_vector = []
        for i in range(filas):
            entry = tk.Entry(self.gauss_vector_frame, width=10, font=self.fonts["normal"], 
                             bg=self.colors["bg_light"], relief="solid", borderwidth=1)
            entry.grid(row=i, column=0, padx=4, pady=4, ipadx=3, ipady=3)
            self.gauss_entries_vector.append(entry)
    
    def generar_campos_gauss_jordan(self):
        """Genera los campos de entrada para el sistema Gauss-Jordan."""
        for widget in self.gj_matriz_frame.winfo_children():
            widget.destroy()
        for widget in self.gj_vector_frame.winfo_children():
            widget.destroy()
        
        filas = int(self.gj_filas.get())
        columnas = int(self.gj_columnas.get())
        
        self.gj_entries_matriz = []
        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                entry = tk.Entry(self.gj_matriz_frame, width=8, font=self.fonts["normal"], 
                                 bg=self.colors["bg_light"], relief="solid", borderwidth=1)
                entry.grid(row=i, column=j, padx=4, pady=4, ipadx=3, ipady=3)
                fila_entries.append(entry)
            self.gj_entries_matriz.append(fila_entries)
        
        self.gj_entries_vector = []
        for i in range(filas):
            entry = tk.Entry(self.gj_vector_frame, width=10, font=self.fonts["normal"], 
                             bg=self.colors["bg_light"], relief="solid", borderwidth=1)
            entry.grid(row=i, column=0, padx=4, pady=4, ipadx=3, ipady=3)
            self.gj_entries_vector.append(entry)
    
    def generar_campos_operaciones(self):
        """Genera los campos de entrada para operaciones matriciales."""
        for widget in self.op_matriz_a_frame.winfo_children():
            widget.destroy()
        for widget in self.op_matriz_b_frame.winfo_children():
            widget.destroy()
        
        filas_a = int(self.op_filas_a.get())
        columnas_a = int(self.op_columnas_a.get())
        
        # Matriz A
        self.op_entries_a = []
        for i in range(filas_a):
            fila_entries = []
            for j in range(columnas_a):
                entry = tk.Entry(self.op_matriz_a_frame, width=8, font=self.fonts["normal"], 
                                 bg=self.colors["bg_light"], relief="solid", borderwidth=1)
                entry.grid(row=i, column=j, padx=4, pady=4, ipadx=3, ipady=3)
                fila_entries.append(entry)
            self.op_entries_a.append(fila_entries)
        
        # Matriz B o escalar
        operacion = self.operacion_var.get()
        if operacion == "escalar":
            # Solo un campo para el escalar
            ttk.Label(self.op_matriz_b_frame, text="Escalar k:", font=self.fonts["normal"]).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.op_escalar_entry = tk.Entry(self.op_matriz_b_frame, width=10, font=self.fonts["normal"], 
                                            bg=self.colors["bg_light"], relief="solid", borderwidth=1)
            self.op_escalar_entry.grid(row=1, column=0, padx=5, pady=5, ipadx=3, ipady=3)
        else:
            # Campos para matriz B
            filas_b = int(self.op_filas_b.get())
            columnas_b = int(self.op_columnas_b.get())
            
            self.op_entries_b = []
            for i in range(filas_b):
                fila_entries = []
                for j in range(columnas_b):
                    entry = tk.Entry(self.op_matriz_b_frame, width=8, font=self.fonts["normal"], 
                                     bg=self.colors["bg_light"], relief="solid", borderwidth=1)
                    entry.grid(row=i, column=j, padx=4, pady=4, ipadx=3, ipady=3)
                    fila_entries.append(entry)
                self.op_entries_b.append(fila_entries)
    
    def generar_campos_vectores(self):
        """Genera los campos de entrada para vectores."""
        for widget in self.vec_entrada_frame.winfo_children():
            widget.destroy()
        
        cantidad = int(self.vec_cantidad.get())
        dimension = int(self.vec_dimension.get())
        
        self.vec_entries = []
        for i in range(cantidad):
            ttk.Label(self.vec_entrada_frame, text=f"Vector {i+1}:", font=self.fonts["normal"]).grid(row=i, column=0, padx=8, pady=4, sticky="w")
            
            vector_entries = []
            for j in range(dimension):
                entry = tk.Entry(self.vec_entrada_frame, width=8, font=self.fonts["normal"], 
                                 bg=self.colors["bg_light"], relief="solid", borderwidth=1)
                entry.grid(row=i, column=j+1, padx=4, pady=4, ipadx=3, ipady=3)
                vector_entries.append(entry)
            self.vec_entries.append(vector_entries)
    
    def generar_campos_transpuesta(self):
        """Genera los campos de entrada para transpuesta."""
        for widget in self.trans_entrada_frame.winfo_children():
            widget.destroy()
        
        filas = int(self.trans_filas.get())
        columnas = int(self.trans_columnas.get())
        
        self.trans_entries = []
        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                entry = tk.Entry(self.trans_entrada_frame, width=8, font=self.fonts["normal"], 
                                 bg=self.colors["bg_light"], relief="solid", borderwidth=1)
                entry.grid(row=i, column=j, padx=4, pady=4, ipadx=3, ipady=3)
                fila_entries.append(entry)
        self.trans_entries.append(fila_entries)
    
    def generar_campos_matriz_inversa(self):
        """Genera los campos de entrada para matriz inversa."""
        for widget in self.inversa_entrada_frame.winfo_children():
            widget.destroy()
        
        n = int(self.inversa_dimension.get())
        
        self.inversa_entries = []
        for i in range(n):
            fila_entries = []
            for j in range(n):
                entry = tk.Entry(self.inversa_entrada_frame, width=8, font=self.fonts["normal"], 
                                 bg=self.colors["bg_light"], relief="solid", borderwidth=1)
                entry.grid(row=i, column=j, padx=4, pady=4, ipadx=3, ipady=3)
                fila_entries.append(entry)
            self.inversa_entries.append(fila_entries)
    
    def cambiar_operacion(self):
        """Actualiza la interfaz cuando cambia el tipo de operación."""
        self.generar_campos_operaciones()
    
    def validar_matriz(self, entries):
        """Valida y extrae una matriz de los campos de entrada."""
        matriz = []
        for i, fila_entries in enumerate(entries):
            fila = []
            for j, entry in enumerate(fila_entries):
                texto = entry.get().strip()
                if not texto:
                    messagebox.showerror("Error", f"Campo vacío en posición ({i+1}, {j+1})")
                    return None
                try:
                    valor = float(texto)
                    fila.append(valor)
                except ValueError:
                    messagebox.showerror("Error", f"Valor no numérico en posición ({i+1}, {j+1}): '{texto}'")
                    return None
            matriz.append(fila)
        return matriz
    
    def validar_vector(self, entries):
        """Valida y extrae un vector de los campos de entrada."""
        vector = []
        for i, entry in enumerate(entries):
            texto = entry.get().strip()
            if not texto:
                messagebox.showerror("Error", f"Campo vacío en posición {i+1}")
                return None
            try:
                valor = float(texto)
                vector.append(valor)
            except ValueError:
                messagebox.showerror("Error", f"Valor no numérico en posición {i+1}: '{texto}'")
                return None
        return vector
    
    def mostrar_resultado(self, area_texto, pasos):
        """Muestra el resultado en el área de texto especificada."""
        area_texto.delete(1.0, tk.END)
        
        # Aplicar formato con etiquetas
        area_texto.tag_configure("title", font=self.fonts["subheading"], foreground=self.colors["secondary"])
        area_texto.tag_configure("step", font=self.fonts["normal"], foreground=self.colors["text_dark"])
        area_texto.tag_configure("result", font=self.fonts["subheading"], foreground=self.colors["accent"])
        area_texto.tag_configure("matrix", font=self.fonts["normal"], foreground=self.colors["primary"])
        
        for i, paso in enumerate(pasos):
            # Añadir formato según el tipo de contenido
            if paso.startswith('==='):
                # Título de sección
                area_texto.insert(tk.END, paso + "\n\n", "title")
            elif paso.startswith('Matriz'):
                # Mostrar matrices con color diferente
                area_texto.insert(tk.END, paso + "\n", "matrix")
            elif "resultado" in paso.lower() or "solución" in paso.lower():
                # Destacar resultados
                area_texto.insert(tk.END, paso + "\n", "result")
            else:
                # Pasos normales
                area_texto.insert(tk.END, paso + "\n", "step")
        
        area_texto.see(tk.END)
    
    def resolver_gauss(self):
        """Resuelve el sistema usando eliminación gaussiana."""
        try:
            A = self.validar_matriz(self.gauss_entries_matriz)
            if A is None:
                return
            
            b = self.validar_vector(self.gauss_entries_vector)
            if b is None:
                return
            
            self.status_bar.config(text="Resolviendo sistema con eliminación gaussiana...")
            self.root.update()
            
            estado, solucion, pasos = gauss_resolver(A, b)
            
            self.mostrar_resultado(self.gauss_resultado, pasos)
            
            # Guardar para exportación
            self.ultimo_resultado = solucion
            self.ultimos_pasos = pasos
            self.ultimos_datos_entrada = {"Matriz A": A, "Vector b": b}
            self.ultimo_tipo_calculo = "Eliminación Gaussiana"
            
            self.status_bar.config(text=f"Sistema resuelto - Estado: {estado}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver sistema: {str(e)}")
            self.status_bar.config(text="Error en el cálculo")
    
    def resolver_gauss_jordan(self):
        """Resuelve el sistema usando Gauss-Jordan."""
        try:
            A = self.validar_matriz(self.gj_entries_matriz)
            if A is None:
                return
            
            b = self.validar_vector(self.gj_entries_vector)
            if b is None:
                return
            
            self.status_bar.config(text="Resolviendo sistema con Gauss-Jordan...")
            self.root.update()
            
            estado, solucion, pasos = gauss_jordan_resolver(A, b)
            
            self.mostrar_resultado(self.gj_resultado, pasos)
            
            self.ultimo_resultado = solucion
            self.ultimos_pasos = pasos
            self.ultimos_datos_entrada = {"Matriz A": A, "Vector b": b}
            self.ultimo_tipo_calculo = "Eliminación de Gauss-Jordan"
            
            self.status_bar.config(text=f"Sistema resuelto - Estado: {estado}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver sistema: {str(e)}")
            self.status_bar.config(text="Error en el cálculo")
    
    def ejecutar_operacion(self):
        """Ejecuta la operación matricial seleccionada."""
        try:
            operacion = self.operacion_var.get()
            
            A = self.validar_matriz(self.op_entries_a)
            if A is None:
                return
            
            self.status_bar.config(text=f"Ejecutando {operacion}...")
            self.root.update()
            
            if operacion == "escalar":
                try:
                    k = float(self.op_escalar_entry.get())
                except ValueError:
                    messagebox.showerror("Error", "El escalar debe ser un número válido")
                    return
                
                resultado, pasos = escalar_por_matriz(k, A)
                self.ultimos_datos_entrada = {"Escalar k": k, "Matriz A": A}
                self.ultimo_tipo_calculo = "Producto por Escalar"
            else:
                B = self.validar_matriz(self.op_entries_b)
                if B is None:
                    return
                
                if operacion == "suma":
                    resultado, pasos = sumar_matrices(A, B)
                    self.ultimo_tipo_calculo = "Suma de Matrices"
                elif operacion == "resta":
                    resultado, pasos = restar_matrices(A, B)
                    self.ultimo_tipo_calculo = "Resta de Matrices"
                elif operacion == "multiplicacion":
                    resultado, pasos = multiplicar_matrices(A, B)
                    self.ultimo_tipo_calculo = "Multiplicación de Matrices"
                
                self.ultimos_datos_entrada = {"Matriz A": A, "Matriz B": B}
            
            if resultado is not None:
                self.mostrar_resultado(self.op_resultado, pasos)
                self.ultimo_resultado = resultado
                self.ultimos_pasos = pasos
                self.status_bar.config(text=f"{operacion.capitalize()} completada")
            else:
                self.status_bar.config(text="Error en la operación")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en operación: {str(e)}")
            self.status_bar.config(text="Error en el cálculo")
    
    def analizar_vectores(self):
        """Analiza la independencia lineal de los vectores."""
        try:
            vectores = []
            for i, vector_entries in enumerate(self.vec_entries):
                vector = self.validar_vector(vector_entries)
                if vector is None:
                    return
                vectores.append(vector)
            
            self.status_bar.config(text="Analizando independencia lineal...")
            self.root.update()
            
            resultado, pasos = analizar_independencia(vectores)
            
            self.mostrar_resultado(self.vec_resultado, pasos)
            
            self.ultimo_resultado = resultado
            self.ultimos_pasos = pasos
            self.ultimos_datos_entrada = {"Vectores": vectores}
            self.ultimo_tipo_calculo = "Análisis de Independencia Lineal"
            
            independientes = resultado.get('independientes', None)
            if independientes is True:
                self.status_bar.config(text="Vectores linealmente independientes")
            elif independientes is False:
                self.status_bar.config(text="Vectores linealmente dependientes")
            else:
                self.status_bar.config(text="Análisis completado")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis: {str(e)}")
            self.status_bar.config(text="Error en el cálculo")
    
    def calcular_matriz_inversa(self):
        """Calcula la matriz inversa de la matriz ingresada."""
        try:
            A = self.validar_matriz(self.inversa_entries)
            if A is None:
                return
            
            self.status_bar.config(text="Calculando matriz inversa...")
            self.root.update()
            
            matriz_inversa, pasos = calcular_matriz_inversa(A)
            
            self.mostrar_resultado(self.inversa_resultado, pasos)
            
            # Guardar para exportación
            self.ultimo_resultado = matriz_inversa
            self.ultimos_pasos = pasos
            self.ultimos_datos_entrada = {"Matriz A": A}
            self.ultimo_tipo_calculo = "Matriz Inversa"
            
            if matriz_inversa is not None:
                self.status_bar.config(text="Matriz inversa calculada exitosamente")
            else:
                self.status_bar.config(text="La matriz no es invertible")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular matriz inversa: {str(e)}")
            self.status_bar.config(text="Error en el cálculo")
    
    def solo_verificar_invertibilidad(self):
        """Solo verifica si la matriz es invertible sin calcular la inversa."""
        try:
            A = self.validar_matriz(self.inversa_entries)
            if A is None:
                return
            
            self.status_bar.config(text="Verificando invertibilidad...")
            self.root.update()
            
            es_invertible, razon, det, pasos = verificar_invertibilidad(A)
            
            self.mostrar_resultado(self.inversa_resultado, pasos)
            
            # Guardar para exportación
            self.ultimo_resultado = {"es_invertible": es_invertible, "determinante": det, "razon": razon}
            self.ultimos_pasos = pasos
            self.ultimos_datos_entrada = {"Matriz A": A}
            self.ultimo_tipo_calculo = "Verificación de Invertibilidad"
            
            if es_invertible:
                self.status_bar.config(text="La matriz es invertible")
            else:
                self.status_bar.config(text="La matriz no es invertible")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar invertibilidad: {str(e)}")
            self.status_bar.config(text="Error en la verificación")
    
    def calcular_transpuesta(self):
        """Calcula la transpuesta de la matriz."""
        try:
            A = self.validar_matriz(self.trans_entries)
            if A is None:
                return
            
            self.status_bar.config(text="Calculando transpuesta...")
            self.root.update()
            
            resultado, pasos = transponer_matriz(A)
            
            if resultado is not None:
                self.mostrar_resultado(self.trans_resultado, pasos)
                
                self.ultimo_resultado = resultado
                self.ultimos_pasos = pasos
                self.ultimos_datos_entrada = {"Matriz A": A}
                self.ultimo_tipo_calculo = "Transpuesta de Matriz"
                
                self.status_bar.config(text="Transpuesta calculada")
            else:
                self.status_bar.config(text="Error en el cálculo")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular transpuesta: {str(e)}")
            self.status_bar.config(text="Error en el cálculo")
    
    def limpiar_gauss(self):
        """Limpia los campos de Gauss."""
        for fila in self.gauss_entries_matriz:
            for entry in fila:
                entry.delete(0, tk.END)
        for entry in self.gauss_entries_vector:
            entry.delete(0, tk.END)
        self.gauss_resultado.delete(1.0, tk.END)
    
    def limpiar_gauss_jordan(self):
        """Limpia los campos de Gauss-Jordan."""
        for fila in self.gj_entries_matriz:
            for entry in fila:
                entry.delete(0, tk.END)
        for entry in self.gj_entries_vector:
            entry.delete(0, tk.END)
        self.gj_resultado.delete(1.0, tk.END)
    
    def limpiar_operaciones(self):
        """Limpia los campos de operaciones."""
        for fila in self.op_entries_a:
            for entry in fila:
                entry.delete(0, tk.END)
        
        operacion = self.operacion_var.get()
        if operacion == "escalar":
            self.op_escalar_entry.delete(0, tk.END)
        else:
            for fila in self.op_entries_b:
                for entry in fila:
                    entry.delete(0, tk.END)
        
        self.op_resultado.delete(1.0, tk.END)
    
    def limpiar_vectores(self):
        """Limpia los campos de vectores."""
        for vector_entries in self.vec_entries:
            for entry in vector_entries:
                entry.delete(0, tk.END)
        self.vec_resultado.delete(1.0, tk.END)
    
    def limpiar_transpuesta(self):
        """Limpia los campos de transpuesta."""
        for fila in self.trans_entries:
            for entry in fila:
                entry.delete(0, tk.END)
        self.trans_resultado.delete(1.0, tk.END)
    
    def limpiar_matriz_inversa(self):
        """Limpia los campos de matriz inversa."""
        for fila in self.inversa_entries:
            for entry in fila:
                entry.delete(0, tk.END)
        self.inversa_resultado.delete(1.0, tk.END)
    
    def guardar_resultado(self):
        """Guarda el último resultado en un archivo."""
        if not self.ultimos_pasos:
            messagebox.showwarning("Advertencia", "No hay resultado para guardar")
            return
        
        try:
            nombre_archivo = generar_nombre_archivo(
                f"resultado_{self.ultimo_tipo_calculo.lower().replace(' ', '_')}", 
                "txt"
            )
            
            archivo = filedialog.asksaveasfilename(
                title="Guardar Resultado",
                initialname=nombre_archivo,
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            
            if archivo:
                exito, mensaje = exportar_resultado_completo(
                    self.ultimos_datos_entrada,
                    self.ultimos_pasos,
                    self.ultimo_resultado,
                    archivo,
                    self.ultimo_tipo_calculo
                )
                
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    self.status_bar.config(text="Resultado guardado")
                else:
                    messagebox.showerror("Error", mensaje)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        self.root.mainloop()

def main():
    """Función principal."""
    try:
        app = CalculadoraAlgebraLineal()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
