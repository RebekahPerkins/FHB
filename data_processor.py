import nltk
import os
import shutil
import argparse
import shelve
from sentence_processor import process_sentences
from pos_processor import process_pos

#Do we want to download the file?
def process_file(filename):
    """Reads a file and performs nltk analysis and markov analysis on the sentence structures.
    filename: string. run the script with 
    """
    fp = open(filename)
    skip_gutenberg_header(fp)
    #TODO skip chapter numbers and names like: 1\n\nSara

    sentences = list()
    pos_map = list()

# must we read line by line instead of the whole file? do we even want to tokenize the whole file at once? going line by line could help with chapter breaks
#looks like read instead of readlines goes letter by letter
    punct_was_last = False
    sentence_in_progress = list()
    with open(filename) as fp:
        for line in fp.readlines():
            if line.startswith('End of Project'): 
                break
            #TODO continue (twice if possible?) if line is just a number. that is a chapter header
            words = nltk.word_tokenize(line)
            words_tagged = nltk.pos_tag(words);
            for word, pos in words_tagged:
                if punct_was_last and pos != "''": #TODO see readme for what this even means. so it wont work because sentences are not always markov - sometimes they are just random like the first sentence. so anything inside quotes must be part of 1 sentence
                    sentences.append(sentence_in_progress)
                    sentence_in_progress = list()
                sentence_in_progress.append(pos)
                pos_map.append((word, pos))
                punct_was_last = pos is '.'
    process_sentences(sentences)
    process_pos(pos_map)

def skip_gutenberg_header(fp):
    """Reads from fp until it finds the line that ends the header.
    fp: open file object
    """
    for line in fp:
        if line == ('Sara'):
            break

def main(cleanup=False, filename='thelittletest.txt'):
	#TODO check if filename is the test default. if so, run tests. (otherwise the tests will fail)
	print("Testing main data_processor module...")
	process_file(filename)
	proper_names_file = 'histogram_pos/NNP_pos.txt'
	sentence_map_db = 'sentence_markov'
	sentence_list_db = 'sentence_list'
	assert(os.path.exists(proper_names_file))
	with open(proper_names_file) as fp:
		for line in fp.readlines():
			assert "8: 'Sara'" in line
#	assert(os.path.exists('sentence_list.txt'))
#	assert(os.path.exists(sentence_markov_file))
#	with dbm.open(sentence_map_db) as fin_sentences:
#		for key in fin_sentences:
#			print(key, fin_sentences[key])
#		print(fin_sentences[str.encode(str((0,1)))])
#	with open(sentence_markov_file) as fp2:
#		for line2 in fp2.readlines():
#			assert "{(0, 1): [2], (1, 2): [3], (2, 3): [4]}" in line2
	with shelve.open(sentence_list_db) as shelf_ids:
		assert(len(shelf_ids.items()) is 5)
	with shelve.open(sentence_map_db) as shelf:
		assert(len(shelf.items()) is 3)
	print("Success!")

	if cleanup is True:
		print("Cleaning up...")
		shutil.rmtree('histogram_pos')
		#print(os.listdir())
		os.remove(sentence_map_db + '.dat')
		os.remove(sentence_map_db + '.dir')
		os.remove(sentence_map_db + '.bak')
		os.remove(sentence_list_db + '.dat')
		os.remove(sentence_list_db + '.dir')
		os.remove(sentence_list_db + '.bak')
		print("Done.")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-C", "--cleanup", help="delete data files afterwards", action="store_true")
	parser.add_argument("-f", "--filename", help="txt file to process")
	args = parser.parse_args()
	kwargs={'cleanup': args.cleanup}
	if args.filename:
		kwargs['filename'] = args.filename
	main(**kwargs)

#consider making a human-readable database option. saving as text with no pickling to bytes

#consider putting this "main" stuff in another file
#consider honoring cleanup when something goes wrong
#TODO consider refactoring to be more OO