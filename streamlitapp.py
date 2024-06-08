import time
import streamlit as slit
from Cohort_Statistics import Cohort_Statistics
from typing import List
from DfServices import DfServicesModule, Visuals

def getMeanStat(grade, year, subjectName):
    # Stat for hypotesis 1
    scatterPlotFig = Visuals.makeScatterPlot(scatterData = 
        DfServicesModule.getScatterData(grade, year, subjectName))
    stat = Cohort_Statistics.cohortStat(
        DfServicesModule.getMeanData(grade, year, subjectName))
    
    color = 'red' if grade == 10 else 'blue'
    
    # Headers
    slit.header(f'{grade} grade', divider= color)

    return stat, color, scatterPlotFig

def getPercentileStat():
    # Stat for hypotesis 2
    scatterPlotFig = Visuals.makeScatterPlot(
        scatterData = DfServicesModule.getCompleteScatterData())
    stat = Cohort_Statistics.cohortStat(
        DfServicesModule.getPercentileData())

    color = 'rainbow'
    
    return stat, color, scatterPlotFig

def writeColumn(getStatData):
    '''Fuction to add info to a streamlit column'''

    # Calculating stats
    stat, color, scatterPlotFig = getStatData
    

    slit.subheader(f'Result is {stat.boolResult}')
    # Visuals
    slit.markdown(f"#### :{color}-background[Visuals:]")
    slit.write('* ScatterPlot for prizes\' percentiles year ago and now')
    slit.pyplot(scatterPlotFig)
    slit.write('* HistPlot for last year prizes and others in current year')
    slit.pyplot(stat.histPlotFig)
    slit.write('* Same but BoxPlot')
    slit.pyplot(stat.boxPlotFig)
    slit.write('* Confidence interval plot(T-test) or QQ-plot: red line is norm.(No T-Test)')
    slit.pyplot(stat.qqOrCIPlotFig)
    slit.divider()
    # Statistics
    slit.markdown(f"#### :{color}-background[Statistics:]")

    def stream_data(list : List[str]):
        '''Used to parse list to streamlit' write_stream'''
        for line in list:
            yield line + '\n\n'
            time.sleep(0.05)
    
    slit.write_stream(stream_data(stat.logs))

if __name__ == "__main__":

    # Adds a toggle for both hypotesis
    byGroups = slit.sidebar.toggle('Toggle to get stats for groups')

    if not byGroups:
        slit.header('Percentile stats for all data', divider='rainbow')
        writeColumn(getPercentileStat())
    else:
            
        subjectNameRadio = slit.sidebar.radio("Select a subject", 
                        options=['Math', 'Economics', 'Physics'], 
                        )
        yearRadio = slit.sidebar.radio("Select a year", 
                        options=['22-23', '23-24'], 
                        )
        slit.sidebar.divider()
        slit.sidebar.markdown('''Source code and documentation is availible [here](https://github.com/Otkloneniye/statsForPrizesLastYear)''')


        year = int(yearRadio[3:])
        subjectName = subjectNameRadio

        # Page header
        slit.header(f'{subjectName} {year - 1}-{year}', divider='rainbow')
        

        col1, col2 = slit.columns(2)

        with col1:
            writeColumn(getMeanStat(10, year, subjectName)) 
            

        with col2:
            writeColumn(getMeanStat(11, year, subjectName))
