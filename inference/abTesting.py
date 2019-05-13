# -*- coding: utf-8 -*-
"""
Created on Sun May 12 19:17:03 2019

@author: Nawal Yala
"""

from inference.Inference import *

class abTesting(Inference):
    
    
        def __repr__(self):
            if self._is_simulate_null_method:
                method = 'simulate the null hypothesis'
            else:
                method = 'confidence interval'
            
            return f'You are about to apply an A/B testing with the following settings:\n{self._test} {self._test_type},\nUsing {method} method,\nType I error(alpha) is set to {self._alpha} and the number of bootstrap samples is {self._nb_samples}'
    
        def _abtesting_by_ci(self):
            [lower, upper] = self._compute_ci()
                  
            # Result interpretation
            
            if self._test_type == 'two_tailed':

                if lower < self._population_parameter and self._population_parameter < upper:
                    result = f' we fail to reject the null hypothesis, population {self._statistic} = {self._population_parameter} is within the confidence interval'
                else:
                    result = f' we reject the null hypothesis, population {self._statistic} = {self._population_parameter} is not within the confidence interval'
            
            elif self._test_type == 'right_tailed':
                lowc = (lower > self._population_parameter or lower == self._population_parameter)
                upc = upper > self._population_parameter 
                if lowc and upc:
                    result = f' we fail to reject the null hypothesis, values in confidence interval are greater than or equal to the population {self._statistic} = {self._population_parameter}'
                else:
                    result = f' we reject the null hypothesis, values in confidence interval are not greater than or equal to the population {self._statistic} = {self._population_parameter}'
                
            else:
                lowc = (lower < self._population_parameter or lower == self._population_parameter)
                upc = upper < self._population_parameter 
                if lowc and upc:
                    result = f' we fail to reject the null hypothesis,  values in confidence interval are less than or equal to the  population {self._statistic} = {self._population_parameter}'
                else:
                    result= f' we reject the null hypothesis, values in confidence interval are not less than or equal to the  population {self._statistic} = {self._population_parameter}'
            
            return result, [lower, upper]
 

        def _abtesting_simulate_null(self):

            mu , sampling_std = self._population_parameter, np.std(self._bootstrap_sampling())   
            null_val = np.random.normal(mu, sampling_std, self._nb_samples)
            
            if self._test_type == 'two_tailed':
                
                from_mean =  np.abs(self._population_parameter - self._sample_statistic)
                pvalue = (null_val < self._population_parameter-from_mean).mean() + (null_val > self._population_parameter + from_mean ).mean()
             
            elif self._test_type == 'right_tailed':
                
                pvalue = (null_val > self._sample_statistic).mean()
                
            else:
                pvalue = (null_val < self._sample_statistic).mean()
    
            # Result interpretation
            if pvalue > self._alpha:
                result = ' We fail to reject the null hypothesis, p_value is equal to {} and it is > {}'.format(pvalue, self._alpha)
            else:
                result = ' We reject the null hypothesis, p_value is equal to {} and it is < {}'.format(pvalue, self._alpha)
                
            return result, pvalue, null_val
        
        def _fill_curve(self):
            obs = self._sample_statistic
            null_mean = self._population_parameter
            from_mean = np.abs(null_mean - obs)
            _, pvalue, null_val = self._abtesting_simulate_null()
                        
            if self._test_type == 'two_tailed':              
                lower = np.percentile(null_val, (100-self._CI)/2)
                upper = np.percentile(null_val, ((100-self._CI)/2) + self._CI)
                reject1_sec = np.arange(min(null_val), lower, 1/20.)
                reject2_sec = np.arange(upper, max(null_val), 1/20.)
            
                sec_pvalue1 = np.arange(min(null_val), null_mean-from_mean, 1/20.)
                sec_pvalue2 = np.arange(null_mean+from_mean, max(null_val), 1/20.)
                return reject1_sec,sec_pvalue1,reject2_sec,sec_pvalue2
                
            elif self._test_type == 'right_tailed':
                upper = np.percentile(null_val, self._CI)
                reject_sec = np.arange(upper, max(null_val), 1/20.)
                sec_pvalue = np.arange(obs, max(null_val), 1/20.)  
                return reject_sec,sec_pvalue
            else:
                lower = np.percentile(null_val, 100-self._CI)
                reject_sec = np.arange(min(null_val), lower, 1/20.)
                sec_pvalue = np.arange(min(null_val),obs, 1/20.)
                return reject_sec,sec_pvalue

                
#        @property
        def _visualazation(self):
            if self._is_simulate_null_method: 
                
                plt.style.use('ggplot')
                means = self._bootstrap_sampling()
                null_mean = self._population_parameter
                std = np.std(means)
                x = np.linspace(null_mean-4*std, null_mean+4*std, self._nb_samples)
                iq = st.norm(null_mean,std)
                fig = plt.figure(figsize=(10,7))
                plt.plot(x,iq.pdf(x),'black')
        #             plt.axvline(self._sample_statistic)

                sec_color = iter(['r','b','r','b'])
                sec_label = iter(['rejection region','p_value', '',''])
                transp = iter([1,0.5,1,0.5])

                section =  self._fill_curve()
                for sec in section:  
                    plt.fill_between(sec, iq.pdf(sec),color=next(sec_color), label=next(sec_label), alpha = next(transp))
                plt.legend()
                plt.show()
        
        
        @property
        def result(self):
            if not self._ab_statistics:
                
                if self._is_simulate_null_method:   
                    interpretaion, pvalue,_ = self._abtesting_simulate_null()
                    self._ab_statistics[self._mess] = self._sample_statistic
                    self._ab_statistics['probability_value'] = pvalue 
                    self._ab_statistics['ab testing interpretation'] =  interpretaion
                    
                else:
                    interpretaion, ci =  self._abtesting_by_ci()
                    self._ab_statistics[self._mess] = self._sample_statistic
                    self._ab_statistics['confidence interval'] = ci
                    self._ab_statistics['ab testing interpretation'] = interpretaion
            self._visualazation()    
            return self._ab_statistics