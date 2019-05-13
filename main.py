# -*- coding: utf-8 -*-
"""
Created on Sun May 12 19:18:18 2019

@author: Nawal Yala
"""
import sys
sys.path.append(r'C:\\Users\\dell\\Desktop\\InferentialStatistics')

# import libraries
import numpy as np
import pandas as pd
from inference.confidenceInterval import confidenceInterval
from inference.abTesting import abTesting

# import  Student Survey Data from MASS package
#link to data: https://vincentarelbundock.github.io/Rdatasets/datasets.html
survey = pd.read_csv('survey.csv',index_col= 0)
survey.head()

# drop NaN values
survey.dropna(axis=0, how='any', inplace =True)
survey.head()


#Estimate the population parameters of all students in the university 
#by computing their confidence interval
#Let's first take one variable: the Height of students sample and 
#estimate the mean μ of all students in the university

# Height is a numpy araay now
Height = survey.Height.values 
# Instanciate a confidenceInterval object with a default settings
ci_95 = confidenceInterval(Height)
ci_95
ci_95.result


#Let's now estimate the median of the height of all student
# Instanciate a confidenceInterval object with a different settings
ci_95 = confidenceInterval(Height, statistic = 'median', CI = 0.99)
ci_95
ci_95.result


#Instanciate a confidenceInterval object with a different settings
ci_95 = confidenceInterval(Height, statistic = 'standard deviation')
ci_95.result


ci_95.statistic_type

#As you can see the default statistics are stored in statistic_type. 
#If your statistic is not between them, you can add new statistic. 
#The following cell show you how to add a new statistic.
#Let's suppose we wants to estimate the range of the all students height


# Instanciate a confidenceInterval object with new statistic, its correspond function must be a lambda 
ci_95 = confidenceInterval(Height, new_statistic = 'range' , new_statistic_func = lambda x: max(x)-min(x), nb_samples =100000)
ci_95.result


# AB testing

NW = survey['NW.Hnd'].values
Wr = survey['Wr.Hnd'].values

# instanciate an abTesting object
ab = abTesting(Wr, NW, test_type = 'two_tailed')
ab
ab.result



