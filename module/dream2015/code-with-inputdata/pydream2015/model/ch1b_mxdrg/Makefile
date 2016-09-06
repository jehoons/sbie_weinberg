#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of Pydream2015.
#*************************************************************************
outputFiles=$(subst input, score, $(wildcard input*.json))

all: $(outputFiles)

output%.json: input%.json
	python mxdrg_fs.py $< $@

score%.json: output%.json
	python mxdrg_tr.py $< $@

clean: 
	rm -f output*.json
	rm -f output*.tar.gz
	rm -f score*.tar.gz
	rm -f score*.json
	rm -rf datafiles/*


