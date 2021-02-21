import shelve

DIALOG_CHAIN_DB = 'dialog'
NARRATION_CHAIN_DB = 'narration'

def save(suffix_maps):
	save_collection(suffix_maps[0], NARRATION_CHAIN_DB)
	save_collection(suffix_maps[1], DIALOG_CHAIN_DB)

def load():
	narration = load_collection(NARRATION_CHAIN_DB)
	dialog = load_collection(DIALOG_CHAIN_DB)
	return (narration, dialog)

def save_collection(d, db_name):
	with shelve.open(db_name, 'c') as shelf:
		for k, v in d.items():
			shelf[k] = v

def load_collection(db_name):
	d = dict()
	with shelve.open(db_name) as shelf:
		for k, v in shelf.items():
			d[k] = v
	return d
