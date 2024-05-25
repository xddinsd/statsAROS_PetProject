# Format the xlsx data Economics 22-23 Economics 23-24
# dependency: openpyxl

import pandas as pd

# df11 = pd.read_excel("Data\\23-24\\not parsed\\Результаты ЗЭ по экономике-2024.xlsx", sheet_name='11 класс')
# df10 = pd.read_excel("Data\\23-24\\not parsed\\Результаты ЗЭ по экономике-2024.xlsx", sheet_name='10 класс')
# df9 = pd.read_excel("Data\\23-24\\not parsed\\Результаты ЗЭ по экономике-2024.xlsx", sheet_name='9 класс')
# df = pd.concat([df11, df10, df9])

df = pd.read_excel("Data\\22-23\\not_formatted\\Economics.xlsx")

data = {
    'Name' : df['Фамилия'] + ' ' + df['Имя'] + ' ' + df['Отчество'],
    'Grade' : df['Класс, за который выступает участник'],
    'Score' : df['Итого'],
    'Result' : df['Статус'],
}

df = pd.DataFrame(data)

def formatName(name): # Name format ex: 'Дьячкова Анна Викторовна' -> 'Дьячкова А.В.'
    name = str(name).split(' ')
    try:
        return name[0] + ' ' + name[1][0] + '.' + name[2][0] + '.'
    except:
        return None
    
def formatResult(resultRussian):
    match resultRussian.lower():
        case 'победитель':
            result = 'winner'
        case 'призер' | 'призёр':
            result = 'prize'
        case 'участник':
            result = 'participant'
        case _:
            return None, None, None
    return result

df['Name'] = df['Name'].apply(formatName)
df['Result'] = df['Result'].apply(formatResult)
print(df.tail(5))
print(df.head(5))

df.to_csv("Data\\22-23\\Economics.csv", sep=' ', encoding='utf-8')