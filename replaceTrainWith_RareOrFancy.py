import sys
import re

def patternOf(category):
	"""
	Returns Pattern object of regular expression for words of type category
	"""
	if category == '_NUM_':
		return re.compile('^[0-9]+$')
	elif category == '_CAPS_DOTS_':
		return re.compile('^[A-Z\.]+$')
	elif category == '_CAPITALIZED_':
		return re.compile('^[A-Z].*')

def replaceRare_Fancy(countsFile, trainFile, replaceWith):
	"""
	Prints new training data with words replaced with desired categories in the format:
			<Word> <Tag>
	where Word can be the original word, or '_RARE_', if replaceWith is 'rare'
	   or Word can be the original word, '_RARE_', '_NUM_', '_CAPS_DOTS_', or '_CAPITALIZED_', if replaceWith is 'fancy'
	"""

	f = open(countsFile, 'r')
	
	''' dictionary with 
		key: <Tag>
		value: dictionary with 
				key: <word>
				value: <count of (Tag, word) pair>
	'''
	outer = {}

	for line in f:
		words = line.strip().split(' ')
		if words[1] == 'WORDTAG':
			if outer.has_key(words[2]):
				temp = outer[words[2]]
				if temp.has_key(words[3]):
					temp[words[3]] = temp[words[3]] + float(words[0])
				else:
					temp[words[3]] = float(words[0])
			else:
				outer[words[2]] = {}
				outer[words[2]][words[3]] = float(words[0])

	f.close()
	f = open(trainFile,'r')

	for line in f:
		line = line.strip()
		if line:
			words = line.split(' ')
			thisWord = words[0]
			thisWordCount = 0

			for tag in outer.keys():
				temp = outer[tag]
				if temp.has_key(thisWord):
					thisWordCount = thisWordCount + temp[thisWord]
					continue

			if thisWordCount<5:
				if replaceWith == 'rare':
					print '_RARE_ ', words[1]

				elif replaceWith == 'fancy':
					if patternOf('_NUM_').match(thisWord):
						print '_NUM_ ', words[1]
					elif patternOf('_CAPITALIZED_').match(thisWord):
						print '_CAPITALIZED_ ', words[1]
					elif patternOf('_CAPS_DOTS_').match(thisWord):
						print '_CAPS_DOTS_ ', words[1]
					else:
						print '_RARE_ ', words[1]
			else:
				print line
		else:
			print

def usage():
    print """
    python replaceTrainWith_RareOrFancy.py [counts_file] [training_file] [rare/fancy] > [new_training_file]
        Reads in a file conatining WORDTAG and N-GRAM counts, a training data file, and a string 'rare' or 'fancy'
			'rare' - to replace infrequent (count < 5) words with _RARE_
			'fancy' - to replace infrequent (count <5) words with _NUM_, _CAPS_DOTS_, _CAPITALIZED_, and _RARE_)
		
		Generates new training data with words replaced with desired categories in the format:
			<Word> <Tag>
    """

if __name__ == "__main__":

    if len(sys.argv)!=4: # Expect exactly three arguments
        sys.exit(2)
    countsFile = sys.argv[1]
    trainFile = sys.argv[2]
    replaceWith = sys.argv[3]

    replaceRare_Fancy(countsFile, trainFile, replaceWith)



