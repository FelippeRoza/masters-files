import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#figure patterns for standarizing the document
line_width = 2

out_folder = 'figs/'
def plot_simple_turbine():
    plt.figure()
    folder = 'data/simple-turbine/power-x-voltage/'
    for i in range(1,7):
        df = pd.read_csv(folder + str(i) + '.csv')
        df[df < 0]  = 0
        label = str(int(df.head(1)['S2.v_ms'])) + ' m/s'
        plt.plot(df['Vo'], df['Pe'], label = label, linewidth = line_width)

    # fig.suptitle('test title')
    plt.xlabel('Vo (V)')
    plt.ylabel('Po (W)')
    plt.legend(loc="upper left")
    axes = plt.gca()
    axes.set_ylim([0,150])
    plt.savefig(out_folder + 'simple-turbine-power-x-voltage.eps')

    x = np.arange(0.0, 40.0, 0.1)
    y = 0.0067 * (x**3) # equation fitted in matlab by least squares
    plt.plot(x, y, label = 'MPP')
    plt.legend(loc="upper left")
    plt.savefig(out_folder + 'simple-turbine-cubic-fitted.eps')

def cp(alfa, beta):
    #turbine standard power coeficient
    #alfa is the Tip Speed Ratio and beta is the pitch angle
    alfa_i = (1/(alfa + 0.08*beta)) - 0.035/(beta**3 + 1)
    c1 = 0.5
    c2 = 116*alfa_i
    c3 = 0.4
    c4 = 0
    c5 = 5
    c6 = 21*alfa_i
    x = 1.5
    cp = c1*(c2 - c3*beta - c4*(beta**x) - c5) * np.exp(-c6)
    return cp

def plot_complex_turbine():
    beta = 8
    tsr = np.arange(0.0, 14.0, 0.1)
    c_p = cp(tsr, beta)
    c_p[c_p < 0.0] = 0.0
    plt.figure()
    plt.plot(tsr, c_p, linewidth = line_width, color = 'black', label = 'Pitch = '+str(beta)+'$^{\circ}$')
    plt.xlabel(r'$\lambda$', fontsize=20)
    plt.ylabel(r'$C_p$', fontsize=20)
    plt.legend(loc="upper left")

    plt.savefig(out_folder + 'small-turbine-cp.eps')


def plot_complex_cubic():
    plt.figure()
    beta = 10
    r = 1.5 #blade radius
    m = 0.5*1.25*3.14*r**2 #1/2 rho pi r^2
    wind_speed_list = [6, 8, 10, 12]
    w = np.arange(0.0, 110.0, 0.1)
    temp = 1
    for v in wind_speed_list:
        tsr = (w * r)/v
        c_p = cp(tsr, beta)
        c_p[c_p < 0.0] = 0.0
        p = m * c_p * v**3 # mechanical power
        plt.plot(w, p, linewidth = line_width, label = 'V' + str(temp))
        temp += 1
    y = 0.0075 * (w**3) # equation fitted in matlab by least squares
    plt.plot(w, y, label = 'MPP', linewidth = line_width)
    plt.xlabel(r'$\omega (rad/s)$', fontsize=20)
    plt.ylabel(r'$Power (W)$', fontsize=20)
    plt.legend(loc="upper left")
    axes = plt.gca()
    axes.set_ylim([0,1700])
    axes.set_xlim([0,110])
    plt.savefig(out_folder + 'small-turbine-cubic.eps')

def plot_fitted_turbine():
    #it is the turbine model fitted by least squares
    #cp = -0.0011(lambda + 0.0007 beta**2 - 5.37)e**( 1.36 lambda)
    plt.figure()
    beta = 15
    r = 0.1 #blade radius
    m = 0.5*1.25*3.14*r**2 #1/2 rho pi r^2
    tsr = np.arange(0.0, 6.0, 0.1) #tip speed ratio
    wind_speed_list = [16, 20, 24, 28]
    for v in wind_speed_list:
        # tsr = (w * r)/v
        c_p = -0.0011*(tsr + 0.0007*(beta**2) - 5.37)*np.exp(1.36*tsr)
        c_p[c_p < 0.0] = 0.0
        p = m * c_p * v**3 # mechanical power
        plt.plot(tsr, p, linewidth = line_width, label = 'V = ' + str(v) + 'm/s')
    plt.xlabel(r'$\lambda$', fontsize=20)
    plt.ylabel(r'$Power (W)$', fontsize=20)
    plt.legend(loc="upper left")
    plt.savefig(out_folder + 'fitted-turbine-power.png')
    plt.savefig(out_folder + 'fitted-turbine-power.eps')



#
plot_simple_turbine()
plot_complex_turbine()
plot_complex_cubic()
plot_fitted_turbine()
