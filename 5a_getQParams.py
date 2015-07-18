import sys
import math

''' dictionary with
		key: tuples for trigrams (tag1, tag2, tag3)
		value: count for trigram tuple
'''
allTrigrams = {}

''' dictionary with
		key: tuples for bigrams (tag1, tag2)
		value: count for bigram tuple
'''
allBigrams = {}

''' dictionary with
		key: tuples for trigrams (tag1, tag2, tag3)
		value: log value of q(tag3 | tag1, tag2)
'''
qValues = {}

def getQParamValues():
	"""
	Generates a text file qParamValues.txt conatining log values of q parameters in the format:
			<Tag1> <Tag2> <Tag3> <log value of q(Tag3 | Tag1, Tag2)>
	"""

	f = open('qParamValues.txt', 'w')

	tags = ['*', 'I-ORG', 'B-LOC', 'I-LOC', 'I-PER', 'B-ORG', 'I-MISC', 'O', 'B-MISC', 'STOP']

	for tag1 in tags:
		if tag1=='STOP':
			continue
		for tag2 in tags:
			if tag2=='STOP':
				continue
			# if tag2 is *, make sure tag1 was also *
			if tag2=='*':
				if tag1!='*':
					continue
					
			for tag3 in tags:
				if tag3=='*':
					continue
				foundNum = 0
				foundDenom = 0
				thisBigram = (tag1, tag2)
				if thisBigram in allBigrams:
					foundDenom = 1
					bigramCount = allBigrams[thisBigram]
				
				thisTrigram = (tag1, tag2, tag3)
				if thisTrigram in allTrigrams:
					foundNum = 1
					trigramCount = allTrigrams[thisTrigram]

				if foundNum and foundDenom:
					qValues[thisTrigram] = math.log(trigramCount/bigramCount)
				else:
					qValues[thisTrigram] = -1000000

				f.write(tag1 + ' ' + tag2 + ' ' + tag3 + ' ' + str(qValues[thisTrigram]) + '\n')


def readTestTrigrams():
	"""
	Reads lines of space-separated tag trigrams 
		<Tag1> <Tag2> <Tag3>
	and prints log value of q(Tag3 | Tag1, Tag2)
	"""

	for line in sys.stdin:
		line = line.strip().split(' ')
		desiredCount = qValues[qValues.index(line) + 1]
		print desiredCount

def readCountsFile(counts_filename):
	"""
	Reads the counts_filename and populates the dictionaries allTrigrams and allBigrams
	"""

	counts_file = file(counts_filename, 'r')

	count = 0
	for line in counts_file:
		line = line.strip()
		words = line.split(' ')
		if words[1]=='2-GRAM':
			temp = tuple(words[2:])
			allBigrams[temp] = float(words[0])
		elif words[1]=='3-GRAM':
			temp = tuple(words[2:])
			allTrigrams[temp] = float(words[0])

def usage():
	print """
	python 5a_getQParams.py [counts_file]

	Reads a file containing WORDTAG and N-GRAM counts
	and generates a text file conatining log values of q parameters in the format:
			<Tag1> <Tag2> <Tag3> <log value of q(Tag3 | Tag1, Tag2)>
	"""

if __name__ == "__main__":

	if len(sys.argv)!=2: # Expect exactly one argument
		usage()
		sys.exit(2)

	counts_file = sys.argv[1]
	readCountsFile(counts_file)

	getQParamValues()
	# readTestTrigrams()