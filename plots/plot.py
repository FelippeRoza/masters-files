import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

out_folder = 'figs/'
def plot_simple_turbine():
    folder = 'data/simple-turbine/power-x-voltage/'
    for i in range(1,7):
        df = pd.read_csv(folder + str(i) + '.csv')
        df[df < 0]  = 0
        label = str(int(df.head(1)['S2.v_ms'])) + ' m/s'
        plt.plot(df['Vo'], df['Pe'], label = label, linewidth=2)

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


plot_simple_turbine()
