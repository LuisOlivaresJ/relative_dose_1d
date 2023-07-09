# Getting Started

To run the demo, create a script or start a python interpreter and input:

```python
from relative_dose_1d import GUI_tool
GUI_tool.run_demo()
```

To plot data in form of a numpy array, use [build_from_array_and_step()](Tools_module_label) function:

```python
import relative_dose_1d.GUI_tool as rd

a = np.array([1,2,3,4,5])
b = a + np.random.random_sample((5,))

A = build_from_array_and_step(a, 1)
B = build_from_array_and_step(b, 1)

rd.plot(A,B)
```