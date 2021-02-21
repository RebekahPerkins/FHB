import argparse
from dao import save, load
from writer import random_text, flatten
from reader import process_file

def main(run_test=False, filename=None):
	suffix_maps = ''
	if filename not None:
		suffix_maps = process_file(filename)
		if not run_test:
			save(suffix_maps)
	else:
		if not run_test:
			suffix_maps = load()
		narration = random_text(suffix_maps[0])
		dialog = random_text(suffix_maps[1])
		text = flatten(narration, dialog)
		print(text)

	#TODO tests
	#TODO fun options like genderqueer pronouns, combine characters
	#TODO at least 2 bugs: space after dialog before quote. Occasionally 2 quotes together, not sure why

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-R", "--run_test", help="test mode", action="store_true")
	parser.add_argument("-f", "--filename", help="txt file to process")
	args = parser.parse_args()
	kwargs={'run_test': args.run_test}
	if args.filename:
		kwargs['filename'] = args.filename
	main(**kwargs)
