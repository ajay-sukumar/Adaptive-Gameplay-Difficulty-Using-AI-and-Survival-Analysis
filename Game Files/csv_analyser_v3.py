import csv
import os
from collections import Counter
param = 'Pipe_gap'
directory = './' + param + '_scores'
uniform = True
ur =''
sd = ''
score_list=[]
res=0
high=0
low=0
s=''
flag=True
diff = dict()
std_dev = dict()
uni_range = dict()
variants = []
stat = dict()
res_csv_d = 'difficulty_analysis.csv'
res_csv_v = 'variant_analysis.csv'
start = True
n_scores = 0
for i in os.listdir(directory):
    if(i.endswith(".csv")):
        print(i)
        count_samples = 0
        if start == True:
            stat[count_samples] = []
        with open('./' + param + '_scores/' + i) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            j = 0
            count=0
            score_list = []
            for row in csv_reader:
                while('' in row):
                    row.remove('')
                if(len(list(row))>4):
                    if score_list:
                        print(score_list)
                        score_list=[int(i) for i in score_list]
                        maxi=max(score_list)
                        mini=min(score_list)
                        avg=sum(score_list)/len(score_list)
                        high = max(set(score_list), key = score_list.count)
                        res = Counter(score_list)
                        low = res.most_common()[-1][0]
                        stat[count_samples].append([avg,maxi,mini,high,low])
                        with open(res_csv_d, 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(["Difficulty",difficulty])
                            if uniform:
                                writer.writerow(["Range ",ur])
                            else:
                                writer.writerow(["Standard deviation ",sd])
                            writer.writerow(["avg", "max", "min","high freq","low freq"])
                            writer.writerow([avg,maxi,mini,high,low])
                        count_samples +=1
                        if start == True:
                            stat[count_samples] = []
                    score_list=[]
                    parameter=row
                    if parameter not in variants:
                        variants.append(parameter)
                    with open(res_csv_d, 'a', newline='') as file:
                        writer = csv.writer(file)
                        if flag:
                            writer.writerow([parameter])
                            flag=False
                    #print(parameter)
                elif(len(list(row))==4):
                    if uniform:
                        ur = '(' + row[0] + ',' + row[1] + ')'
                        if count_samples not in uni_range:
                            uni_range[count_samples] = ur 
                    else:
                        sd=row[1]
                        if count_samples not in std_dev:
                            std_dev[count_samples] = sd 
                    #print(sd)
                elif(len(list(row))==1):
                    if '.' in row[0]:
                        difficulty = row[0]
                        if count_samples not in diff:
                            diff[count_samples] = difficulty
                    else:
                        score_list.append(int(row[0])) 
            print(score_list)

            score_list=[int(i) for i in score_list]
            maxi=max(score_list)
            mini=min(score_list)
            avg=sum(score_list)/len(score_list)
            high = max(set(score_list), key = score_list.count)
            res = Counter(score_list)
            low = res.most_common()[-1][0]
            stat[count_samples].append([avg,maxi,mini,high,low])
            n_scores = len(score_list)
            start = False
            with open(res_csv_d, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Difficulty",difficulty])
                if uniform:
                    writer.writerow(["Range ",ur])
                else:
                    writer.writerow(["Standard deviation ",sd])
                writer.writerow(["avg", "max", "min","high freq","low freq"])
                writer.writerow([avg,maxi,mini,high,low])
                writer.writerow('')
            flag=True

with open(res_csv_v, 'a', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(diff)):
        writer.writerow(['n_scores', n_scores])
        writer.writerow(['Difficulty',diff[i]])
        if uniform:
            writer.writerow(["Range ",uni_range[i]])
        else:
            writer.writerow(["Standard Deviation ",std_dev[i]])
        writer.writerow(["avg", "max", "min","high freq","low freq"])
        for j in range(len(variants)):
            writer.writerow([variants[j]])
            writer.writerow(stat[i][j])
            writer.writerow('')
        writer.writerow('')

