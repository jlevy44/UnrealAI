## Car AI

Coolest project ever. I was motivated to doing this project from https://www.youtube.com/watch?v=8V2sX9BhAW8

This is also cool: https://www.youtube.com/watch?v=BhsgLeY_Q-Y

And this: https://www.youtube.com/watch?v=Aut32pR5PQA

Essentially, we are going to copy the project above:
1. teach a car how to drive itself by evolving neural networks (that control steering and acceleration of car) using genetic Algorithms
2. Run this evolutionary simulation after programming Unreal Engine using Python
3. Daniel will generate the models for unreal engine; essentially our environment that the car interacts with.
4. Hide will generate visualizations of the results using javascript, and we will compare self-trained cars to human input and see if machine beats humans...
5. Maybe add time constraints to additionally change the evolution of the NNs.
6. Use of C++ in this project where needed.
7. After training the cars, place them in new tracks.
8. Collect a population of the best cars, and train new cars based on the best ones via NN?

Short term goals:
1. Daniel and Josh meet to discuss creation of environment
  * Car design + track
2. Josh learns how to use python with unreal engine (free for students!)
  * Or should I use Unity or Pandas 3d. Pandas 3D has more python support than the other two engines and AutoCad, Daniel's modeling tool of choice, exports to Panda3d's .egg format.
3. Josh begins design of GA+NN algorithm
  * NN input is a couple of distance sensors that track distance in front and left and right diagonally in front of the car. x is an R^3 space vector.
  * Output of NN is a two dimensional vector, the first one controls acceleration if above 0.5 and the second one steers left if less than 0.5 and right if more than 0.5.
  * Couple of hidden layers.
  * GA either evolves weights, neural network shape (number of hidden layers and sizes of hidden layers), or both, or maybe there is some backprop we can use as well... Maybe shape remains constant and weights evolve via GA instead of using backpropagation.
  * Fitness scores are determined by:
    * How far the car travels, maybe as percentage of course.
    * How much time it takes; the faster the better.
    * Equation could be something like f(x,t) = x/l + n*(1/t) if t is time per lap, l is length of course, and n is number of laps, which can terminate at a certain number.
    * User can change how the output layer of the NN controls speed and steering, setting new values for speed and steering.

Background:

Using python with 3D game engine:
* Unreal Engine: https://github.com/20tab/UnrealEnginePython
* Unity: https://github.com/exodrifter/unity-python https://github.com/Unity-Technologies/ml-agents
* Panda3d: https://www.panda3d.org/reference/python
* Blender python: https://docs.blender.org/api/current/


More details to come but I can't wait to get started!
