import numpy as np


def f1(x):
    return (np.e ** -(x ** 2)) * (np.log(x) ** 2)


def f2(x):
    return 1 / (x ** 3 - 2 * x - 5)


def f3(x):
    return x ** 5 * np.e ** -x * np.sin(x)


def f4(x, y):
    return 1 / (np.sqrt(x + y) * (1 + x + y))


def f5(x, y):
    return x ** 2 + y ** 2
