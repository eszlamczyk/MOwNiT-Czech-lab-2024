import numpy as np
from scipy import integrate
from funkcje import *


def simpQuadrature(x, y):
    n = len(x)
    if n < 2 or n % 2 == 0:
        raise ValueError("Musi być nie parzysty input")

    h = x[1] - x[0]
    S = y[0] + y[-1]  # y0 + yn

    for i in range(1, n-1, 2):
        S += 4 * y[i]  # nieparzyste
    for i in range(2, n-1, 2):
        S += 2 * y[i]  # parzyste

    return (h / 3) * S


def test_functions(f, name, lowerLimit, upperLimit, amountPoints=100_001):
    print("============== TEST", name, "==============")
    points = np.linspace(lowerLimit, upperLimit, amountPoints)
    values = []

    for point in points:
        values.append(f(point))

    myRes = simpQuadrature(points, values)
    libRes, _ = integrate.quad(f, lowerLimit, upperLimit)

    print("Mój wynik:", myRes)
    print("Ich wynik:", libRes)
    print("Różnica:", abs(myRes-libRes))
    print("\n\n")


test_functions(f1, "f1", 10, 20)
test_functions(f2, "f2", 5, 10)
test_functions(f3, "f3", -10, -5)
