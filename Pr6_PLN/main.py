import nltk
import re
import os

from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk

if __name__ == '__main__':

    if os.path.isfile('./carroll-alice.txt'):

        tokenizer = TreebankWordTokenizer()
        _POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
        sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        tagger = nltk.data.load(_POS_TAGGER)

        with open('carroll-alice.txt') as file:
            text = file.read()
            tags = tagger.tag(tokenizer.tokenize(text.lower()))
            adjectives = nltk.FreqDist(word for (word, tag) in tags if tag == 'JJ' or tag == 'JJR' or tag == 'JJS')
            most_frequent_adjective = adjectives.most_common(1)
            print("The most frequent adjective is " + str(most_frequent_adjective[0][0]) + ' with ' +
                  str(most_frequent_adjective[0][1]) + ' occurrences')

        # Exercise 1

        sentences = sentence_tokenizer.tokenize(text)
        substitutions = {}

        with open('carroll-alice-synonyms.txt', 'w') as file:
            for sentence in sentences:
                sent = tokenizer.tokenize(sentence.lower())
                tags = tagger.tag(sent)
                for word, tag in tags:
                    if tag == 'JJ' or tag == 'JJR' or tag == 'JJS':
                        correct_sense = lesk(sent, word, 'a')
                        correct_sense = re.sub("Synset\('", '', str(correct_sense))
                        correct_sense = re.sub("'.*\)", '', str(correct_sense))
                        correct_sense = correct_sense.split('.')[0]

                        if correct_sense != 'None' and correct_sense != word:
                            my_tuple = (word, correct_sense)
                            sentence.replace(word, correct_sense)
                            if substitutions.get(my_tuple) is None:
                                substitutions[(word, correct_sense)] = 1
                            else:
                                substitutions[(word, correct_sense)] = substitutions[(word, correct_sense)] + 1
                        else:
                            correct_sense = lesk(sent, word, 's')
                            correct_sense = re.sub("Synset\('", '', str(correct_sense))
                            correct_sense = re.sub("'.*\)", '', str(correct_sense))
                            correct_sense = correct_sense.split('.')[0]

                            if correct_sense != 'None' and correct_sense != word:
                                my_tuple = (word, correct_sense)
                                sentence.replace(word, correct_sense)
                                if substitutions.get(my_tuple) is None:
                                    substitutions[(word, correct_sense)] = 1
                                else:
                                    substitutions[(word, correct_sense)] = substitutions[(word, correct_sense)] + 1
                file.write(sentence + '\n')

        with open('results.txt', 'w') as file:
            for pair in substitutions:
                file.write(str(pair) + ': ' + str(substitutions[pair]) + '\n')

        # Exercise 2

        print('Senses of the word ' + most_frequent_adjective[0][0] + ':')
        senses = []
        for ss in wn.synsets(most_frequent_adjective[0][0]):
            print('\t', ss, ss.definition())
            ss = re.sub("Synset\('", '', str(ss))
            ss = re.sub("'\)", '', str(ss))
            senses.append(ss)

        print()
        print('Synonyms of the word ' + most_frequent_adjective[0][0] + ':')
        synonyms = set()
        for sense in senses:
            for lemma in wn.synset(sense).lemma_names():
                if lemma != most_frequent_adjective[0][0]:
                    synonyms.add(lemma)

        for synonym in synonyms:
            print('\t' + synonym)

        print()
        print('Antonyms of the word ' + most_frequent_adjective[0][0] + ':')
        for sense in senses:
            for lemma in wn.synset(sense).lemmas():
                if lemma.antonyms():
                    print('\t' + lemma.antonyms()[0].name())

    else:
        print('carroll-alice.txt not found, please add the file to the program directory and try again.')
