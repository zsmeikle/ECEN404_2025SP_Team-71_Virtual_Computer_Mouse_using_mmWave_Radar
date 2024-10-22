

with open("Test_Data.csv", "w") as Test_Data:
    tempX = 0 
    tempY = 1
    tempRight_Click = 2
    tempLeft_Click = 3
    Test_Data.write(str(tempX) + " " + str(tempY) + " " + str(tempRight_Click) + " " + str(tempLeft_Click) + "\n")
