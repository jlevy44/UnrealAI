## MNIST AI

Hey all! Just start I'd kickstart this project. Jeffrey and Jordan wanted to work with the MNIST dataset and try to submit our attempt to classify digits on Kaggle's competition.

So let's go over some of the goals and what we can learn from the project, maybe some initial readings and short term goals to get started:

What are some questions that we want to answer (At least in my mind)?

* Find out what MNIST is?
  * 70k images of handwritten digits
* What are neural networks?
  * I have done some previous work comparing nearest neighbor classifiers to NN classifiers, although my description of a NN is bad, I hope to update this:
    * https://github.com/jlevy44/JupyterTests/blob/master/Python:SQL/fixed_LMC_Stats_Final.ipynb
    * https://github.com/jlevy44/JupyterTests/tree/master/Python:SQL/output_stats_project
    * I also have a doc that describes what was done.
* What are genetic algorithms?
  * I have some background in using GAs. [sklearn-deap](https://github.com/rsteca/sklearn-deap) has been my library of choice so far.
* Are there better models for classifying digits?
* My interest: How can we combine GAs and NNs?

And we want to submit to Kaggle:
* https://www.kaggle.com/c/digit-recognizer

Here's what I think we should work on:

Jordan:
* Look up what the MNIST dataset is?
* Read up on what neural networks are?
I have some background here:
* https://www.youtube.com/watch?v=aircAruvnKk
* https://github.com/jlevy44/JupyterTests/blob/master/R/Joshua_Project_Report_Math_34.zip
* https://github.com/jlevy44/JupyterTests/blob/master/R/LMC_Math_34_Joshua_Levy_Final_Classifiers_Test.pdf
* Definitely consult other areas. My text is an intro, but there is much more.
Then, your first task should be to:
1. Use the MLPRegressor from scikit-learn to train and classify handwritten digits of the MNIST dataset
2. Try to attain an accuracy greater than 83%
3. Upload a jupyter notebook to this repository than contains your test and the accuracy results outputs.
4. Ask us if you have more q's about NN, MNIST etc....

Joshua:
* I'll script some data visualization that uses [Multicore TSNE](https://github.com/DmitryUlyanov/Multicore-TSNE) to project each handwritten digit into lower dimensions, I already have PCA implemented, so this should not be a hard step
* I'll work out my own GA + NN model and upload some tests onto the project page.
* I'll make some new jupyter notebooks that will help Jordan answer his questions.

Jeffrey:
* Not sure what you have in mind, let us know!
* Can you tell us more about what you'd like us to do with Kaggle?

I think these are some good first steps for future exploration.
