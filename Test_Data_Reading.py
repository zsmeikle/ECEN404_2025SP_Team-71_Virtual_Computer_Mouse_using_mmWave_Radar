import csv

def get_data(line):
    result = -1
    with open("Test_Data.csv", "r") as Test_Data:
        data = csv.reader(Test_Data)
        for i, row in enumerate(data):
            if i == line:
                result = row

    return result


Frame_Num = 0
while True: 
    test = get_data(Frame_Num)
    if (test == -1):
        print("end of file")
        break
    tempX = test[0] 
    tempY = test[1]
    tempRight_Click = test[2]
    tempLeft_Click = test[3]

    print(tempX, tempY, tempRight_Click, tempLeft_Click)

    Frame_Num += 1
    