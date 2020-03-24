import matplotlib 
import numpy as np
import matplotlib.pyplot as plt

base=10 # параметр, может принимать любые целые значения > 1

def exact_sum(K):
    """Точное значение суммы всех элементов."""
    return 1.

def samples(K):
    """"Элементы выборки"."""
    # создаем K частей из base^k одинаковых значений
    parts=[np.full((base**k,), float(base)**(-k)/K) for k in range(0, K)] 
    # создаем выборку объединяя части
    samples=np.concatenate(parts) 
    # перемешиваем элементы выборки и возвращаем
    return np.random.permutation(samples)

def direct_sum(x):
    """Последовательная сумма всех элементов вектора x"""
    s=0.
    for e in x: 
        s+=e
    return s

def number_of_samples(K):
    """Число элементов в выборке"""
    return np.sum([base**k for k in range(0, K)])

def exact_mean(K):
    """Значение среднего арифметического по выборке с близкой к машинной точностью."""
    return 1./number_of_samples(K)

def exact_variance(K):
    """Значение оценки дисперсии с близкой к машинной точностью."""
    # разные значения элементов выборки
    values=np.asarray([float(base)**(-k)/K for k in range(0, K)], dtype=np.double)
    # сколько раз значение встречается в выборке
    count=np.asarray([base**k for k in range(0, K)])
    return np.sum(count*(values-exact_mean(K))**2)/number_of_samples(K)

K=7 # число слагаемых
x=samples(K) # сохраняем выборку в массив
print(x)
print("Число элементов:", len(x))
print("Самое маленькое и большое значения:", np.min(x), np.max(x))

exact_sum_for_x=exact_sum(K) # значение суммы с близкой к машинной погрешностью
direct_sum_for_x=direct_sum(x) # сумма всех элементов по порядку

def relative_error(x0, x):
    """Погрешность x при точном значении x0"""
    return np.abs(x0-x)/np.abs(x)

print("Погрешность прямого суммирования:", relative_error(exact_sum_for_x, direct_sum_for_x))

sorted_x=x[np.argsort(x)]
sorted_sum_for_x=direct_sum(sorted_x)
print("Погрешность суммирования по возрастанию:", relative_error(exact_sum_for_x, sorted_sum_for_x))

sorted_x=x[np.argsort(x)[::-1]]
sorted_sum_for_x=direct_sum(sorted_x)
print("Погрешность суммирования по убыванию:", relative_error(exact_sum_for_x, sorted_sum_for_x))

def Kahan_sum(x):
    s=0.0 # частичная сумма
    c=0.0 # сумма погрешностей
    for i in x:
        y=i-c      # первоначально y равно следующему элементу последовательности
        t=s+y      # сумма s может быть велика, поэтому младшие биты y будут потеряны
        c=(t-s)-y  # (t-s) отбрасывает старшие биты, вычитание y восстанавливает младшие биты
        s=t        # новое значение старших битов суммы
    return s

Kahan_sum_for_x=Kahan_sum(x) # сумма всех элементов по порядку
print("Погрешность суммирования по Кэхэну:", relative_error(exact_sum_for_x, Kahan_sum_for_x))

# параметры выборки
mean=1e6 # среднее
delta=1e-5 # величина отклонения от среднего

def samples(N_over_two):
    """Генерирует выборку из 2*N_over_two значений с данным средним и среднеквадратическим 
    отклонением."""
    x=np.full((2*N_over_two,), mean, dtype=np.double)
    x[:N_over_two]+=delta
    x[N_over_two:]-=delta
    return np.random.permutation(x)

def exact_mean():
    """Значение среднего арифметического по выборке с близкой к машинной точностью."""
    return mean

def exact_variance():
    """Значение оценки дисперсии с близкой к машинной точностью."""
    return delta**2

x=samples(1000000)

print("Размер выборки:", len(x))
print("Среднее значение:", exact_mean())
print("Оценка дисперсии:", exact_variance())
print("Ошибка среднего для встроенной функции:",relative_error(exact_mean(),np.mean(x)))
print("Ошибка дисперсии для встроенной функции:",relative_error(exact_variance(),np.var(x)))

def direct_mean(x):
    """Среднее через последовательное суммирование."""
    return direct_sum(x)/len(x)

print("Ошибка среднего для последовательного суммирования:",relative_error(exact_mean(),direct_mean(x)))

def direct_second_var(x):
    """Вторая оценка дисперсии через последовательное суммирование."""
    return direct_mean(x**2)-direct_mean(x)**2

def online_second_var(x):
    """Вторая оценка дисперсии через один проход по выборке"""
    m=x[0] # накопленное среднее 
    m2=x[0]**2 # накопленное среднее квадратов
    for n in range(1,len(x)):
        m=(m*(n-1)+x[n])/n
        m2=(m2*(n-1)+x[n]**2)/n
    return m2-m**2

print("Ошибка второй оценки дисперсии для последовательного суммирования:",relative_error(exact_variance(),direct_second_var(x)))
print("Ошибка второй оценки дисперсии для однопроходного суммирования:",relative_error(exact_variance(),online_second_var(x)))

def direct_first_var(x):
    """Первая оценка дисперсии через последовательное суммирование."""
    return direct_mean((x-direct_mean(x))**2)

print("Ошибка первой оценки дисперсии для последовательного суммирования:",relative_error(exact_variance(),direct_first_var(x)))

def exact_sum_sin_x(n):
    ctg = 1.0 / np.tan(0.5)
    return 0.5 * (np.sin(n) - ctg * np.cos(n) + ctg)

def relative_error(x0, x):
    """Погрешность x при точном значении x0"""
    return np.abs(x0-x)/np.abs(x)

n = 10 ** 5
sin_x = np.sin([i + 1 for i in range(n)])
direct_sum_sin_x = direct_sum(sin_x)
print("Погрешность чисел разных знаков:", relative_error(exact_sum_sin_x(n), direct_sum_sin_x))


sorted_sin_x = sin_x[np.argsort(sin_x)]
direct_sorted_sum_sin_x = direct_sum(sorted_sin_x)
print("Погрешность чисел разных знаков по позрастанию:",
      relative_error(exact_sum_sin_x(n), direct_sorted_sum_sin_x))

sorted_abs_sin_x = sorted(sin_x, key=abs)
direct_sorted_abs_sum_sin_x = direct_sum(sorted_abs_sin_x)
print("Погрешность чисел разных знаков по позрастанию абсолютной величины:",
          relative_error(exact_sum_sin_x(n), direct_sorted_abs_sum_sin_x))

def Dnp1(sum_, n, x, Dn):
    a = n/(n+1) * Dn + n/((n+1)*(n+1)) * (x - sum_/n)
    return a
