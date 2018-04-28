import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#figure patterns for standarizing the document
line_width = 2

out_folder = 'figs/'
folder_psim = 'data/psim/'
def plot_simple_turbine():
    plt.figure()
    folder = 'data/simple-turbine/power-x-voltage/'
    for i in range(1,7):
        df = pd.read_csv(folder + str(i) + '.csv')
        df[df < 0]  = 0
        label = str(int(df.head(1)['S2.v_ms'])) + ' m/s'
        plt.plot(df['Vo'], df['Pe'], label = label, linewidth = line_width)

    # fig.suptitle('test title')
    plt.xlabel('Vo [V]')
    plt.ylabel('Po [W]')
    plt.legend(loc="upper left")
    axes = plt.gca()
    axes.set_ylim([0,150])
    plt.savefig(out_folder + 'simple-turbine-power-x-voltage.pdf')

    x = np.arange(0.0, 40.0, 0.1)
    y = 0.006 * (x**3) # equation fitted in matlab by least squares
    plt.plot(x, y, label = 'MPP', linewidth = line_width)
    plt.legend(loc="upper left")
    plt.savefig(out_folder + 'simple-turbine-cubic-fitted.pdf')

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

    plt.savefig(out_folder + 'small-turbine-cp.pdf')


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
    plt.xlabel(r'$\omega [rad/s]$', fontsize=20)
    plt.ylabel(r'$Power [W]$', fontsize=20)
    plt.legend(loc="upper left")
    axes = plt.gca()
    axes.set_ylim([0,1700])
    axes.set_xlim([0,110])
    plt.savefig(out_folder + 'small-turbine-cubic.pdf')

def plot_fitted_turbine():
    #it is the turbine model fitted by least squares
    #cp = -0.0011(lambda + 0.0007 beta**2 - 5.37)e**( 1.36 lambda)
    plt.figure()
    beta = 15
    r = 0.1 #blade radius
    m = 0.5*1.25*3.14*r**2 #1/2 rho pi r^2
    tsr = np.arange(0.0, 6.0, 0.01) #tip speed ratio
    wind_speed_list = [16, 20, 24, 28]
    for v in wind_speed_list:
        # tsr = (w * r)/v
        c_p = -0.0011*(tsr + 0.0007*(beta**2) - 5.37)*np.exp(1.36*tsr)
        c_p[c_p < 0.0] = 0.0
        p = m * c_p * v**3 # mechanical power
        plt.plot(tsr, p, linewidth = line_width, label = 'V = ' + str(v) + 'm/s')
    print 'MPP TSR = ', tsr[p == p.max()]
    plt.xlabel(r'$\lambda$', fontsize=20)
    plt.ylabel(r'$Power [W]$', fontsize=20)
    plt.legend(loc="upper left")
    plt.savefig(out_folder + 'fitted-turbine-lambda-power.pdf')
    plt.figure()
    plt.plot(tsr, c_p, linewidth = line_width, label = r'$\beta = 15^{\circ}$', color = 'black')
    plt.xlabel(r'$\lambda$', fontsize=20)
    plt.ylabel(r'$C_p$', fontsize=20)
    plt.legend(loc="upper left")
    plt.savefig(out_folder + 'fitted-turbine-lambda-cp.pdf')


def plot_fitted_cubic_rpm():
    plt.figure()
    beta = 15
    r = 0.1 #blade radius
    m = 0.5*1.25*3.14*r**2 #1/2 rho pi r^2
    wind_speed_list = [16, 20, 24, 28]
    w = np.arange(0.0, 1500.0, 1)
    for v in wind_speed_list:
        tsr = (w * r)/v
        c_p = -0.0011*(tsr + 0.0007*(beta**2) - 5.37)*np.exp(1.36*tsr)
        c_p[c_p < 0.0] = 0.0
        p = m * c_p * v**3 # mechanical power
        plt.plot(w, p, linewidth = line_width, label = 'V = ' + str(v) + 'm/s')
    y = 0.000000075 * (w**3) # equation fitted in matlab by least squares
    axes = plt.gca()
    axes.set_xlim([0,1500])
    axes.set_ylim([0,200])
    plt.xlabel(r'$\omega [rad/s]$', fontsize=20)
    plt.ylabel(r'$Power [W]$', fontsize=20)
    plt.legend(loc="upper left")
    plt.savefig(out_folder + 'simple-turbine-rotation.pdf')
    plt.plot(w, y, label = 'MPP', linewidth = line_width)
    plt.legend(loc="upper left")
    plt.savefig(out_folder + 'simple-turbine-rotation-cubic.pdf')


