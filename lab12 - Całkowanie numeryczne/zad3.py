import numpy as np
from funkcje import *
from scipy.integrate import dblquad

print("Wartość podanej całki f4:", dblquad(
    f4, 0, 1, lambda x: 0, lambda x: 1-x)[0], "\n\n")
# wolfram nie liczy :c


x_min, x_max = -3, 3
y_min, y_max = -5, 5


def trapezoidal_double_integral(f, x_min, x_max, y_min, y_max, nx, ny):
    x = np.linspace(x_min, x_max, nx)
    y = np.linspace(y_min, y_max, ny)
    dx = (x_max - x_min) / (nx - 1)
    dy = (y_max - y_min) / (ny - 1)
    integral = 0.0

    for i in range(nx):
        for j in range(ny):
            weight = 1
            if i == 0 or i == nx - 1:
                weight /= 2
            if j == 0 or j == ny - 1:
                weight /= 2
            integral += weight * f(x[i], y[j])

    integral *= dx * dy
    return integral


grid_sizes = [10, 20, 50, 100, 1000]
results = [trapezoidal_double_integral(
    f5, x_min, x_max, y_min, y_max, n, n) for n in grid_sizes]

y = dblquad(f5, x_min, x_max, lambda x: y_min, lambda x: y_max)[0]

for i in range(len(grid_sizes)):
    print("Rozmiar siatki: ", grid_sizes[i], ", wynik: ", results[i], sep="")

print("Wynik biblioteczny:", y)
