import csv
import matplotlib.pyplot as plt 
import pickle
import sys
score_count = dict()
start_line = 2
probability_dist_list = []
survival_fun_list = []
hazard_rate_list = []
scores = []
source_csv = None
total_score_count = 0
if(len(sys.argv)>1):
    source_csv = sys.argv[1] 
else:
    print("source csv required")
    exit()
    
def plotGraph(plot_file_name):
    fig,ax = plt.subplots()
    plt.plot(scores, probability_dist_list, label = "probability_dist") 
    plt.plot(scores, survival_fun_list, label = "survival_fun") 
    plt.plot(scores, hazard_rate_list, label = "hazard_rate") 
    plt.xlabel('score') 
    plt.ylabel('y') 
    plt.legend() 
    pickle.dump(fig, open(plot_file_name, 'wb'))


class ScoreFunctions:
    def __init__(self, score):
        self.score = score  
        self.probability_dist_value = 0      
        self.survival_fun_value = 0
        self.hazard_rate_value = -1

    def probability_dist(self,score):
        try:
            return score_count[score]/total_score_count
        except:
            return 0

    def survival_fun(self):
        s = 0
        for i in range(self.score,101): # s>=x
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
    

  

with open(source_csv) as csv_file:
    i = 0
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

for score in sorted(score_count.keys()):
    scores.append(score)
    f = ScoreFunctions(score)
    [p,s,h] = f.get_values()
    print(score,p,s,h)
    probability_dist_list.append(p)
    survival_fun_list.append(s)
    hazard_rate_list.append(h)
    
plotGraph(source_csv+".plot")