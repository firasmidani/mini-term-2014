import platform

import matplotlib
if 'Darwin' in platform.platform():  # on OSX
    matplotlib.use('TkAgg')

import pylab
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, MultiCursor

from pnsim import Node, pulse


# Equation
eqnstr = r'''$\frac{dY}{dt} = \beta - \alpha Y$'''

# time variable
t = range(1,201)

# node properties
yinit = 0
beta0, alpha0 = 0.2, 0.04
ylogic = lambda t: (beta0, alpha0) 
y = Node(ylogic, initval=yinit)
y.evaluate(t)


# figure drawing
fig, ax1 = plt.subplots(1, 1, sharex=True)
plt.subplots_adjust(left=0.30, bottom=0.30)
lines = ax1.plot(t, y)
ax1.set_xlabel('Time')
ax1.set_ylabel('Conc. of Y')
ax1.set_ylim(0,max(y)*1.1)

textLabel = plt.text(0.75*max(t), 0.15*max(y), "$Y_{st}$=%0.2f" % (beta0/alpha0))

# interactive controls
axcolor = 'lightgoldenrodyellow'

t_axis = plt.axes([0.25, 0.18, 0.65, 0.03], axisbg=axcolor)
axbeta  = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
axalpha = plt.axes([0.25, 0.05, 0.65, 0.03], axisbg=axcolor)


timeSlider = Slider(t_axis, "$t_{max}$", 10, 500, valinit=max(t),valfmt='%1d')

betaSlider = Slider(axbeta, "$\\beta$", 0, 0.5, valinit=beta0,valfmt='%1.3f')
alphaSlider = Slider(axalpha, "$\\alpha$", 0.001, 0.5, valinit=alpha0,valfmt='%1.3f')   
multi = MultiCursor(fig.canvas, [ax1,], color='k', lw=1,linestyle='dashed')


# Draw formula in upper left corner
bbX = ax1.get_position()
fig.text(0.025, bbX.y0+0.5, 
         "Equation:\n\n  %s" % eqnstr,
         fontsize=18)



# update the plot as interactive controls
def update(val):
    n = int(timeSlider.val)
    beta = betaSlider.val
    alpha = alphaSlider.val
    ylogic = lambda t: (beta, alpha)
    y = Node(ylogic, initval=yinit)

    times = range(1,n+1)
    ax1.set_xlim(0,n)
    y.evaluate(times)

    lines[0].set_data(times,y)
    ax1.set_ylim(0, max(0.1, max(y)*1.1))

    if alpha != 0:
        textLabel.set_text("$Y_{st}$=%0.2f" % (beta/alpha))
    else:
        textLabel.set_text("max(y)=Infinity")
    textLabel.set_position((0.75*max(times), max(0.01, 0.15*max(y))))
    pylab.draw()

# register slider changes     
timeSlider.on_changed(update) 
betaSlider.on_changed(update)
alphaSlider.on_changed(update)

# show the plot
pylab.show()

