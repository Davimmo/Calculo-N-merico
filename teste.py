import tkinter as tk
from tkinter import messagebox, Toplevel
from tkinter import ttk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def validar_entradas(app, campos):
    """
    Valida as entradas nos campos especificados.
    Retorna True se todas as entradas forem válidas, caso contrário, exibe um alerta e retorna False.
    """
    for campo in campos:
        valor = app.__getattribute__(f'entry_{campo}').get()
        if not valor:
            messagebox.showerror("Erro", f"O campo {campo} não pode estar vazio.")
            return False
        try:
            float(valor)  # Verifica se pode converter para float
        except ValueError:
            messagebox.showerror("Erro", f"O valor no campo {campo} não é um número válido.")
            return False
    return True

# Função para criar e mostrar a nova janela com resultados e gráfico
def mostrar_resultados(func_str, resultados, metodo):
    resultado_janela = Toplevel()
    resultado_janela.title(f"Resultados - {metodo}")
    resultado_janela.geometry("600x600")
    resultado_janela.state('zoomed')  # Maximiza a janela no Windows
    resultado_janela.config(bg='lightgreen')

    # Exibindo o gráfico
    x = sp.symbols('x')
    func = sp.sympify(func_str)
    func_np = sp.lambdify(x, func)

    x_vals = np.linspace(-10, 10, 400)
    y_vals = func_np(x_vals)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x_vals, y_vals, label=f"f(x) = {func_str}")
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title(f"Gráfico de f(x) = {func_str}")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=resultado_janela)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Criando a tabela
    table_frame = tk.Frame(resultado_janela)
    table_frame.pack(pady=10)

    columns = ["Iteração", "x", "f(x)", "Diferença", "Erro"]
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)

    for i, (x_val, f_val, diff_val, erro_val) in enumerate(resultados):
        tree.insert("", "end", values=(i + 1, x_val, f_val, diff_val, erro_val))

    tree.pack(side=tk.LEFT, fill=tk.BOTH)
    scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scroll.set)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Função para executar o método de Bisseção e mostrar os resultados
def executar_bissecao(app):
    func_str = app.entry_func.get()
    if validar_entradas(app, ["xe", "xd", "eps", "rmax"]):
        xe = float(app.entry_xe.get())
        xd = float(app.entry_xd.get())
        eps = float(app.entry_eps.get())
        rmax = int(app.entry_rmax.get())
        resultados = bissec(func_str, xe, xd, eps, rmax)
        mostrar_resultados(func_str, resultados, "Bisseção")

# Função para executar o método de Falsa Posição e mostrar os resultados
def executar_falsa_posicao(app):
    func_str = app.entry_func.get()
    if validar_entradas(app, ["xe", "xd", "eps", "rmax"]):
        xe = float(app.entry_xe.get())
        xd = float(app.entry_xd.get())
        eps = float(app.entry_eps.get())
        rmax = int(app.entry_rmax.get())
        resultados = fp(func_str, xe, xd, eps, rmax)
        mostrar_resultados(func_str, resultados, "Falsa Posição")

# Função para executar o método de Newton e mostrar os resultados
def executar_newton(app):
    func_str = app.entry_func.get()
    if validar_entradas(app, ["xe", "eps", "rmax"]):
        xe = float(app.entry_xe.get())
        eps = float(app.entry_eps.get())
        rmax = int(app.entry_rmax.get())
        resultados = newton(func_str, xe, eps, rmax)
        mostrar_resultados(func_str, resultados, "Newton")

# Função para executar o método de Secantes e mostrar os resultados
def executar_secantes(app):
    func_str = app.entry_func.get()
    if validar_entradas(app, ["xe", "xd", "eps", "rmax"]):
        x0 = float(app.entry_xe.get())  
        x1 = float(app.entry_xd.get())  
        eps = float(app.entry_eps.get())
        rmax = int(app.entry_rmax.get())
        resultados = secante(func_str, x0, x1, eps, rmax)
        mostrar_resultados(func_str, resultados, "Secantes")

# Função Bisseção
def bissec(func, xe, xd, eps, rmax):
    x = sp.symbols('x')
    func_py = sp.sympify(func)
    fx = sp.lambdify(x, func_py)
    dfx = sp.lambdify(x, sp.diff(func_py, x))
    a = xe
    b = xd
    xm = (a + b) / 2
    fxm = fx(xm)
    iter = 0
    resultados = []
    
    if ((dfx(a) >= 0 and dfx(b) >= 0) or (dfx(a) < 0 and dfx(b) < 0)) and ((fx(a) * fx(b)) < 0):
        while abs(fxm) > eps and iter < rmax:
            xm = (a + b) / 2
            fxm = fx(xm)
            diff = fxm - eps
            resultados.append((xm, fxm, diff, fxm - eps))
            if (fx(a) * fxm) < 0:
                b = xm
            else:
                a = xm
            iter += 1
        resultados.append((xm, fxm, None, fxm - eps))
        return resultados
    return []

