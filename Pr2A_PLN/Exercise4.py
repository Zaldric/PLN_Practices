from nltk import WhitespaceTokenizer, SpaceTokenizer, WordPunctTokenizer, TreebankWordTokenizer

if __name__ == '__main__':

    tokenizer = TreebankWordTokenizer()

    print('Using TreebankWordTokenizer:')
    sentence = "Sorry, I can't go to the workbench meeting.\n"
    tokens = tokenizer.tokenize(sentence)
    print(tokens)
    print('Number of tokens: ' + str(len(tokens)))

    print()

    tokenizer = WhitespaceTokenizer()

    print('Using WhitespaceTokenizer:')
    tokens = tokenizer.tokenize(sentence)
    print(tokens)
    print('Number of tokens: ' + str(len(tokens)))

    print()

    tokenizer = SpaceTokenizer()

    print('Using SpaceTokenizerr:')
    tokens = tokenizer.tokenize(sentence)
    print(tokens)
    print('Number of tokens: ' + str(len(tokens)))

    print()

    tokenizer = WordPunctTokenizer()

    print('Using WordPunctTokenize:')
    tokens = tokenizer.tokenize(sentence)
    print(tokens)
    print('Number of tokens: ' + str(len(tokens)))