

with open("Test_Data.csv", "w") as Test_Data:
    tempX = -10 
    tempY = -10
    tempRight_Click = 0
    tempLeft_Click = 0
    x = 0
    while x < 1800:
        x += 1
        Test_Data.write(str(tempX) + ", " + str(tempY) + ", " + str(tempRight_Click) + ", " + str(tempLeft_Click) + "\n")
        if (x == 400):
            tempX = 10
            tempY = 0
        elif (x == 800):
            tempX = 0
            tempY = 10
        elif (x == 1200):
            tempX = -10
            tempY = 0
        elif (x == 1600):
            tempX = 0
            tempY = 0
            tempLeft_Click = 1
        elif (x == 1650):
            tempLeft_Click = 0
        elif (x == 1700):
            tempRight_Click = 1
        elif (x == 1750):
            tempRight_Click = 0
        
