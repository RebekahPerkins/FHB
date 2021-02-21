from dao import save, load
from writer import random_text, flatten
from reader import process_file

def main(run_test=False, read_file=None):
	suffix_maps = ''
	if read_file not None:
		suffix_maps = process_file(read_file)
		if not run_test:
			save(suffix_maps)
	else:
		if not run_test:
			suffix_maps = load()
		narration = random_text(suffix_maps[0])
		dialog = random_text(suffix_maps[1])
		text = flatten(narration, dialog)
		print(text)

	#TODO command line options
	#TODO tests
	#TODO fun options like genderqueer pronouns, combine characters
	#TODO at least 2 bugs: space after dialog before quote. Occasionally 2 quotes together, not sure why

if __name__ == '__main__':
	main()
