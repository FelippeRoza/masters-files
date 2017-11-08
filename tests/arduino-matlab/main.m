clc
clear all
%%
% Save the serial port name in comPort variable.

delete(instrfindall);
comPort = 'COM7';
%% 
% It creates a serial element calling the function "stupSerial"

if(~exist('serialFlag','var'))
    [arduino,serialFlag] = setupSerial(comPort);
end

%%
% Time to create our plot window in order to visualize data collectoed 
% from serial port readings

if (~exist('h','var') || ~ishandle(h))
    h = figure(1);
    set(h,'UserData',1);
end

if (~exist('button','var'))
    button = uicontrol('Style','togglebutton','String','Stop',...
        'Position',[0 0 50 25], 'parent',h);
end


%%
% After creating a system of two axis, a line object through which the data
% will be plotted is also created

if(~exist('myAxes','var'))
    
    buf_len = 50;
    index = 1:buf_len; 
    zeroIndex = zeros(size(index)); 
    
    limits = [0 10000];
    
    myAxes = axes('Xlim',[0 buf_len],'Ylim',limits);
    grid on;
    
    %tcdata = zeros(buf_len,8);
    %l = zeros(1,8);
    for i = 1:8
        tcdata(i,:) = zeroIndex;
        l{i} = line(index,[tcdata;zeroIndex]);
    end
    drawnow;
end
%%

mode = 'R';
data = readValue(arduino,mode);
tic;
while (get(button,'Value') == 0 )
    for i = 1:5 %gather data
        tc = readValue(arduino,mode)
        data = [data; tc];
        pause(0.2);
    end
    for i = 1:8 %display data
        tcdata(i,:) = [tcdata(i,2:end),tc(i)];
        set(l{i},'Ydata',tcdata(i,:));
    end
    drawnow;
end

dlmwrite('vazio_pitch0.txt', data, 'delimiter', '\t','newline', 'pc');
close(h);
fclose(arduino);
% To remeber: when you are satisfied with you measurement click on the 
% "stop" button in the bottom left corner of the figure. Now you have to
% close the serial object "Arduino" using the command "fclose(arduino)",
% and close the h figure typing "close(h)". Now in "tcdata" variable you
% have your real time data. 
