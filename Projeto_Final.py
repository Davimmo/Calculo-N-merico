import tkinter as tk
from tkinter import messagebox, Toplevel
from tkinter import ttk
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def validar_entradas(app, campos):
    for campo in campos:
        valor = app.__getattribute__(f'entry_{campo}').get()
        if not valor:
            messagebox.showerror("Erro", f"O campo {campo} não pode estar vazio.")
            return False
        try:
            float(valor)
        except ValueError:
            messagebox.showerror("Erro", f"O valor no campo {campo} não é um número válido.")
            return False
    return True

def mostrar_resultados(func_str, resultados, metodo):
    resultado_janela = Toplevel()
    resultado_janela.title(f"Resultados - {metodo}")
    resultado_janela.geometry("600x600")
    resultado_janela.state('zoomed')
    resultado_janela.config(bg='lightgreen')

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

    table_frame = tk.Frame(resultado_janela)
    table_frame.pack(pady=10)

    if metodo == "Bisseção" or metodo == "Falsa Posição":
        columns = ["Iteração", "a", "b", "x", "f(x)", "Diferença"]
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')

        for i, (a, b, xm, fxm, diff_val) in enumerate(resultados):
            if i == len(resultados) - 1:  # Se for o último elemento
                tree.insert("", "end", values=("resultado", f"{a:.6f}", f"{b:.6f}", f"{xm:.6f}", f"{fxm:.6f}", f"{diff_val:.6f}"))
            else:
                tree.insert("", "end", values=(i + 1, f"{a:.6f}", f"{b:.6f}", f"{xm:.6f}", f"{fxm:.6f}", f"{diff_val:.6f}"))

    elif metodo == "Newton":
        columns = ["Iteração", "x(k)", "x(k+1)", "f(x(k+1))", "Diferença"]
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')

        for i, (x0, x1, fxm, diff_val) in enumerate(resultados):
            if i == len(resultados) - 1:  # Se for o último elemento
                tree.insert("", "end", values=("resultado", f"{x0:.6f}", f"{x1:.6f}", f"{fxm:.6f}", f"{diff_val:.6f}"))
            else:
                tree.insert("", "end", values=(i + 1, f"{x0:.6f}", f"{x1:.6f}", f"{fxm:.6f}", f"{diff_val:.6f}"))

    elif metodo == "Secantes":
        columns = ["Iteração", "x(k-1)", "x(k)", "x(k+1)", "f(x(k+1))", "Diferença"]
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')

        for i, (x0, x1, xm, fxm, diff_val) in enumerate(resultados):
            if i == len(resultados) - 1:  # Se for o último elemento
                tree.insert("", "end", values=("resultado", f"{x0:.6f}", f"{x1:.6f}", f"{xm:.6f}", f"{fxm:.6f}", f"{diff_val:.6f}"))
            else:
                tree.insert("", "end", values=(i + 1, f"{x0:.6f}", f"{x1:.6f}", f"{xm:.6f}", f"{fxm:.6f}", f"{diff_val:.6f}"))


    tree.pack(side=tk.LEFT, fill=tk.BOTH)
    scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scroll.set)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)


def executar_bissecao(app):
    func_str = app.entry_func.get()
    if validar_entradas(app, ["xe", "xd", "eps", "rmax"]):
        xe = float(app.entry_xe.get())
        xd = float(app.entry_xd.get())
        eps = float(app.entry_eps.get())
        rmax = int(app.entry_rmax.get())
        resultados = bissec(func_str, xe, xd, eps, rmax)
        mostrar_resultados(func_str, resultados, "Bisseção")

def executar_falsa_posicao(app):
    func_str = app.entry_func.get()
    if validar_entradas(app, ["xe", "xd", "eps", "rmax"]):
        xe = float(app.entry_xe.get())
        xd = float(app.entry_xd.get())
        eps = float(app.entry_eps.get())
        rmax = int(app.entry_rmax.get())
        resultados = fp(func_str, xe, xd, eps, rmax)
        mostrar_resultados(func_str, resultados, "Falsa Posição")

def executar_newton(app):
    func_str = app.entry_func.get()
    if validar_entradas(app, ["xe", "eps", "rmax"]):
        xe = float(app.entry_xe.get())
        eps = float(app.entry_eps.get())
        rmax = int(app.entry_rmax.get())
        resultados = newton(func_str, xe, eps, rmax)
        mostrar_resultados(func_str, resultados, "Newton")

def executar_secantes(app):
    func_str = app.entry_func.get()
    if validar_entradas(app, ["xe", "xd", "eps", "rmax"]):
        x0 = float(app.entry_xe.get())  
        x1 = float(app.entry_xd.get())  
        eps = float(app.entry_eps.get())
        rmax = int(app.entry_rmax.get())
        resultados = secante(func_str, x0, x1, eps, rmax)
        mostrar_resultados(func_str, resultados, "Secantes")

