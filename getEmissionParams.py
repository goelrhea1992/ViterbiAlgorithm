#! /usr/bin/python

import sys
import math

''' dictionaty with 
	key: <Tag>
	value: dictionary with 
				key: <Word>
				value: <log value of emission(Word | Tag)>
'''
emissionValues = {}

def getEmissionParamValues(counts_file):
	"""
	Generates a text file containing log values of emission parameters in the format:
			<Tag> <Word> <log value of emission(Word | Tag)>

	Text file is called:
		emissionParamsRare.txt: if counts_file name conatins 'rare' 
		emissionParamsFancy.txt: if counts_file name conatins 'fancy'
		emissionParams.txt: otherwise
	"""
	for line in counts_file:
		words = line.strip().split(' ')
		if words[1] == 'WORDTAG':
			if emissionValues.has_key(words[2]):
				temp = emissionValues[words[2]]
				if temp.has_key(words[3]):
					temp[words[3]] = temp[words[3]] + float(words[0])
				else:
					temp[words[3]] = float(words[0])
			else:
				emissionValues[words[2]] = {}
				emissionValues[words[2]][words[3]] = float(words[0])
	
	if 'rare' in counts_file.name:
		writeToFile = 'emissionParamsRare.txt'
	elif 'fancy' in counts_file.name:
		writeToFile = 'emissionParamsFancy.txt'
	else:
		writeToFile = 'emissionParams.txt'
	
	f2 = open(writeToFile, 'w')

	for tag in emissionValues.keys():
		temp = emissionValues[tag]
		thisSum = 0.0
		for value in temp.values():
			thisSum = thisSum + value
		for word in temp.keys():
			temp[word] = math.log(temp[word]/thisSum)
			line = tag + ' ' + word + ' ' + str(temp[word]) + '\n'
			f2.write(line)

def usage():
    print """
    python getEmissionParams.py [counts_file]
	
	Reads a file containing WORDTAG and N-GRAM counts
	and generates a text file containing log values of emission parameters in the format:
			<Tag> <Word> <log value of emission(Word | Tag)>
	"""

if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly one argument
        usage()
        sys.exit(2)

    try:
        input = file(sys.argv[1],"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)

    getEmissionParamValues(input)

