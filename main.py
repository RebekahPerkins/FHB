import argparse
from dao import save, load
from writer import random_text, flatten
from reader import process_file

def main(run_test=False, filename=None, n=500):
	suffix_maps = ''
	print("file is " + filename)
	if filename is not None:
		suffix_maps = process_file(filename)
		if not run_test:
			save(suffix_maps)
	if not run_test:
		suffix_maps = load()
	narration = random_text(suffix_maps[0], n)
	dialog = random_text(suffix_maps[1], n)
	text = flatten(narration, dialog, n)
	print(text)
	if run_test:
		test(text, n, filename)

	#TODO fun options like genderqueer pronouns, combine characters
	#TODO at least 2 bugs: space after dialog before quote. Occasionally 2 quotes together, not sure why

def test(text, n, filename=None):
	assert(len(text)) == n
	#python .\main.py --run_test --filename='thelittletest2.txt' -n=34
	if name == 'thelittletest2.txt' and n == 34:
		assert(text == 'Only one possibility. "This is it.')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-R", "--run_test", help="test mode", action="store_true")
	parser.add_argument("-f", "--filename", help="txt file to process")
	parser.add_argument("-n", "--num_chars", type=int, help="num of characters to write")
	args = parser.parse_args()
	kwargs={'run_test': args.run_test}
	if args.filename:
		kwargs['filename'] = args.filename
	if args.num_chars:
		kwargs['n'] = args.num_chars
	main(**kwargs)
