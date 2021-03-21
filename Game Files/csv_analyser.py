import csv
import os
for i in os.listdir():
    if(i.endswith("csv")):
        with open(i) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            j = 0
            row_sum = []
            for row in csv_reader:
                if(j==0):
                    print(row)
                elif(j==2):
                    pass
                elif(j==3):
                    row_sum=[int(i) for i in row]
                else: 
                    for index in range(len(row_sum)):
                        row_sum[index] += int(row[index])
                j+=1
            print([i/(j-2) for i in row_sum])
