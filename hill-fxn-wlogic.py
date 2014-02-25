import platform

import matplotlib
if 'Darwin' in platform.platform():  # on OSX
    matplotlib.use('TkAgg')
import numpy as np

import pylab
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, MultiCursor


def hillfxn(x, B, K, n):
    xn = float(x**n)
    return (B * xn)/(K**n + xn)

def logic_approx(x, B, K):
    if x > K:
        return B
    else:
        return 0


# time variable
Xrange= np.linspace(0,30,250)

# initial settings
B = 5
K = 5
n = 1
showlogic = False

y = [hillfxn(i, B, K, n) for i in Xrange]
ylogic = [logic_approx(i, B, K) for i in Xrange]


# figure drawing
fig, ax1 = plt.subplots(1, 1, sharex=True)
plt.subplots_adjust(left=0.35, bottom=0.25)
lines = ax1.plot(Xrange, y)
ax1.set_xlabel('Activator concentration (X)')
ax1.set_ylabel('Promoter activity')
ax1.set_ylim(0,max(ylogic)*1.1)

logicplot = ax1.plot(Xrange, ylogic, color='red', visible=False)

# interactive controls
axcolor = 'lightgoldenrodyellow'

axK = plt.axes([0.25, 0.05, 0.65, 0.03], axisbg=axcolor)
axB  = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
axN  = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)

Nslider = Slider(axN, "$n$", 1, 10, valinit=n, valfmt='%1.3f')
Bslider = Slider(axB, "$\\beta$", 0, 20, valinit=B, valfmt='%1.3f')
Kslider = Slider(axK, "$K$", 0.01, 20, valinit=K, valfmt='%1.3f')   

multi = MultiCursor(fig.canvas, [ax1,], color='k', lw=1,linestyle='dashed')


# Draw formula in upper left corner
bbX = ax1.get_position()
fig.text(0.015, bbX.y0+0.5, 
         "Hill Equation:\n\n  $f(X) = \\frac{\\beta X^n}{K^n + X^n}$",
         fontsize=18)

# Draw logic-fxn radio box
rax = plt.axes([0.05, bbX.y0, 0.15, 0.15], axisbg=axcolor)
fig.text(0.015, bbX.y0+0.16, "Logic Approximation")
radio = RadioButtons(rax, ('Off', 'On'), active=0)


# update the plot as interactive controls
def update(val):
    global showlogic
    n = Nslider.val
    B = Bslider.val
    K = Kslider.val

    y = [hillfxn(i, B, K, n) for i in Xrange]    
    ylogic = [logic_approx(i, B, K) for i in Xrange]

    lines[0].set_ydata(y)
    logicplot[0].set_ydata(ylogic)
    ax1.set_ylim(0, max(0.1, max(ylogic)*1.1))

    if showlogic:
        logicplot[0].set_visible(True)
    else:
        logicplot[0].set_visible(False)

    pylab.draw()


def update_logic(label):
    global showlogic
    if label == 'On':
        showlogic = True
    else:
        showlogic = False
    update(None)

# register slider changes      
Nslider.on_changed(update)
Bslider.on_changed(update)
Kslider.on_changed(update)
radio.on_clicked(update_logic)


# show the plot
pylab.show()

