Hide:
	Oh dude
	Visualize a book through semantic and syntactic NLP Machine Learning and image recognition
Images are generated as you read the book
	This one
	Actually worked on something like this
	But never published it
	So like basically I took a movie script and visualized it
Joshua Levy:
	Oh dude! We should work on it!
Hide:
	Here, lemme see if I can find it
Joshua Levy:
	I’d like to start out with the Car project and this one!
	Ok I was picturing something like it conceptualizes what an object looks like by scouring google for that image and creating a neural network model trained on those images.
	Filtered of course
	And then the images can be plotted in relation to each other via NLP scanning of text, which elucidates positional info etc..
Hide:
	Can’t find the image
	But I basically visualized character interactions int he script over time
Joshua Levy:
	Isn't that the project you've been showing me? Did you get the distance matrix to work?
Hide:
	its related, it was a kind of extension to it
	Like get data from a different source and render it
	Ya I fixed the network graph tho, looks much better
Joshua Levy:
	Hmmm... you should show me man. Maybe we can build on it
	Oh sweet, did my thing help?
	Can you send me it?
Hide:
	ya, I had to change my data structure to an adj matrix
Joshua Levy:
	Ah ok. I’m glad it worked 😊
Hide:
	Its a little different from the function that we pseudo-wrote tho
Joshua Levy:
	https://rule-plots-kmers.herokuapp.com
	Ah ok. Does it always account for variable number of nearest neighbors? Maybe you can change it to radius neighbors.. Have it search within a certain distance, that way each node is not required to have a certain number of neighbors
Hide:
	We had to make it simpler than that, so basically if they interact have them closer if not farther away
	B/c the alg. Was kind of getting away from the core idea of the system
Joshua Levy:
	Oh okay. I’m glad it worked out 😊
Hide:
	Ya it helped tho cuz it exposed a bunch of flaws in my code
	So tty
	Anyway ya this looks interesting
	The book one is really hard tho
	Cuz you have to rely on semantics
	Scripts are easy because they’re all structured so you know exactly what ur getting
	So it sounds like maybe a similarity scale based on how close images are to each other?



Joshua Levy:
	Yeah we just need to ID the core elements of a paragraph, translate those into a few key words, and then NN those images. We could take the word frequency of paragraphs and turn them into vectors and perform topic modeling, but topics translate to images
	Nah thats not what I mean by closeness of images
	What we could do first is find representative pictures of each paragraph
	Maybe 3-4 side by side images
Hide:
	Ahhh I see
	Interesting problem
Joshua Levy:
	Then we can relate them later and generate unique never before seen images
	but that can come later
	we can break it into components
Hide:
	what genre of book do u want to do it for?
Joshua Levy:
	Doesn't matter. We can try to grab any paragraph of any book
	Just need to ID the most important words for now. Then we can expand. At least that’s how I see it. Maybe the genre thing is a good idea
	Just speculating, because I’ve been doing this for genomics, we can take words in a paragraph find their frequency across millions of books. If a definite pattern emerges, then that word can be labelled as important, for which we then query google for an image
Hide:
	Finding millions of books might be difficult tho
	There's literature out there for this problem I think
	Ah
Joshua Levy:
	Yeah, we can look for some. But downloading millions of books shouldn’t be too hard
Hide:
	https://datascience.stackexchange.com/questions/5316/general-approach-to-extract-key-text-from-sentence-nlp
Joshua Levy:
	Cool. I’ll add some of what we discussed to our documentation and start this project on GitHub as a subdirectory if you’re down
Hide:
	Ya for sure
	I'm pretty swamped until the 19th tho so I can put some work in after that
Joshua Levy:
	Ok no prob homie. I'll see if I can motivate others to work on it as well.
	How did you visualize it?
