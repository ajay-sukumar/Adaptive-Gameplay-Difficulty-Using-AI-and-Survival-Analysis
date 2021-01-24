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
f1 = NONE
f2 = NONE
f_writer = NONE
f_reader = NONE
ideal_sim_mode = False #decides whether to simulate variants or ganrate variants.
port = 6006
if(ideal_sim_mode):
    f1 = open('trained_verified_variants.csv',mode='a')
    f_writer = csv.writer(f1,delimiter=',', lineterminator = '\n') # file to save variants
    f2 = open('trained_variants.csv',mode='r')
    f_reader = csv.reader(f2,delimiter=',')
    port = 6005
else: 
    f1 = open('trained_variants.csv',mode='a')
    f_writer = csv.writer(f1,delimiter=',', lineterminator = '\n') # file to save variants
    #port = 6006
while(True):
    try:
        address = ('localhost', port)
        conn = Client(address, authkey=b'secret password')
        i = 0
        variant_limit = 25 # number of variants to be generated
        while(ideal_sim_mode or  i<variant_limit):
            # [GAP,SEPARATION,VELOCITY,PIPE_VELOCITY,JUMP_VELOCITY,GRAVITY,WIN_HEIGHT] variants are genrated and send to the port
            if(ideal_sim_mode):
                msg = next(f_reader)
            else:
                msg  = [500,random.randint(0,150),60,4,random.randint(-15,1),3,random.randint(350,950)]
            conn.send(msg) #send variants to *flappy_bird_variant_generate.py*
            print(i," param update:",msg)      
            msg = conn.recv() #wait for response from *flappy_bird_variant_generate.py*
            if(msg==None):
                print("Failed") # variants sent are not playable for ai agent
            elif(len(msg)==1):
                print("Failed",msg) # print score
                f_writer.writerow("Failed"+str(msg[0]))
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
    except EOFError: # usually *flappy_bird_variant_generate.py* is training is complete
        print("flappy_bird_variant_generate.py server closed")
        break
    except Exception as e:
        print("Error occurred "+str(e))
    
if(f1!=NONE):
    f1.close()
if(f2!=NONE):
    f2.close()   
print("completed")
        