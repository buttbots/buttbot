function [angs] = getMotorAngles(xCoord,yCoord,lenD,lenLO,lenUP, minAng, maxAng)
%GETMOTORANGLES Summary of this function goes here
%   Detailed explanation goes here

posM1 = [-lenD/2 0];
posM2 = [lenD/2 0];

%left motor
elbowLeftIntersections = intersectCircles(xCoord,yCoord,lenUP,posM1(1),posM1(2),lenLO);
leftElbow =  elbowLeftIntersections(2,:)-posM1;

angleM1 = atan2d(leftElbow(2),leftElbow(1)); %dY,dX


%right motor
elbowRightIntersections = intersectCircles(xCoord,yCoord,lenUP,posM2(1),posM2(2),lenLO);
rightElbow =   elbowRightIntersections(1,:)-posM2 

angleM2 = 180-atan2d(rightElbow(2),rightElbow(1)); %dY,dX



angs = [angleM1 angleM2];


end

