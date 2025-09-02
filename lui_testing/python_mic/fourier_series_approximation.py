# developed with strong help from Copilot chat

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Editable function definition
def f(x):
    return x # This function is used here

# Interval
L = np.pi

# Number of Fourier terms
N = 5

# Compute a0
def integrand_a0(x):
    return f(x)

a0 = (1 / (2 * L)) * quad(integrand_a0, -L, L)[0]

# Compute an and bn
an = []
bn = []

def integrand_an(x, n):
    return f(x) * np.cos(n * x)

def integrand_bn(x, n):
    return f(x) * np.sin(n * x)

for n in range(1, N + 1):
    an_val = (1 / L) * quad(integrand_an, -L, L, args=(n,))[0]
    bn_val = (1 / L) * quad(integrand_bn, -L, L, args=(n,))[0]
    an.append(an_val)
    bn.append(bn_val)

# Fourier approximation using stored coefficients
def fourier_approx(x):
    sum = a0
    for n in range(1, N + 1):
        sum += an[n-1] * np.cos(n * x) + bn[n-1] * np.sin(n * x)
    return sum

# Generate x values and compute approximations
x_vals = np.arange(-L, L, 0.1)
f_vals = [f(x) for x in x_vals]
approx_vals = [fourier_approx(x) for x in x_vals]

# Plotting
plt.plot(x_vals, f_vals, label='Original Function', color='blue')
plt.plot(x_vals, approx_vals, label='Fourier Approximation', color='red', linestyle='--')
plt.title('Fourier Series Approximation')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)
plt.savefig("fourier_approximation.png")
plt.show()
