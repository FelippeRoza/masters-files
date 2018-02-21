clear all
close all
%parameters
r = 0.1; %turbine radious
eta = 0.85; %generator efficiency
rho = 1.225; %air density
A = pi*(r^2); %turbine area

%experimental data
pitch = [15 15 15 15 25 25 25 25]; %angle of the blades
rpm = [5700 7400 9000 10700 4900 6200 7400 8700]; %rotational velocity
vwind = [13 17 20 23 13 17 20 23]; %wind velocity
Pe = [14 25 38 55 10 17 25 36]; %electrical output power

%data calculated from experimental data
w = rpm * 0.104719755;
lambda = (r*w)./vwind;
cp = 2*Pe./(eta*rho*A*(vwind.^3));
cp = cp'

xdata = [pitch' lambda'];
f = @(v, x) v(1)*(x(:,2) + (v(2)*(x(:,1).^2)) + v(3)).*exp(v(4)*x(:,2));

opts = optimoptions(@lsqcurvefit,'Display','off');
x0 = [0.5; -0.22; -5.6; -0.17];

%[vestimated,resnorm] = lsqcurvefit(objfcn,x0,pitch, lambda ,cp,[],[],opts)
[vestimated,resnorm] = lsqcurvefit(f,x0,xdata,cp)

f = @(x) -0.0011*(x(:,2) - (-0.0007*(x(:,1).^2)) - 5.3738).*exp(1.362*x(:,2));
(f(xdata)'.*eta*rho*A.*(vwind.^3))/2
Pe

lambda = 0:0.01:6;
x = [ones(length(lambda),1)*15 lambda'];
y = f(x);
y(y<0) = 0;
plot(lambda, y)
