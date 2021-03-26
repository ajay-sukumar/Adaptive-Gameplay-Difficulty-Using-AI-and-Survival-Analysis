import csv
import os
# First line : variants parameter
# Second line : not so important stuff
# From third line : n samples of scores
start_index=3
for i in os.listdir():
    if(i.endswith("csv")):
        with open(i) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            j = 0
            col_sum = []
            for row in csv_reader:
                if(j>start_index): 
                    for index in range(len(col_sum)):
                        col_sum[index] += int(row[index])
                elif(j==start_index):
                    col_sum=[int(i) for i in row]
                elif(j==1):
                    pass 
                else:
                    print(row, i)
                j+=1
            print([i/(j-start_index) for i in col_sum])