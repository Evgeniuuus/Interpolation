import numpy as numpy  # Для массивов и мат функций
import matplotlib.pyplot as plt  # Для отрисовки графиков
import sympy as sympy
import math

window, figura = plt.subplots()  # Создаем окно для графиков и оси
figura.set_title('Погрешности')
figura.set_xlabel('x')
figura.set_ylabel('y')
figura.set_xlim(0, 12)
figura.set_ylim(-1, 3)
figura.grid()
plt.figure()

a = 1
b = 11
n = 10

x = numpy.linspace(a, b, 1000)  # Заполняем массив
y = numpy.cos(numpy.sin(x) ** 2)  # добавили уравнение
plt.plot(x, y, color="red", label="Исходная функция")  # Смоделировали график

# -----------Это основной график, теперь ищем ---------------------------------------------------------
# ------------ --полином интерполяции------------------------------------------------------------------

x_node = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # точки узлов интерполяции где x
y_node = [math.cos(math.sin(x_node[i]) ** 2) for i in range(len(x_node))]  # точки узлов где y

poly = ""

for i in range(n+1):
    poly += str(y_node[i]) + "*"
    for j in range(n+1):  # Ищем вид полинома по формуле
        if i == j:
            continue
        poly += "(x-" + str(x_node[j]) + ")/"
        poly += "(" + str(x_node[i] - x_node[j]) + ")"
        poly += "*"
    poly = poly[:-1]

    if i != n:
        poly += "+"
polynome = sympy.poly(poly)

# -----------Нашли полином интерполяции ---------------------------------------------------------
# -------подставляем точки и выводим на экран----------------------------------------------------

y_polynomial = [polynome.subs(sympy.Symbol('x'), x[i]) for i in range(len(x))]

plt.plot(x, y_polynomial, '--', color="green", label="Интерполяция")

# --------------Построили интерполяцию ---------------------------------------------------------
# ----------Находим абсолютную погрешность------------------------------------------------------

absolute_error = [math.fabs(y[i] - y_polynomial[i]) for i in range(len(x))]

dif_list = [math.fabs(y[i] - y_polynomial[i]) for i in range(len(y))]
print("Практическая погрешность : ", max(dif_list))  # По формуле это тоже все есть

figura.plot(x, absolute_error, ':', color="magenta", label="абс.Погрешность")

# -----------Построили график абсолютной погрешности ---------------------------------------
# --------------Находим теоретическую погрешность-------------------------------------------
func = "cos(sin(x^2))"
func_diff = sympy.diff(func, sympy.Symbol('x'), n + 1)
func_diff_list = [abs(func_diff.subs(sympy.Symbol('x'), x[i])) for i in range(len(x))]

omega = ""
for i in range(n):
    omega += "(x-" + str(x_node[i]) + ")*"
omega = omega[:-1]

omega_abs = "Abs(" + omega + ")"

theory_error = sympy.poly(str(float(math.fabs(max(func_diff_list))) / float(math.factorial(n + 1))) +
                          "*" + str(sympy.poly(omega)))
y_theory_error = [theory_error.subs(sympy.Symbol('x'), x[i]) for i in range(len(x))]

figura.plot(x, y_theory_error, color="gray", label="теор.погрешность")

print("Теоретическая ошибка:", max(y_theory_error))

# -----------Теперь ищем полином Гаусса и пытаемся вычислить значение функции---------------
print("---------------------- Второе задание ----------------------")

tochka = 2.2           # Не стал писать дополнительную обработку вводить tochka от (0 ; 5)
epsilon = 0.001
h = b - a                                                  # Длина всего интервала

x_j = a
x_j_1 = b

diff_func = "cos(sin(x)**2)"    # Производная на всем промежутке [a;b] (не на кси!) так сказал преподаватель
diff_func = sympy.diff(diff_func, sympy.Symbol('x'), 3)
diff_func_list = [abs(diff_func.subs(sympy.Symbol('x'), x[i])) for i in range(len(x))]
F = max(diff_func_list)             # Наша константа которая будет использоваться при пересчетах

while True:
    h_step = h
    mass = [0]                  # Создаем массив из узловых точек на [a;b] с заданным шагом
    while h_step < b:
        mass.append(h_step)
        h_step += h
    mass.append(h_step)

    min_distance = 11   # Типо берем любое число большее нашего промежутка
    for i in mass:      # Нашли самый ближний узел к заданной точке (tochka)
        distance = abs(i - tochka)
        if distance < min_distance:
            min_distance = distance
            x_j = i

    index_j = mass.index(x_j)               # Извлекаем индекс ближайшего узла
    x_j_1 = mass[mass.index(x_j) - 1]       # Левый узел от ближайшего
    x_j_2 = mass[mass.index(x_j) + 1]       # Правый узел от ближайшего

    t = (tochka - x_j)/(x_j - x_j_1)
    R2_x = F * h**3 * (t * (t**2 - 1))/(math.factorial(3))
    h /= 2

    if abs(R2_x) < epsilon:
        break


print(mass)
x_usli = [x_j_1, x_j, x_j_2]
print("Найденные узлы :", x_usli, "\n")

# ------------------ Все теперь можно считать конечные разности ----------------------------

y_usli = [math.cos(math.sin(x_usli[i]) ** 2) for i in range(len(x_usli))]

y_1 = y_usli[2] - y_usli[1]            # Все по известным формулам
y_2 = y_usli[0] - 2 * y_usli[1] + y_usli[2]

Iskomaya_tochka = y_usli[1] + y_1 * t + y_2 * (t*(t-1))/(math.factorial(2)) + R2_x   # Да-Дань!!!

y_func = math.cos(math.sin(tochka) ** 2)

print("Координаты точки равны :  (", tochka, " ; ", y_func, ")")
print("R2_x = ", R2_x)
print("epsilon = ", epsilon)
print("Координаты искомой точки равны :  (", tochka, " ; ", Iskomaya_tochka, ")")

figura.legend()
plt.legend()  # Отобразить легенду
plt.show()