# Função Falsa Posição
def fp(func, xe, xd, eps, rmax):
    x = sp.symbols('x')
    func_py = sp.sympify(func)
    fx = sp.lambdify(x, func_py)
    dfx = sp.lambdify(x, sp.diff(func_py, x))
    a = xe
    b = xd
    fa = fx(a)
    fb = fx(b)
    xm = (a * fb - b * fa) / (fb - fa)
    fxm = fx(xm)
    iter = 0
    resultados = []

    if ((dfx(a) >= 0 and dfx(b) >= 0) or (dfx(a) < 0 and dfx(b) < 0)) and ((fx(a) * fx(b)) < 0):
        while abs(fxm) > eps and iter < rmax:
            fa = fx(a)
            fb = fx(b)
            xm = (a * fb - b * fa) / (fb - fa)
            fxm = fx(xm)
            diff = fxm - eps
            resultados.append((xm, fxm, diff, fxm - eps))
            if (fx(a) * fxm) < 0:
                b = xm
            else:
                a = xm
            iter += 1
        resultados.append((xm, fxm, None, fxm - eps))
        return resultados
    return []

# Função Newton
def newton(func, xe, eps, rmax):
    x = sp.symbols('x')
    func_py = sp.sympify(func)
    fx = sp.lambdify(x, func_py)
    dfx = sp.lambdify(x, sp.diff(func_py, x))
    x0 = xe
    xn = x0 - (fx(x0) / dfx(x0))
    fxn = fx(xn)
    iter = 0
    resultados = []

    while abs(fxn) > eps and iter < rmax:
        resultados.append((x0, fx(x0), fxn - eps, fxn - eps))
        xn = x0 - (fx(x0) / dfx(x0))
        fxn = fx(xn)
        x0 = xn
        iter += 1
    resultados.append((xn, fxn, None, fxn - eps))
    return resultados

# Função Secantes
def secante(func, x0, x1, eps, rmax):
    x = sp.symbols('x')
    func_py = sp.sympify(func)
    fx = sp.lambdify(x, func_py)
    fxa = fx(x0)
    fxb = fx(x1)
    xm = (x0 * fxb - x1 * fxa) / (fxb - fxa)
    fxm = fx(xm)
    iter = 0
    resultados = []

    while abs(fxm) > eps and iter < rmax:
        resultados.append((x0, fxa, fxm - eps, fxm - eps))
        fxa = fx(x0)
        fxb = fx(x1)
        xm = (x0 * fxb - x1 * fxa) / (fxb - fxa)
        fxm = fx(xm)
        x0 = x1
        x1 = xm
        iter += 1
    resultados.append((xm, fxm, None, fxm - eps))
    return resultados

# Exemplo de como a classe App pode ser definida
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Métodos Numéricos")
        self.geometry("500x400")
        self.state('zoomed')  # Maximiza a janela no Windows
        self.config(bg='lightblue') 

        self.label_func = tk.Label(self, text="Função:")
        self.label_func.pack()
        self.entry_func = tk.Entry(self)
        self.entry_func.pack()

        self.label_xe = tk.Label(self, text="Estimativa Inicial (xe):")
        self.label_xe.pack()
        self.entry_xe = tk.Entry(self)
        self.entry_xe.pack()

        self.label_xd = tk.Label(self, text="Estimativa Final (xd):")
        self.label_xd.pack()
        self.entry_xd = tk.Entry(self)
        self.entry_xd.pack()

        self.label_eps = tk.Label(self, text="Epsilon:")
        self.label_eps.pack()
        self.entry_eps = tk.Entry(self)
        self.entry_eps.pack()

        self.label_rmax = tk.Label(self, text="Máximo de iterações (rmax):")
        self.label_rmax.pack()
        self.entry_rmax = tk.Entry(self)
        self.entry_rmax.pack()

        self.button_bissecao = tk.Button(self, text="Bisseção", command=lambda: executar_bissecao(self))
        self.button_bissecao.pack(pady=5)

        self.button_falsa_posicao = tk.Button(self, text="Falsa Posição", command=lambda: executar_falsa_posicao(self))
        self.button_falsa_posicao.pack(pady=5)

        self.button_newton = tk.Button(self, text="Newton", command=lambda: executar_newton(self))
        self.button_newton.pack(pady=5)

        self.button_secantes = tk.Button(self, text="Secantes", command=lambda: executar_secantes(self))
        self.button_secantes.pack(pady=5)
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
