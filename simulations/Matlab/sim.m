clear global
data = readtable('24V_complete.csv');

rotation = table2array([data(:,6) data(:,5)]);
pitch = table2array([data(:,6) data(:,14)]);
wind = table2array([data(:,6) data(:,12)]);