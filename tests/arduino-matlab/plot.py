import pandas as pd
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import re

folder_name = 'test_2017_12_06/'
folder_name = 'test_2017_11_07/'
# rawfile_name_list = ['24v_pitch05_v', '24v_pitch15_v', '24v_pitch25_v', '24v_pitch35_v']
rawfile_name_list =  ['10ohm_pitch15', '10ohm_pitch25']
# rawfile_name_list =  ['vazio_pitch05_v', 'vazio_pitch15_v', 'vazio_pitch25_v', 'vazio_pitch35_v']
open_list =  ['vazio_pitch05.csv', 'vazio_pitch15.csv', 'vazio_pitch25.csv', 'vazio_pitch35.csv']
battery_list =  ['24v_pitch05.csv', '24v_pitch15.csv', '24v_pitch25.csv', '24v_pitch35.csv']

def convert_voltage(series):
    return series*5*110/(1024*10)

def convert_current(series):
    output = series/260
    output[output < 0.15] = 0
    return output

def plot_multiple(files_list, output_name, title, mode = 'voltage'):
    f, axarr = plt.subplots(3, sharex=True)

    for filename in files_list:
        df = pd.read_csv(folder_name + filename)
        pitch = 'Pitch = ' + re.search('pitch(.+?).csv', filename).group(1)
        axarr[1].plot(df['time'], df['rpm'], label = pitch)
        if mode == 'voltage':
            axarr[2].plot(df['time'], df['v3'], label = pitch)
            axarr[2].set_ylabel('Voltage (V)')
        elif mode == 'power':
            axarr[2].plot(df['time'], df['v3']*df['i3'], label = pitch)
            axarr[2].set_ylabel('Power (W)')
    axarr[0].plot(df['time'], df['wind_km/h'], label = 'Wind Vel')

    axarr[0].set_title(title)
    axarr[0].set_ylabel('Wind Vel. (Km/h)')
    axarr[1].set_ylabel(r'$\omega$ (RPM)')

    axarr[2].set_xlabel('t(s)')
    for ax in axarr:
        ax.yaxis.set_label_position("right")
        ax.legend(loc='upper left', prop={'size': 7})
    # legend(loc='upper left')
    plt.savefig(folder_name + output_name)
    plt.show()

def plot_wind_old(files_list):
    f, axarr = plt.subplots(3, sharex=True)

    df_complete = pd.DataFrame()

    df = pd.DataFrame()
    last_time = 0.0
    for file_name in files_list:
        filename = folder_name+'raw/'+file_name+'.txt'
        if df.empty:
            df = pd.read_csv(filename, sep = '\t', skiprows = 1, header = None)
            df.columns = ['v1', 'i1', 'v2', 'i2', 'v3', 'i3', 'rpm', 'windspeed', 'time']
            # df = df[df['time'] < 20.0]
            df = df.fillna(df.mean())
            last_time = float(df.tail(1)['time'])
        else:
            temp = pd.read_csv(filename, sep = '\t', skiprows = 1, header = None)
            temp.columns = ['v1', 'i1', 'v2', 'i2', 'v3', 'i3', 'rpm', 'windspeed', 'time']
            # temp = temp[temp['time'] < 20.0]
            temp['time'] = temp['time'] + last_time
            temp = temp.fillna(temp.mean())
            df = df.append(temp)

    for col in df.columns:
        if col[0] == 'v':
            df[col] = convert_voltage(df[col])
        if col[0] == 'i':
            df[col] = convert_current(df[col])
    df['power'] = (df['v3']*df['v3'])/10
    axarr[0].plot(df['time'], df['power'])
    axarr[1].plot(df['time'], df['rpm'])
    axarr[2].plot(df['time'], df['windspeed'])
    show()



def plot_wind(files_list):
    ax = {}
    fig = {}

    fig = plt.figure()
    df_complete = pd.DataFrame()
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
        df['pitch'] = int(re.search('pitch(.+?)_', file_name).group(1))
        if not df_complete.empty:
            df['time'] = df['time'] + df_complete['time'].iloc[-1]
        df_complete = df_complete.append(df, ignore_index=True)
        # df['rpm'] = df['rpm']/1000 #to fit in scale
        ax[file_name] = fig.add_subplot(111)
        ax[file_name].plot(df['time'], df['rpm'], label = pitch)
        # ax[file_name].plot(df['time'], df['flow'], label = pitch)
        xlabel('t(s)')
        ylabel(r'$\omega$ (RPM)')
        title('Open circuit')
        # ax[file_name].plot(df['time'], df['v3'], label= 'V_gen')
    #
    print 'frango'
    df_complete['time'] = df_complete['time']/10
    df_complete.to_csv(folder_name + 'vazio_complete.csv', index=False)
    legend(loc='upper left')
    ax2 = fig.add_subplot(211)
    ax2 = plot(df['time'], df['wind_m/s'])
    show()

plot_wind_old(rawfile_name_list)
# plot_wind(rawfile_name_list)
# plot_multiple(battery_list, '24V_power.png', '24V Lead-Acid Battery', mode = 'power')
# plot_multiple(open_list, 'opencircuit.png', 'Open Circuit')
