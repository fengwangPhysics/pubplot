# pubplot

`pubplot` is a `python` module for making publication-quality figures with `matplotlib`.

## Install
```
python setup.py install --prefix=${HOME}/.local/
```
Make sure `${HOME}/.local/` is in your `PYTHONPATH`.

## Usage

Here we illustrate how to use those functions in `pubplot`.

```python
import matplotlib.pyplot as plt
import pubplot as pplt
%matplotlib inline

import numpy as np
```

```python
fig = pplt.figure(H=0.35, facecolor='w')

# add two panels
fig.axes(0.1, 0., 0.4, 0.25)
fig.axes(0.6, 0., 0.4, 0.25)

# to access the panels
axs = fig.axesList

# add data to plot
ax = axs[0]
x = np.linspace(0, 10, 100)
ax.plot(x, x*x, label=r'$x^2$')
ax.plot(x, x*x*np.sqrt(x), label=r'$x^{2.5}$')
# put labels in the line
pplt.labelLines(ax, align=False, xvals=[8, 8])

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_yticks([0,100,200,300])

# change the label position
ax.xaxis.set_label_coords(0.5, -0.15)
ax.yaxis.set_label_coords( -0.19, 0.5)

ax = axs[1]
ax.plot(x, np.sin(x))
ax.set_xlabel('x')
ax.set_ylabel('wave')
ax.set_ylim(-2,2)
ax.set_yticks([-2, -1, 0, 1, 2])

# change the label position
ax.xaxis.set_label_coords(0.5, -0.15)
ax.yaxis.set_label_coords(-0.1, 0.5)

# add panel lables using default (PRL) style
fig.PanelLabel(pos=[(0.18, 0.97)])

# adjust the position of xy tick label in (b)
pplt.alignEndTickLabel(axs[1], which='x')
pplt.alignEndTickLabel(axs[1], which='y')

plt.savefig('example.pdf')
```

Check the generated pdf file, one can check the figure layout.
