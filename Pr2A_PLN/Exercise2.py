from lxml import etree
from time import time
import nltk.data
import os

if __name__ == '__main__':

    corruptedFiles = []
    sentencesCount = 0
    processedFiles = 0
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    initial_time = time()

    for path in os.listdir('MCE-corpus'):

        try:
            parser = etree.XMLParser(recover=True)
            tree = etree.parse('MCE-corpus/' + path, parser)
            root = tree.getroot()
            sentences = sentence_tokenizer.tokenize(root.find('body').text)
            sentencesCount += len(sentences)
            processedFiles += 1
        except:
            corruptedFiles.append(path)

    final_time = time()

    print('The files has been processed.')
    print('Average number of sentences per comment: ' + str(round(sentencesCount / processedFiles, 2)))

    if len(corruptedFiles) > 0:
        print('The following files cannnot be processed: \n')
        for x in corruptedFiles:
            print(x)

    print()
    print('Execution time: ' + str(round(final_time - initial_time, 4)))