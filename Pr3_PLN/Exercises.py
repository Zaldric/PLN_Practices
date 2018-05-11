import nltk
import os

from contextlib import redirect_stdout
from nltk import WhitespaceTokenizer, FreqDist, re
from nltk.corpus import stopwords
from nltk.text import Text
from operator import itemgetter

if __name__ == '__main__':

    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    english_stops = set(stopwords.words('english'))
    readability = []

    with open('files.txt', 'r') as files:
        for text_file in files.readlines():

            current_file = text_file.split('.')[0]
            text_file = re.sub('\n', '', text_file)

            if not os.path.exists(current_file):
                os.makedirs(current_file)

            print(text_file + ': ')
            print()

            with open(text_file, 'r') as file:
                text_content = file.read().lower()

            tokenizer = WhitespaceTokenizer()
            tokens = tokenizer.tokenize(text_content)
            text = Text(tokens)
            total_words = len(text)

            with open(current_file + '/occurrences.txt', 'w') as file:
                with redirect_stdout(file):
                    text.concordance('girl')

            with open(current_file + '/occurrences.txt', 'r') as file:
                print(
                    'There are ' + file.readline().split()[
                        1] + " occurrences of 'girl' in the text, you can check them in "
                             "file 'occurrences.txt'.")
            # Vocabulary

            with open(current_file + '/vocabulary.txt', 'w') as file:
                with redirect_stdout(file):
                    for word, frequency in text.vocab().items():
                        print(word + ': ' + str(frequency))

            print("The text's vocabulary has " + str(len(text.vocab())) + " words, you can check them in the file "
                                                                          "'vocabulary.txt'.")

            # Top 10 frequent words

            print()
            print('Top 10 frequent words: ')
            frequent_words_list = FreqDist(text).most_common(10)

            for word, frequency in frequent_words_list:
                print('\t' + word + ': ' + str(frequency) + ' times.')

            print()
            print('Top 10 frequent words after cleaning the text: ')

            cleaned_tokens = tokenizer.tokenize(' '.join(re.sub('[,\.;"\':\[\]()¿?!¡\n]', ' ', text_content).split()))
            cleaned_text = Text(cleaned_tokens)

            filtered_tokens = [token for token in cleaned_tokens if token not in english_stops]
            filtered_frequent_words_list = FreqDist(filtered_tokens).most_common(10)

            for word, frequency in filtered_frequent_words_list:
                print('\t' + word + ': ' + str(frequency) + ' times.')

            # Four words with mayor similarity to the most frequent word

            print()
            with open(current_file + '/similarity_for_filtered_words.txt', 'w') as file:
                with redirect_stdout(file):
                    text.similar([word[0] for word in filtered_frequent_words_list][0], 4)

            print('Four words with mayor similarity (filtered tokens): ')
            with open(current_file + '/similarity_for_filtered_words.txt', 'r') as file:
                i = 1
                for similar_word in file.readline().split():
                    print(str(i) + '. ' + similar_word + '.')
                    i = i + 1

            # Four words with mayor similarity to the most frequent word (without filtering) and dispersion diagram

            print()
            with open(current_file + '/similarity.txt', 'w') as file:
                with redirect_stdout(file):
                    text.similar([word[0] for word in frequent_words_list][0], 4)

            print('Four words with mayor similarity (without filtering): ')
            similar_words_list = []
            with open(current_file + '/similarity.txt', 'r') as file:
                i = 1
                similar_words_list.append([word[0] for word in frequent_words_list][0])
                for similar_word in file.readline().split():
                    print(str(i) + '. ' + similar_word + '.')
                    similar_words_list.append(similar_word)
                    i = i + 1
                text.dispersion_plot(similar_words_list)
            # Proportion of the text occupied by the 50 most frequent words

            print()
            print("Proportion of the text occupied by the 50 most frequent words (without filtering): ")
            fdist = FreqDist(text)
            most_common = fdist.most_common(50)
            fdist.plot(50, cumulative=True)

            print()
            print("Proportion of the text occupied by the 50 most frequent words (filtered): ")
            fdist = FreqDist(filtered_tokens)
            most_common = fdist.most_common(50)
            fdist.plot(50, cumulative=True)

            # ARI

            characters = len("".join(text_content.split()))
            sentences = len(sentence_tokenizer.tokenize(text_content))

            score = round((4.71 * (characters / total_words)) + (0.5 * (total_words / sentences)) - 21.43)

            print('ARI score: ' + str(score))
            readability.append([current_file, score])
            print()

    readability = sorted(readability, key=itemgetter(1))

    print('Readability of the texts (easiest to hardest): ')

    i = 1
    with open('readability.txt', 'w') as file:
        for key, value in readability:
            print(str(i) + '. ' + key + ': ' + str(value))
            file.write(key + ': ' + str(value) + '\n')
            i = i + 1



