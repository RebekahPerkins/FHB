# FHB
The Frances Hodgson Burnett Coauthor

## Installation
if you have python and anaconda already, 
install nltk package with conda: 
```
conda install -c anaconda nltk
```
then:
```
conda install -c conda-forge nltk_data
```
verify:
```
conda list
```

##To test:
```
python sentence-processor.py #(no data is saved in this test)
python data_processor.py #(by default, does not delete data afterwards)
python data_processor.py --cleanup #(deletes data afterwards)
python pos_processor.py #(always cleans up)
python writer.py #(after setting up data with 'python data_processor.py')
```

##To run:
for The Little Princess, download to same dir: https://www.gutenberg.org/cache/epub/146/pg146.txt
then call:
```
python data_processor.py --filename pg146.txt
python writer.py
```
