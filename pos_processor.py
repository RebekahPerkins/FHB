import os
import ast
import shutil
import random

HISTOGRAM_POS_FILE_NAME_FORMAT = 'histogram_pos/%s_pos.txt'

def process_pos(pos_map):
	hists = pos_map_to_hist(pos_map)
	cf = accumulate_frequency(hists)
	save(cf)

#frequency as cumulative totals within each pos
def accumulate_frequency(hists):
	for hist in hists:
		tot = 0
		acc_freq = dict()
		for word, count in hists[hist].items():
			tot += count
			acc_freq[tot] = word
		hists[hist] = acc_freq
	return hists


def pos_map_to_hist(pos_map):
	hists = dict()
	for word, pos in pos_map:
		if pos != 'NNP':
			word = word.lower()
		pos_hist = hists.get(pos, dict())
		pos_hist[word] = pos_hist.get(word, 0) + 1
		hists[pos] = pos_hist
	return hists

def save(hists):
	os.makedirs('histogram_pos', exist_ok=True)
	for hist in hists:
		s = HISTOGRAM_POS_FILE_NAME_FORMAT % hist
		with open(s, 'w') as fout:
			fout.write(str(hists[hist])) #TODO just one long line? fix after poc

def pos_to_words(sentences):
	real_sentences = list()
	hists = init_words()#TODO after proof of concept, do more here. we dont want to make 2 new lists for every word
	for sentence in sentences:
		real_sentence = ''
		for pos in sentence:
			hist = hists[pos]
			word = random.choices(list(hist.values()), cum_weights=list(hist.keys()))[0]
			real_sentence += " " + word
		real_sentences.append(real_sentence)
	return real_sentences

def init_words():
	hists = dict()
	for file in os.listdir('histogram_pos'):
		with open('histogram_pos/' + file) as fin:
			for line in fin.readlines(): #actually just 1 line, fix all this later
				d = ast.literal_eval(line)
				pos_from_filename = file[:-8]#trim the _pos.txt suffix
				hists[pos_from_filename] = d
	return hists

def main():
	print("Testing pos-processor module...")
	hists = pos_map_to_hist([('Is', 'VBZ'), ('this', 'DT'), ('the', 'DT'), ('place', 'NN')])
	assert(hists == {'VBZ': {'is': 1}, 'DT': {'this': 1, 'the': 1}, 'NN': {'place': 1}})
	hists = accumulate_frequency(hists)
	asserts(hists == {'VBZ': {1: 'is'}, 'DT': {1: 'this', 2: 'the'}, 'NN': {1: 'place'}})
	process_pos([('Is', 'VBZ'), ('this', 'DT'), ('the', 'DT'), ('place', 'NN')])
	assert(os.path.exists('histogram_pos/VBZ_pos.txt'))
	print("Success!")

	print("Cleaning up...")
	shutil.rmtree('histogram_pos')
	print("Done.")

if __name__ == '__main__':
	main()
