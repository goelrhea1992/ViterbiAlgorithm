Natural Language Processing
Programming Assignment 1
(Rhea Goel, rg2936)
——————————————————————————————————————————————————————————————————————————————————————————

Assignment Report: [NLP] Programming Assignment 1 - Report.pdf
——————————————————————————————————————————————————————————————————————————————————————————

Script that executes all questions: run.sh

Running Instructions:

	./run.sh

——————————————————————————————————————————————————————————————————————————————————————————

Python scripts included:

	- count_freqs.py 
		- Input: a training data file
		- Output: WORDTAG, and N-GRAM counts

	- replaceTrainWith_RareOrFancy.py
		- Input: a file conatining WORDTAG and N-GRAM counts, a training data file, and a string 'rare' or 'fancy'
			('rare' - to replace infrequent (count < 5) words with _RARE_
			'fancy' - to replace infrequent (count <5) words with _NUM_, _CAPS_DOTS_, _CAPITALIZED_, and _RARE_)
		- Output: new training data with words replaced with desired categories in the format:
			<Word> <Tag>

	- getEmissionParams.py
		- Input: a file containing WORDTAG and N-GRAM counts
		- Output: Generates a text file containing log values of emission parameters in the format:
			<Tag> <Word> <log value of emission(Word | Tag)>

	- baselineNamedEntityTagger.py
		- Input: development data file
		- Output: tags for words in the development data file, predicted using the emission parameters, in the format:
			<Word> <Tag> <log value of emission(Word | Tag)>

	- eval_ne_tagger.py
		- Input: annotated development data file and file with predicted output in the format 
		<word> <Tag> <<log value of emission probability>
		- Output: Total Precision, Recall and F-measure, and for different tags

	- 5a_getQParams.py
		- Input: a file containing WORDTAG and N-GRAM counts
		- Output: Generates a text file conatining log values of q parameters in the format:

		For every trigram (Tag1, Tag2, Tag3), files contains a line of the form:
			<Tag1> <Tag2> <Tag3> <log value of q(Tag3 | Tag1, Tag2)>

	- 5b_viterbi.py 
		- Input: development data file, a file conatining WORDTAG and N-GRAM counts
		- Output: tags for word in the development data file, predicted using Viterbi Algorithm, in the format:
			<Word> <Tag> <log-probability of the tagged sequence up to this Word>



