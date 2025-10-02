def compute_average(numbers):
    return sum(numbers) / len(numbers)

# Exemple d'utilisation
nums = [12, 45, 67, 23, 89]
print("Exercise 1 - Average:", compute_average(nums))


# -------------------
# Exercise 2: Simulate two dice rolls 1000 times and plot the histogram of sums
# -------------------
import random
import matplotlib.pyplot as plt

sums = [random.randint(1, 6) + random.randint(1, 6) for _ in range(1000)]
plt.hist(sums, bins=range(2, 14), edgecolor='black', align='left')
plt.title('Exercise 2 - Dice Roll Sums')
plt.xlabel('Sum')
plt.ylabel('Frequency')
plt.show()


# -------------------
# Exercise 3: Solve a system of linear equations using numpy
# -------------------
import numpy as np

A = np.array([[2, -1], [1, 3]])
B = np.array([3, 7])
X = np.linalg.solve(A, B)
print("Exercise 3 - Solution of AX=B:", X)


# -------------------
# Exercise 4: Euler's method for solving dy/dx = f(x, y)
# -------------------
def euler(f, x0, y0, h, n):
    x = x0
    y = y0
    for _ in range(n):
        y = y + h * f(x, y)
        x = x + h
    return y

# dy/dx = x + y, y(0) = 1
print("Exercise 4 - Euler method:", euler(lambda x, y: x + y, 0, 1, 0.1, 10))


# -------------------
# Exercise 5: Compute derivative and integral using sympy
# -------------------
import sympy as sp

x = sp.symbols('x')
f = sp.sin(x) * sp.exp(x)
derivative = sp.diff(f, x)
integral = sp.integrate(f, x)
print("Exercise 5 - Derivative:", derivative)
print("Exercise 5 - Integral:", integral)


# -------------------
# Exercise 6: Descriptive statistics on random data
# -------------------
data = np.random.normal(loc=50, scale=10, size=1000)
mean = np.mean(data)
std = np.std(data)
median = np.median(data)
print("Exercise 6 - Mean:", mean)
print("Exercise 6 - Std Dev:", std)
print("Exercise 6 - Median:", median)


# -------------------
# Exercise 7: Read and analyze data from CSV
# -------------------
import csv

# Création d'un fichier temporaire de test
with open('test_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Score'])
    writer.writerow(['Alice', 88])
    writer.writerow(['Bob', 92])
    writer.writerow(['Charlie', 79])

# Lecture et analyse
scores = []
with open('test_data.csv', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        scores.append(int(row['Score']))

print("Exercise 7 - CSV Average:", compute_average(scores))


# -------------------
# Exercise 8: Plot a mathematical function
# -------------------
x_vals = np.linspace(-10, 10, 400)
y_vals = np.sin(x_vals) / x_vals
plt.plot(x_vals, y_vals)
plt.title("Exercise 8 - sin(x)/x Function")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.show()
