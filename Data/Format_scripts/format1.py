# Formatted with this file: Everything except Economics 22-23. Data provided in .xlsx, see format2 for more info
''' 
Also in Math 21-22 Data was fuck all around the world, IDK what drug got em fucked that hard, 
but the results they provided are absolute shit,
So for Math 21-22 around 5% of users were lost :) 
'''

import pandas as pd

year = '23-24'
fileName = 'Economics(1)'
directory = ("Data\\" 
            + year + "\\not parsed\\" + fileName + ".txt")

directoryOutput = directory[:-4] + '.csv'

def anyInLine(strArray, line) -> bool:
    # make it lowercase to get compared better
    line = line.lower()
    strArray = map(str.lower, strArray)
    
    for string in strArray:
        if string in line:
            return True
        
    return False

def formatLine(line):
    def printBug(error, line):
        print(f"BUG!!! {error} on line: \n{' '.join([word for word in line])}", end = '')
        print(f"The score, result are: {line[-3:]} \n ")
        
    line = line.split(' ')
    line = list(filter(lambda word: word != '', line))
    
    
    if line[-1] == '\n': #In case some files lines contains \n symbol in the end not separated with ' '
        line.pop() # Evict EOS from line
    else:
        line[-1] = line[-1][:-1] # Evict EOS from latest word in line
        
    
    if '.' in line[2]: # In case name is presented as should. Ex: "Пушкарева Ф.А."
        name = line[1] + ' ' + line[2]
    else: # Means name is presented as Full name. Ex: "Пушкарева Фанатка Анала"
        try:
            name = line[1] + ' ' + line[2][0] + '.' + line[3][0] + '.'
        except:
            printBug('Name dont format', line)
            return None, None, None
    
    try:
        score = float(line[-2].replace(',', '.'))
    except ValueError:
        printBug('ValueError', line)
        return None, None, None
    
    resultRussian = line[-1]
    match resultRussian.lower():
        case 'победитель' | 'победитель\n':
            result = 'winner'
        case 'призер' | 'призёр' | 'призер\n' | 'призёр\n':
            result = 'prize'
        case 'участник' | 'участник\n':
            result = 'participant'
        case _:
            printBug('Result has different naming', line)
            return None, None, None
            
        
    return name, score, result
    
def addFileDataToPandasDataFrame() -> pd.DataFrame:
    dataForDataFrame = []
    with open(directory, encoding='utf-8') as file:
        arrayLines = file.readlines()
        grade = 8
        for line in arrayLines:
            
            if anyInLine(['9 grade', '10 grade', '11 grade'], line):
                grade += 1
                continue
            
            name, score, result = formatLine(line)
            dataForDataFrame.append([name, grade, score, result])
    return pd.DataFrame(data = dataForDataFrame, columns = ['Name', 'Grade', 'Score', 'Result'])

    
df = addFileDataToPandasDataFrame()
print(df.head(5))
df.to_csv(directoryOutput, sep=' ', encoding='utf-8')