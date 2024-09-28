import numpy as np
import matplotlib.pyplot as plt

# Definir a função
def f(x):
    return x**3 - x - 1

# Gerar valores de x
x = np.linspace(-2, 2, 400)

# Calcular valores de y
y = f(x)

# Criar o gráfico
plt.figure(figsize=(8,6))
plt.plot(x, y, label=r'$f(x) = x^3 - x - 1$', color='b')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.title('Gráfico da função $f(x) = x^3 - x - 1$')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()

# Salvar o gráfico como uma imagem PNG
plt.savefig('grafico_funcao_x3_menos_x_menos_1.png')

# Mostrar o gráfico
plt.show()
