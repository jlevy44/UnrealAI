## Story AI

Hey there! So I really like this project. Essentially, when you read a book, you are usually visualizing something in your head as you read a chapter. Well what if the computer can take care of that for you with some AI?

The goal would be:
* Algorithm scans paragraph of text, finds most important words and relation between words.
* Trains important words on millions of internet images and generates the most characteristic image through deep learning.
* Analyzes syntax and semantics of sentence via NLP to find where images describing important words are in relation to each other, and generates a scene for the text you are reading by placing characteristic images in proximal locations to each other dependent on strength of relationship.

There is a lot that will go into this project, so a short term goal would be:
1. to ID the important words in a paragraph and
2. find images on the web automatically that is representative of that idea.
3. Then we'll display those images side by side as you scan through the text

Hide started out lit review on (1): https://datascience.stackexchange.com/questions/5316/general-approach-to-extract-key-text-from-sentence-nlp

Some ideas I've had:
* ID the core elements of a paragraph, translate those into a few key words, and then NN those images. We could take the word frequency of paragraphs and turn them into vectors and perform topic modeling, but topics translate to images
* I’ve been doing this for genomics, we can take words in a paragraph find their frequency across millions of books. If a definite pattern emerges, then that word can be labelled as important, for which we then query google for an image
* relate the words

Joshua Goal:
1. Develop algorithm to ID most important words in a paragraph,
2. post as jupyter notebook
3. Preliminary research on how to find representative images on the web
