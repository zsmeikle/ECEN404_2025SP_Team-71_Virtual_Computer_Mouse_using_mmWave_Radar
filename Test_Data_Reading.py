import csv

def get_data(line, size):
    result = -1
    with open("Test_Data.csv", "r") as Test_Data:
        data = csv.reader(Test_Data)
        row = list(data)
        if (line < size):
            result = row[line]
            

    return result

def get_size():
    result = 0
    with open("Test_Data.csv", "r") as Test_Data:
        data = csv.reader(Test_Data)
        for i, row in enumerate(data):
            result += 1

    return result


Frame_Num = 0
while True: 
    size = get_size()
    test = get_data(Frame_Num, size)
    if (test == -1):
        print("end of file")
        break
    tempX = test[0] 
    tempY = test[1]
    tempRight_Click = test[2]
    tempLeft_Click = test[3]

    print(tempX, tempY, tempRight_Click, tempLeft_Click)

    Frame_Num += 1
    