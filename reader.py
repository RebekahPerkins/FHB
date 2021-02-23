import random
import nltk
from character_merge import merge

suffix_map = {}        # map from prefixes to a list of suffixes
prefix = ()            # current tuple of words
suffix_map_dialog = {}
prefix_dialog = ()

def process_file(filename, encoding='cp1252', order=4):
	fin = open(filename, encoding=encoding)
	is_dialog = False
	word_so_far = ''
	line = fin.readline()
	while line is not '':
		line = skip_chapter_headers(fin, line)
		if encoding == 'utf8':
			line = line.replace('“', '"').replace('”', '"').replace("’", "'").replace("‘", "'")
		words = nltk.word_tokenize(line)
		words_tagged = nltk.pos_tag(words)
		for word, pos in words_tagged:
			if pos == '``':
				is_dialog = True
				word = '"'
			elif pos == "''":
				is_dialog = False
				word = '"'
			elif pos == 'NNP':
				word = merge(word)
			process_word(word, is_dialog, order)
		line = fin.readline()
	fin.close()
	return (suffix_map, suffix_map_dialog)

def skip_chapter_headers(fin, line):
	if line.isupper():
		return fin.readline()
	elif line.rstrip().isdigit():
		fin.readline()
		return fin.readline()
	else:
		return line

def process_word(word, is_dialog, order):
	if is_dialog:
		process_word_dialog(word, order)
		return

	global prefix
	
	if len(prefix) < order:
		prefix += (word,)
		return

	try:
		suffix_map[prefix].append(word)
	except KeyError:
		suffix_map[prefix] = [word]

	prefix = shift(prefix, word)

def process_word_dialog(word, order):
	global prefix_dialog

	if len(prefix_dialog) < order:
		prefix_dialog += (word,)
		return

	try:
		suffix_map_dialog[prefix_dialog].append(word)
	except KeyError:
		suffix_map_dialog[prefix_dialog] = [word]#Theres a better way to do this, like setdefault or something

	prefix_dialog = shift(prefix_dialog, word)

def shift(t, word):
    """Forms a new tuple by removing the head and adding word to the tail.
    t: tuple of strings
    word: string
    Returns: tuple of strings
    """
    return t[1:] + (word,)
