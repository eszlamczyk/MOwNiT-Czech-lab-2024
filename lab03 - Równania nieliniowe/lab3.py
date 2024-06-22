import math
import numpy as np
import time

def f1(x):
  if x > 2*math.pi or x < 3*math.pi/2:
    return "itsover"
  return (math.cos(x)*math.cosh(x)) - 1

def f1prime(x):
  return math.cos(x)*math.sinh(x) -math.sin(x)*math.cosh(x)

def f2(x):
  if x > math.pi/2 or x < 0:
    return float('-inf')
  return (1/x - math.tan(x))

def f2prime(x):
    if x == 0:
        return float('-inf')
    if x <= math.pi / 2 and x > 0:
        return -1 / (x ** 2) - 1 / (math.cos(x) ** 2)
    else:
        return None


def f3(x):
  if x > 3 or x < 1:
    return "itsover"
  return 2**(-x) + (math.e)**x + 2*math.cos(x) - 6

def f3prime(x):
    if x <= 3 and x >= 1:
        return math.e ** x - (2 ** -x) * math.log(2) - 2 * math.sin(x)
    else:
        return None




def bisection(precision,a,b,epsilon,function):
  if function(a) > 0  and function(b) < 0:
    z = -1
  elif function(a) < 0  and function(b) > 0:
    z = 1
  else:
    return None
  mid = a + (b-a)/2  
  iterations = 0
  while abs(function(mid)) > epsilon:
    #print(iterations)
    mid = a + (b-a)/2
    if function(mid) * z < 0:
      a = mid
    else: 
      b = mid
    iterations += 1

  return mid, iterations

print("BISECTION")
print(bisection(1,3*math.pi/2,2*math.pi,1e-12,f1))
print(bisection(1,1e-12,math.pi/2,1e-12,f2))
print(bisection(1,1,3,1e-12,f3))

def netwonMethod(b,epsilon:float,function,functionPrime,iterLimit:int):
  x = b
  for i in range(iterLimit):
     if function(x) < epsilon:
        return x, i
     x = x - function(x)/functionPrime(x)


print("\nNETWON")
print(netwonMethod(2*math.pi,1e-12,f1,f1prime,10**6))
print(netwonMethod(0.001,1e-12,f2,f2prime,10**6))
print(netwonMethod(2,1e-12,f3,f3prime,10**6))

def siecz(a,b,eps,function):
    i = 0
    x = a
    x1 = b
    while True:
        i += 1
        if abs(function(x)) < eps or (function(x1) - function(x)) == 0:
            return x, i
        temp = (function(x1) * x - function(x) * x1) / (function(x1) - function(x))
        x = x1
        x1 = temp


print("\nSIECZNYCH")
print(siecz(0.001+3*math.pi/2,2*math.pi,1e-12,f1))
print(siecz(1/2,1,1e-12,f2))
print(siecz(1.1,2.9,1e-12,f3))