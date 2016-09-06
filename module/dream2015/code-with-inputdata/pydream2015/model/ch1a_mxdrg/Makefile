outputFiles=$(subst input, output, $(wildcard input*.json))

all: $(outputFiles)

output%.json: input%.json
	python featureselect.py $< $@

clean: 
	rm -f output*.json
	rm -rf datafiles/*


