from multiprocessing.connection import Client
from time import sleep
import random
while(True):
    try:
        address = ('localhost', 6006)
        conn = Client(address, authkey=b'secret password')
        i = 0
        variant_limit = 25 # number of variants to be generated
        while(i<variant_limit):
            # [GAP,SEPARATION,VELOCITY,PIPE_VELOCITY,JUMP_VELOCITY,GRAVITY,WIN_HEIGHT] variants are genrated and send to port 6006
            msg  = [random.randint(150,250),random.randint(0,150),60,random.randint(5,13),random.randint(-15,1),3,random.randint(350,950)]
            # msg = [166, 110, 40, 9, -11, 3, 706]
            # msg = [197, 141, 40, 5, -11, 3, 531]
            msg = [250, 100, 40, 6, -12, 3, 800]
            conn.send(msg) #send variants to *flappy_bird_variant_generate.py*
            print(i," param update:",msg)      
            msg = conn.recv() #wait for response from *flappy_bird_variant_generate.py*
            if(msg==None):
                print("Failed") # variants sent are not playable for ai agent
            else:
                print(msg)  # variants sent are playable for ai agent
                i+=1  

        conn.close()
        break
    except ConnectionRefusedError: # usually *flappy_bird_variant_generate.py* is not started yet, so waits till it is running
        print("refused")
        sleep(3)
    except EOFError: # usually *flappy_bird_variant_generate.py* is training is complete
        print("flappy_bird_variant_generate.py server closed")
        break
    except Exception as e:
        print("Error occurred "+str(e))
print("completed")
        