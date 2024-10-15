import matlab.engine
import time

m = matlab.engine.connect_matlab('MATLAB_28744')
x = m.sqrt(4.0)
print(x)

while True:
    x = m.workspace['r']
    print(x)
    time.sleep(0.05)