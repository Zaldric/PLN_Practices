if __name__ == '__main__':

    validation = False
    while not validation:
        myInput = input('Please introduce a value: ')
        if not myInput.isdigit():
            print('Error: \"' + str(myInput) + '\" is not a valid number, please enter an integer number.')
        else:
            if (int(myInput) % 2) == 1:
                print('Error: \"' + str(myInput) + '\" is not an even number.')
            else:
                validation = True
    print('Good job, \"' + str(myInput) + '\" is an even number, program finished.')