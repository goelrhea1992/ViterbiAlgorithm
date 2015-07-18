#!/bin/sh

echo
echo '--------------------------------------------------------------------'
echo 'Problem 4.'
echo '--------------------------------------------------------------------\n'
echo '1. Running count_freqs.py on original training data.....'
python count_freqs.py ner_train.dat > output/ner.counts
echo '---> Generated ner.counts\n'

echo '2. Replacing infrequent words with _RARE_ in the training data....'
python replaceTrainWith_RareOrFancy.py output/ner.counts ner_train.dat rare > output/ner_train_rare.dat
echo '---> Generated ner_train_rare.dat\n'

echo '3. Running count_freqs.py on new training data.....'
python count_freqs.py output/ner_train_rare.dat > output/ner.counts.rare
echo '---> Generated ner.counts.rare\n'

echo '4. Computing emission parameters (log values).....'
python getEmissionParams.py output/ner.counts.rare
echo '---> Generated emissionParamsRare.txt\n'

echo '5. Implementing baseline (max-emission) named entity tagger.....'
python baselineNamedEntityTagger.py ner_dev.dat > output/predicted_output
echo '---> Generated predicted_output\n'

echo '6. Evaluating predicted output....'
python eval_ne_tagger.py ner_dev.key output/predicted_output
echo

echo '--------------------------------------------------------------------'
echo 'Problem 5.'
echo '--------------------------------------------------------------------\n'
echo '7. Computing q parameters (log values).....'
python 5a_getQParams.py output/ner.counts.rare
echo '---> Generated qParamValues.txt\n'

echo '8. Running Viterbi Algorithm.....'
echo '(Takes about a minute)'
python 5b_viterbi.py ner_dev.dat output/ner.counts.rare > output/predicted_output_new
echo '---> Generated predicted_output_new\n'

echo '9. Evaluating predicted output.....'
python eval_ne_tagger.py ner_dev.key output/predicted_output_new
echo

echo '--------------------------------------------------------------------'
echo 'Problem 6.'
echo '--------------------------------------------------------------------\n'
echo '10. Replacing infrequent words with _RARE_, _CAPS_DOTS_, _NUM_, _CAPITALIZED_ in the training data....'
python replaceTrainWith_RareOrFancy.py output/ner.counts ner_train.dat fancy > output/ner_train_fancy.dat
echo '---> Generated ner_train_fancy.dat\n'

echo '11. Repeating the procedure and running Viterbi Algorithm.....'
echo '(Takes about 2 minutes)'
python count_freqs.py output/ner_train_fancy.dat > output/ner.counts.fancy
python getEmissionParams.py output/ner.counts.fancy
python 5b_viterbi.py ner_dev.dat output/ner.counts.fancy > output/predicted_output_newFancy
python eval_ne_tagger.py ner_dev.key output/predicted_output_newFancy
echo














