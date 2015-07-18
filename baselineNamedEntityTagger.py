import sys
import operator
import math

def useDumbTagger(dev_filename):
    """
    Prints tags for words in the development data file, predicted using the emission parameters, in the format:
            <Word> <Tag> <log value of emission(Word | Tag)>
    """

    dev_file = file(dev_filename,"r")
    
    ''' dictionary with
            key: <word>
            value: <frequency of word in the dev file>
    '''
    dict = {}
    for word in dev_file:
        word = word.strip();
        if word:
            if dict.has_key(word):
                dict[word] = dict[word] + 1
            else:
                dict[word] = 1

    refDict = {}
    f = open('emissionParamsRare.txt', 'r')
    for line in f:
        line = line.strip()
        myList = line.split(' ')
        if refDict.has_key(myList[1]):
            temp = refDict[myList[1]]
            temp[myList[0]] = float(myList[2])
        else:
            temp = {}
            temp[myList[0]] = float(myList[2])
            refDict[myList[1]] = temp

    dev_file = file(dev_filename,"r")
    for word in dev_file:
        word = word.strip()
        if word:
            count = dict[word]
            if (refDict.has_key(word) == 0):
                temp = refDict['_RARE_']
            elif refDict.has_key(word):
                temp = refDict[word]
            print word, max(temp.iteritems(), key=operator.itemgetter(1))[0], max(temp.iteritems(), key=operator.itemgetter(1))[1]
        else:
            print


def usage():
    print """
    python baselineNamedEntityTagger.py [dev_dat_file] > [predicted_output]

    Reads in a development data file and generates tags for words in the development data file, 
    predicted using the emission parameters, in the format:

        <Word> <Tag> <log value of emission(Word | Tag)>
    """

if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly one argument
        usage()
        sys.exit(2)

    try:
        input = sys.argv[1]
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)

    useDumbTagger(input)