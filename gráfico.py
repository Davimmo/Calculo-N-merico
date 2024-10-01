import numpy as np
import sympy
import matplotlib.pyplot as plt

# Definir a função
func = "1/x^2"
xpy = sympy.symbols('x')
func_py = sympy.sympify(func)
f = sympy.lambdify(xpy, func_py)

# Gerar valores de x
x = np.linspace(-5, 5, 100000)

# Calcular valores de y
y = f(x)

# Criar o gráfico
plt.figure(figsize=(8,6))
plt.scatter(x, y, label = func, color='b',s=0.2,marker='.')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.title("Gráfico da função:" + func)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.ylim(-50, 50)
plt.xlim(-5, 5)
plt.legend()

# Salvar o gráfico como uma imagem PNG
plt.savefig('grafico_funcao.png')

# Mostrar o gráfico
plt.show()
