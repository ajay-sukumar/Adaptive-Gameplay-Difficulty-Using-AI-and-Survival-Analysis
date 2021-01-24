from multiprocessing.connection import Client
from time import sleep
import csv
import random
f1 = open('trained_variants-1.csv',mode='r')
f_reader = csv.reader(f1,delimiter=',')
f2 = open('trained_verified_variants.csv',mode='w')
f_writer = csv.writer(f2,delimiter=',', lineterminator = '\n')
while(True):
    try:
        address = ('localhost', 6005)
        conn = Client(address, authkey=b'secret password')
        # can also send arbitrary objects:
        i = 0
        for row in f_reader:
            # [GAP,SEPERATION,VELOCITY,PIPE_VELOCITY,JUMP_VELOCITY,GRAVITY,WIN_HEIGHT
            msg  = row
            # msg = [166, 110, 40, 9, -11, 3, 706]
            conn.send(msg)
            print(i," param update:",msg)      
            msg = conn.recv()
            if(msg==None):
                print("Failed")
            else:
                print(msg)    
                f_writer.writerow(list(msg.split('|')))
            i+=1
        # while(True):
        #     # [GAP,SEPARATION,VELOCITY,PIPE_VELOCITY,JUMP_VELOCITY,GRAVITY,WIN_HEIGHT
        #     a= input()
        #     msg  = [random.randint(150,250),random.randint(0,150),40,random.randint(5,13),random.randint(-15,0),3,random.randint(350,950)]
        #     conn.send(msg)
        #     print(" param update:",msg)      
        #     # msg = conn.recv()
        #     # print(msg)   

        conn.close()
    except ConnectionRefusedError: # usually *flappy_bird_variant_generate.py* is not started yet, so waits till it is running
        print("refused")
        sleep(3)
    except EOFError: # usually *flappy_bird_variant_generate.py* is training is complete
        print("flappy_bird_variant_generate.py server closed")
        break
    except Exception as e:
        print("Error occurred "+str(e))
print("completed")
        
        