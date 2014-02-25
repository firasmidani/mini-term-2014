
import platform
import numpy as np

import matplotlib
if 'Darwin' in platform.platform():  # on OSX
    matplotlib.use('TkAgg')
import pylab
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, MultiCursor

from pnsim import pulse, Node

# time variable
t = range(1, 201)

# node properties
yinit = 0
beta0, beta1, alpha = 0.2, 0.2, 0.15
kx = 0.5
ky = 0.4

def autoreg_logic(y, beta0, beta1, alpha, Kx, Ky):
    if y < Ky:
        return (beta0, alpha)
    else:
        return (beta1, alpha)


pulseon = 25
pulseoff = 100
totaltime = 250

x = pulse(pulseon, pulseoff, totaltime, 1)
t = range(totaltime)

y = Node(autoreg_logic, initval=yinit)
y.append(y.now)

[y.update(y.now, beta0, beta1, alpha, kx, ky) for i in t]

t = range(len(y))

# figure drawing
fig, ax1 = plt.subplots(1, 1, sharex=True)
plt.subplots_adjust(left=0.25, bottom=0.35)
lines, = ax1.plot(t, y)
ax1.set_xlabel('Time')
ax1.set_ylabel('Conc. of gene y')
ax1.set_ylim(0,max(y)*1.1)
ax1.set_xlim(-10, 100)

#textLabel = plt.text(0.75*max(t), 0.15*max(y), "max(y)=%0.2f" % (beta0/alpha0))

# interactive controls
axcolor = 'lightgoldenrodyellow'
axalpha = plt.axes([0.25, 0.05, 0.65, 0.03], axisbg=axcolor)
axbeta1 = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
axbeta0  = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)
kaxis  = plt.axes([0.25, 0.2, 0.65, 0.03], axisbg=axcolor)

kSlider =     Slider(kaxis, "$K_y$", 0, 1, valinit=ky, valfmt='%1.3f')
beta0Slider = Slider(axbeta0, "$\\beta_0$", 0, 0.5, valinit=beta0,valfmt='%1.3f')
beta1Slider = Slider(axbeta1, "$\\beta_1$", 0, 0.5, valinit=beta1,valfmt='%1.3f')
alphaSlider = Slider(axalpha, "$\\alpha$", 0, 0.5, valinit=alpha,valfmt='%1.3f')

multi = MultiCursor(fig.canvas, [ax1,], color='k', lw=1,linestyle='dashed')

# update the plot as interactive controls
def update(val):
    global t
    beta0 = beta0Slider.val
    beta1 = beta1Slider.val
    alpha = alphaSlider.val
    ky = kSlider.val

    y.reset(yinit)
    y.append(y.now)
    [y.update(y.now, beta0, beta1, alpha, kx, ky) for i in t]
    t = range(len(y))

    lines.set_data(t, y)
    ax1.set_ylim(0, max(0.1, max(y)*1.1))


    pylab.draw()

kSlider.on_changed(update)
beta0Slider.on_changed(update)
beta1Slider.on_changed(update)
alphaSlider.on_changed(update)


# show the plot
pylab.show()

