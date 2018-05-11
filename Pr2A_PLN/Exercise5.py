import re


def tokenizer(input_sentence):
    cleaned_sentence = re.sub('[,\.;:\[\]()¿?!¡\n]', '', input_sentence)
    return cleaned_sentence.split()


if __name__ == '__main__':

    sentence = input('Please introduce a sentence to tokenize: ')
    sentenceTokens = tokenizer(sentence)
    print('Number of tokens: ' + str(len(sentenceTokens)))
    print('Tokens: ')
    print(sentenceTokens)