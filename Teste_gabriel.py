import numpy as np
import sympy
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def bissec(func, xe, xd, eps, rmax): #func = string funcao / xe e xd = [a,b] inicial / eps = epsilon / rmax = maximo de repeticoes
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    dfx = sympy.lambdify(x, sympy.diff(func_py,x))
    a = xe
    b = xd
    xm = (a+b)/2
    fxm = fx(xm)
    iter = 0
    if( ( (dfx(a) >= 0 and dfx(b) >= 0) or (dfx(a) < 0 and dfx(b) < 0) ) and ( (fx(a)*fx(b))<0 ) ):
        lista_de_string=[]
        while(abs(fxm) > eps and iter < rmax):
            xm = (a+b)/2
            fxm= fx(xm)
            lista_de_string.append(f'[ {a:.6f} , {b:.6f} ] | xm = {xm:.6f} | f(xm) = {fxm:.6f} | diferença de f(x) e epsilon = {fxm-eps:.6f}')
            if( ( fx(a)*fxm ) < 0):
                b=xm
            else:
                a=xm
            iter+=1
        lista_de_string.append(f'\nx = {xm:.9f} | f(x) = {fxm:.9f} | {iter} iterações! | erro: {fxm-eps:.9f}')
        return xm
    return lista_de_string

def fp(func, xe, xd, eps, rmax): #func = string funcao / xe e xd = [a,b] inicial / eps = epsilon / rmax = maximo de repeticoes
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    dfx = sympy.lambdify(x, sympy.diff(func_py,x))
    a = xe
    b = xd
    fa = fx(a)
    fb = fx(b)
    xm = ( (a*fb-b*fa)/(fb-fa) )
    fxm= fx(xm)
    iter = 0
    if( ( (dfx(a) >= 0 and dfx(b) >= 0) or (dfx(a) < 0 and dfx(b) < 0) ) and ( (fx(a)*fx(b))<0 ) ):
        lista_de_string=[]
        while(abs(fxm) > eps and iter < rmax):
            fa = fx(a)
            fb = fx(b)
            xm = ( (a*fb-b*fa)/(fb-fa) )
            fxm= fx(xm)
            (f'[ {a:.6f} , {b:.6f} ] | xm = {xm:.6f} | f(xm) = {fxm:.6f} | diferença de f(x) e epsilon = {fxm-eps:.6f}')
            if( ( fx(a)*fxm ) < 0):
                b=xm
            else:
                a=xm
            iter+=1
        lista_de_string.append(f'\nx = {xm:.9f} | f(x) = {fxm:.9f} | {iter} iterações! | erro: {fxm-eps:.9f}')
        return xm
    return lista_de_string

def newton(func, xe, eps, rmax): #func = string funcao / xe = x estimado / eps = epsilon / rmax = maximo de repeticoes
    lista_de_string=[]
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    dfx = sympy.lambdify(x, sympy.diff(func_py,x))
    x0 = xe
    xn = x0-( fx(x0)/dfx(x0) )
    fxn = fx(xn)
    iter = 0
    while(abs(fxn) > eps and iter < rmax):
        xn = x0-( fx(x0)/dfx(x0) )
        fxn = fx(xn)
        lista_de_string.append(f'x{iter} = {x0:.6f} | x{iter+1} = {xn:.6f} | f(x{iter+1}) = {fxn:.6f} | diferença de f(x{iter+1}) e epsilon = {fxn-eps:.6f}')
        x0 = xn
        iter+=1
    lista_de_string.append(f'\nx{iter} = {xn:.9f} | f(x{iter}) = {fxn:.9f} | {iter} iterações! | erro: {fxn-eps:.9f}')
    return lista_de_string

def secante(func, x0, x1, eps, rmax): #func = string funcao / x0 e x1 = estimativas iniciais / eps = epsilon / rmax = maximo de repeticoes
    lista_de_string=[]
    x = sympy.symbols('x')
    func_py = sympy.sympify(func)
    fx = sympy.lambdify(x, func_py)
    dfx = sympy.lambdify(x, sympy.diff(func_py,x))
    a = x0
    b = x1
    fxa = fx(a)
    fxb = fx(b)
    xm = ( (a*fxb-b*fxa)/(fxb-fxa) )
    fxm = fx(xm)
    iter = 0
    while(abs(fxm) > eps and iter < rmax):
        fxa = fx(a)
        fxb = fx(b)
        xm = ( (a*fxb-b*fxa)/(fxb-fxa) )
        fxm = fx(xm)
        lista_de_string.append(f'x{iter} = {a:.6f} | x{iter+1} = {b:.6f} | x{iter+2} = {xm:.6f} | f(x{iter+2}) = {fxm:.6f} | diferença de f(x{iter+2}) e epsilon = {fxm-eps:.6f}')
        a = b
        b = xm
        iter+=1
    lista_de_string.append(f'x{iter+1} = {xm:.9f} | f(x{iter+1}) = {fxm:.9f} | {iter} iterações! | erro: {fxm-eps:.9f}')
    return lista_de_string

def selecionar_método(nome_do_método):
    métodos={'Bissecção':bissec,"Falsa Posição":fp,'Newton':newton,"Secante":secante}
    métodos[nome_do_método]()

