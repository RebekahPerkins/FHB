from sentence_processor import random_structures
from pos_processor import pos_to_words

#get 10 sentence structures, markov style
#fill in with pos

def write():
	sentences = random_structures() # we want a list of sentences, or just a long str, idk
	#print(sentences)
	sentences = pos_to_words(sentences)
	print(' '.join(sentences))

#first call data_processor
if __name__ == '__main__':
	write()