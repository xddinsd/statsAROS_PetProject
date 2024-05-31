import pandas as pd
import seaborn as sns 
from matplotlib import pyplot as plt
import scipy.stats as st
from typing import Iterable

class DfServices:
    
    def reportBUG(errorName:str, info = "No info") -> None:
        '''Small debugger'''
        print(f"BUG!!! {errorName.upper()}. Additional info: {info}")
        
    def getSubjectInfo(year: int, subjectName:str) -> pd.DataFrame:
        '''Get DF filtered by year and subjectName. Works with csv files from data'''
        
        # Check for valid subjectName
        if subjectName != 'Math' and subjectName != 'Economics' and subjectName != 'Physics':
            DfServices.reportBUG("subjectName is not correct", f"Year is {year}, Subject is {subjectName}")
            return None
        
        # Creating a path
        path = f"./Data/{year}-{year+1}/{subjectName}.csv"
        
        # Parsing csv
        try:
            df = pd.read_csv(path, sep=" ")
        except Exception:
            DfServices.reportBUG("Can't parse", f"Year is {year}, subject is {subjectName}")
            return None
        else:
            return df

    def getYearSubjectDf(grade, year, subjectName) -> pd.DataFrame:
        '''Get DF filtered by grade, year and subjectname'''
        df = DfServices.getSubjectInfo(year, subjectName)
        return df[df['Grade'] == grade]
    
    


    def getCohort_and_NextYearDf(grade_start : int, year_start : int, subjectName : str) -> tuple[pd.DataFrame, pd.DataFrame]:
        '''Returns df of prizes' cohort DF and next year DF'''
        cohort_df = DfServices.getYearSubjectDf(grade_start, year_start, subjectName)
        nextYear_df = DfServices.getYearSubjectDf(grade_start + 1, year_start + 1, subjectName)
        return cohort_df, nextYear_df

    def getPrizesOthers(cohort_df : pd.DataFrame, nextYear_df : pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        '''Input: Cohord DF and next year DF Output: DF with last year and DF with others'''

        cohort_Prizes = cohort_df[cohort_df['Result'] == 'prize']
        cohort_Prizes_Names = set(cohort_Prizes['Name']) # set to check if in quickly  # noqa: F841
        
        prizesInNextYear = nextYear_df.query('Name in @cohort_Prizes_Names')
        othersInNextYear = nextYear_df.query('Name not in @cohort_Prizes_Names')
        
        return prizesInNextYear, othersInNextYear

    def histTwo(firstDf : pd.DataFrame, secondDf : pd.DataFrame, firstColor:str = 'Blue', secondColor:str='Black', bins:int = 20) -> None:
        '''Seaborn histplot for two distributions'''
        sns.histplot(firstDf, bins=bins, stat='density', kde = True, color=firstColor)
        sns.histplot(secondDf, bins=bins, stat = 'density', kde=True, color= secondColor)
        plt.show()
    
    def isVarCloseEOLevene(array1, array2) -> bool:
        '''Check if two distributions has variances close to each others using Levene's criteria for variances'''
        p_value = st.levene(array1, array2).pvalue
        if p_value > 0.05:
            return True
        else:
            return False
    
    def isNormal(array1) -> bool:
        '''Check if normal using Shapiro-Wilk criteria for normality'''
        p_value = st.shapiro(array1,).pvalue
        if p_value > 0.05:
            return True
        else:
            return False
    
    def plotCI(array1 : pd.Series, array1Name : str, array2 : pd.Series, array2Name : str):
        '''boxplot and graph of confidence intervals with T-Test'''
        # Basic statistics
        df = pd.DataFrame({array1Name:array1, array2Name:array2}).agg(['mean','std','count','sem']).transpose()
        df.columns = ['Mx','SD','N','SE']

        # Counting the 95% confidence interval:
        p = 0.95
        K = st.t.ppf((1 + p) / 2, df['Mx'] - 1)
        df['interval'] = K * df['SE']

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3, 3))

        # confidence intervals plot
        ax.errorbar(x=df.index, 
                             y=df['Mx'], 
                             yerr=df['interval'],
                            color="black", 
                            capsize=3, 
                            markersize=4, 
                            mfc="red", mec="black", fmt ='o')

            
        # add names for both plots:
        ax.yaxis.grid(True)
        ax.set_title('')
        ax.set_ylabel('Score')
            
        return fig
    
    def twoSeriesToSnsData(series1 : pd.Series, name1 : str, series2 : pd.Series, name2 : str) -> pd.DataFrame:
        '''Sns requires data as dataframe with rows as names of series'''
        snsData1 = pd.Series(series1, name = name1)
        snsData2 = pd.Series(series2, name = name2)
        return pd.concat([snsData1, snsData2], axis = 1)
    
    def calculatePercentiles(series1 : Iterable[int], series2 : Iterable[int]) -> (pd.Series, pd.Series):
        '''Calculates percentile rank for two iterables of prizes and others'''
        
        # Series => Df of concatted
        series1Df = pd.DataFrame(
            {
                'Score':series1, 
                'whichDf':['series1'] * len(series1)
            })
        series2Df = pd.DataFrame(
            {
                'Score':series2, 
                'whichDf':['series2'] * len(series2)
                })
        fullSeries = pd.concat([series1Df, series2Df])
        
        # Sort to rank
        fullSeries = fullSeries.sort_values('Score', ascending=True)
        fullSeries['Rank'] = [i + 1 for i in range(len(fullSeries))]

        # Calculating percentile
        N = len(fullSeries)
        fullSeries['Percentile'] = fullSeries['Rank'] / N

        # Getting data from fullSeries
        percentile1 = fullSeries[fullSeries['whichDf'] == 'series1']['Percentile']
        percentile2 = fullSeries[fullSeries['whichDf'] == 'series2']['Percentile']
        return percentile1, percentile2