def bissec(func, xe, xd, eps, rmax):
    x = sp.symbols('x')
    func_py = sp.sympify(func)
    fx = sp.lambdify(x, func_py)
    a = xe
    b = xd
    xm = (a + b) / 2
    fxm = fx(xm)
    iter = 0
    resultados = []
    
    while (abs(fxm) > eps and iter < rmax):
        xm = (a + b) / 2
        fxm = fx(xm)
        diff = abs(fxm) - eps
        resultados.append((a, b, xm, fxm, diff))
        if fx(a) * fxm < 0:
            b = xm
        else:
            a = xm
        iter += 1
    diff = abs(fxm) - eps
    resultados.append((a, b, xm, fxm, diff))
    return resultados

def fp(func, xe, xd, eps, rmax):
    x = sp.symbols('x')
    func_py = sp.sympify(func)
    fx = sp.lambdify(x, func_py)
    a = xe
    b = xd
    fa = fx(a)
    fb = fx(b)
    iter = 0
    resultados = []
    xm = ( (a*fb-b*fa)/(fb-fa) )
    fxm= fx(xm)
    while (abs(fxm) > eps and iter < rmax):
        xm = (a * fb - b * fa) / (fb - fa)
        fxm = fx(xm)
        diff = abs(fxm) - eps
        resultados.append((a, b, xm, fxm, diff))
        if fx(a) * fxm < 0:
            b = xm
        else:
            a = xm
        fa = fx(a)
        fb = fx(b)
        iter += 1
    resultados.append((a, b, xm, fxm, diff))
    return resultados

def newton(func, xe, eps, rmax):
    x = sp.symbols('x')
    func_py = sp.sympify(func)
    fx = sp.lambdify(x, func_py)
    dfx = sp.lambdify(x, sp.diff(func_py, x))
    x0 = xe
    iter = 0
    resultados = []
    xn = x0-( fx(x0)/dfx(x0) )
    fxn = fx(xn)
    while (abs(fxn) > eps and iter < rmax):
        fxn = fx(x0)
        dfxn = dfx(x0)
        if abs(fxn) < eps or iter >= rmax:
            break
        x1 = x0 - fxn / dfxn
        diff = abs(fx(x1)) - eps
        resultados.append((x0, x1, fx(x1), diff))
        x0 = x1
        iter += 1
    resultados.append((x0, x1, fx(x1), diff))
    return resultados

def secante(func, x0, x1, eps, rmax):
    x = sp.symbols('x')
    func_py = sp.sympify(func)
    fx = sp.lambdify(x, func_py)
    a = x0
    b = x1
    fxa = fx(a)
    fxb = fx(b)
    xm = x1 - fxb * (x1 - x0) / (fxb - fxa)
    fxm = fx(xm)
    iter = 0
    resultados = []
    while (abs(fxm) > eps and iter < rmax):
        fxa = fx(x0)
        fxb = fx(x1)
        if abs(fxb) < eps or iter >= rmax:
            break
        xm = x1 - fxb * (x1 - x0) / (fxb - fxa)
        diff = abs(fx(xm)) - eps
        resultados.append((x0, x1, xm, fx(xm), diff))
        x0, x1 = x1, xm
        iter += 1
    resultados.append((x0, x1, xm, fx(xm), diff))
    return resultados

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Métodos Numéricos")
        self.geometry("500x400")
        self.state('zoomed')
        self.config(bg='lightblue')

        # Espaçamento vertical (pady) adicionado para cada elemento
        self.label_func = tk.Label(self, text="Função:")
        self.label_func.pack(pady=(10, 0))  # Espaço superior de 10 pixels

        self.entry_func = tk.Entry(self)
        self.entry_func.pack(pady=(0, 10))  # Espaço inferior de 10 pixels

        self.label_xe = tk.Label(self, text="X inicial (ou X(k-1)):")
        self.label_xe.pack(pady=(10, 0))

        self.entry_xe = tk.Entry(self)
        self.entry_xe.pack(pady=(0, 10))

        self.label_xd = tk.Label(self, text="X final (ou X(K)):")
        self.label_xd.pack(pady=(10, 0))

        self.entry_xd = tk.Entry(self)
        self.entry_xd.pack(pady=(0, 10))

        self.label_eps = tk.Label(self, text="Precisão (epsilon):")
        self.label_eps.pack(pady=(10, 0))

        self.entry_eps = tk.Entry(self)
        self.entry_eps.pack(pady=(0, 10))

        self.label_rmax = tk.Label(self, text="Iterações Máximas:")
        self.label_rmax.pack(pady=(10, 0))

        self.entry_rmax = tk.Entry(self)
        self.entry_rmax.pack(pady=(0, 10))

        # Botões com espaçamento adicional
        self.button_bissecao = tk.Button(self, text="Bisseção", command=lambda: executar_bissecao(self))
        self.button_bissecao.pack(pady=(20, 5))

        self.button_fp = tk.Button(self, text="Falsa Posição", command=lambda: executar_falsa_posicao(self))
        self.button_fp.pack(pady=(5, 5))

        self.button_newton = tk.Button(self, text="Newton", command=lambda: executar_newton(self))
        self.button_newton.pack(pady=(5, 5))

        self.button_secante = tk.Button(self, text="Secantes", command=lambda: executar_secantes(self))
        self.button_secante.pack(pady=(5, 20))

if __name__ == "__main__":
    app = App()
    app.mainloop()
