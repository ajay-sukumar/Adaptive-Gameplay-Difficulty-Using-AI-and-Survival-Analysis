from multiprocessing.connection import Client
from time import sleep
import random
while(True):
    try:
        address = ('localhost', 6005)
        conn = Client(address, authkey=b'secret password')
        # can also send arbitrary objects:
        flag = True
        i = 0
        while(i<25):
            # [GAP,SEPARATION,VELOCITY,PIPE_VELOCITY,JUMP_VELOCITY,GRAVITY,WIN_HEIGHT
            msg  = [random.randint(150,250),random.randint(0,150),40,random.randint(5,13),random.randint(-15,0),3,random.randint(350,950)]
            # msg = [166, 110, 40, 9, -11, 3, 706]
            conn.send(msg)
            print(i," param update:",msg)      
            msg = conn.recv()
            if(msg==None):
                print("Failed")
            else:
                print(msg)  
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
    except ConnectionRefusedError:
        print("refused")
        sleep(3)
        
        