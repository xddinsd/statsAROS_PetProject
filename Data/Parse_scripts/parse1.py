# Parsed with this file: Almost everything
year = '23-24'
fileName = 'Economics'
directory = ("Data\\" 
            + year
            + "\\not parsed\\" + fileName + ".txt")

directoryOutput = directory[:-4] + '(1).txt'

# stringsSplit = ['Призёр', 'Победитель', 'Участник', '9 grade', '10 grade', '11 grade']
stringsSplit = ['призер', 'победитель', 'участник', '9 grade', '10 grade', '11 grade']

stringsFilter = ['№', 'п/п', 'Фамилия', 'имя', 'отчество', 'Субъект РФ', 'Наименование', 'Класс',
                'организации', 'обучения', 'Результат', '(баллы)', 'Статус', '/', 'участник)', 'приложение',
                'Рейтинговая', 'этапа', 'олимпиады', 'экономике', 'страница', '[>']

def anyInLine(strArray, line) -> bool:
    # make it lowercase to get compared better
    line = line.lower()
    strArray = map(str.lower, strArray)
    
    for string in strArray:
        if string in line:
            return True
        
    return False
    
def parse():
    arrayLinesRes = []
    with open(directory, encoding='utf-8') as file:
        arrayLines = file.readlines()
        userLine = ''
        for line in arrayLines:
            # Filter Values
            if anyInLine(stringsFilter, line):
                continue
            # Add to a line
            userLine += (' ' + line[:-1] + ' ')
            
            
            # Split by line
            if (anyInLine(stringsSplit, line)):
                arrayLinesRes.append(userLine + '\n')
                userLine = ''

    with open(directoryOutput, 'w', encoding='utf-8') as file:
        file.writelines(arrayLinesRes)

parse()