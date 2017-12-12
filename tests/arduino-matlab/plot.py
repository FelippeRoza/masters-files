import pandas as pd
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import re

folder_name = 'test_2017_12_06/'
rawfile_name_list = ['24v_pitch05_v', '24v_pitch15_v', '24v_pitch25_v', '24v_pitch35_v']
# rawfile_name_list =  ['vazio_pitch05_v', 'vazio_pitch15_v', 'vazio_pitch25_v', 'vazio_pitch35_v']
file_name_list =  ['vazio_pitch05.csv', 'vazio_pitch15.csv', 'vazio_pitch25.csv', 'vazio_pitch35.csv']
file_name_list =  ['24v_pitch05.csv', '24v_pitch15.csv', '24v_pitch25.csv', '24v_pitch35.csv']

def convert_voltage(series):
    return series*5*110/(1024*10)

def convert_current(series):
    output = series/260
    output[output < 0.15] = 0
    return output

def plot_multiple(files_list, output_name):
    f, axarr = plt.subplots(3, sharex=True)

    for filename in files_list:
        df = pd.read_csv(folder_name + filename)
        axarr[1].plot(df['time'], df['rpm'])
        axarr[2].plot(df['time'], df['v3'])
    axarr[0].plot(df['time'], df['wind_km/h'])

    axarr[0].set_title('Open Circuit')
    axarr[0].set_ylabel('Wind Vel. (Km/h)')
    axarr[1].set_ylabel(r'$\omega$ (RPM)')
    axarr[2].set_ylabel(r'Voltage (V)')
    axarr[2].set_xlabel('t(s)')
    for ax in axarr:
        ax.yaxis.set_label_position("right")
    plt.savefig(folder_name + output_name)
    plt.show()

def plot_wind(files_list):
    ax = {}
    fig = {}

    fig = plt.figure()

    for file_name in files_list:
        last_time = 0.0
        df = pd.DataFrame()

        for i in range(1, 5):
            filename = folder_name+'raw/'+file_name+str(i)+'.txt'
            flow = list(pd.read_csv(folder_name + 'raw/vazao_v'+str(i))['Vazao (m^3/h)'])

            if df.empty:
                df = pd.read_csv(filename, sep = '\t', skiprows = 1, header = None)
                df.columns = ['v1', 'i1', 'v2', 'i2', 'v3', 'i3', 'rpm', 'windspeed', 'time']
                df = df[df['time'] < 20.0]
                df['flow'] = pd.DataFrame(flow * (len(df)/len(flow)+1) ).loc[1:len(df.index)]
                df['wind_lev'] = 'v'+str(i)
                df = df.fillna(df.mean())
            else:
                temp = pd.read_csv(filename, sep = '\t', skiprows = 1, header = None)
                temp.columns = ['v1', 'i1', 'v2', 'i2', 'v3', 'i3', 'rpm', 'windspeed', 'time']
                temp = temp[temp['time'] < 20.0]
                temp['time'] = temp['time'] + last_time
                temp['flow'] = pd.DataFrame(flow * (len(df)/len(flow)+1) ).loc[1:(len(temp.index))]
                temp['wind_lev'] = 'v'+str(i)
                temp = temp.fillna(temp.mean())
                df = df.append(temp)

            df['wind_m/s'] = 4*(df['flow']/3600)/(np.pi*(0.175**2))
            df['wind_km/h'] = df['wind_m/s']*3.6
            last_time = float(df.tail(1)['time'])
        df = df[df['rpm'] > df['rpm'].median()/1.5]
        df = df.fillna(df.mean())

        for col in df.columns:
            if col[0] == 'v':
                df[col] = convert_voltage(df[col])
            if col[0] == 'i':
                df[col] = convert_current(df[col])
        pitch = 'Pitch = ' + re.search('pitch(.+?)_', file_name).group(1)
        df.to_csv(folder_name + file_name[:-2] + '.csv', index=False)
        # df['rpm'] = df['rpm']/1000 #to fit in scale
        ax[file_name] = fig.add_subplot(111)
        ax[file_name].plot(df['time'], df['rpm'], label = pitch)
        # ax[file_name].plot(df['time'], df['flow'], label = pitch)
        xlabel('t(s)')
        ylabel(r'$\omega$ (RPM)')
        title('Open circuit')
        # ax[file_name].plot(df['time'], df['v3'], label= 'V_gen')
    #
    legend(loc='upper left')
    ax2 = fig.add_subplot(211)
    ax2 = plot(df['time'], df['wind_m/s'])
    show()

# plot_wind(rawfile_name_list)
plot_multiple(file_name_list, '24V.png')
# frango = pd.read_csv(folder_name + 'flow_v2')['flow (m^3/h)']
# print(frango)
