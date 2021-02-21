import random

def random_text(suffix_map, n=500):
    """Generates random wordsfrom the analyzed text.
    Starts with a random prefix from the dictionary.
    n: number of characters to generate
    """
    s = get_start(suffix_map)
    text = ' '.join(s)
    while len(text) < n:
        word = next_word(suffix_map, s)
        if word == None:
            s = get_start(suffix_map)
            text += ' '.join(s)
        else:
            space = get_space(word)
            text += space + word
            s = shift(s, word)
    return text

def shift(t, word):
    """Forms a new tuple by removing the head and adding word to the tail.
    t: tuple of strings
    word: string
    Returns: tuple of strings
    """
    return t[1:] + (word,)

def get_start(suffix_map):
	sentence_boundaries = set('.?!"')
	start = random.choice(list(suffix_map.keys()))
	if start[0] not in sentence_boundaries:
		return get_start(suffix_map)
	else:
		suffixes = suffix_map.get(start, None)
		word = random.choice(suffixes)
		start = shift(start, word)
		return start

def get_space(word):
	if word in '.?!,':
		return ''
	else:
		return ' '

def next_word(suffix_map, start):
    suffixes = suffix_map.get(start, None)
    if suffixes == None:
    	return None
    return random.choice(suffixes)

def flatten(narration, dialog):
	is_dialog = False
	text = ''
	more_quotes = True
	while more_quotes:
		if is_dialog:
			i = get_quote_pos(dialog)
			text += dialog[0:i]
			dialog = dialog[i:]
			more_quotes = bool(dialog)
		else:
			i = get_quote_pos(narration)
			text += narration[0:i]
			narration = narration[i:]
			more_quotes = bool(narration)
		is_dialog = not is_dialog
	return text

def get_quote_pos(text):
	if '"' in text:
		return text.index('"') + 1
	else:
		return len(text)