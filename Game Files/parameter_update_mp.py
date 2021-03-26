"""
    variant generate mode
    1)genrate a random variant within the limits
    2)send the varaint to flappy_bird_variant_generate.py to test it's playability
    3)If playable the data is 
        saved to trained_verified_variants.csv file
    else 
        data is discarded.
    4)new variants are selected and passed to flappy_bird_variant_generate.py

    ideal simulation mode
    1)read genrated variants from trained_variants.csv and sent them to flappy_bird_ideal_test.py
    2)playability with new click per seconds contraint are tested 
        if passed 
            saved to trained_verified_variants.csv
        else 
            discarded
    3)new variants are selected and passed to flappy_bird_ideal_test.py
"""

from multiprocessing.connection import Client
from pickle import NONE
from time import sleep
import random
import csv
import os
import threading
f1 = NONE
f2 = NONE
f_writer = NONE
f_reader = NONE
port = 6006
variant_limit = 0
ideal_sim_mode =  input("Modes\n1 : ideal simulation mode \n2 : variant generation\nSelect the mode:") == "1" #decides whether to simulate variants or ganrate variants.
threads = []
system_call_command=""
parameter = "Pipe_gap"
def generate(port,msg,f_writer):
    os.system(system_call_command+str(port))
    while(True):
        try:
            address = ('localhost', port)
            conn = Client(address, authkey=b'secret password')        
            conn.send(msg) #send variants to *flappy_bird_variant_generate.py*
            print(i," param update:",msg)      
            msg = conn.recv() #wait for response from *flappy_bird_variant_generate.py*
            if(msg==None):
                print("Failed") # variants sent are not playable for ai agent
            elif(len(msg)==2):
                print("Failed",msg) # print score
                f_writer.writerow(["Failed",msg[0],"",""])
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

if(ideal_sim_mode):
    if(not os.path.exists(parameter + "_trained_variants.csv")):
        print('No such file exist: {}_trained_variants.csv'.format(parameter))
        exit()
    if not os.path.exists(parameter + "_pickles"):
        print("No such directory exist: {}_pickles".format(parameter))
        exit()
    if not os.path.exists(parameter + "_verified_pickles"):
        os.makedirs(parameter + "_verified_Pickles")
        print("directory created: {}_verified_pickles".format(parameter))
    f1 = open(parameter + '_trained_verified_variants.csv',mode='a')
    f_writer = csv.writer(f1,delimiter=',', lineterminator = '\n') # file to save variants
    f2 = open(parameter + '_trained_variants.csv',mode='r')
    f_reader = csv.reader(f2,delimiter=',')
    if not os.path.exists(parameter + "_pickles"):
        print("No such directory: {}_pickles".format(parameter))
        exit()
    system_call_command = "start py flappy_bird_ideal_tune.py "


else: 
    if not os.path.exists(parameter + "_pickles"):
        os.makedirs(parameter + "_pickles")
        print("directory created: {}_pickles".format(parameter))
    f1 = open(parameter + '_trained_variants.csv',mode='a')
    f_writer = csv.writer(f1,delimiter=',', lineterminator = '\n') # file to save variants
    variant_limit = int(input("number of variants to generate:"))
    system_call_command = "start py flappy_bird_variant_generate.py "



i = 0
while(ideal_sim_mode or  i<variant_limit):
    try:
        # [GAP,SEPARATION,VELOCITY,PIPE_VELOCITY,JUMP_VELOCITY,GRAVITY,WIN_HEIGHT] variants are genrated and send to the port
        if(ideal_sim_mode):
            msg = next(f_reader)
        else:
            msg = [150,100,60,9,-9,3,800]
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
if(f1!=NONE):
    f1.close()
if(f2!=NONE):
    f2.close()   
print("completed")