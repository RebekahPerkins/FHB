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
				process_word(c, is_dialog)#True for opening quote only. i think its good like that but test
			elif c.isspace():
				if len(word_so_far) > 0:
					process_word(word_so_far, is_dialog)
					word_so_far = ''
			else:
				word_so_far += c

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

def get_start(is_dialog):
	sentence_boundaries = set('.?!"')
	s_m = get_suffix_map(is_dialog)
	start = random.choice(list(s_m.keys()))
	if start[0] not in sentence_boundaries:
		return get_start(is_dialog)
	else:
		suffixes = s_m.get(start, None)
		word = random.choice(suffixes)
		start = shift(start, word)
		return start

def random_text(is_dialog, n=500):
    """Generates random wordsfrom the analyzed text.
    Starts with a random prefix from the dictionary.
    n: number of characters to generate
    """
    s = get_start(is_dialog)
    text_so_far = ' '.join(s)
    while len(text_so_far) < n:
        word = next_word(is_dialog, s)
        if word == None:
            s = get_start(is_dialog)
            text_so_far += ' '.join(s)
        else:
            space = get_space(word, is_dialog)
            text_so_far += space + word
            s = shift(s, word)
    return text_so_far

def get_space(word, is_dialog):
	if word in '.?!,':
		return ''
	else:
		return ' '

def next_word(is_dialog, start):
    suffixes = get_suffix_map(is_dialog).get(start, None)
    if suffixes == None:
    	return None
    return random.choice(suffixes)

def get_suffix_map(is_dialog):
	return suffix_map if not is_dialog else suffix_map_dialog

def flatten(narration, dialog):
	is_dialog = False
	text = ''
	more_quotes = True
	while more_quotes:
		if is_dialog:
			i = get_quote_i(dialog)
			text += dialog[0:i]
			dialog = dialog[i:]
			more_quotes = bool(dialog)
		else:
			i = get_quote_i(narration)
			text += narration[0:i]
			narration = narration[i:]
			more_quotes = bool(narration)
		is_dialog = not is_dialog
	return text

def get_quote_i(text):
	if '"' in text:
		return text.index('"') + 1
	else:
		return len(text)

def main(cleanup=False, filename='thelittletest3.txt'):
	process_file(filename)
	narration = random_text(False)
	dialog = random_text(True)
	text = flatten(narration, dialog)
	print(text)
	#TODO save and load the markov chains
	#TODO command line options
	#TODO tests
	#TODO fun options like genderqueer pronouns, combine characters
	#TODO at least 2 bugs: space after dialog before quote. Occasionally 2 quotes together, not sure why

if __name__ == '__main__':
	main()
