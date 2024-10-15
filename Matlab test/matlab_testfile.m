x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
i = 1;
r = x(1);

while i < 10000
    r = x(mod(i, 10)+1);
    disp(r);
    i = i + 1;
    pause(0.05);
end