# Variável global para armazenar o canvas
canvas = None
texto_inferior = None  # Text widget para o texto abaixo do gráfico
lista_de_string = None

def selecionar_método(nome_do_método, Função, Epsilon, Número_de_iterações, valor_inicial=None, valor_final=None, valor_de_x=None):
    métodos = {'Bissecção': bissec, "Falsa Posição": fp, 'Newton': newton, "Secante": secante}
    if nome_do_método == 'Newton':
        return métodos['Newton'](Função, float(valor_de_x), float(Epsilon), int(Número_de_iterações))
    else:
        return métodos[nome_do_método](Função, float(valor_inicial), float(valor_final), float(Epsilon), int(Número_de_iterações))

def mostrar_inputs(event):
    # Limpa as entradas existentes
    for widget in frame.winfo_children():
        widget.destroy()

    metodo = combo.get()

    # Títulos e quantidades de entradas com base no método selecionado
    if metodo == "Bissecção" or metodo == "Falsa Posição" or metodo == "Secante":
        titulos = ["Função", "Intervalo inicial", "Intervalo final", "epsilon", "Número de iterações"]
    elif metodo == "Newton":
        titulos = ["Função", "Valor de x", "epsilon", "Número de iterações"]

    # Criação dos rótulos e entradas de acordo com o método
    for titulo in titulos:
        label = tk.Label(frame, text=titulo)
        label.grid(sticky=tk.W)  # Alinha à esquerda
        entry = tk.Entry(frame)
        entry.grid(sticky=tk.W)  # Alinha à esquerda
        entradas[titulo] = entry  # Salva a referência da entrada no dicionário

def calcular():
    # Inicializa um dicionário para armazenar as entradas capturadas
    valores = {}

    # Captura os valores das entradas
    for chave in entradas.keys():
        if entradas[chave]:  # Verifica se a entrada existe
            valores[chave] = entradas[chave].get()  # Armazena o valor da entrada

    # Obtém os valores das entradas
    Função = valores.get("Função", "")
    Valor_inicial = valores.get("Intervalo inicial", "")
    Valor_final = valores.get("Intervalo final", "")
    Epsilon = valores.get("epsilon", "")
    Número_de_iterações = valores.get("Número de iterações", "")
    Valor_de_x = valores.get("Valor de x", "")
    nome_do_método = combo.get()

    global lista_de_string
    lista_de_string = selecionar_método(nome_do_método, Função, Epsilon, Número_de_iterações, Valor_inicial, Valor_final, Valor_de_x)

    # Gerar e mostrar o gráfico
    plotar_grafico(Função)

def plotar_grafico(func):
    global canvas  # Referenciar a variável global do canvas
    global texto_inferior  # Referenciar a variável do texto abaixo do gráfico

    # Limpar o gráfico anterior, se existir
    if canvas is not None:
        canvas.get_tk_widget().destroy()

    # Criar a figura do gráfico
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Definir a função usando SymPy
    xpy = sympy.symbols('x')
    func_py = sympy.sympify(func)
    f = sympy.lambdify(xpy, func_py)

    # Gerar valores de x
    x = np.linspace(-1, 1, 400)

    # Calcular valores de y
    y = f(x)

    # Criar o gráfico
    ax.plot(x, y, label=func, color='b')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title("Gráfico da função: " + func)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.grid(True)
    ax.legend()

    # Integrando o gráfico com a interface Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Exibir o texto abaixo do gráfico com rolagem
    if texto_inferior is not None:
        texto_inferior.destroy()

    # Frame para a área de texto com scrollbar
    frame_texto = tk.Frame(frame_grafico)
    frame_texto.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame_texto)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    texto_inferior = tk.Text(frame_texto, height=6, yscrollcommand=scrollbar.set)
    texto_inferior.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=texto_inferior.yview)

    # Inserir o texto no widget Text
    texto_inferior.insert(tk.END, "\n".join(lista_de_string))

    # Tornar o widget Text não editável
    texto_inferior.config(state=tk.DISABLED)

# Criação da janela principal
root = tk.Tk()
root.title("Seleção de Método")

# Mensagem inicial
mensagem = tk.Label(root, text="Selecione um método:")
mensagem.grid(row=0, column=0, columnspan=2, pady=10)

# Menu dropdown
combo = ttk.Combobox(root, values=["Bissecção", "Falsa Posição", "Newton", "Secante"])
combo.grid(row=1, column=0, columnspan=2, pady=10)
combo.bind("<<ComboboxSelected>>", mostrar_inputs)

# Frame para as entradas
frame = tk.Frame(root)
frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

# Frame para o gráfico
frame_grafico = tk.Frame(root)
frame_grafico.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

# Dicionário para armazenar as entradas
entradas = {}

# Botão Calcular
botao_calcular = tk.Button(root, text="Calcular", command=calcular)
botao_calcular.grid(row=3, column=0, columnspan=2, pady=10)

# Configuração de peso para permitir redimensionamento
root.grid_rowconfigure(2, weight=1)  # O row 2 (onde estão os frames) pode expandir
root.grid_columnconfigure(1, weight=1)  # A coluna 1 (onde está o gráfico) pode expandir

# Iniciar o loop da interface gráfica
root.mainloop()