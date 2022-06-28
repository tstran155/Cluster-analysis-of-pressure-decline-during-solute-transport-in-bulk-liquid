from scipy import optimize
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
import numpy.polynomial.polynomial as npoly
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
path=('/content/Times_New_Roman.ttf')
fontprop = fm.FontProperties(fname=path)

%matplotlib inline
data = pd.read_csv('/content/EXP1_C1SK_noP_bar.csv').values
x = data[0:200,0]
y= data[0:200,1]
plt.scatter(x, y, marker='o', c='white', edgecolors='blue', s=18)
%config InlineBackend.figure_format = 'svg'

def f(breakpoints, x, y, fcache):
    breakpoints = tuple(map(int, sorted(breakpoints)))
    if breakpoints not in fcache:
        total_error = 0
        for f, xi, yi in find_best_piecewise_polynomial(breakpoints, x, y):
            total_error += ((f(xi) - yi)**2).sum()
        fcache[breakpoints] = total_error
    # print('{} --> {}'.format(breakpoints, fcache[breakpoints]))
    return fcache[breakpoints]

def find_best_piecewise_polynomial(breakpoints, x, y):
    breakpoints = tuple(map(int, sorted(breakpoints)))
    xs = np.split(x, breakpoints)
    ys = np.split(y, breakpoints)
    result = []
    for xi, yi in zip(xs, ys):
        if len(xi) < 2: continue
        coefs = npoly.polyfit(xi, yi, 1)
        f = npoly.Polynomial(coefs)
        result.append([f, xi, yi])
    return result

num_breakpoints = 2
breakpoints = optimize.brute(f, [slice(1, len(x), 1)]*num_breakpoints, args=(x, y, {}), finish=None)

plt.scatter(x, y, marker='o', c='white', edgecolors='blue', s=18)
for f, xi, yi, in find_best_piecewise_polynomial(breakpoints, x, y):
    x_interval = np.array([xi.min(), xi.max()])
    linreg = linregress(y[0:xi.size], f(xi))
    print('y = {:35s}, if x in [{}, {}]'.format(str(f), *x_interval))
    plt.plot(x_interval, f(x_interval), 'r-', linewidth=2)
    #plt.xlim(0, 175)
    plt.ylim(133, 139)
    plt.xlabel('Time (hours)', fontproperties=fontprop, fontsize =18)
    plt.ylabel('Pressure (bar)', fontproperties=fontprop, fontsize=18)
    #plt.xticks(np.arange(0, 175, step=25), fontsize=16)
    plt.xticks(fontproperties=fontprop, fontsize=18)
    plt.yticks(fontproperties=fontprop, fontsize=18)
    #plt.text((xi.min()+xi.max())/2+1,(yi.min()+yi.max())/2+0.15, '$R^{2}$=%0.2f,' % linreg.rvalue, fontproperties=fontprop, fontsize =16)
    plt.text((xi.min()+xi.max())/2+1,(yi.min()+yi.max())/2+0.2, 'S=%0.2f' % linreg.slope,  fontproperties=fontprop, fontsize =16)


