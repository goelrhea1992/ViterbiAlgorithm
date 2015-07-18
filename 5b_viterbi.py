import sys
import math
import re

''' dictionaty with 
    key: <Tag>
    value: dictionary with 
                key: <Word>
                value: <log value of emission(Word | Tag)>
'''
emissionValues = {}

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

''' 
list of all sentences in the development data file
'''
allSentences = []

def patternOf(category):
    """
    Returns Pattern object of regular expression for words of type category
    """

    if category == '_NUM_':
        return re.compile('^[0-9]+$')
    elif category == '_CAPS_DOTS_':
        return re.compile('^[A-Z|\.]+$')
    elif category == '_CAPITALIZED_':
        return re.compile('^[A-Z].*')

def getQValues():
    """
    Populates the dictionary qValues
    """

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

def getTrigrams(counts_filename):
    """
    Reads the counts_filename and populates the dictionary allTrigrams
    """
    counts_file = file(counts_filename, 'r')
    for line in counts_file:
        line = line.strip()
        words = line.split(' ')
        if words[1]=='3-GRAM':
            temp = tuple(words[2:])
            allTrigrams[temp] = float(words[0])


def getBigrams(counts_filename):
    """
    Reads the counts_filename and populates the dictionary allBigrams
    """
    counts_file = file(counts_filename, 'r')
    for line in counts_file:
        line = line.strip()
        words = line.split(' ')
        if words[1]=='2-GRAM':
            temp = tuple(words[2:])
            allBigrams[temp] = float(words[0])

def getEmissionValues(counts_file):
    """
    Reads the appropriate emissionParams text file and populates the dictionary emissionValues
        Reads emissionParamsRare.txt: if counts_file name contains 'rare'
        Reads emissionParamsFancy.txt: if counts_file name contains 'fancy'
        Reads emissionParams.txt: otherwise
    """

    if 'rare' in counts_file:
        desiredFile = 'emissionParamsRare.txt'
    elif 'fancy' in counts_file:
        desiredFile = 'emissionParamsFancy.txt'
    else:
        desiredFile = 'emissionParams.txt'

    f = open(desiredFile, 'r')
    for line in f:
        line = line.strip()
        myList = line.split(' ')
        if emissionValues.has_key(myList[1]):
            temp = emissionValues[myList[1]]
            temp[myList[0]] = float(myList[2])
        else:
            temp = {}
            temp[myList[0]] = float(myList[2])
            emissionValues[myList[1]] = temp

def getAllSentences(input_file):
    """
    Reads the developement data input_file, and populates the list allSentences
    """

    f = open(input_file, "r")
    thisSentence = []
    for word in f:
        word = word.strip()
        # print word
        if word:
            thisSentence.append(word)
        else:
            allSentences.append(thisSentence)
            thisSentence = []

def viterbiAlgo(input_file, counts_file):
    """
    Prints tags for each word in the development data file, using Viterbi Algorithm, in the format:
            <Word> <Tag> <log-probability of the tagged sequence up to this Word>   
    """

    getAllSentences(input_file)

    for sentence in allSentences:
        k = 0

        ''' dictionary to store pi values in Viterbi Algorithm'''
        pi = {}

        ''' dictionary to store back pointers in Viterbi Algorithm'''
        bp = {}

        ''' storing log value of pi'''
        pi[(k,'*','*')] = 0        

        ''' list representing the set K in Viterbi Algorithm, where K[i] is a set of tags allowed at position i'''
        K = []
        K.append(['*'])
        
        for i in range(1, len(sentence)+1):
            K.append(['I-ORG', 'B-LOC', 'I-LOC', 'I-PER', 'B-ORG', 'I-MISC', 'O', 'B-MISC'])

        for k in range(1, len(sentence)+1):
            x = sentence[k-1]
            for v in K[k]:
                for u in K[k-1]:
                    if k==1:
                        possibleTags_atMinus2 = ['*']
                    else:
                        possibleTags_atMinus2 = K[k-2]
                    for w in possibleTags_atMinus2:

                        if emissionValues.has_key(x)==0:
                            if 'fancy' in counts_file:
                                if patternOf('_NUM_').match(x):
                                    x = '_NUM_'
                                elif patternOf('_CAPITALIZED_').match(x):
                                    x = '_CAPITALIZED_'
                                elif patternOf('_CAPS_DOTS_').match(x):
                                    x = '_CAPS_DOTS_'
                                else:
                                    x = '_RARE_'
                                
                                if emissionValues.has_key(x)==0:
                                    x = '_RARE_'
                            else:
                                x = '_RARE_'

                        if emissionValues[x].has_key(v)==0:
                                emissionValues[x][v] = -1000000

                        thisVal = pi[(k-1, w, u)] + qValues[(w,u,v)] + emissionValues[x][v]
                        if pi.has_key((k,u,v)):
                            if thisVal > pi[(k,u,v)]:
                                pi[(k,u,v)] = thisVal
                                bp[(k,u,v)] = (k-1, w, u)
                        else:
                            pi[(k,u,v)] = thisVal
                            bp[(k,u,v)] = (k-1, w, u)

        resultsDict = {}

        for key, val in pi.iteritems():
            if k==key[0]:
                qStop = qValues[(u,v,'STOP')]
                currVal = val + qStop
                if k in resultsDict:
                    if currVal > resultsDict[k][1]:
                        resultsDict[k] = (key[2], currVal)
                        resultsDict[k-1] = (key[1], currVal)
                else:
                    resultsDict[k] = (key[2], currVal)
                    resultsDict[k-1] = (key[1], currVal)

        for i in range(k-2, 0, -1):
            currBP = bp[(i+2, resultsDict[i+1][0], resultsDict[i+2][0])]
            currVal = pi[(i+2, resultsDict[i+1][0], resultsDict[i+2][0])]
            resultsDict[i] = (currBP[1], currVal)

        for i in range(1, len(sentence)+1):
            print sentence[i-1] + ' ' + str(resultsDict[i][0])+ ' ' +str(resultsDict[i][1])

        print

def usage():
    print """
    python 5b_viterbi.py [dev_data_file] [counts_file] > [predicted_output_new]
    
    Reads in a development data file, and a file conatining WORDTAG and N-GRAM counts
    and generates tags for word in the development data file, predicted using Viterbi Algorithm, in the format:
            <Word> <Tag> <log-probability of the tagged sequence up to this Word>    
    """

if __name__ == "__main__":

    if len(sys.argv)!=3: # Expect exactly two arguments
        usage()
        sys.exit(2)
    dev_datafile = sys.argv[1]
    counts_file = sys.argv[2]

    getEmissionValues(counts_file)
    getTrigrams(counts_file)
    getBigrams(counts_file)
    getQValues()
    viterbiAlgo(dev_datafile, counts_file)
