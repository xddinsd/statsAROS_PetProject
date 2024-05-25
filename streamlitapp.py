import time
import streamlit as slit
from cohort_Statistics import cohort_Statistics
from typing import List

# As default for Subject-Year in sidebar
subjectNameRadio = slit.sidebar.radio("Select a subject", 
                   options=['None', 'Math', 'Economics', 'Physics'], 
                   )
yearRadio = slit.sidebar.radio("Select a year", 
                   options=['None', '22-23', '23-24'], 
                   )
slit.sidebar.divider()
slit.sidebar.markdown('''Source code and documentation is availible [here](https://github.com/Otkloneniye/statsForPrizesLastYear)''')

if subjectNameRadio != 'None' and yearRadio != 'None':
    # Getting data from radio
    year = int(yearRadio[3:])
    subjectName = subjectNameRadio

    # Page header
    slit.header(f'{subjectName} {year - 1}-{year}', divider='rainbow')
    
    
    def stream_data(list : List[str]):
        '''Used to parse list to streamlit' write_stream'''
        for line in list:
            yield line + '\n\n'
            time.sleep(0.05)

    

    col1, col2 = slit.columns(2)
    
    def writeColumn(grade):
        '''Fuction to add streamlit info to a column'''
        global year, subjectName
        # Calculating stats
        stat = cohort_Statistics.cohort_Stat(grade, year, subjectName)
        resultList, result, histPlotFig, barPlotFig, qqOrCiFig = stat
        # Headers
        color = 'red' if grade == 10 else 'blue'
        slit.header(f'{grade} grade', divider= color)
        slit.subheader(f'Result is {result}')
        # Visuals
        slit.markdown(f"#### :{color}-background[Visuals:]")
        slit.pyplot(histPlotFig)
        slit.pyplot(barPlotFig)
        slit.pyplot(qqOrCiFig)
        slit.divider()
        # Statistics
        slit.markdown(f"#### :{color}-background[Statistics:]")
        slit.write_stream(stream_data(resultList))

    with col1:
        writeColumn(10) 
        

    with col2:
        writeColumn(11)
        
else:
    slit.header('Choose subject name and year in sidebar', divider='rainbow')
    slit.markdown('# :red[&#8592;]')