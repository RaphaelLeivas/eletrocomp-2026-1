import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Or 'Qt5Agg', 'QtAgg', or 'WebAgg'
import matplotlib.pyplot as plt

# Generate data
x = np.linspace(0, 2*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

# Print some values (test NumPy)
print("First 5 x values:", x[:5])
print("First 5 sin(x):", y_sin[:5])

# Plot
plt.figure()
plt.plot(x, y_sin, label="sin(x)")
plt.plot(x, y_cos, label="cos(x)")

plt.title("NumPy + Matplotlib Test")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()

# Show plot
plt.show()