

with open("Test_Data.csv", "w") as Test_Data:
    tempX = -10 
    tempY = -10
    tempRight_Click = 0
    tempLeft_Click = 0
    x = 0
    while x < 900:
        x += 1
        Test_Data.write(str(tempX) + ", " + str(tempY) + ", " + str(tempRight_Click) + ", " + str(tempLeft_Click) + "\n")
        if (x == 200):
            tempX = 10
            tempY = 0
        elif (x == 400):
            tempX = 0
            tempY = 10
        elif (x == 600):
            tempX = -10
            tempY = 0
        elif (x == 800):
            tempX = 0
            tempY = 0
            tempLeft_Click = 2
        elif (x == 825):
            tempLeft_Click = 1
        elif (x == 826):
            tempLeft_Click = 0
        elif (x == 850):
            tempRight_Click = 2
        elif (x == 875):
            tempRight_Click = 1
        elif (x == 876):
            tempRight_Click = 0
        
