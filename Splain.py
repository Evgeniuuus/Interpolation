import numpy as numpy
import matplotlib.pyplot as plt
import sympy as sympy
import math

function = "sin(x)^2 * cos(x+1)"                            # Исходная функция
n = 20                                                      # Количество интервалов, а количество точек то как раз n+1
a = 0                                                       # Границы
b = 10
h = (b - a) / n                                             # Шаг
quantity_points = 1000                                      # Количество точек для отрисовки графиков

x = numpy.linspace(a, b, quantity_points)                   # Массивы для исходного графика
y = numpy.sin(x) ** 2 * numpy.cos(x + 1)

x_node = [a]                                                # Находим значения узлов в равномерной сетке
for i in range(n):                                          # Они будут нужны для построения полиномов
    x_node.append(x_node[i] + h)
y_node = [math.sin(x_node[i]) ** 2 * math.cos(x_node[i] + 1) for i in range(len(x_node))]


# ==================================Линейный сплайн============================================
def Splain_1(mas1, mas2):
    for i in range(1, n + 1):
        x_line = numpy.linspace(x_node[i - 1], x_node[i], int(quantity_points / n))  # От узла до узла
        mas1.extend(x_line)

        S_i = ""                                                    # Вычисляем коэффициенты полинома
        a_poli = y_node[i]
        h_poli = x_node[i] - x_node[i - 1]
        b_poli = (y_node[i - 1] - y_node[i]) / h_poli

        S_i += str(a_poli) + " + (" + str(x_node[i]) + " - x) * " + str(b_poli)

        Splain = sympy.poly(S_i)

        mas2 += [Splain.subs(sympy.Symbol('x'), x_line[i]) for i in range(len(x_line))]

    return mas1, mas2


plt.subplot(121)                                                    # Левое окно для графиков
plt.title('Линейный сплайн', fontsize=14, fontname='Times New Roman')
plt.plot(x, y, color="red", label=str(function))
plt.grid()

x_polinomial_collect = []                                           # Массивы для построения интерполяции
y_polynomial_collect = []

Splain_1(x_polinomial_collect, y_polynomial_collect)                # Заполнили

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


plt.subplot(121)                                                    # Левое окно для графиков
plt.title('Параболический сплайн', fontsize=14, fontname='Times New Roman')
plt.plot(x, y, color="red", label=str(function))
plt.grid()

x_polinomial_collect = []                                           # Массивы для построения интерполяции
y_polynomial_collect = []

Splain_2(x_polinomial_collect, y_polynomial_collect)                # Заполнили

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
    p_i = 0                                 # самые первые p и q у нас нулевые (по условию)
    q_i = 0
    p = [p_i]
    q = [q_i]
                                            # h задавали в самом начале
    h_poli = h                              # Так как у нас равномерная сетка, то hi = hi+1

    # цикл делает до n не включая конец
    for i in range(1, n):  # Считаем коэффициенты альфа бета гамма фи внутри промежутка. => Их будет n-1
        alpha_poli = h_poli
        beta_poli = 2 * (h_poli + h_poli)
        gamma_poli = h_poli
        phi_poli = 6 * ((y_node[i + 1] - y_node[i]) / h_poli - (y_node[i] - y_node[i - 1]) / h_poli)

        # Считаем коэффициенты p и q которые внутри
        p_i_1 = (-1) * (gamma_poli / (beta_poli + alpha_poli * p_i))
        q_i_1 = (phi_poli - alpha_poli * q_i) / (beta_poli + alpha_poli * p_i)

        p.append(p_i_1)
        q.append(q_i_1)

        p_i = p_i_1
        q_i = q_i_1

    # Соответственно количество коэффициентов p и q будет n (начальные и то что внутри)

    c_n = 0                                         # тобишь самая последняя c
    c = [c_n]
    for i in range(n - 1, 0, -1):                   # до 0-го элемента не включая конец
        c_i = p[i] * c[n - i - 1] + q[i]
        c.append(c_i)
    c += [0]                                        # самое первое c (тоже по условию)
    c.reverse()
    # Всего коэффициентов c будет n+1 (столько же сколько точек)

    d = []
    for i in range(0, n):
        d.append((c[i] - c[i + 1]) / h_poli)

    b = []
    for i in range(0, n):
        b_i = (y_node[i] - y_node[i + 1]) / h_poli - (c[i + 1] * h_poli)/2 - ((c[i] - c[i + 1]) * h_poli)/6
        b.append(b_i)

    a = []
    for i in range(0, n+1):                         # Коэфициенты a возьмем с запасом от ноля
        a.append(y_node[i])

    # Коэффициентов d, b должно быть n (столько же сколько сплайнов, что логично)
    print("d = ", d)
    print("b = ", b)
    print("a = ", a)
    print("x_node = ", x_node)
    print("y_node = ", y_node)
    for i in range(0, n):
        x_line = numpy.linspace(x_node[i], x_node[i + 1], int(quantity_points / n))
        mas1.extend(x_line)
                                                                # Очень вниматошно смотрим на коэффициенты
        S_i = ""                                                # И правильно строим сплайн
        S_i += str(a[i+1]) + " + " + str(b[i]) + "*(" + str(x_node[i+1]) + "-x) + "
        S_i += "1/2 * " + str(c[i+1]) + "*(" + str(x_node[i+1]) + "-x)**2 + "
        S_i += "1/6 * " + str(d[i]) + "*(" + str(x_node[i+1]) + "-x)**3"

        Splain = sympy.poly(S_i)
        print(S_i)
        print(Splain)
        mas2 += [Splain.subs(sympy.Symbol('x'), x_line[i]) for i in range(len(x_line))]

    return mas1, mas2


plt.subplot(121)  # Левое окно для графиков
plt.title('Кубический сплайн', fontsize=14, fontname='Times New Roman')
plt.plot(x, y, color="red", label=str(function))
plt.grid()

x_polinomial_collect = []                                                   # Массивы для построения интерполяции
y_polynomial_collect = []

Splain_3(x_polinomial_collect, y_polynomial_collect)                        # Заполнили

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
