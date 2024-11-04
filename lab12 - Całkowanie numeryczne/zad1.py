import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid, trapezoid


def oblicz_droge(predkosci, czasy):
    predkosci = np.array(predkosci) * (1000 / 3600)
    czasy = np.array(czasy)

    droga_cumulative_trapezoid = cumulative_trapezoid(
        predkosci, czasy, initial=0) / 1000

    droga_trapezoid = trapezoid(predkosci, czasy) / 1000

    return droga_cumulative_trapezoid, droga_trapezoid


predkosci = [10, 30, 50, 70, 90]  # prędkości w km/h
czasy = [0, 10, 20, 30, 40]  # czas w sekundach


droga_cumulative_trapezoid, droga_trapezoid = oblicz_droge(predkosci, czasy)


plt.figure(figsize=(12, 6))


plt.subplot(2, 1, 1)
plt.plot(czasy, predkosci, marker='o')
plt.title('Prędkość w funkcji czasu')
plt.xlabel('Czas (s)')
plt.ylabel('Prędkość (km/h)')
plt.grid(True)


plt.subplot(2, 1, 2)
plt.plot(czasy, droga_cumulative_trapezoid, marker='o', color='r')
plt.title('Przebyta droga w funkcji czasu')
plt.xlabel('Czas (s)')
plt.ylabel('Droga (km)')
plt.grid(True)

plt.tight_layout()
plt.show()


print(
    f"Całkowita przebyta droga (metoda trapezów - trapezoid): {droga_trapezoid} km")
