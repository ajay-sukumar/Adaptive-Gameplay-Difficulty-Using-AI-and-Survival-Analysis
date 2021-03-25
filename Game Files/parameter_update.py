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
from time import sleep
import random
import csv
import os
f1 = NONE
f2 = NONE
f_writer = NONE
f_reader = NONE
port = 6006
ideal_sim_mode = True #decides whether to simulate variants or ganrate variants.
ideal_sim_mode =  input("Modes\n 1 : ideal simulation mode \n2 : variant generation\nSelect the mode:") == "1" #decides whether to simulate variants or ganrate variants.

if(ideal_sim_mode):
    if(not os.path.exists("Pipe_gap_trained_variants.csv")):
        print("No such file exist: Pipe_gap_trained_variants.csv")
        exit()
    if not os.path.exists("Pipe_gap_pickles"):
        print("No such directory exist: Pipe_gap_pickles")
        exit()
    if not os.path.exists("Pipe_gap_verified_Pickles"):
        os.makedirs("Pipe_gap_verified_Pickles")
        print("directory created: Pipe_gap_verified_Pickles")
    f1 = open('Pipe_gap_trained_verified_variants.csv',mode='a')
    f_writer = csv.writer(f1,delimiter=',', lineterminator = '\n') # file to save variants


    f2 = open('Pipe_gap_trained_variants.csv',mode='r')
    f_reader = csv.reader(f2,delimiter=',')
    port = 6005
    if not os.path.exists("Pickles"):
        print("No such directory: Pickles")
        exit()
    system_call_command = "gnome-terminal -x python flappy_bird_ideal_tune.py "  


else: 
    if not os.path.exists("Pipe_gap_pickles"):
        os.makedirs("Pipe_gap_pickles")
        print("directory created: Pipe_gap_pickles")
    f1 = open('Pipe_gap_trained_variants.csv',mode='a')
    f_writer = csv.writer(f1,delimiter=',', lineterminator = '\n') # file to save variants
    variant_limit = int(input("number of variants to generate:"))
    system_call_command = "gnome-terminal -x python flappy_bird_variant_generate.py "



i = 0
while(ideal_sim_mode or i<variant_limit):
    try:
        address = ('localhost', port)
        conn = Client(address, authkey=b'secret password')
        i = 0
        if not ideal_sim_mode:
            variant_limit = int(input("number of variants to generate:"))
        while(ideal_sim_mode or  i<variant_limit):
            # [GAP,SEPARATION,VELOCITY,PIPE_VELOCITY,JUMP_VELOCITY,GRAVITY,WIN_HEIGHT] variants are genrated and send to the port
            if(ideal_sim_mode):
                msg = next(f_reader)
            else:
                msg = [150+i*10,100,60,9,-9,3,800]
                # msg  = [random.randint(150,250),random.randint(0,200),60,random.randint(4,13),random.randint(-12,-5),3,random.randint(350,950)]
            conn.send(msg) #send variants to *flappy_bird_variant_generate.py*
            print(i," param update:",msg)      
            msg = conn.recv() #wait for response from *flappy_bird_variant_generate.py*
            if(msg==None):
                print("Failed") # variants sent are not playable for ai agent
            elif(len(msg)==1):
                print("Failed",msg) # print score
                f_writer.writerow(["Failed",msg[0],"",""])
            else:
                print(msg)  # variants sent are playable for ai agent
                f_writer.writerow(msg)
                i+=1  
        conn.close()
        break
    except StopIteration: #end of csv
        print("End of CSV")
        break
    except ConnectionRefusedError: # usually *flappy_bird_variant_generate.py* is not started yet, so waits till it is running
        print("refused")
        sleep(3)
    except EOFError: # usually *flappy_bird_variant_generate.py* training is complete
        print("flappy_bird_variant_generate.py server closed")
        break
    except Exception as e:
        print("Error occurred "+str(e))
    
if(f1!=NONE):
    f1.close()
if(f2!=NONE):
    f2.close()   
print("completed")
        