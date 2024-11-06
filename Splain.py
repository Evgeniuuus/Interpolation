import numpy as numpy
import matplotlib.pyplot as plt
import sympy as sympy
import math

function = "sin(x)^2 * cos(x+1)"    # Исходная функция
n = 20                              # Количество интервалов, а количество точек то как раз n+1
a = 0                               # Границы
b = 10
h = (b - a) / n                     # Шаг
quantity_points = 1000              # Количество точек для отрисовки графиков

x = numpy.linspace(a, b, quantity_points)  # Массивы для исходного графика
y = numpy.sin(x) ** 2 * numpy.cos(x + 1)


# ==================================Линейный сплайн============================================
def Splain_1(mas1, mas2):
    for i in range(1, n + 1):
        x_line = numpy.linspace(x_node[i - 1], x_node[i], int(quantity_points / n))  # От узла до узла
        mas1.extend(x_line)

        S_i = ""  # Вычисляем коэффициенты полинома
        a_poli = y_node[i]
        h_poli = x_node[i] - x_node[i - 1]
        b_poli = (y_node[i - 1] - y_node[i]) / h_poli

        S_i += str(a_poli) + " + (" + str(x_node[i]) + " - x) * " + str(b_poli)

        Splain = sympy.poly(S_i)

        mas2 += [Splain.subs(sympy.Symbol('x'), x_line[i]) for i in range(len(x_line))]

    return mas1, mas2


plt.subplot(121)  # Левое окно для графиков
plt.title('Линейный сплайн', fontsize=14, fontname='Times New Roman')
plt.plot(x, y, color="red", label=str(function))
plt.grid()

x_node = [a]                                # Находим значения узлов в равномерной сетке
for i in range(n):                          # Они будут нужны для построения полиномов
    x_node.append(x_node[i] + h)
y_node = [math.sin(x_node[i]) ** 2 * math.cos(x_node[i] + 1) for i in range(len(x_node))]

x_polinomial_collect = []                   # Массивы для построения интерполяции
y_polynomial_collect = []

Splain_1(x_polinomial_collect, y_polynomial_collect)  # Заполнили

plt.plot(x_polinomial_collect, y_polynomial_collect, '--', color="green", label="Интерполяция")
plt.legend()

# ------------------------------Практическая погрешность---------------------------------------

absolute_error = [abs(y[i] - y_polynomial_collect[i]) for i in range(len(x))]
error = "max = " + str(max(absolute_error))

plt.subplot(122)
plt.title('Погрешность', fontsize=14, fontname='Times New Roman')
plt.plot(x_polinomial_collect, absolute_error, '--', color="magenta", label="Абсолютная")
plt.text(0, 0, error, fontsize=10, bbox={'facecolor': 'yellow'})

plt.grid()
plt.legend()
plt.show()


# ==============================Параболический сплайн============================================
def Splain_2(mas1, mas2):
    b_poli = sympy.diff(function)
    b_poli = b_poli.subs(sympy.Symbol('x'), a)
    for i in range(1, n + 1):
        x_line = numpy.linspace(x_node[i-1], x_node[i], int(quantity_points / n))
        mas1.extend(x_line)

        S_i = ""
        a_poli = y_node[i-1]
        h_poli = x_node[i] - x_node[i-1]
        z_poli = 2 * (y_node[i] - y_node[i-1]) / h_poli
        b_poli_1 = z_poli - b_poli
        c_poli = (b_poli_1 - b_poli) / (2 * h_poli)

        S_i += str(a_poli) + " + (x - " + str(x_node[i-1]) + ") * " + str(b_poli)
        S_i += " + (x - " + str(x_node[i-1]) + ")^2 * " + str(c_poli)

        Splain = sympy.poly(S_i)
        b_poli = b_poli_1
        mas2 += [Splain.subs(sympy.Symbol('x'), x_line[i]) for i in range(len(x_line))]

    return mas1, mas2


plt.subplot(121)  # Левое окно для графиков
plt.title('Параболический сплайн', fontsize=14, fontname='Times New Roman')
plt.plot(x, y, color="red", label=str(function))
plt.grid()

x_polinomial_collect = []                   # Массивы для построения интерполяции
y_polynomial_collect = []

Splain_2(x_polinomial_collect, y_polynomial_collect)  # Заполнили

plt.plot(x_polinomial_collect, y_polynomial_collect, '--', color="black", label="Интерполяция")
plt.legend()

# ------------------------------Практическая погрешность---------------------------------------

absolute_error = [abs(y[i] - y_polynomial_collect[i]) for i in range(len(x))]
error = "max = " + str(max(absolute_error))

plt.subplot(122)
plt.title('Погрешность', fontsize=14, fontname='Times New Roman')
plt.plot(x_polinomial_collect, absolute_error, '--', color="magenta", label="Абсолютная")
plt.text(0, 0, error, fontsize=10, bbox={'facecolor': 'yellow'})

plt.grid()
plt.legend()
plt.show()


# ==============================Кубический сплайн============================================
def Splain_3(mas1, mas2):
    pass


plt.subplot(121)  # Левое окно для графиков
plt.title('Кубический сплайн', fontsize=14, fontname='Times New Roman')
plt.plot(x, y, color="red", label=str(function))
plt.grid()


x_polinomial_collect = []                   # Массивы для построения интерполяции
y_polynomial_collect = []

Splain_3(x_polinomial_collect, y_polynomial_collect)  # Заполнили

plt.plot(x_polinomial_collect, y_polynomial_collect, '--', color="green", label="Интерполяция")
plt.legend()


# ------------------------------Практическая погрешность---------------------------------------

# absolute_error = [abs(y[i] - y_polynomial_collect[i]) for i in range(len(x))]
error = "max = " + str(max(absolute_error))

plt.subplot(122)
plt.title('Погрешность', fontsize=14, fontname='Times New Roman')
# plt.plot(x_polinomial_collect, absolute_error, '--', color="magenta", label="Абсолютная")
plt.text(0, 0, error, fontsize=10, bbox={'facecolor': 'yellow'})

plt.grid()
plt.legend()
plt.show()