def plot_mppt(method, converter, ref, var, ylabel):
    plt.figure()
    df = pd.read_csv(folder_psim + 'mppt-'+method+'-'+converter+'.csv')
    df['Vwind'] = df['Vwind']/3.6
    wind_speed_list = df['Vwind'].unique()
    beta = 15
    r = 0.1 #blade radius
    m = 0.5*1.25*3.14*r**2 #1/2 rho pi r^2
    w = np.arange(0.0, 1500.0, 1)
    df['max_pm'] = 0.0
    for v in wind_speed_list:
        tsr = (w * r)/v
        c_p = -0.0011*(tsr + 0.0007*(beta**2) - 5.37)*np.exp(1.36*tsr)
        c_p[c_p < 0.0] = 0.0
        p = m * c_p * v**3 # mechanical power
        df['max_pm'][df['Vwind'] == v] = p.max() # theoretical maximum power for given wind velocity

    df['max_pe'] = df['max_pm'] * 0.85
    # ax1 = plt.subplot(411)
    # plt.plot(df['Time'], df['Pm'], label = r'$Pm$', linewidth = line_width, color = 'black')
    # plt.plot(df['Time'], df['max_pm'], label = r'$Pm_{max}$', linewidth = line_width, color = 'black', linestyle = '--')
    # plt.ylabel('Mechanical\nPower (W)')#, fontsize=16)
    # plt.legend(loc="best")
    # plt.setp(ax1.get_xticklabels(), visible=False)

    ax1 = plt.subplot(311)
    plt.plot(df['Time'], df['Pout'], label = r'$Pe$', linewidth = line_width, color = 'black')
    plt.plot(df['Time'], df['max_pe'], label = r'$Pe_{max}$', linewidth = line_width, color = 'black', linestyle = '--')
    plt.ylabel('Electrical\nPower [W]')#, fontsize=16)
    plt.legend(loc="best")
    plt.setp(ax1.get_xticklabels(), visible=False)


    ax2 = plt.subplot(312, sharex=ax1)
    plt.plot(df['Time'], df[ref], label = r'$' + var + '$', linewidth = line_width, color = 'black')
    plt.plot(df['Time'], df[ref+'_REF'], label = r'$' + var + r'_{ref}$', linewidth = line_width, color = 'black', linestyle = '--')
    plt.ylabel(ylabel)#, fontsize=16)
    plt.legend(loc="best")
    plt.setp(ax2.get_xticklabels(), visible=False)

    ax3 = plt.subplot(313, sharex=ax1)
    plt.plot(df['Time'], df['Vwind'], label = 'Vwind', linewidth = line_width, color = 'black')
    plt.xlabel('Time [s]', fontsize=20)
    plt.ylabel('Wind speed\n[m/s]')#, fontsize=16)

    axes = plt.gca()
    # axes.set_ylim([20,30])
    axes.set_xlim([0,15])
    plt.savefig(out_folder + 'mppt-'+method+'-'+converter+'-sim.pdf')

def plot_awe_wind():
    plt.figure()
    folder = 'data/matlab/'
    df = pd.read_csv(folder + 'awe_vel.csv')
    df = df[df['time'] < 200]
    ax1 = plt.subplot(211)
    plt.plot(df['time'], df['apparent_wind'], label = 'Apparent wind', linewidth = line_width, color = 'black')
    plt.plot(df['time'], df['airfoil_vel'], label = 'Airfoil speed', linewidth = line_width, color = 'black', linestyle = '--')
    plt.ylabel('[m/s]')#, fontsize=16)
    plt.legend(loc="best")
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax2 = plt.subplot(212, sharex=ax1)
    plt.plot(df['time'], df['cable_length'], label = 'Cable Length', linewidth = line_width, color = 'black')
    plt.ylabel('Cable Lenght [m]')#, fontsize=16)
    # plt.legend(loc="best")
    plt.savefig(out_folder + 'awe-model-wind.pdf')

