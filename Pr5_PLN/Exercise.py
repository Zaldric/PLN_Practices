import nltk
import re
from nltk.parse.stanford import StanfordDependencyParser

if __name__ == '__main__':

    path_to_jar = './stanford-parser-full-2018-02-27/stanford-parser.jar'
    path_to_models = 'stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models.jar'
    model_path = 'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'

    dependency_parser = StanfordDependencyParser(path_to_jar, path_to_models, model_path, java_options='-mx2048m')
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    with open('carroll-alice.txt') as file:
        text = file.read().lower()

    text = " ".join(re.sub('\n', ' ', text).split())
    sentences = sentence_tokenizer.tokenize(text)
    print(str(len(sentences)))

    nominal_subjects = {}  # nsubj
    direct_objects = {}  # dobj
    negations_count = {}
    negation_modifiers = []  # neg
    adjectival_modifiers = {}  # amod

    for sentence in sentences:
        iterator = dependency_parser.raw_parse(sentence)
        for dep in iterator:
            categories = list(dep.triples())
        for first, second, third in categories:
            if second == 'nsubj':
                if third[0] not in nominal_subjects:
                    nominal_subjects[third[0]] = 1
                else:
                    nominal_subjects[third[0]] = nominal_subjects[third[0]] + 1
            if second == 'dobj':
                if third[0] not in direct_objects:
                    direct_objects[third[0]] = 1
                else:
                    direct_objects[third[0]] = direct_objects[third[0]] + 1
            if second == 'neg':
                if third[0] not in negations_count:
                    negations_count[third[0]] = 1
                else:
                    negations_count[third[0]] = negations_count[third[0]] + 1
                negation_modifiers.append([third[0], first[0]])
            if second == 'amod':
                if third[0] not in adjectival_modifiers:
                    adjectival_modifiers[third[0]] = 1
                else:
                    adjectival_modifiers[third[0]] = adjectival_modifiers[third[0]] + 1

    print('Top 5 most frequent nominal subjects: ')
    for key, value in sorted(nominal_subjects.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(key + ': ' + str(value))
    print()

    print('Top 5 most frequent negations: ')
    number = 1
    for key, value in sorted(negations_count.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(str(number) + '- ' + key + ': ' + str(value))
        print("\t Top 3 words affected by the negation '" + key + "':")
        affected_words = {}
        for negation, word in negation_modifiers:
            if negation == key:
                if word not in affected_words:
                    affected_words[word] = 1
                else:
                    affected_words[word] = affected_words[word] + 1
        for word, frequency in sorted(affected_words.items(), key=lambda x: x[1], reverse=True)[:3]:
            print('\t \t' + word + ': ' + str(frequency))
        number += 1
    print()

    print('Top 5 most frequent direct objects: ')
    for key, value in sorted(direct_objects.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(key + ': ' + str(value))
    print()

    print('Top 5 most frequent adjectival modifiers: ')
    for key, value in sorted(adjectival_modifiers.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(key + ': ' + str(value))
