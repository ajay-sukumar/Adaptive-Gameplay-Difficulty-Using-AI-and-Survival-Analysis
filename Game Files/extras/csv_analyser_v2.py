import csv
import os
from collections import Counter
directory = './Pipe_gap_scores'
score_list=[]
res=0
high=0
low=0
for i in os.listdir(directory):
    if(i.endswith(".csv")):
        print(i)
        with open('./Pipe_gap_scores/' + i) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            j = 0
            count=0
            score_list = []
            for row in csv_reader:
                if(j==0):
                    parameter=list(row)
                elif(j==1):
                    pass
                elif(j==2):
                    difficulty = row
                else:
                    if count>=30:
                        break
                    score_list.append(row[0])
                    count+=1 
                j+=1
            score_list=[int(i) for i in score_list]
            maxi=max(score_list)
            mini=min(score_list)
            avg=sum(score_list)/len(score_list)
            high = max(set(score_list), key = score_list.count)
            res = Counter(score_list)
            low = res.most_common()[-1][0]
            with open('analysis.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow("pickle")
                writer.writerow(parameter)
                writer.writerow(difficulty)
                writer.writerow(["avg", "max", "min","high freq","low freq"])
                writer.writerow([avg,maxi,mini,high,low])
