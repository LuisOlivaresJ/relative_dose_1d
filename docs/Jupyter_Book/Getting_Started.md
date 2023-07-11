# Getting Started

## Demo
To run the demo, create a script or start a python interpreter and input:

```python
from relative_dose_1d import GUI_tool
GUI_tool.run_demo()
```
## Numpy array
To plot data in form of numpy array

```python
import numpy as np
from scipy.stats import norm
from relative_dose_1d.GUI_tool import plot

# Profile positions from [-50 to 49), with 50 points.
x = np.linspace(-50, 50, 50)

# Normalized normal distribution
y = norm.pdf(x, loc = 0, scale = 15)
y = 100 * y / np.max(y)

# Define uniform random error [-4, 4)
error = 8 * np.random.random(50) - 4
y_error = y + error

p_ref = np.stack((x,y), axis = -1)
p_eval = np.stack((x,y_error), axis = -1)

plot(p_ref, p_eval)
```