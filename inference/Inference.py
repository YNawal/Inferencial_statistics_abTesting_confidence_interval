# -*- coding: utf-8 -*-
"""
Created on Sun May 12 19:11:13 2019

@author: Nawal Yala
"""

import numpy as np
import scipy.stats as st
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import seaborn as sns

class Inference:
    
        ''' Inference class does two tasks: AB testing and confidence interval using a modern method: BOOTSTRAPING.
        It can estimate any parameter (or difference in parameters) with a p% of confidence.
        It can also do any AB testing:
        tow_tailed test, 
        one_tailed (right_tailed and left_tailed) test.
        Input: 
        inference class takes for any of its tasks:
        1- one sample or two samples: sample1 or/ sample1 and sample2. a numpy array
        2- statistic: a string to specify the type of sample statistic. default value : 'mean'
            It can be any statistic, statistic_type class variable contain the available statistics
        3- new_statistic and , new_statistic_func :this is for the user that wants to add a statistic that doesn't exist in the
           statistic_type list. new_statistic: string. new_statistic_func: lambda function.
        4- nb_samples: int. nombre of bootstrap samples to draw from a sample.
        5- CI: level of confidence interval: int between 0 and 1. default value = 0.95
        6- alpha: type I error: int. User can fill one of them since CI = 1-alpha.  default value: 0.05
        7- test_type: str. To specify the type of the AB tesing, default: 'two_tailed'.
            It can be : 'two_tailed', 'right-tailed','left_tailed'
        8- is_simulate_null_method: bool. A flag used to select the method used to apply the AB testning
            If it is True, so the simulate null hypothesis based technique is used,
            otherwise the confidence interval technique method is used. default: True.
        9- population_parameter: int.  It is specific to AB testing. If it is two sample test, the default value is 0.
            Otherwise it must be set.
        '''
    
         # list of statistic types 
        statistic_type = ['mean','proportion','median', 'q25','q75','iqr', 'standard deviation','variance']
        # list of functions correspond to the statistics.
        _statistic_func = [lambda x: np.mean(x),lambda x: np.mean(x),lambda x: np.median(x),
                            lambda x: np.percentile(x,25), lambda x: np.percentile(x,25),
                           lambda x: np.subtract(*np.percentile(x, [75, 25])),lambda x: np.std(x),lambda x: np.var(x)]
        
        def __init__(self, sample1, *sample2, statistic ='mean', CI = 0.95, nb_samples = 10000, alpha = 0.05,
                           new_statistic = '', new_statistic_func='',
                           test_type = 'two_tailed', is_simulate_null_method = True, population_parameter=0 ):
        
            #####initialization specific to the both tasks
            self._sample1 = sample1
            self._size1 = np.size(sample1)    
            self._nb_samples = nb_samples
            self._statistic = statistic
            self._CI = CI*100
            self._alpha = alpha

            self._ci_statistics = defaultdict(str)
            self._ab_statistics = defaultdict(str)
            self._func_stat = defaultdict(int)
                
            # We add the new statistic and new statistic function to the class lists
            # new statistic function must be a lambda
            self._add_statistic = bool(new_statistic  and new_statistic_func)
            if self._add_statistic:
                self._statistic = new_statistic 
            if self._add_statistic:
                if  new_statistic_func.__name__ == "<lambda>":               
                    Inference.statistic_type.append(new_statistic)
                    Inference._statistic_func.append(new_statistic_func)
                else:
                    raise Exception('The new statistic function should be a lambda function')
            
            # construct a dict containn the statistic anf the correspond function
            self._statistic_type_func = zip(Inference.statistic_type, Inference._statistic_func)
            for stat,func in self._statistic_type_func:
                self._func_stat[stat] = func
                
            if np.any(sample2):
                self._is_diff_statistic = True            
                self._sample2 = sample2[0]
                self._size2 = np.size(sample2) 
                self._test = 'it is a two samples test'
                self._mess = 'difference in {}s'.format(self._statistic)
                self._sample_statistic = self._func_stat[self._statistic](self._sample1)- self._func_stat[self._statistic](self._sample2)
         
            else: 
                self._is_diff_statistic = False
                self._test = 'it is a one sample test'
                self._mess = 'sample {}'.format(self._statistic)
                self._sample_statistic = self._func_stat[self._statistic](self._sample1)
             
            
            #####initialization specific to the AB testing
            self._test_type = test_type
            self._is_simulate_null_method = is_simulate_null_method
            if self._is_diff_statistic:
                self._population_parameter = 0
            else:
                self._population_parameter = population_parameter
            

            
        
        def __repr__(self):
            return f'You are about to apply one or the two methods of inferencial statistics: AB testing and confidence interval. \n The statistic is the {self._statistic}, and {self._test}. You are using confidence interval level of {self._CI}%,\n and number of bootstrap samples equal to {self._nb_samples}'
        
            
         # bootstraping sample (or two samples)
        def _bootstrap_sampling(self):
            '''
             sampling the sample with replacement.
             This function compute the sampling distribution
             of the sample statistic (any statistic)
             
            '''
            means = []
            if self._is_diff_statistic:
                for _ in range(self._nb_samples):        
                    bootstrap_sample1 = np.random.choice(self._sample1, self._size1, replace=True)
                    bootstrap_sample2 = np.random.choice(self._sample2, self._size2, replace=True)
                    means.append(self._func_stat[self._statistic](bootstrap_sample1)
                                                         - self._func_stat[self._statistic](bootstrap_sample2)) 
            else:
                for _ in range(self._nb_samples):        
                    bootstrap_sample = np.random.choice(self._sample1,self._size1, replace=True)
                    means.append(self._func_stat[self._statistic](bootstrap_sample))
            return means



         # compute confidence nterval
        def _compute_ci(self): 
            '''
            This function compute a confidence interval from the sampling 
            distribution of the sample statistic (any statistic)
            '''
            means = self._bootstrap_sampling()
            lower = np.percentile(means, (100-self._CI)/2)
            upper = np.percentile(means, ((100-self._CI)/2) + self._CI)
            return [lower, upper]
          