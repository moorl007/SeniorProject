import os
import os.path
import csv
#8 15 30 60
#Get directory to work on files from
###########
###Shit for Jon's Local Environment
os.chdir('SeniorDataset')
os.chdir('allCSV')
###########

####function dec's
#returns list of names of all files with extension "suffix" within dir at "path_to_dir" 
def find_csv_folderNames( path_to_dir): 
    folderNames = os.listdir(path_to_dir)
    folderNames = filter(os.path.isdir, os.listdir(os.getcwd()))
    return folderNames
###End function dec's

#get address of dir w/ CSVs from user + Keep asking until valid input
token = 0
while token == 0:
    path = input("\nEnter Directory Containing CSV files or 'WD' to use the current Working Directory:\n")
    if os.path.exists(path) or path== "WD":
        token = 1
    else:
        print("Invalid or Directory Doesn't Exist...Try Again")

if path == "WD":
    path = os.getcwd()

#############DEBUG   
print("Path: " + path)
######################

date = input("Input File Generation Date as mm-dd: ")
scale = int(input("Input desired timescale (assumed in units of Hz but do not enter unit): "))

##############DEBUG
# print("scale= ")
# print(scale)
###################

#load CSV names into "csv_files" + remove file names beggining with "aggregate" from list (that've been outputted by this script)
csv_folders = find_csv_folderNames(path)

################DEBUG#####
# for folder in csv_folders:
#     print(folder)
############################

meter_num = 1
for folder in csv_folders:
    avg_bucket = [0]*scale
    bucket_itr = 0
    temp= 0
    rows = []
    count = -1
    start = 1640995200
    filename = folder + "(" + date + ")"
    with open(folder + "/" + filename + ".csv", 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
      
        # extracting each data row one by one
        time_steps = 10000 - (10000%scale)
       
        #################DEBUG
        # print("time_steps")
        # print(time_steps)
        #####################
       
        for row in csvreader:
            if(count == -1):
                rows.append(['timestamp','power'])
                rows.append(["",'apparent'])
                count+=1
            
            elif( (count < time_steps+1) and (count > -1) ): #fails to caputre row at time of averaging
                
                if (bucket_itr <= scale-2):
                    avg_bucket[bucket_itr] = float(row[1])  
                    bucket_itr += 1
                
                elif (bucket_itr == scale-1): 
                    avg_bucket[bucket_itr] = float(row[1])
                    for i in range(scale):
                        temp += avg_bucket[i]
                    temp1 = float(temp)/float(scale)
                    rows.append([start + (count-scale), temp1 * 1000])
                    temp = 0
                    bucket_itr = 0
            count+=1
        
        while(count < 10000):
            rows.append([start + count, 0.0])
            count += 1
        
        count = 0
        #######################DEBUG
        # print(len(rows))
        ############################

        #####################DEBUG
        # for j in range(5):
        #     print(rows[j])
        #########################
    os.chdir('..')
    with open("building1/elec/meter" + str(meter_num) + ".csv", 'w', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        
        # writing the data rows
        csvwriter.writerows(rows)
    meter_num += 1
    os.chdir('allCSV')
