import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

def SDT_demo():
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.25)
    t = np.arange(-5, 10, 0.001)
    a0 = 3   # distance
    f0 = 1   # noise (std)
    #delta_f = 5.0
    #line = 


    mu, sigma = 0, f0 # mean and standard deviation
    #x1 = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    #x2 = np.linspace(mu+a0 - 3*sigma, mu+a0 + 3*sigma, 100)
    l1, = plt.plot(t, stats.norm.pdf(t, mu, sigma))
    l2, = plt.plot(t, stats.norm.pdf(t, mu+a0, sigma))



    #s = a0*np.sin(2*np.pi*f0*t)
    #l, = plt.plot(t, s, lw=2, color='red')
    #plt.axis([-10, 20, 0, 1])

    axcolor = 'lightgoldenrodyellow'
    axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

    sfreq = Slider(axfreq, 'separation', 0.01, 3, valinit=f0)
    samp = Slider(axamp, 'noise (std)', 0.1, 5, valinit=a0)


    def update(val):
        amp = samp.val
        freq = sfreq.val
        l1.set_ydata(stats.norm.pdf(t, mu, freq))
        l2.set_ydata(stats.norm.pdf(t, mu+amp, freq))

        fig.canvas.draw_idle()
    sfreq.on_changed(update)
    samp.on_changed(update)

    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


    def reset(event):
        sfreq.reset()
        samp.reset()
    button.on_clicked(reset)

    #rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)


    plt.show()