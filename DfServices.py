import pandas as pd
import seaborn as sns 
from matplotlib import pyplot as plt
import scipy.stats as st
from typing import Iterable
from collections import namedtuple

class DfServicesModule:
    '''Class full of getting and formatting data'''

    def reportBUG(errorName:str, info = "No info") -> None:
        '''Small debugger'''
        print(f"BUG!!! {errorName.upper()}. Additional info: {info}")
        
    def getSubjectInfo(year: int, subjectName:str) -> pd.DataFrame:
        '''Get DF filtered by year and subjectName. Works with csv files from data'''
        
        # Check for valid subjectName
        if subjectName not in ['Math', 'Economics', 'Physics']: 
            DfServicesModule.reportBUG(
                "subjectName is not correct", 
                f"Year is {year}, Subject is {subjectName}")
            return None
        
        # Creating a path
        path = f"./Data/{year}-{year+1}/{subjectName}.csv"
        
        # Parsing csv
        try:
            df = pd.read_csv(path, sep=" ")
        except Exception:
            DfServicesModule.reportBUG(
                "Can't parse", 
                f"Year is {year}, subject is {subjectName}")
            return None
        else:
            return df

    def getYearSubjectDf(grade, year, subjectName) -> pd.DataFrame:
        '''Get DF filtered by grade, year and subjectname'''
        df = DfServicesModule.getSubjectInfo(year, subjectName)
        return df[df['Grade'] == grade]

    def twoSeriesToSnsData(
        series1 : pd.Series, name1 : str, 
        series2 : pd.Series, name2 : str
        ) -> pd.DataFrame:
        '''Sns requires data as dataframe with rows as names of series'''
        snsData1 = pd.Series(series1, name = name1)
        snsData2 = pd.Series(series2, name = name2)
        return pd.concat([snsData1, snsData2], axis = 1)
    


    def getCohort_and_NextYearDf(grade_start : int, year_start : int, subjectName : str) -> tuple[pd.DataFrame, pd.DataFrame]:
        '''Returns df of prizes' cohort DF and next year DF'''
        cohort_df = DfServicesModule.getYearSubjectDf(
            grade_start, year_start, subjectName)
        nextYear_df = DfServicesModule.getYearSubjectDf(
            grade_start + 1, year_start + 1, subjectName)
        return cohort_df, nextYear_df

    def getPrizesOthers(cohort_df : pd.DataFrame, nextYear_df : pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        '''Input: Cohord DF and next year DF Output: DF with last year and DF with others'''

        cohort_Prizes = cohort_df[cohort_df['Result'] == 'prize']
        cohort_Prizes_Names = set(cohort_Prizes['Name']) # set to check if in quickly  # noqa: F841
        
        prizesInNextYear = nextYear_df.query('Name in @cohort_Prizes_Names')
        othersInNextYear = nextYear_df.query('Name not in @cohort_Prizes_Names')
        
        return prizesInNextYear, othersInNextYear
    
    def getScatterData(grade, year, subjectName) -> pd.DataFrame:
        '''
        result: namedtuple('Percentiles', 'prizesLastYear prizes')
        '''
        grade_start = grade - 1 
        year_start = year - 2

					# Getting data
        cohortDf, nextYearDf = DfServicesModule.getCohort_and_NextYearDf(
            year_start = year_start, 
            grade_start = grade_start, 
            subjectName = subjectName)

        # Calculating percentiles for each Year
        percentilesYear1 = Percentiles.getPercentilesYear1(cohortDf)
        percentilesYear2 = Percentiles.getPercentilesYear2(cohortDf, nextYearDf)

        # Joining by name
        percentiles = percentilesYear1.merge(
            percentilesYear2, 
            left_on = 'Name', 
            right_on = 'Name', 
            how = 'inner')

        percentiles = percentiles[
            ['Name', 'Percentile_x', 'Percentile_y']]

        column_names = {
            'Percentile_x' : "Prizes' percentiles year 1",
            'Percentile_y' : "Prizes' percentiles year 2"
        }
        percentiles.rename(columns = column_names, inplace=True)

        return percentiles
    
    def getCompleteScatterData() -> pd.DataFrame:
        to_concat = []
        for year in [23, 24]:
            for grade in [10, 11]:
                for subjectName in ['Math', 'Economics', 'Physics']:
                    to_concat.append(DfServicesModule.getScatterData(
                        grade, year, subjectName))
        
        return pd.concat(to_concat)

    def getMeanData(grade: int, year: int, subjectName : str) -> namedtuple:
        '''Returns mean hypotesis data for cohort_stat'''
        grade_start = grade - 1 
        year_start = year - 2 # for ex: 21-22 => year = 22 => year_start = 20
        
        # Get prizes and cohort data
        cohort_df, nextYear_df = DfServicesModule.getCohort_and_NextYearDf(grade_start, year_start, subjectName)
        prizesInNextYear, othersInNextYear = DfServicesModule.getPrizesOthers(cohort_df, nextYear_df)
        
        # Get its scores
        scoresPrizes = prizesInNextYear["Score"]
        scoresOthers = othersInNextYear["Score"]

        result_data = namedtuple('scores', 'prizes others')
        return result_data(
            prizes = scoresPrizes, 
            others = scoresOthers)

    def getPercentileData() -> namedtuple:
        '''Returns percentile hypotesis data for cohort_stat'''
        scoresPrizes, scoresOthers = [], []
        for subjectName in ['Math', 'Economics', 'Physics']:
            for year in [23, 24]:
                for grade in [10, 11]:
                    meanData = DfServicesModule.getMeanData(grade, year, subjectName)
                    tt_scoresPrizes = meanData.prizes
                    tt_scoresOthers = meanData.others
                    scoresPrizes += tt_scoresPrizes.tolist()
                    scoresOthers += tt_scoresOthers.tolist()


        scoresPrizes, scoresOthers = Percentiles.calculatePercentiles(scoresPrizes, scoresOthers)
        
        result_data = namedtuple('scores', 'prizes others')
        return result_data(
            prizes = scoresPrizes, 
            others = scoresOthers)

class StatTests:
    def isVarCloseEOLevene(array1, array2) -> bool:
        '''Check if two distributions has variances close to each others using Levene's criteria for variances'''
        p_value = st.levene(array1, array2).pvalue
        if p_value > 0.05:
            return True
        else:
            return False
    
    def isNormal(array1) -> bool:
        '''Check if normal using Shapiro-Wilk criteria for normality'''
        p_value = st.kstest(array1, 'norm').pvalue
        if p_value > 0.05:
            return True
        else:
            return False

class Visuals:
    '''Contains funcs to create plots'''
    def histTwo(firstDf : pd.DataFrame, secondDf : pd.DataFrame, firstColor:str = 'Blue', secondColor:str='Black', bins:int = 20) -> None:
        '''Seaborn histplot for two distributions'''
        sns.histplot(firstDf, bins=bins, stat='density', kde = True, color=firstColor)
        sns.histplot(secondDf, bins=bins, stat = 'density', kde=True, color= secondColor)
        plt.show()
    
    
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
    
    def makeScatterPlot(scatterData : pd.DataFrame) -> plt.Figure:
        '''
        Input: DFServices.DFServices getScatterData() or getCompleteScatterData()
        '''
        

        regressionData = scatterData
        figScatter, axs = plt.subplots()
        sns.scatterplot(
            data = regressionData, 
            x = "Prizes' percentiles year 1", 
            y = "Prizes' percentiles year 2",
            color='orange')
        return figScatter
    
    
    

class Percentiles:
    '''Some funcs to calculate percentiles'''
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
        
    def getPercentilesYear1(cohortDf) -> pd.DataFrame:
		# Calculating percentiles for Year1
        cohortDf = cohortDf.sort_values('Score', ascending=True)
        N = len(cohortDf)
        cohortDf['Percentile'] = [(i + 1) / N for i in range(N)]
        return cohortDf[cohortDf['Result'] == 'prize']
	
    def getPercentilesYear2(cohortDf, nextYearDf) -> pd.DataFrame:
		# Calculating percentiles for Year2 
		
        cohort_Prizes_Names = set(  # noqa: F841
            cohortDf[cohortDf['Result'] == 'prize']['Name']) # set to check if in quickly  # noqa: F841

        # Joining
        prizesNextYear = nextYearDf.query('Name in @cohort_Prizes_Names')
        othersNextYear = nextYearDf.query('Name not in @cohort_Prizes_Names')

        pd.options.mode.chained_assignment = None
        prizesNextYear.loc[:, 'WhichCohort'] = 'prizes'
        othersNextYear.loc[:, 'WhichCohort'] = 'others'

        # Concat arrays to get ranks
        fullSeries = pd.concat([prizesNextYear, othersNextYear])
        fullSeries = fullSeries.sort_values('Score', ascending=True)

        # Calculating percentile
        N = len(fullSeries)
        fullSeries['Percentile'] = [(i + 1) / N for i in range(N)]

        return fullSeries[fullSeries['WhichCohort'] == 'prizes']

	
    
	
