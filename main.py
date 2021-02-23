import argparse
import time
import os
from dao import save, load
from writer import random_text, flatten
from reader import process_file

def main(run_test=False, new_data=False, n=500):
	suffix_maps = ''
	if new_data:
		print("Refreshing Data.")
		for db in ['narration.dat', 'narration.dir', 'narration.bak', 'dialog.dat', 'dialog.dir', 'dialog.bak']:
			if os.path.exists(db):
				os.remove(db)
		for filename, encoding in ({'alp.txt': None, 'tsg.txt':'utf8', 'llf.txt':'utf8', 'hhc.txt':'utf8'}.items()):
			suffix_maps = process_file(filename, encoding)
		if not run_test:
			save(suffix_maps)

	time_0 = time.time()
	print("Loading data...")
	if not run_test:
		suffix_maps = load()
	time_1  = time.time()
	print("Data loaded! Time:" + str(time_1 - time_0))
	narration = random_text(suffix_maps[0], n)
	time_2  = time.time()
	print("Narration created! Time:" + str(time_2 - time_1))
	dialog = random_text(suffix_maps[1], n)
	time_3  = time.time()
	print("Dialog created! Time:" + str(time_3 - time_2))
	text = flatten(narration, dialog, n)
	time_4  = time.time()
	print("Text flattened! Time:" + str(time_4 - time_3))
	print("##################################################################")
	print(text)

# python .\main.py --new_data
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-R", "--run_test", help="test mode", action="store_true")
	parser.add_argument("-D", "--new_data", help="replace databases from files", action="store_true")
	parser.add_argument("-n", "--num_chars", type=int, help="num of characters to write")
	args = parser.parse_args()
	kwargs={'run_test': args.run_test, 'new_data': args.new_data}
	if args.num_chars:
		kwargs['n'] = args.num_chars
	main(**kwargs)
