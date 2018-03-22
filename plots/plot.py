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
    plt.savefig(out_folder + 'simple-turbine-power-x-voltage.png')

    x = np.arange(0.0, 40.0, 0.1)
    y = 0.0067 * (x**3) # equation fitted in matlab by least squares
    plt.plot(x, y, label = 'MPP')
    plt.legend(loc="upper left")
    plt.savefig(out_folder + 'simple-turbine-cubic-fitted.png')

def cp(alfa, beta):
    #turbine power coeficient
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
    plt.plot(tsr, c_p, linewidth = line_width, color = 'black')
    plt.xlabel(r'$\lambda$', fontsize=20)
    plt.ylabel(r'$C_p$', fontsize=20)
    # plt.legend(loc="upper left")

    plt.savefig(out_folder + 'small-turbine-cp.png')


plot_simple_turbine()
plot_complex_turbine()
