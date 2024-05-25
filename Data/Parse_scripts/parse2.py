# Parsed with this file: Math 21-22

year = '21-22'
fileName = 'Math'
directory = ("Data\\" 
            + year + "\\" + fileName + ".txt")

directoryOutput = directory[:-4] + '(2).txt'

#stringsSplit = ['Призёр', 'Победитель', 'Участник', '9 grade', '10 grade', '11 grade']
stringsSplit = ['призер', 'победитель', 'участник', '9 grade', '10 grade', '11 grade']

stringsFilter = ['№', 'п/п', 'Фамилия', 'имя', 'отчество', 'Субъект РФ', 'Наименование', 'Класс',
                'организации', 'обучения', 'Результат', '(баллы)', 'Статус', '/', 'участник)']

def anyInLine(strArray, line) -> bool:
    # make it lowercase to get compared better
    line = line.lower()
    strArray = map(str.lower, strArray)
    
    for string in strArray:
        if string in line:
            return True
        
    return False

def isInt(string) -> bool:
    try:
        a = int(string)
    except:
        return False
    else:
        return True
    
def parse():
    arrayLinesRes = []
    with open(directory, encoding='utf-8') as file:
        arrayLines = file.readlines()
        userLine = ''
        
        for line in arrayLines:
            # Split by first two words in a line. One word should be a rank, 
            # Second should be a last name
            
            if len(line.split()) > 1:
                first_word = line.split()[0]
                second_word = line.split()[1]
                if isInt(first_word) and not isInt(second_word):
                    arrayLinesRes.append(userLine + '\n')
                    userLine = ''
                    
            # Filter Values
            if anyInLine(stringsFilter, line):
                continue
            # Add to a line
            userLine += (' ' + line[:-1] + ' ')
            
        arrayLinesRes = arrayLinesRes[1:]

            

    with open(directoryOutput, 'w', encoding='utf-8') as file:
        file.writelines(arrayLinesRes)

def filter():
    arrayLinesRes = []
    with open(directory, encoding='utf-8') as file:
        arrayLines = file.readlines()
        for line in arrayLines:
            splitted_line = line.split(' ')
            if not isInt(splitted_line[1]):
                continue
            else:
                arrayLinesRes.append(line)
            
        arrayLinesRes = arrayLinesRes[1:]

    print(arrayLinesRes[:5])

    with open(directoryOutput, 'w', encoding='utf-8') as file:
        file.writelines(arrayLinesRes)

# parse()
# filter()