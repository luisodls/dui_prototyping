# developed with strong help from Copilot chat

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

pi = 3.14159235358

# Editable function definition
def f(x):
    return x # This function is used here

# Interval
L = 5.0

# Number of Fourier terms
N = 5


# Compute a0
def integrand_a0(x):
    return f(x)

a0 = (1 / L) * quad(integrand_a0, 0, L)[0]

print("a0 =", a0)

# Compute an and bn
an = []
bn = []

def integrand_an(x, n):
    return f(x) * np.cos(2 * pi * n * x / L)

def integrand_bn(x, n):
    return f(x) * np.sin(2 * pi * n * x / L)

for n in range(1, N + 1):
    an_val = (2 / L) * quad(integrand_an, 0, L, args=(n,))[0]
    bn_val = (2 / L) * quad(integrand_bn, 0, L, args=(n,))[0]
    an.append(an_val)
    bn.append(bn_val)

print("an=\n", an, "\n")
print("bn=\n", bn, "\n")

# Fourier approximation using stored coefficients
def fourier_approx(x):
    sum = a0
    for n in range(1, N + 1):
        sum += an[n-1] * np.cos(2 * pi * n * x / L) + bn[n-1] * np.sin(2 * pi * n * x / L)
    return sum

# Generate x values and compute approximations
x_vals = np.arange(0, L, 0.1)

f_vals = []
for x in x_vals:
    f_vals.append(f(x))

approx_vals = []
for x in x_vals:
    approx_y = fourier_approx(x)
    approx_vals.append(approx_y)
    print("x =", x,"f_approx =", approx_y)

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

