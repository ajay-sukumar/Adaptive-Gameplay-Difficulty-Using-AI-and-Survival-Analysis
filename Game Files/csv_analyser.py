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
                    row_sum=row
                else: 
                    for index in len(row_sum):
                        row_sum[index] += row[index]
                j+=0
            print(csv_reader[0],row_sum)
