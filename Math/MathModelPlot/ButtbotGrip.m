clear all
clf



% ALL LENGTHS IN MM
lenD = 150;   %space between motors 
lenLO = 75;   %length of lower arms
lenUP = 150;   %length of upper arms






limitMargin =2;

angMotor1 = 90; %angle of M1 in DEG
angMotor2 = 90; %angle of M2 in DEG

resolution =4; %higher is lower resolution
o= [0 0];

minAngMotor = round(acosd((lenD/2)/(lenLO+lenUP)))+limitMargin
maxAngMotor = round(180-acosd((lenUP-lenD/2)/lenLO))-limitMargin

if not(isreal(maxAngMotor))
    maxAngMotor = 180;
end

axis manual
axis equal
axis([-(lenD/2+lenLO) 1.2*(lenD/2+lenLO) -lenLO lenUP+lenLO])
grip(angMotor1,angMotor2,lenD,lenLO,lenUP,o,true);


possiblePoints = [];

for m1 = minAngMotor:resolution:maxAngMotor
    for m2 = minAngMotor:resolution:maxAngMotor
    possiblePoints = [ possiblePoints ; grip(m1,m2,lenD,lenLO,lenUP,o,false)];
   pause(0);
    end
    %// MATLAB pauses for 0.001 sec before moving on to execue the next 
    %%// instruction and thus creating animation effect
        
end

possiblePoints =possiblePoints.';
ppX=possiblePoints(1,:).';
ppY=possiblePoints(2,:).';
k = boundary(ppX,ppY);


cla;
axis manual
axis equal
axis([-(lenD/2+lenLO) 1.2*(lenD/2+lenLO) -lenLO lenUP+lenLO])


grip(angMotor1,angMotor2,lenD,lenLO,lenUP,o,true);
hold on;
plot(ppX(k),ppY(k));

outerPoints= [ppX(k),ppY(k)];

% animate the arm to limits

cla;
    axis manual
    axis equal
    currentPoint=[0 20]; % insert point here
    calcAngs = getMotorAngles(currentPoint(1),currentPoint(2),lenD,lenLO,lenUP, minAngMotor, maxAngMotor);

    axis([-(lenD/2+lenLO) 1.2*(lenD/2+lenLO) -lenLO lenUP+lenLO])
    

    plot(ppX(k),ppY(k));
    grip(calcAngs(1) ,calcAngs(2),lenD,lenLO,lenUP,o,true);

%% 
for i = 0:1
for ang = minAngMotor:resolution*2:maxAngMotor
    
    cla;
    axis manual
    axis equal
    axis([-(lenD/2+lenLO) 1.2*(lenD/2+lenLO) -lenLO lenUP+lenLO])
    

    plot(ppX(k),ppY(k));
    grip(ang,ang,lenD,lenLO,lenUP,o,true);
    pause(0.2);
    
    %// MATLAB pauses for 0.001 sec before moving on to execue the next 
    %%// instruction and thus creating animation effect
        
end
for ang = minAngMotor:resolution*2:maxAngMotor
    
    cla;
    axis manual
    axis equal
    axis([-(lenD/2+lenLO) 1.2*(lenD/2+lenLO) -lenLO lenUP+lenLO])
    

    plot(ppX(k),ppY(k));
    grip(minAngMotor +maxAngMotor-ang ,minAngMotor+maxAngMotor- ang,lenD,lenLO,lenUP,o,true);
    pause(0.2);
    
    %// MATLAB pauses for 0.001 sec before moving on to execue the next 
    %%// instruction and thus creating animation effect
        
end
end
for k1 = 1:length(outerPoints)
    
    cla;
    axis manual
    axis equal
    currentPoint=outerPoints(k1,:);
    calcAngs = getMotorAngles(currentPoint(1),currentPoint(2),lenD,lenLO,lenUP, minAngMotor, maxAngMotor);

    axis([-(lenD/2+lenLO) 1.2*(lenD/2+lenLO) -lenLO lenUP+lenLO])
    

    plot(ppX(k),ppY(k));
    grip(calcAngs(1) ,calcAngs(2),lenD,lenLO,lenUP,o,true);
    pause(0.2);
    
    %// MATLAB pauses for 0.001 sec before moving on to execue the next 
    %%// instruction and thus creating animation effect   
end