def plot_open_loop():
    plt.figure()
    df = pd.read_csv(folder_psim + 'open-loop.csv')
    # df = df[df['Time'] < 10]
    ax1 = plt.subplot(411)
    lab = r'Wind speed = ' + str(df['S1.v_ms'].max()) + ' m/s'
    plt.plot(df['Time'], df['Pout'], label = lab, linewidth = line_width, color = 'black')
    plt.ylabel('Output\nPower [W]')#, fontsize=16)
    plt.legend(loc="best")
    ax1.set_ylim([0,df['Pout'].max()*1.1])
    plt.setp(ax1.get_xticklabels(), visible=False)


    ax2 = plt.subplot(412, sharex=ax1)
    plt.plot(df['Time'], df['Vcc'], linewidth = line_width, color = 'black')
    plt.ylabel(r'$Vcc$ [V]')#, fontsize=16)
    ax2.locator_params(which='y', nbins=4)
    plt.setp(ax2.get_xticklabels(), visible=False)

    ax3 = plt.subplot(413, sharex=ax1)
    plt.plot(df['Time'], df['S1.rad_s'], linewidth = line_width, color = 'black')
    plt.ylabel('$\omega$\n[rad/s]')#, fontsize=16)
    ax3.locator_params(which='y', nbins=3, tight=True)
    plt.setp(ax3.get_xticklabels(), visible=False)

    ax4 = plt.subplot(414, sharex=ax1)
    plt.plot(df['Time'], df['D'], linewidth = line_width, color = 'black')
    plt.xlabel('Time [s]', fontsize=20)
    plt.ylabel('Duty cycle')#, fontsize=16)
    plt.yticks(np.arange(0, 1.1, step=0.5))
    axes = plt.gca()
    axes.set_ylim([0,1])
    axes.set_xlim([0,10])
    plt.savefig(out_folder + 'open-loop.pdf')

def plot_efficiency():
    plt.figure()
    df = pd.read_csv(folder_psim + 'gen-efficiency.csv')
    df = df[df['Time'] > 2]
    ax1 = plt.subplot(311)
    lab = r'Wind speed = ' + str(df['S1.v_ms'].max()) + ' m/s'
    plt.plot(df['Time'], df['Pout'], label = 'Pe', linewidth = line_width, color = 'black')
    plt.plot(df['Time'], df['S1.Pm'], label = 'Pm', linewidth = line_width, color = 'black', linestyle = '--')
    plt.ylabel('Output\nPower [W]')#, fontsize=16)
    plt.legend(loc="lower right")
    ax1.set_ylim([0,df['S1.Pm'].max()*1.1])
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax2 = plt.subplot(312, sharex=ax1)
    ef = 100*df['Pout']/df['S1.Pm']
    ef[ef > 100] = 100
    ef[ef < 78] = 78
    plt.plot(df['Time'], ef, linewidth = 1, color = 'black')
    plt.ylabel(r'Efficiency [%]')#, fontsize=16)
    plt.setp(ax2.get_xticklabels(), visible=False)

    ax3 = plt.subplot(313, sharex=ax1)
    plt.plot(df['Time'], df['Vcc'], linewidth = line_width, color = 'black', label = lab)
    plt.ylabel(r'$Vcc$ [V]')#, fontsize=16)
    # ax3.locator_params(which='y', nbins=5)
    ax3.set_ylim([df['Vcc'].min()/1.1,df['Vcc'].max()*1.1])
    plt.legend(loc="lower right")
    plt.xlabel('Time [s]')#, fontsize=20)
    plt.savefig(out_folder + 'gen-efficiency.pdf')

def plot_ripple():
    #plot the NIBB converter voltage and current output plot_ripple
    df_voltage = pd.read_csv(folder_psim + 'ripple_voltage.csv')
    df_current = pd.read_csv(folder_psim + 'ripple_current.csv')
    df_voltage['Time'] = df_voltage['Time'] - 0.1
    df_current['Time'] = df_current['Time'] - 0.1
    current = 'Io'
    print 'Voltage Ripple = ' + str(df_voltage['Vo'].max() - df_voltage['Vo'].min())
    print 'Current Ripple = ' + str(df_current[current].max() - df_current[current].min())
    plt.figure()
    plt.plot(df_voltage['Time']*1000000, df_voltage['Vo'], linewidth = line_width, color = 'black')
    plt.ylabel('Ouput Voltage [V]')#, fontsize=20)
    plt.xlabel(r'Time [$\mu$s]')#, fontsize=20)
    plt.savefig(out_folder + 'ripple_voltage.pdf')
    plt.figure()
    plt.plot(df_current['Time']*1000000, df_current[current], linewidth = line_width, color = 'black')
    plt.ylabel('Ouput Current [A]')#, fontsize=20)
    plt.xlabel(r'Time [$\mu$s]')#, fontsize=20)
    plt.savefig(out_folder + 'ripple_current.pdf')


# plot_simple_turbine()
# plot_complex_turbine()
# plot_complex_cubic()
# plot_fitted_turbine()
# plot_fitted_cubic_rpm()
# plot_mppt('PSF', 'boost', 'IL', 'I', 'Current\n[A]')
# plot_mppt('OTSR', 'boost', 'lambda', '\lambda', 'Tip-Speed\nRatio')
# plot_awe_wind()
# plot_open_loop()
# plot_efficiency()
plot_ripple()
plt.show()
