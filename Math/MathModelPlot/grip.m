function [gripper]= grip(angM1,angM2,lenD,lenLO,lenUP,o,drawLines)

% Set Vars


posM1 = [-lenD/2 0];
posM2 = [lenD/2 0];


posEL1 = posM1 + lenLO * [cosd(angM1) sind(angM1)]; %pos left ellbow
posEL2 = posM2 + lenLO * [cosd(180-angM2) sind(180-angM2)]; %pos right ellbow

%calculate arms
disElbows =norm(posEL2-posEL1); %distance between elbows
posTriCent = posEL2 + (posEL1-posEL2)/2;

triHeight = sqrt(lenUP^2 - (disElbows/2)^2) ;



gripper = posTriCent+ (posEL2-posEL1)/disElbows*[0 1;-1 0]*triHeight; %%vector that is the height of the upper triangle

%draw

if drawLines
hold on

plot(o(1),o(2),'x') %draw origin

plot(posM1(1),posM1(2),'o') %draw M1

drawLine(posM2,posM1) %draw w

plot(posM2(1),posM2(2),'o') %draw M2


drawLine(posEL1,posM1) %draw left lowerArm
plot(posEL1(1),posEL1(2),'o') %draw left ellbow


drawLine(posEL2,posM2) %draw right lowerArm
plot(posEL2(1),posEL2(2),'o') %draw right ellbow

plot(gripper(1),gripper(2),'o') %draw gripper
drawLine(posEL1,gripper)
drawLine(posEL2,gripper)
else
plot(gripper(1),gripper(2),'.') 
end

end

