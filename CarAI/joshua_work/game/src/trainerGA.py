from evolutionary_search import maximize
import os, pickle, numpy as np
# pickle the current set of weights used
# return a distance in form of pickle
# what parameters to set? randomized? can randomize the whole process.


architecture, activation = [5,3,3,2], 'tanh'
if architecture[0] < 2:
    architecture[0] = 2
n_weights = sum([architecture[i]*architecture[i+1] for i in range(len(architecture)-1)])
X = []
y = []
#count = 0
#plt.figure()
def distance(**kargs):
    #global count
    weights = kargs
    X.append(list(weights.values()))
    #print(weights)
    pickle.dump((weights, architecture, activation),open('weights.p','wb'), protocol = 2)
    os.system('python simulation.py >/dev/null 2>&1')
    distance = pickle.load(open('distance.p','rb'))
    #plt.clear()
    #plt.plot(y)
    y.append(distance)
    print("Max Distance = %f"%max(y))
    #pickle.dump(distance,open('distance_realtime.p','wb'))
    #count += 1
    return distance
weights_permutations = {'w%d'%i:np.linspace(-5,5,1000) for i in range(n_weights)} # (np.random.rand(100)-0.5)*0.5
best_params, best_score, score_results, hist, log = maximize(distance,weights_permutations,{}, population_size=20, generations_number=50, gene_mutation_prob=0.15, gene_crossover_prob = 0.15, verbose=True)
pickle.dump((best_params, best_score, score_results, hist, log),open('final_model.p','wb'))
best_weights = {best_params[weight] for weight in weights_permutations}
pickle.dump((best_weights,architecture,activation),open('weights.p','wb'), protocol=2)
## FIXME send best weights/model to weights.p when done
# FIXME do some ML on the evolution of the hyperparameters
# PCA plot of weights with showing evaluation results colored
# individual vs score, real time
pickle.dump((np.array(X),np.array(y)), open('X_y.p','wb')) # plot these later on
