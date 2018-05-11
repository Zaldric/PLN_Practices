from pathlib import Path


def generate_sum():
    file1 = Path('./fichero1.txt')

    if not file1.is_file():
        return 'File \"fichero1.txt\" is missing'

    file2 = Path('./fichero2.txt')

    if not file2.is_file():
        return 'File \"fichero2.txt\" is missing'

    with open('./fichero1.txt') as file1, open('./fichero2.txt') as file2:
        num_lines1 = sum(1 for line in open('fichero1.txt'))
        num_lines2 = sum(1 for line in open('fichero2.txt'))

        if num_lines1 != num_lines2:
            return 'Error: files must have the same length.'

    with open('./fichero1.txt') as file1, open('./fichero2.txt') as file2, open('./fichero_suma.txt', 'w') as file3:

        lineCount = 1

        for file1_line, file2_line in zip(file1, file2):

            lineFile1 = file1_line.rstrip('\n')
            lineFile2 = file2_line.rstrip('\n')

            if len(lineFile1.split(' ')) > 1 or len(lineFile2.split(' ')) > 1:
                return 'Error: the files must have a single value per line.'

            if lineFile1 == '':
                return 'Error: the files are empty.'

            if not lineFile1.replace('.', '', 1).isdigit() or not lineFile2.replace('.', '', 1).isdigit():
                return 'All the lines of the files must be numbers.'
            else:
                if lineCount < num_lines1:
                    file3.write('{0:g}'.format(float(lineFile1) + float(lineFile2)) + '\n')
                    lineCount += 1
                else:
                    file3.write(str(float(lineFile1) + float(lineFile2)))

    return 'Operation finished.'


if __name__ == '__main__':

    print(generate_sum())
