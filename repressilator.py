
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import pylab
from matplotlib import pyplot as plt, lines, image
from matplotlib.widgets import Slider, Button, RadioButtons, MultiCursor


from pnsim import Node

# simulaiton aprameters

n = 200


# setup initial variables
x0 = 2
xbeta0, xalpha0 = 0.8, 0.1
kx = 1

y0 = 1
ybeta0, yalpha0 = 0.8, 0.1
ky = 1

z0 = 2
zbeta0, zalpha0 = 0.8, 0.1
kz = 1



def make_logic(beta, alpha, k):
    return lambda x: (beta, alpha) if (x < k) else (0, alpha)

xlogic = make_logic(xbeta0, xalpha0, kx)
ylogic = make_logic(ybeta0, yalpha0, ky)
zlogic = make_logic(zbeta0, zalpha0, kz)

x = Node(xlogic, x0)
y = Node(ylogic, y0)
z = Node(zlogic, z0)


for i in range(n):
    x.update(z.now)
    y.update(x.now)
    z.update(y.now)

times = range(1,len(x)+1)

# figure drawing
fig, ax1 = plt.subplots(1, 1, sharex=True)
plt.subplots_adjust(left=0.25, bottom=0.45)

linesX = ax1.plot(times, x, 'b', label='x')
ax1.set_ylim(0,max(x)*1.1)
ax1.set_ylabel('x, y, or z')

linesY = ax1.plot(times, y, 'r', label='y')
linesZ = ax1.plot(times, z, 'g', label='z')


# interactive controls
axcolor = 'lightgoldenrodyellow'

t_axis = plt.axes([0.25, 0.38, 0.65, 0.03], axisbg=axcolor)

axalpha = plt.axes([0.25, 0.32, 0.65, 0.03], axisbg=axcolor)
axbeta  = plt.axes([0.25, 0.29, 0.65, 0.03], axisbg=axcolor)
axk  = plt.axes([0.25, 0.26, 0.65, 0.03], axisbg=axcolor)

yaxalpha = plt.axes([0.25, 0.20, 0.65, 0.03], axisbg=axcolor)
yaxbeta  = plt.axes([0.25, 0.17, 0.65, 0.03], axisbg=axcolor)
yaxk  = plt.axes([0.25, 0.14, 0.65, 0.03], axisbg=axcolor)

zaxalpha = plt.axes([0.25, 0.08, 0.65, 0.03], axisbg=axcolor)
zaxbeta  = plt.axes([0.25, 0.05, 0.65, 0.03], axisbg=axcolor)
zaxk  = plt.axes([0.25, 0.02, 0.65, 0.03], axisbg=axcolor)


timeSlider = Slider(t_axis, "$t$", 10, 500, valinit=n,valfmt='%1d')

betaSlider = Slider(axbeta, "$\\beta_x$", 0, 2, valinit=xbeta0,valfmt='%1.3f')
alphaSlider = Slider(axalpha, "$\\alpha_x$", 0, 0.5, valinit=xalpha0,valfmt='%1.3f')
kSlider = Slider(axk, "$k_x$", 0, 5, valinit=kx,valfmt='%1.3f')

y_betaSlider = Slider(yaxbeta, "$\\beta_y$", 0, 2, valinit=ybeta0,valfmt='%1.3f')
y_alphaSlider = Slider(yaxalpha, "$\\alpha_y$", 0, 0.5, valinit=yalpha0,valfmt='%1.3f')
y_kSlider = Slider(yaxk, "$k_y$", 0, 5, valinit=ky,valfmt='%1.3f')

z_betaSlider = Slider(zaxbeta, "$\\beta_z$", 0, 2, valinit=zbeta0,valfmt='%1.3f')
z_alphaSlider = Slider(zaxalpha, "$\\alpha_z$", 0, 0.5, valinit=zalpha0,valfmt='%1.3f')
z_kSlider = Slider(zaxk, "$k_z$", 0, 5, valinit=kz,valfmt='%1.3f')



multi = MultiCursor(fig.canvas, [ax1,], color='k', lw=1,linestyle='dashed')

# update the plot as interactive controls
def update(val):
    global x0, y0, z0, ax1

    n = int(timeSlider.val)

    xbeta = betaSlider.val
    xalpha = alphaSlider.val
    kx = kSlider.val

    ybeta = y_betaSlider.val
    yalpha = y_alphaSlider.val
    ky = y_kSlider.val

    zbeta = z_betaSlider.val
    zalpha = z_alphaSlider.val
    kz = z_kSlider.val


    xlogic = make_logic(xbeta, xalpha, kx)
    ylogic = make_logic(ybeta, yalpha, ky)
    zlogic = make_logic(zbeta, zalpha, kz)

    x = Node(xlogic, initval=x0)
    y = Node(ylogic, initval=y0)
    z = Node(zlogic, initval=z0)

    for i in range(n):
        x.update(z.now)
        y.update(x.now)
        z.update(y.now)

    times = range(1,len(x)+1)
    ax1.set_xlim(0,n)

    linesX[0].set_data(times,x)
    linesY[0].set_data(times,y)
    linesZ[0].set_data(times,z)

    #linesX[0].set_ydata(x)
    #linesY[0].set_ydata(y)
    #linesZ[0].set_ydata(z)

    ax1.set_ylim(0, max(0.1, max(max(x),max(y), max(z))*1.1))
    pylab.draw()

timeSlider.on_changed(update)
betaSlider.on_changed(update)
kSlider.on_changed(update)

alphaSlider.on_changed(update)
y_betaSlider.on_changed(update)
y_alphaSlider.on_changed(update)
y_kSlider.on_changed(update)

z_betaSlider.on_changed(update)
z_alphaSlider.on_changed(update)
z_kSlider.on_changed(update)


def draw_network():
    global fig, ax1

    img=image.imread('repress-fig.png')
    height = img.shape[0]
    fig.figimage(img, 10, 10, origin='upper')


draw_network()


pylab.show()

