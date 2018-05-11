from lxml import etree
from nltk.tokenize import sent_tokenize
from time import time
import os

if __name__ == '__main__':

    initial_time = time()
    corruptedFiles = []
    sentencesCount = 0
    processedFiles = 0

    for path in os.listdir('MCE-corpus'):

        try:
            parser = etree.XMLParser(recover=True)
            tree = etree.parse('MCE-corpus/' + path, parser)
            root = tree.getroot()
            sentences = sent_tokenize(root.find('body').text)
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
