import pandas as pd
from pylab import *
import re

folder_name = 'test_2017_12_06/'
# file_name_list = ['24v_pitch05_v', '24v_pitch15_v', '24v_pitch25_v', '24v_pitch35_v']
file_name_list =  ['vazio_pitch05_v', 'vazio_pitch15_v', 'vazio_pitch25_v', 'vazio_pitch35_v']

def convert_voltage(series):
    return series*5*110/(1024*10)

def convert_current(series):
    return series/260

def plot_wind(files_list):
    ax = {}
    fig = {}
    print 'frango'
    fig = plt.figure()

    for file_name in files_list:
        last_time = 0.0
        df = pd.DataFrame()

        for i in range(1, 5):
            filename = folder_name+file_name+str(i)+'.txt'
            if df.empty:
                df = pd.read_csv(filename, sep = '\t', skiprows = 1, header = None)
                df.columns = ['v1', 'i1', 'v2', 'i2', 'v3', 'i3', 'rpm', 'windspeed', 'time']
                df = df[df['time'] < 20.0]
            else:
                temp = pd.read_csv(filename, sep = '\t', skiprows = 1, header = None)
                temp.columns = ['v1', 'i1', 'v2', 'i2', 'v3', 'i3', 'rpm', 'windspeed', 'time']
                temp = temp[temp['time'] < 20.0]
                temp['time'] = temp['time'] + last_time
                df = df.append(temp)

            last_time = float(df.tail(1)['time'])
        df = df[df['rpm'] > df['rpm'].median()/1.5]

        for col in df.columns:
            if col[0] == 'v':
                df[col] = convert_voltage(df[col])
            if col[0] == 'i':
                df[col] = convert_current(df[col])
        pitch = 'Pitch = ' + re.search('pitch(.+?)_', file_name).group(1)

        # df['rpm'] = df['rpm']/1000 #to fit in scale
        ax[file_name] = fig.add_subplot(111)
        ax[file_name].plot(df['time'], df['rpm'], label = pitch)

        xlabel('t(s)')
        ylabel(r'$\omega$ (RPM)')
        title('Open circuit')
        # ax[file_name].plot(df['time'], df['v3'], label= 'V_gen')

    legend(loc='upper left')
    show()

plot_wind(file_name_list)
