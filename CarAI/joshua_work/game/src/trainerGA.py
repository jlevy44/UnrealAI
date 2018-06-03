from evolutionary_search import maximize
import os, pickle, numpy as np
import pyqtgraph as pg
import sys, io
import random

# pickle the current set of weights used
# return a distance in form of pickle
# what parameters to set? randomized? can randomize the whole process.

open('out.txt','w').close()
architecture, activation = [3,4,4,2], 'tanh' # relu
population_size=70
generations_number=15
gene_mutation_prob=0.15
gene_crossover_prob = 0.85
tournament_size = 3
rand_init = False
n_possible_weight_values = 100
weights_scaling_factor = 30.
bias_scaling_factor = 20.
suppress_output = True
colors = [(random.randint(1,255),random.randint(1,255),random.randint(1,255)) for x in range(1,generations_number+2)]
if architecture[0] < 2:
    architecture[0] = 2
n_weights = sum([architecture[i]*architecture[i+1] for i in range(len(architecture)-1)])
n_bias = sum(architecture[1:])
X = []
y = []
brushes = []
#count = 0
#plt.figure()
w = pg.GraphicsWindow()
w.setGeometry(870,440,400,350)
#v = w.addViewBox()
#v.setAspectLocked()
p = w.addPlot(title='Distance Traveled Per Individual')#pg.plotItem()
#v.addItem(graph)
#p.setData(pos=[[0,0]],symbol='o',color='k',size=2)
plot = p.plot(pos=[[0,0]],symbol='o',color='w',size=0.5)
pg.QtGui.QApplication.processEvents()
def distance(**kargs):
    global plot
    weights_bias = kargs
    weights_dict, bias_dict = {w:v for w,v in weights_bias.items() if 'w' in w}, {b:v for b,v in weights_bias.items() if 'b' in b},
    #print(weights_dict,bias_dict)
    X.append(list(weights_dict.values())+list(bias_dict.values()))
    #print(weights)
    pickle.dump((weights_dict, bias_dict, architecture, activation),open('weights.p','wb'), protocol = 2)
    os.system('python simulation.py %s >/dev/null 2>&1'%('#' if not suppress_output else ''))
    distance = pickle.load(open('distance.p','rb'))

    #plt.clear()
    #plt.plot(y)

    y.append(distance)
    plot_dat = np.array(list(enumerate(y)))
    #print(plot_dat)

    if distance >= max(y):
        os.system('scp distance.p distance_max.p')
    sys.stdout.flush()
    with open('out.txt','r') as f:
        generation_lines = [line for line in f.read().split("--- Evolve in 0 possible combinations ---")[-1].splitlines(False) if line]
    with open('generation_lines.txt','w') as f:
        f.write('\n'.join(generation_lines))
    brushes.append(pg.mkBrush(color=colors[len(generation_lines)]))

    plot.setData(x=plot_dat[:,0],y=plot_dat[:,1],symbolBrush=brushes)
    pg.QtGui.QApplication.processEvents()
    #print("Max Distance = %f"%max(y))
    #pickle.dump(distance,open('distance_realtime.p','wb'))
    #count += 1
    return distance
weights_permutations = {'w%d'%i:(np.linspace(-weights_scaling_factor,weights_scaling_factor,n_possible_weight_values) if rand_init else (np.random.rand(n_possible_weight_values)-0.5)*weights_scaling_factor) for i in range(n_weights)} # (np.random.rand(100)-0.5)*0.5
bias_permutations = {'b%d'%i:(np.linspace(-bias_scaling_factor ,bias_scaling_factor,n_possible_weight_values) if rand_init else (np.random.rand(n_possible_weight_values)-0.5 )*bias_scaling_factor) for i in range(n_bias)}
#weights_permutations = {'w%d'%i:(np.linspace(-weights_scaling_factor,weights_scaling_factor,n_possible_weight_values) + (weights_scaling_factor if activation == 'relu' else 0.) if rand_init else (np.random.rand(n_possible_weight_values)-0.5 + (0.5 if activation == 'relu' else 0.))*weights_scaling_factor) for i in range(n_weights)} # (np.random.rand(100)-0.5)*0.5
#bias_permutations = {'b%d'%i:(np.linspace(-bias_scaling_factor ,bias_scaling_factor,n_possible_weight_values) + (bias_scaling_factor if activation == 'relu' else 0.) if rand_init else (np.random.rand(n_possible_weight_values)-0.5 + (0.5 if activation == 'relu' else 0.))*bias_scaling_factor) for i in range(n_bias)}

weights_permutations.update(bias_permutations)
best_params, best_score, score_results, hist, log = maximize(distance,weights_permutations,{}, population_size=population_size, generations_number=generations_number, gene_mutation_prob=gene_mutation_prob, gene_crossover_prob = gene_mutation_prob, tournament_size=tournament_size, verbose=True)
pickle.dump((best_params, best_score, score_results, hist, log),open('final_model.p','wb'))
best_weights = {best_params[weight] for weight in weights_permutations}
pickle.dump((best_weights,architecture,activation),open('weights.p','wb'), protocol=2)
## FIXME send best weights/model to weights.p when done
# FIXME do some ML on the evolution of the hyperparameters
# PCA plot of weights with showing evaluation results colored
# individual vs score, real time
pickle.dump((np.array(X),np.array(y)), open('X_y.p','wb')) # plot these later on
