import nltk
import codecs
import os
from nltk.tokenize import TreebankWordTokenizer

if __name__ == '__main__':

    if os.path.isdir('./SFU_Review_Corpus_Raw'):

        tokenizer = TreebankWordTokenizer()
        _POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
        tagger = nltk.data.load(_POS_TAGGER)
        content = ''

        for domain in os.listdir('./SFU_Review_Corpus_Raw'):
            domain_path = './SFU_Review_Corpus_Raw/' + domain
            if os.path.isdir(domain_path):
                total_tags, nouns, adjectives, verbs, adverbs = 0, 0, 0, 0, 0

                for comment in os.listdir(domain_path):
                    with codecs.open(domain_path + '/' + comment, "r", encoding='utf-8', errors='ignore') as file:
                        tags = tagger.tag(tokenizer.tokenize(file.read()))
                        tags_occurrences = list(nltk.FreqDist(tag for (word, tag) in tags).items())
                        total_tags += sum(second for _, second in tags_occurrences)
                        nouns += sum(second for first, second in tags_occurrences if
                                     first == 'NN' or first == 'NNS' or first == 'NNP' or first == 'NNPS')
                        adjectives += sum(second for first, second in tags_occurrences if
                                          first == 'JJ' or first == 'JJR' or first == 'JJS')
                        verbs += sum(second for first, second in tags_occurrences if
                                     first == 'VB' or first == 'VBD' or first == 'VBG' or first == 'VBN' or first == 'VBP' or first == 'VBZ')
                        adverbs += sum(second for first, second in tags_occurrences if
                                       first == 'RB' or first == 'RBR' or first == 'RBS')
                content += domain + ':\n' + '\tNouns:\t' + str(nouns) + ' (' + str(
                    round((nouns / total_tags) * 100, 2)) + '%).\n' + '\tAdjectives:\t' + str(adjectives) + ' (' + str(
                    round((adjectives / total_tags) * 100, 2)) + '%).\n' + '\tVerbs:\t' + str(verbs) + ' (' + str(
                    round((verbs / total_tags) * 100, 2)) + '%).\n' + '\tAdverbs:\t' + str(adverbs) + ' (' + str(
                    round((adverbs / total_tags) * 100, 2)) + '%).\n'

        print(content)
        with open('results.txt', 'w') as file:
            file.write(content)
    else:
        print('SFU corpus not found, please add the corpus to the program directory and try again.')
