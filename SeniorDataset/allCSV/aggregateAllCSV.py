import csv

fileList = ['/building1/elec/meter2', '/building1/elec/meter3', '/building1/elec/meter4', '/building1/elec/meter5', '/building1/elec/meter6', '/building1/elec/meter7', '/building1/elec/meter8']
folder = "building"
filename = "meter1"
rows = [[],[],[],[],[],[],[]]
count = 0
for i in fileList:
    start = 1640995200
    with open("SeniorDataset" + i + ".csv", 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # extracting field names through first row
        # fields = next(csvreader)
    
        # extracting each data row one by one

        for row in csvreader:
            rows[count].append(row)
    count += 1

#Determine which is the longest and use it to set the length of wattAgList
print(len(rows[0]))
print(len(rows[1]))
print(len(rows[2]))
print(len(rows[3]))
print(len(rows[4]))
print(len(rows[5]))
print(len(rows[6]))

finalAG = [["",'power'], ["", 'apparent']]
wattAgList = [0] * len(rows[0])
for i in range(len(rows)):
    for j in range(2, len(rows[0])):
        try:
            wattAgList[j] += float(rows[i][j][1])
        except:
            wattAgList[j] += 0

for i in range(2, len(rows[0])):
    finalAG.append([rows[0][i][0], str(wattAgList[i])])

with open("SeniorDataset/building1/elec/meter1" + ".csv", 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
     
    # writing the data rows
    csvwriter.writerows(finalAG)
