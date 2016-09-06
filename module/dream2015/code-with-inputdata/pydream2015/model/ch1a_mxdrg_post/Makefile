outputFiles=$(subst output, score, $(wildcard output*.json))

all: $(outputFiles)

score%.json: output%.json
	python featureselect.py $< $@

#clean: 
#	rm -f output*.json
#	rm -rf datafiles/*


