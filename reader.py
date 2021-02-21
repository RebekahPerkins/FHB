import random

suffix_map = {}        # map from prefixes to a list of suffixes
prefix = ()            # current tuple of words
suffix_map_dialog = {}
prefix_dialog = ()

def process_file(filename, order=3):
	fin = open(filename)
	skip_header(fin, filename)

	is_dialog = False
	word_so_far = ''
	line = fin.readline()
	while line is not '':
		line = skip_chapter_headers(fin, line)
		if line.startswith("End of Project"):
			break
		for c in line:
			if c in '".?!,':
				if len(word_so_far) > 0:
					process_word(word_so_far, is_dialog)
					word_so_far = ''
				process_word(c, is_dialog)
			elif c.isspace():
				if len(word_so_far) > 0:
					process_word(word_so_far, is_dialog)
					word_so_far = ''
			else:
				word_so_far += c
			if c == '"':
				is_dialog = not is_dialog
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

def skip_header(fin, filename):
	start = None
	if filename == '479-0.txt':
		start = 'I'
	elif filename == 'pg146.txt':
		start = 'Sara'
	elif filename == '113-0.txt':
		start = ' THERE IS NO ONE LEFT'
	if start == None:
		return

	for line in fin:
		if line.startswith(start):
			break

def process_word(word, is_dialog, order=3):
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

def process_word_dialog(word, order=3):
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
