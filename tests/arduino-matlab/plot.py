import pandas as pd
from pylab import *

folder_name = 'testes_07_11/'
file_name = 'vazio_pitch0.txt'

def convert_voltage(series):
    return series*5*110/(1024*10)

def convert_current(series):
    return (series*(5/1024)-2.5)*0.086

df = pd.read_csv(folder_name+file_name, sep = '\t', skiprows = 1, header = None)
df.columns = ['v1', 'i1', 'v2', 'i2', 'v3', 'i3', 'rpm', 'windspeed', 'time']
for col in df.columns:
    if col[0] == 'v':
        df[col] = convert_voltage(df[col])
    if col[0] == 'i':
        df[col] = convert_current(df[col])

df['rpm'] = df['rpm']/1000 #to fit in scale
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(df['time'], df['rpm'])
ax1.plot(df['time'], df['v3'])
legend = legend(["RPM", "V_gen"], loc=2);
# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111)
# ax2.plot(df['time'], df['windspeed'])
#
# fig3 = plt.figure()
# ax3 = fig3.add_subplot(111)
# ax3.plot(df['time'], df['v3'])

show()
