import math
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats as st
import statsmodels.api as sm
from matplotlib import pyplot as plt
from DfServices import DfServices

from typing import Tuple, List
class cohort_Statistics:
    def cohort_Stat(grade : int, year : int, subjectName : str) -> Tuple[List[str], str, plt.Figure, plt.Figure]:
        ''' Main function that calculates stat for a cohort of prizes last year and cohort of others'''
        strListResult : List[str] = [] # Contains all stat data 
        grade_start = grade - 1 
        year_start = year - 2 # for ex: 21-22 => year = 22 => year_start = 20
        
        

        # Get prizes and cohort data
        cohort_df, nextYear_df = DfServices.getCohort_and_NextYearDf(grade_start, year_start, subjectName)
        prizesInNextYear, othersInNextYear = DfServices.getPrizesOthers(cohort_df, nextYear_df)
        scoresPrizes = prizesInNextYear["Score"]
        scoresOthers = othersInNextYear["Score"]
        
        # Making a histogramm
        histPlotFig, axs = plt.subplots(ncols=1)
        histPlot = sns.histplot(DfServices.twoSeriesToSnsData(
                scoresOthers.sample(n = scoresPrizes.size), 'Others', 
                scoresPrizes, 'Prizes'),
                    bins = scoresPrizes.size, 
                    stat='density', kde = True,
                    ).get_figure()
        # DfServices.histTwo(scoresOthers, scoresPrizes, 'Blue', 'Black')
        
        
        # Introduce a Hypotesis
        meanPrizes = scoresPrizes.mean()
        othersPrizes = scoresOthers.mean()
        
        strListResult.append((f"Mean of last year prizes' scores is {round(meanPrizes, 4)}"))
        strListResult.append((f"Mean others' scores is {round(othersPrizes, 4)}"))
        strListResult.append((f"    H_0: Actually MeanP == MeanO"))
        strListResult.append((f"    H_1: Not equal"))
        strListResult.append(' ')
        
        # If normal and variances are close to each others -> use T-Test & KS-test
        # Othervise -> KS-test
        
        # Check variances and normal:
        strListResult.append('Check criteria for a T-Test:')
        use_T_Test = True
        
        if not (DfServices.isNormal(scoresPrizes) and DfServices.isNormal(scoresOthers)):
            strListResult.append("     | Shapiro-Wilk for norm. failed: One of the distributions is not normal")
            use_T_Test = False
        elif not DfServices.isVarCloseEOLevene(scoresOthers, scoresPrizes): # elif because levene's test assume that distribution is normal
            strListResult.append("     | Levene failed: Variances are not close to EO")
            use_T_Test = False
        
        
        
        
        
        # Performing tests
            
        def printTestResult(p_value : float) -> bool:
            strListResult.append((f'    p_value is {"{:.5f}".format(p_value)} '))
            if p_value < 0.05:
                strListResult.append('H_0 is false -> H_1 is ACCEPTED')
                return True
            else:
                strListResult.append('Can\'t reject the H_0')
                return False
                
        # Performing a T-Test:
        if use_T_Test:
            strListResult.append('      ...')
            strListResult.append('     Passed! | Levene | Shapiro-Wilk ')
            strListResult.append(' ')
            strListResult.append('Performing a T-Test:')
            p_value = st.ttest_ind(scoresOthers.sample(n = scoresPrizes.size), 
                                scoresPrizes, 
                                equal_var=False
                                    ).pvalue # Sample because we need same samplesize for T-Test
            # Interpreting the T-Test results
            TTestResult = printTestResult(p_value)
        else:
            TTestResult = False
            strListResult.append('     Failed | Levene | Shapiro-Wilk ')
        
        # Performing a KS-test
        strListResult.append(' ')
        strListResult.append('Performing a KS-Test:')
        p_value = st.ks_2samp(scoresOthers, scoresPrizes, alternative = 'greater').pvalue

        # Interpreting the KS-Test results
        KSResult = printTestResult(p_value)
            
        # Perfoming a boxplot and graph of qqPLOT for levene or confidence interval plot if possible 
        boxPlotFig, axs = plt.subplots(ncols=1)
        boxPlot = sns.boxplot(
                                data = DfServices.twoSeriesToSnsData(
                                    scoresOthers, 'Others', scoresPrizes, 'Prizes last year')
                            )
        
        mainPlotFig = None
        if use_T_Test:
            
            # Creating a CI-Plot
            qqOrCIPlotFig = DfServices.plotCI(scoresOthers.sample(n = scoresPrizes.size), 'Non-prizes last year', 
                                    scoresPrizes, 'PRIZES last year')
        else:
            
            qqOrCIPlotFig, axs = plt.subplots(ncols=1)
            #Levene or SW failed so qq-plot:
            qqOrCIPlotFig = sm.qqplot(st.zscore(scoresPrizes), line='s', ax=axs)
            qqOrCIPlotFig.set_alpha(0.1)
            qqOrCIPlotFig = sm.qqplot(st.zscore(scoresOthers.sample(n = scoresPrizes.size)), line='s', ax=axs)
            
        # Output the result data
        strListResult.append(' ')
        if TTestResult or KSResult:
            result = True
        else:
            result = 'Not defined'
        return strListResult, result, histPlotFig, boxPlotFig, qqOrCIPlotFig
        
        
