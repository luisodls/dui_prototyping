from scipy import integrate
y = lambda x: 1 if x<=0 else 0

print("y =", y)

print(integrate.quad(y, -1, 1))
#(1.0, 1.1102230246251565e-14)
print(integrate.quad(y, -1, 100))
#(1.0000000002199108, 1.0189464580163188e-08)
print(integrate.quad(y, -1, 10000))
#(0.0, 0.0)
