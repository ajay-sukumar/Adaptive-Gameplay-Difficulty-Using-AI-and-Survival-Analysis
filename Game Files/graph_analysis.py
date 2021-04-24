import csv
import os
import matplotlib.pyplot as plt
directory =  r"C:\Users\HP\Downloads\normal"
param=['GAP','SEPARATION','VELOCITY','PIPE_VELOCITY','JUMP_VELOCITY','GRAVITY']
x_axis_label='GAP'
x_axis=[]
y_axis=[]
x_axis_result=[]
y_axis_result=[]
label=[]
label_result=[]
count=0
flag=False
for i in os.listdir(directory):
    if(i.endswith(".csv")):
        #print(i)
        
        with open(directory + '/' + i) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')  
            for row in csv_reader:
                while('' in row):
                    row.remove('')
                print(row)
                if not row:
                    pass
                if(len(list(row))==2):
                    if x_axis and y_axis and count<2:
                        print(x_axis)
                        print(y_axis)
                        #plt.plot(x_axis, y_axis)
                        #plt.xticks(x_axis)
                        #plt.xlabel(x_axis_label)
                        #plt.ylabel('Avg')
                        #plt.show()
                        for i in range(len(x_axis)):
      
                        # Find the minimum element in remaining 
                        # unsorted array
                            min_idx = i
                            for j in range(i+1, len(x_axis)):
                                if x_axis[min_idx] > x_axis[j]:
                                    min_idx = j
              
                        # Swap the found minimum element with 
                        # the first element        
                            x_axis[i], x_axis[min_idx] = x_axis[min_idx], x_axis[i]
                            y_axis[i], y_axis[min_idx] = y_axis[min_idx], y_axis[i]
                        x_axis_result.append(x_axis)
                        y_axis_result.append(y_axis)
                        label_result.append(label)
                        label=[]
                        y_axis=[]
                        x_axis=[]
                        #label
                    for j in row:
                        label.append(j)
                    count+=1
                    #print(count)
                if((len(list(row))>4) and row[0]!='avg' and flag!=True):
                    x_axis.append(int(row[param.index(x_axis_label)]))
                    flag=True
                    count=0
                elif((len(list(row))>4) and flag==True and row[0]!='avg'):
                    y_axis.append(float(row[0]))
                    flag=False
            print(x_axis)
            print(y_axis)
            for i in range(len(x_axis)):
      
                # Find the minimum element in remaining 
                # unsorted array
                min_idx = i
                for j in range(i+1, len(x_axis)):
                    if x_axis[min_idx] > x_axis[j]:
                        min_idx = j
              
                # Swap the found minimum element with 
                # the first element        
                x_axis[i], x_axis[min_idx] = x_axis[min_idx], x_axis[i]
                y_axis[i], y_axis[min_idx] = y_axis[min_idx], y_axis[i]
            x_axis_result.append(x_axis)
            y_axis_result.append(y_axis)
            label_result.append(label)
            for p in range(len(x_axis_result)):
                listToStr = ' '.join([str(elem) for elem in label_result[p]])
                print(listToStr)
                plt.plot(x_axis_result[p], y_axis_result[p],label=listToStr)
                plt.xticks(x_axis)
                plt.xlabel(x_axis_label)
                plt.ylabel('Avg')
            plt.legend()
            plt.savefig(r'C:\Users\HP\Documents\programming\python\new_final\analysis\result.png', dpi=300, bbox_inches='tight')
            plt.show()        
        


                
            


