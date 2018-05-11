import nltk.data
import codecs
import os

from nltk import WhitespaceTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter

if __name__ == '__main__':

    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    english_stops = set(stopwords.words('english'))
    tokenizer = WhitespaceTokenizer()
    stemmer = PorterStemmer()

    for domain in os.listdir('./SFU_Review_Corpus_Raw'):
        domain_path = './SFU_Review_Corpus_Raw/' + domain
        if os.path.isdir(domain_path):
            print(domain + ':')
            domain_sentences = 0
            domain_tokens = 0
            domain_stop_words = 0
            domain_comments = 0
            token_list = []

            for comment in os.listdir(domain_path):
                domain_comments += 1
                with codecs.open(domain_path + '/' + comment, "r", encoding='utf-8', errors='ignore') as file:
                    sentences = sentence_tokenizer.tokenize(file.read())
                    domain_sentences += len(sentences)

                    for sentence in sentences:
                        tokens = tokenizer.tokenize(sentence)
                        filtered_tokens = [token for token in tokens if token not in english_stops]
                        token_list += filtered_tokens
                        stems = []
                        for filtered_token in filtered_tokens:
                            stems.append(stemmer.stem(filtered_token))
                        domain_tokens += len(tokens)
                        domain_stop_words += len(tokens) - len(filtered_tokens)
            print('Sentences: ' + str(domain_sentences))
            print('Tokens: ' + str(domain_tokens))
            print('Stop words: ' + str(domain_stop_words))
            print('Sentences per comment: ' + str(round(domain_sentences / domain_comments, 2)))
            print('Tokens per comment: ' + str(round(domain_tokens / domain_sentences, 2)))
            words = Counter(token_list)
            print('Top 5 words: ')
            for word, frequency in words.most_common(5):
                print('\t' + word + ': ' + str(frequency))
            print()
