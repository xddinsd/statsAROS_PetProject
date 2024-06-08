'''Main statistics file with cohort_stat function that calculates stat for a cohort of last year prizes'''


import seaborn as sns
from scipy import stats as st
import statsmodels.api as sm
from matplotlib import pyplot as plt
from DfServices import DfServicesModule, Visuals, StatTests
from typing import List
from collections import namedtuple

class Cohort_Statistics:
    

    def cohortStat(data : namedtuple) -> namedtuple:
        ''' 
        Calculates mean/percentile stat for a cohort of prizes last year and cohort of others. 
        Input: DFServices.DfServicesModule getPercentileData() and getMeanData()
        Result: namedtuple('CohortResult', 'logs boolResult histPlotFig boxPlotFig qqOrCIPlotFig')'''

        logs : List[str] = [] # Contains all stat logs.

        scoresPrizes = data.prizes
        scoresOthers = data.others
        
        # Making a histogramm
        histPlotFig, axs = plt.subplots(ncols=1)
        sns.histplot(DfServicesModule.twoSeriesToSnsData(
                scoresOthers.sample(n = scoresPrizes.size), 'Others', 
                scoresPrizes, 'Prizes'),
                    bins = 30, 
                    stat='density', kde = True,
                    ).get_figure()
        
        
        # Introduce a Hypotesis
        meanPrizes = scoresPrizes.mean()
        othersPrizes = scoresOthers.mean()
        
        logs.append((f"Mean of last year prizes' scores is {round(meanPrizes, 4)}"))
        logs.append((f"Mean others' scores is {round(othersPrizes, 4)}"))
        logs.append(("    H_0: Actually MeanP == MeanO"))
        logs.append(("    H_1: Not equal"))
        logs.append(' ')
        
        # If normal and variances are close to each others -> use T-Test & KS-test
        # Othervise -> KS-test
        
        # Check variances and normal:
        logs.append('Check criteria for a T-Test:')
        use_T_Test = True
        
        if (
                not (StatTests.isNormal(scoresPrizes)) 
                or  
                not (StatTests.isNormal(scoresOthers))
            ):
            logs.append("     | KSTest for normality failed: One of the distributions is not normal")
            use_T_Test = False
        elif not StatTests.isVarCloseEOLevene(scoresOthers, scoresPrizes): # elif because levene's test assume that distribution is normal
            logs.append("     | Levene failed: Variances are not close to EO")
            use_T_Test = False
        
        
        
        
        
        # Performing tests
            
        def printTestResult(p_value : float) -> bool:
            logs.append((f'    p_value is {"{:.5f}".format(p_value)} '))
            if p_value < 0.05:
                logs.append('H_0 is false -> H_1 is ACCEPTED')
                return True
            else:
                logs.append('Can\'t reject the H_0')
                return False
                
        # Performing a T-Test:
        if use_T_Test:
            logs.append('      ...')
            logs.append('     Passed! | Levene | KSTest for normality')
            logs.append(' ')
            logs.append('Performing a T-Test:')
            p_value = st.ttest_ind(scoresOthers.sample(n = scoresPrizes.size), 
                                scoresPrizes, 
                                equal_var=False
                                    ).pvalue # Sample because we need same samplesize for T-Test
            # Interpreting the T-Test results
            TTestResult = printTestResult(p_value)
        else:
            TTestResult = False
            logs.append('     Failed | Levene | Shapiro-Wilk ')
        
        # Performing a KS-test
        logs.append(' ')
        logs.append('Performing a KS-Test:')
        p_value = st.ks_2samp(scoresOthers, scoresPrizes, alternative = 'greater').pvalue

        # Interpreting the KS-Test results
        KSResult = printTestResult(p_value)
            
        # Perfoming a boxplot and graph of qqPLOT for levene or confidence interval plot if possible 
        boxPlotFig, axs = plt.subplots(ncols=1)
        sns.boxplot(
                                data = DfServicesModule.twoSeriesToSnsData(
                                    scoresOthers, 'Others', scoresPrizes, 'Prizes last year')
                            )
        
        if use_T_Test:
            
            # Creating a CI-Plot
            qqOrCIPlotFig = Visuals.plotCI(scoresOthers.sample(n = scoresPrizes.size), 'Non-prizes last year', 
                                    scoresPrizes, 'PRIZES last year')
        else:
            
            qqOrCIPlotFig, axs = plt.subplots(ncols=1)
            #Levene or SW failed so qq-plot:
            qqOrCIPlotFig = sm.qqplot(
                st.zscore(scoresPrizes), 
                line='s', ax=axs, 
                markerfacecolor='orange', markeredgecolor='k', alpha = 0.6)

            qqOrCIPlotFig = sm.qqplot(
                st.zscore(
                    scoresOthers.sample(n = scoresPrizes.size)), 
                line='s', ax=axs, 
                markerfacecolor='lightblue', alpha = 0.4)
            
        # Output the result data
        logs.append(' ')
        if TTestResult or KSResult:
            result = True
        else:
            result = 'Not defined'

        resultTuple = namedtuple('CohortResult', 'logs boolResult histPlotFig boxPlotFig qqOrCIPlotFig')
        return resultTuple(
            logs = logs, 
            boolResult = result, 
            histPlotFig = histPlotFig, 
            boxPlotFig = boxPlotFig, 
            qqOrCIPlotFig = qqOrCIPlotFig)
        
        
