import os
import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.chunk import tree2conlltags

if __name__ == '__main__':

    if os.path.isfile('./nyt.txt'):

        tokenizer = TreebankWordTokenizer()
        sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        _POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
        _BINARY_NE_CHUNKER = 'chunkers/maxent_ne_chunker/english_ace_binary.pickle'
        _MULTICLASS_NE_CHUNKER = 'chunkers/maxent_ne_chunker/english_ace_multiclass.pickle'
        binary_ner = nltk.data.load(_BINARY_NE_CHUNKER)
        multiclass_ner = nltk.data.load(_MULTICLASS_NE_CHUNKER)
        tagger = nltk.data.load(_POS_TAGGER)

        with open('nyt.txt', encoding='utf-8', errors='ignore') as file:
            text = file.read()

        sentences = sentence_tokenizer.tokenize(text)
        persons = {}
        organizations = {}
        locations = {}
        geopolitical_entities = {}
        groups = {}
        facilities = {}
        multi_word = ''

        for sentence in sentences:

            tags = tagger.tag(tokenizer.tokenize(sentence))
            ne_tree_multiclass = multiclass_ner.parse(tags)
            iob_tagged_multiclass = tree2conlltags(ne_tree_multiclass)

            for current, next_value in zip(iob_tagged_multiclass, iob_tagged_multiclass[1:]):

                entity, category, next_entity, next_category = current[0], current[2], next_value[0], next_value[2]

                if 'B-' in category and next_category != 'O':
                    multi_word = entity
                    continue

                if 'I-' in category and next_category != 'O':
                    multi_word = multi_word + ' ' + entity
                    continue

                if 'I-' in category:
                    multi_word = multi_word + ' ' + entity

                if multi_word != '':
                    entity = multi_word

                if 'PERSON' in category:
                    if entity not in persons:
                        persons[entity] = 1
                    else:
                        persons[entity] = persons[entity] + 1

                if 'ORGANIZATION' in category:
                    if entity not in organizations:
                        organizations[entity] = 1
                    else:
                        organizations[entity] = organizations[entity] + 1

                if 'LOCATION' in category:
                    if entity not in locations:
                        locations[entity] = 1
                    else:
                        locations[entity] = locations[entity] + 1

                if 'GPE' in category:
                    if entity not in geopolitical_entities:
                        geopolitical_entities[entity] = 1
                    else:
                        geopolitical_entities[entity] = geopolitical_entities[entity] + 1

                if 'GSP' in category:
                    if entity not in groups:
                        groups[entity] = 1
                    else:
                        groups[entity] = groups[entity] + 1

                if 'FACILITY' in category:
                    if entity not in facilities:
                        facilities[entity] = 1
                    else:
                        facilities[entity] = facilities[entity] + 1

                multi_word = ''

        with open('results.txt', 'w') as file:

            if persons:
                file.write('People: \n')
                for key, value in persons.items():
                    file.write('\t' + key + ': ' + str(value) + '\n')
            else:
                file.write('No Person entities found in the text.\n')
            file.write('\n')

            if organizations:
                file.write('Organizations: \n')
                for key, value in organizations.items():
                    file.write('\t' + key + ': ' + str(value) + '\n')
            else:
                file.write('No Organization entities found in the text. \n')
            file.write('\n')

            if locations:
                file.write('Locations: \n')
                for key, value in locations.items():
                    file.write('\t' + key + ': ' + str(value) + '\n')
            else:
                file.write('No Location entities found in the text. \n')
            file.write('\n')

            if geopolitical_entities:
                file.write('Geopolitical entities: \n')
                for key, value in geopolitical_entities.items():
                    file.write('\t' + key + ': ' + str(value) + '\n')
            else:
                file.write('No Geopolitical entities found in the text. \n')
            file.write('\n')

            if groups:
                file.write('Geo-social-political groups: \n')
                for key, value in groups.items():
                    file.write('\t' + key + ': ' + str(value) + '\n')
            else:
                file.write('No Geo-social-political entities found in the text.\n')
            file.write('\n')

            if facilities:
                file.write('Facilities: \n')
                for key, value in facilities.items():
                    file.write('\t' + key + ': ' + str(value) + '\n')
            else:
                file.write('No Facilities entities found in the text.\n')
            file.write('\n')

        print('Top 2 most frequent persons: ')
        for key, value in sorted(persons.items(), key=lambda x: x[1], reverse=True)[:2]:
            print(key + ': ' + str(value))
        print()

        print('Top 3 most frequent geopolitical entities: ')
        for key, value in sorted(geopolitical_entities.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(key + ': ' + str(value))
    else:
        print('nyt.txt not found, please add the file to the program directory and try again.')
