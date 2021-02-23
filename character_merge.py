
characters_to_merge = {
'Dorincourt':'Dorinate', 'Misselthwaite':'Dorinate', 'Coombe':'Dorinate', 'Manor':'Castle',
'Dr.':'Mr.', 'Fräulein':'Miss', 'Mademoiselle':'Miss',
'Craven':'Haverford', 'Hobbs':'Haverford', 'Havisham':'Haverford', 'Barrow':'Haverford', 'Carrisford':'Haverford',
'Crewe':'Lennox', 'Gareth-Lawless':'Lennox', 'Mary':'Rose', 'Robin':'Rose', 'Sara':'Rose',
'Ram':'Dickard', 'Dass':'Howe', 'Dick': 'Dickard', 'Dickon':'Dickard',
'Ceddie':'Connor', 'Cedric':'Connor', 'Donal':'Connor', 'Muir':'Errol', 'Colin':'Connor',
'Roach':'Weatherstaff', 'Higgins':'Weatherstaff', 'Michael':'Ben',
'Medlock':'Howe', 'Amabel':'Felicia', 'Amelia':'Felicia', 'Feather':'Felicia', 'Sowerby':'Howe',
'Becky':'Betty', 'Susan':'Betty', 'Dawson':'Betty', 'Mariette':'Betty', 'Louisa':'Betty', 'Anne':'Betty', 'Dowson':'Betty', 'Dowie': 'Betty', 'Martha':'Betty',
'Vallé':'Minchin', 'Hirsch':'Minchin', 'Andrews':'Minchin',
'Ermengarde':'Lottie', 'Lugh': 'St. John', 'Lavinia':'Lottie', 'Janet':'Lottie', 'Large':'St. John'
}

def merge(nnp):
	return characters_to_merge.get(nnp, nnp)
