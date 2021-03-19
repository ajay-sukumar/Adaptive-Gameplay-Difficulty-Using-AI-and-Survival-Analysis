import matplotlib.pyplot as plt
import pickle
import sys 
if(len(sys.argv)>1):
    ax = pickle.load(open(sys.argv[1],mode='rb'))
    plt.show()