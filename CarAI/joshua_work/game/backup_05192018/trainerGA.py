from evolutionary_search import maximize
import os, pickle, numpy as np


# pickle the current set of weights used
# return a distance in form of pickle
# what parameters to set? randomized? can randomize the whole process.


architecture, activation = [3,4,4,2], 'tanh'

def distance(**kargs):
    weights = kargs
    #print(weights)
    pickle.dump((weights, architecture, activation),open('weights.p','wb'), protocol = 2)
    os.system('python simulation.py')
    distance = pickle.load(open('distance.p','rb'))
    return distance

best_params, best_score, score_results, hist, log = maximize(distance,{'w%d'%i:np.random.rand(100)-0.5 for i in range(36)},{},verbose=True)
pickle.dump((best_params, best_score, score_results, hist, log),open('final_model.p','wb'))
