import random
import ast
import shelve

suffix_map = {} #if sentence ids in order are 123124, looks like: {(1, 2): [3, 4], (2, 3): [1], (3, 1): [2]}
prefix = () # a tuple of the last 2 sentence ids
ID_DB = 'sentence_list' # simply an unsorted list of sentences. each sentence is a pos list. useful for finding id (index is id)
SENTENCE_MAP_DB = 'sentence_markov'

def process_sentences(sentences, order=2):
    """Processes all sentences.
    sentences: list of sentences, where each sentence is a list of pos
    order: integer
    """
    ids = list()
    for sentence in sentences:
    	if sentence not in ids:
    		ids.append(sentence)
    	process_sentence(ids.index(sentence), order)
    save(ids)

def save(ids):
	global suffix_map

	with shelve.open(SENTENCE_MAP_DB, 'c') as shelf_sm:
		for k, v in suffix_map.items():
			shelf_sm[str(k)] = v

	with shelve.open(ID_DB, 'c') as shelf_ids:
		for n in range(len(ids)):
			shelf_ids[str(n)] = ids[n]

def process_sentence(s_id, order=2):
	"""Processes each sentence to create the suffix_map
    s_id: sentence_id integer
    order: integer
    During the first few iterations, all we do is store up the words; 
    after that we start adding entries to the dictionary.
    """
	global prefix
	if len(prefix) < order:
		prefix += (s_id,)
		return

	try:
		suffix_map[prefix].append(s_id)
	except KeyError:
    	#TODO i know theres a better way than throwing an exception
        # if there is no entry for this prefix, make one
		suffix_map[prefix] = [s_id]

	prefix = shift(prefix, s_id)

# TODO allow an optional prefix input
# TODO this could be cleaned up... later when it works
def random_structures(n=2):
	"""Generates random sentence structures.
    Starts with a random prefix from the dictionary.
    n: number of sentences to generate
    """
	with shelve.open(SENTENCE_MAP_DB) as shelf:
		for k, v in shelf.items():
			suffix_map[ast.literal_eval(k)] = v

	start = random.choice(list(suffix_map.keys()))
	ids = list()
	for i in range(n):
		suffix = random_id(suffix_map, start)
		ids.append(suffix)
		start = shift(start, suffix)

	all_ids = list()

	with shelve.open(ID_DB) as shelf_ids:
		for v in shelf_ids.values():
			all_ids.append(v)

	structures = list()
	for id in ids:
		#get the structure for each id
		structures.append(all_ids[id]) #id is just the index of the list item
	return structures

def random_id(suffix_map, start):
	possible_suffixes = suffix_map.get(start, None)
	if possible_suffixes == None: #The last sentences may not be a prefix
		start = random.choice(list(suffix_map.keys()))
		return random_id(suffix_map, start)
	return random.choice(possible_suffixes)

def shift(t, s_id):
	"""Forms a new tuple by removing the head and adding the new s_id to the tail.
    t: tuple of sentence ids
    s_id: integer
    Returns: tuple of sentence ids
    """
	return t[1:] + (s_id,)

def main():
	global prefix
	print("Testing sentence-processor module...")
	process_sentence(1)
	process_sentence(2)
	process_sentence(3)
	process_sentence(1)
	process_sentence(2)
	process_sentence(4)
	assert prefix == (2,4)
	assert (1,2) in suffix_map
	assert suffix_map[(1,2)] == [3,4]
	print("Success!")

if __name__ == '__main__':
	main()
