import random

suffix_map = {}        # map from prefixes to a list of suffixes
prefix = ()            # current tuple of words
suffix_map_dialog = {}
prefix_dialog = ()

def process_file(filename, order=3):
	with open(filename) as fp:
		is_dialog = False
		word_so_far = ''
		for c in fp.read():
			if c == '"':
				is_dialog = not is_dialog
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
	return (suffix_map, suffix_map_dialog)

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