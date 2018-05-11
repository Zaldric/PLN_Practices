if __name__ == '__main__':

    myInput = input('Please introduce a sentence: ')
    print('A E I O U')
    print(*map(myInput.lower().count, 'aeiou'))
