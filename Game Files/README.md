[![Run on Repl.it](https://repl.it/badge/github/techwithtim/NEAT-Flappy-Bird)](https://repl.it/github/techwithtim/NEAT-Flappy-Bird)
# NEAT-Flappy-Bird
An AI that plays flappy bird! Using the NEAT python module.


#Flappy bird variant generator

Run both flappy_bird_variant_generate.py and parameter_update.py to simulate the game with a given amount of parameter sets
and train the AI for each set of parameters. If the parameter set generates a game playable by humans, the AI is trained until 
an ideal player model is obtained which can play the game with failure. The ideal model for each parameter set is saved as a 
pickle file and can be reused.


#Neat-python implementation

The game runs the neat algorithm to train a neural network to predict whether the bird must make a jump or not. The settings 
required to run the neat algorithm are specified in the Config file which is used to create the population required to run 
the genetic algorithm.The game is run using the parameter settings provided for a number of generations until an ideal AI is obtained.


# Instructions
Simply run *flappy_bird.py* and watch an AI start training itself to play the game of flappy bird!

Replace population.py in neat package with population.py provided here.
Run *flappy_bird_variant_generate.py* to generate variants.Then run *parameter_update.py* to start genration.

Pickles corresponding to varaints can be idenfied using the timestamp given by *parameter_update.py*.


# Video Tutorial

You can view on the details of this project here: https://www.youtube.com/watch?v=OGHA-elMrxI

# Run in Gitpod

You can also run NEAT-Flappy-Bird in Gitpod, a free online dev environment for GitHub:

If you're intersted in a paid subscription with GitPod use the coupon code: TECHWITHTIM19

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/techwithtim/NEAT-Flappy-Bird/blob/master/flappy_bird.py)





