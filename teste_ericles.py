import numpy as np
import sympy
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variável global para armazenar o canvas
canvas = None
texto_inferior = None  # Text widget para o texto abaixo do gráfico
lista_de_string = None

# Funções para os métodos de aproximação
def bissec(func, xe, xd, eps, rmax):  # Bissecção
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    a = xe
    b = xd
    iter = 0
    lista_de_string = []

    while iter < rmax:
        xm = (a + b) / 2
        fxm = fx(xm)
        lista_de_string.append(f'[ {a:.6f} , {b:.6f} ] | xm = {xm:.6f} | f(xm) = {fxm:.6f}')
        if abs(fxm) <= eps:
            break
        if fx(a) * fxm < 0:
            b = xm
        else:
            a = xm
        iter += 1

    lista_de_string.append(f'\nx = {xm:.9f} | f(x) = {fxm:.9f} | {iter} iterações!')
    return lista_de_string

def fp(func, xe, xd, eps, rmax):  # Falsa Posição
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    a = xe
    b = xd
    iter = 0
    lista_de_string = []

    while iter < rmax:
        fa = fx(a)
        fb = fx(b)
        xm = (a * fb - b * fa) / (fb - fa)
        fxm = fx(xm)
        lista_de_string.append(f'[ {a:.6f} , {b:.6f} ] | xm = {xm:.6f} | f(xm) = {fxm:.6f}')
        if abs(fxm) <= eps:
            break
        if fa * fxm < 0:
            b = xm
        else:
            a = xm
        iter += 1

    lista_de_string.append(f'\nx = {xm:.9f} | f(x) = {fxm:.9f} | {iter} iterações!')
    return lista_de_string

def newton(func, xe, eps, rmax):  # Newton-Raphson
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    dfx = sympy.lambdify(x, sympy.diff(func_py, x))
    x0 = xe
    iter = 0
    lista_de_string = []

    while iter < rmax:
        xn = x0 - fx(x0) / dfx(x0)
        fxn = fx(xn)
        lista_de_string.append(f'x{iter} = {x0:.6f} | x{iter+1} = {xn:.6f} | f(x{iter+1}) = {fxn:.6f}')
        if abs(fxn) <= eps:
            break
        x0 = xn
        iter += 1

    lista_de_string.append(f'\nx = {xn:.9f} | f(x) = {fxn:.9f} | {iter} iterações!')
    return lista_de_string

def secante(func, x0, x1, eps, rmax):  # Método da Secante
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    a = x0
    b = x1
    iter = 0
    lista_de_string = []

    while iter < rmax:
        fa = fx(a)
        fb = fx(b)
        xm = (a * fb - b * fa) / (fb - fa)
        fxm = fx(xm)
        lista_de_string.append(f'x{iter} = {a:.6f} | x{iter+1} = {b:.6f} | x{iter+2} = {xm:.6f} | f(x{iter+2}) = {fxm:.6f}')
        if abs(fxm) <= eps:
            break
        a, b = b, xm
        iter += 1

    lista_de_string.append(f'x{iter+1} = {xm:.9f} | f(x{iter+1}) = {fxm:.9f} | {iter} iterações!')
    return lista_de_string

# Selecionar o método e executar
def selecionar_método(nome_do_método, Função, Epsilon, Número_de_iterações, valor_inicial=None, valor_final=None, valor_de_x=None):
    métodos = {'Bissecção': bissec, "Falsa Posição": fp, 'Newton': newton, "Secante": secante}
    if nome_do_método == 'Newton':
        return métodos['Newton'](Função, float(valor_de_x), float(Epsilon), int(Número_de_iterações))
    else:
        return métodos[nome_do_método](Função, float(valor_inicial), float(valor_final), float(Epsilon), int(Número_de_iterações))

# Interface gráfica
def mostrar_inputs(event):
    for widget in frame.winfo_children():
        widget.destroy()

    metodo = combo.get()

    if metodo == "Bissecção" or metodo == "Falsa Posição" or metodo == "Secante":
        titulos = ["Função", "Intervalo inicial", "Intervalo final", "epsilon", "Número de iterações"]
    elif metodo == "Newton":
        titulos = ["Função", "Valor de x", "epsilon", "Número de iterações"]

    for titulo in titulos:
        label = tk.Label(frame, text=titulo)
        label.grid(sticky=tk.W)
        entry = tk.Entry(frame)
        entry.grid(sticky=tk.W)
        entradas[titulo] = entry

def calcular():
    valores = {}
    for chave in entradas.keys():
        if entradas[chave]:
            valores[chave] = entradas[chave].get()

    Função = valores.get("Função", "")
    Valor_inicial = valores.get("Intervalo inicial", "")
    Valor_final = valores.get("Intervalo final", "")
    Epsilon = valores.get("epsilon", "")
    Número_de_iterações = valores.get("Número de iterações", "")
    Valor_de_x = valores.get("Valor de x", "")
    nome_do_método = combo.get()

    global lista_de_string
    lista_de_string = selecionar_método(nome_do_método, Função, Epsilon, Número_de_iterações, Valor_inicial, Valor_final, Valor_de_x)

    plotar_grafico(Função)

def plotar_grafico(func):
    global canvas
    global texto_inferior

    if canvas is not None:
        canvas.get_tk_widget().destroy()

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    xpy = sympy.symbols('x')
    func_py = sympy.sympify(func)
    f = sympy.lambdify(xpy, func_py)

    x = np.linspace(-1, 1, 400)
    y = f(x)

    ax.plot(x, y, label=func, color='b')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title("Gráfico da função: " + func)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.grid(True)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    if texto_inferior is not None:
        texto_inferior.destroy()

    frame_texto = tk.Frame(frame_grafico)
    frame_texto.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame_texto)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    texto_inferior = tk.Text(frame_texto, height=6, yscrollcommand=scrollbar.set)
    texto_inferior.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=texto_inferior.yview)

    texto_inferior.insert(tk.END, "\n".join(lista_de_string))
    texto_inferior.config(state=tk.DISABLED)

# Interface gráfica principal
root = tk.Tk()
root.title("Seleção de Método")

mensagem = tk.Label(root, text="Selecione um método:")
mensagem.grid(row=0, column=0, columnspan=2, pady=10)

combo = ttk.Combobox(root, values=["Bissecção", "Falsa Posição", "Newton", "Secante"], state="readonly")
combo.grid(row=1, column=0, columnspan=2)
combo.bind("<<ComboboxSelected>>", mostrar_inputs)

frame = tk.Frame(root)
frame.grid(row=2, column=0, columnspan=2, pady=10)

botao_calcular = tk.Button(root, text="Calcular", command=calcular)
botao_calcular.grid(row=3, column=0, columnspan=2)

frame_grafico = tk.Frame(root)
frame_grafico.grid(row=4, column=0, columnspan=2, pady=10)

entradas = {}

root.mainloop()
