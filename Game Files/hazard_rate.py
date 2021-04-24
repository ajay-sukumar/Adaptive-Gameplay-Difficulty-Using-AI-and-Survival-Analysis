import csv
import matplotlib.pyplot as plt 
import pickle
import sys
import os
import math
import numpy as np
total_score_count = None
score_count = None

#adjustables
score_limit = 18 #limit for calculation
plot_score_limit = 15 #limit for plot
start_line = 3 # number of intial lines to ignore
# directory = "/home/bobby/Documents/Projects/final year project/Adaptive-Gameplay-Difficulty-Using-AI-and-Survival-Analysis/Game Files/scores/survival analysis/" # should end with \ or /
directory = "" # should end with \ or / 

if(len(sys.argv)>1):
    directory = sys.argv[1]



class ScoreFunctions:
    def __init__(self, score):
        self.score = score  
        self.probability_dist_value = 0      
        self.survival_fun_value = 0
        self.hazard_rate_value = 1

    def probability_dist(self,score):
        try:
            return score_count[score]/total_score_count
        except:
            return 0

    def survival_fun(self):
        s = 0
        for i in range(self.score,score_limit+1): # s>=x
            s+=self.probability_dist(i)
        return s 

    def hazard_rate(self):
        self.survival_fun_value = self.survival_fun()
        self.probability_dist_value = self.probability_dist(self.score)
        if(self.survival_fun_value!=0):
            self.hazard_rate_value =  self.probability_dist_value/self.survival_fun_value

    def get_values(self):
        self.hazard_rate()
        return [self.probability_dist_value,self.survival_fun_value ,self.hazard_rate_value]
    
fig,ax = plt.subplots()
for source_csv in (os.listdir() if directory=="" else os.listdir(directory)):
    hazard_rate_list = []
    probability_list = []
    probability_log_list = []

    scores = []
    total_score_count = 0
    score_count = dict()
    if(not (directory + source_csv).endswith("csv")):
        continue
    print(source_csv)
    with open(directory + source_csv) as csv_file:
        i = 1
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if(i>start_line):
                score = int(row[0])
                try:
                    score_count[score] +=1
                except:
                    score_count[score] = 1
            i+=1
        total_score_count = i - start_line - 1 #gets 500
    print(total_score_count ,score_count)

    for score in range(0,plot_score_limit+1):
        scores.append(score)
        [p,s,h] = ScoreFunctions(score).get_values()
        print(score,p,s,h,score_limit)
        hazard_rate_list.append(h)
        probability_list.append(p)
        probability_log_list.append(math.log(p) if p!=0 else -1)
    plt.figure(1)
    plt.plot(scores, hazard_rate_list, label = source_csv) 
    plt.figure(2)
    plt.plot(scores, probability_list, label = source_csv) 
    plt.figure(3)
    plt.plot(scores, probability_log_list, label = source_csv) 

plt.figure(1)
plt.ylabel('hazard') 
plt.xlabel('score') 
ax.set_ylim(bottom=0)
ax.xaxis.set_major_locator(plt.MultipleLocator(5))
plt.yticks(np.arange(0,1,0.2))
plt.legend() 
plt.figure(2)
plt.ylabel('probability') 
plt.xlabel('score') 
ax.xaxis.set_major_locator(plt.MultipleLocator(5))
plt.legend() 
plt.figure(3)
ax.xaxis.set_major_locator(plt.MultipleLocator(5))
plt.ylabel('log probability') 
plt.xlabel('score') 
plt.legend() 
plt.show()
# pickle.dump(fig, open("hazard_rate_multi.plot"), 'wb')
