import numpy as np
import sympy
import matplotlib.pyplot as plt

# Definir a função
func = "x^3-x-1"
xpy = sympy.symbols('x')
func_py = sympy.sympify(func)
f = sympy.lambdify(xpy, func_py)

# Gerar valores de x
x = np.linspace(-2, 2, 400)

# Calcular valores de y
y = f(x)

# Criar o gráfico
plt.figure(figsize=(8,6))
plt.plot(x, y, label = func, color='b')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.title("Gráfico da função:" + func)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()

# Salvar o gráfico como uma imagem PNG
plt.savefig('grafico_funcao.png')

# Mostrar o gráfico
plt.show()
