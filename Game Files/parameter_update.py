"""
    Modes
        I.variant generate mode
        1)genrate a random variant within the limits
        2)New thread is created and started
        3)create a sub process flappy_bird_variant_generate.py with port as command line argument 
        4)send the varaint to flappy_bird_variant_generate.py to test it's playability
        3)If playable the data is 
            saved to trained_verified_variants.csv file
        else 
            data is discarded.
        4)Response is saved in csv file. 
        

        II.ideal simulation mode
        1)read genrated variants from trained_variants.csv and sent them to flappy_bird_ideal_test.py
        2)New thread is created and started
        3)create a sub process flappy_bird_variant_generate.py with port as command line argument 
        2)playability with new click per seconds contraint are tested 
            if passed 
                saved to trained_verified_variants.csv
            else 
                discarded
        3)new variants are selected and passed to flappy_bird_ideal_test.py

        III.Auto
        completes ideal simulation mode after variant generate mode 
"""

from multiprocessing.connection import Client
from time import sleep
import random
import csv
import os
import threading
port = 7006
operation_mode  = 0 #decides whether to simulate variants or ganrate variants or auto(genrate variants then simulate)
threads = []
terminal_start_command  = "start " if os.name == 'nt' else "gnome-terminal -x"
slave_file_name = None
file_name_prefix = "GAP" 

if(file_name_prefix!=None):
    print("Setting environment variable " + file_name_prefix)
    os.environ["file_name_prefix"] = file_name_prefix # prefix for separate folder for separate parameter testing
    file_name_prefix+="_"
else:
    file_name_prefix=""
def generate(port,msg,f_writer):
    os.system(terminal_start_command+" "+slave_file_name+" "+str(port))
    while(True):
        try:
            address = ('localhost', port)
            conn = Client(address, authkey=b'secret password')        
            conn.send(msg) #send variants to *flappy_bird_variant_generate.py*
            print(" param update:",msg)      
            msg = conn.recv() #wait for response from *flappy_bird_variant_generate.py*
            if(msg==None):
                print("Failed") # variants sent are not playable for ai agent
            elif(len(msg)==2):
                print("Failed",msg) # print score
                f_writer.writerow(["Failed",msg[1],msg[0],""])
            else:
                print(msg)  # variants sent are playable for ai agent
                f_writer.writerow(msg)
            conn.close()
            break
        except ConnectionRefusedError: # usually *flappy_bird_variant_generate.py* is not started yet, so waits till it is running
            print("refused")
            sleep(3)
        except EOFError: # usually *flappy_bird_variant_generate.py* training is complete
            print("flappy_bird_variant_generate.py server closed")
            break
        except Exception as e:
            print("Error occurred "+str(e))
            break

def pickle_picker():
    if not os.path.exists(file_name_prefix+"/"+file_name_prefix+"Scores"):
        os.makedirs(file_name_prefix+"/"+file_name_prefix+"Scores")
        print("directory created: "+file_name_prefix+"/"+file_name_prefix+"Scores")
    i=0
    with open(file_name_prefix+"/"+file_name_prefix+'trained_verified_variants.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(row[0])
            if (row[0]=="Failed"):
                print("skipping failed variant")
            else:    
                os.system(terminal_start_command+" python skill_model_generate_dyna_diff.py "+" ".join(row[0][1:-1].split(", "))+" "+row[1]+" "+str(i))
            i+=1
def main(ideal_sim_mode):
    global slave_file_name
    f1 = None
    f2 = None
    f_writer = None
    f_reader = None
    variant_limit = 0
    if not os.path.exists(file_name_prefix):
        os.makedirs(file_name_prefix)
    if(ideal_sim_mode):
        print("simulation with delay started")
        if(not os.path.exists(file_name_prefix+"/"+file_name_prefix+"trained_variants.csv")):
            print("No such file exist: "+file_name_prefix+"/"+file_name_prefix+"trained_variants.csv")
            exit()
        if not os.path.exists(file_name_prefix+"/"+file_name_prefix+"Pickles"):
            print("No such directory exist: "+file_name_prefix+"/"+file_name_prefix+"Pickles")
            exit()
        if not os.path.exists(file_name_prefix+"/"+file_name_prefix+"Verified_Pickles"):
            os.makedirs(file_name_prefix+"/"+file_name_prefix+"Verified_Pickles")
            print("directory created: "+file_name_prefix+"/"+file_name_prefix+"Verified_Pickles")
        f1 = open(file_name_prefix+"/"+file_name_prefix+'trained_verified_variants.csv',mode='a')
        f_writer = csv.writer(f1,delimiter=',', lineterminator = '\n') # file to save variants
        f2 = open(file_name_prefix+"/"+file_name_prefix+'trained_variants.csv',mode='r')
        f_reader = csv.reader(f2,delimiter=',')
        if not os.path.exists(file_name_prefix+"/"+file_name_prefix+"Pickles"):
            print("No such directory: "+file_name_prefix+"/"+file_name_prefix+"Pickles")
            exit()
        slave_file_name = "python flappy_bird_ideal_tune.py"
    else: 
        print("variant genration started")
        if not os.path.exists(file_name_prefix+"/"+file_name_prefix+"Pickles"):
            os.makedirs(file_name_prefix+"/"+file_name_prefix+"Pickles")
            print("directory created: "+file_name_prefix+"/"+file_name_prefix+"Pickles")
        f1 = open(file_name_prefix+"/"+file_name_prefix+'trained_variants.csv',mode='a')
        f_writer = csv.writer(f1,delimiter=',', lineterminator = '\n') # file to save variants
        variant_limit = int(input("number of variants to generate:"))
        slave_file_name = "python flappy_bird_variant_generate.py"


    i = 0
    while(ideal_sim_mode or  i<variant_limit):
        try:
            # [GAP,SEPARATION,VELOCITY,PIPE_VELOCITY,JUMP_VELOCITY,GRAVITY,WIN_HEIGHT] variants are genrated and send to the port [200,100,60,9,-9,3,800]
            if(ideal_sim_mode):
                msg = next(f_reader)
            else:
                msg = [220,100,60,9,-21,8,800]
                # msg = [200,100,60,5+i,-9,3,800]
                # msg  = [random.randint(150,250),random.randint(0,200),60,random.randint(4,13),random.randint(-12,-5),3,random.randint(350,950)]
            t1 = threading.Thread(target=generate, args=(port+i,msg,f_writer,)) 
            t1.start()
            threads.append(t1)
            i+=1 
        except StopIteration: #end of csv
            print("End of CSV")
            break

    for i in threads:
        i.join()
    if(f1!=None and not f1.closed):
        f1.close()
        f1 = None
    
    if(f2!=None and not f2.closed):
        f2.close()   
        f2 = None
    print("completed")

operation_mode =  input("Modes\n0 : Pickle Picker \n1 : ideal simulation mode \n2 : variant generation\n3 : auto\nSelect the mode:") #decides whether to simulate variants or ganrate variants.

if(operation_mode=="1"):
    main(True)
elif(operation_mode=="2"):
    main(False)
elif(operation_mode=="0"):
    pickle_picker()
else:
    main(False)
    main(True)