from inference.Inference import *

class confidenceInterval(Inference):
    
    def __repr__(self):
        return f'Your are about estimate the population {self._statistic} within an interval, with confidence of={self._CI},\n{self._test},\nThe number of bootstrap samples is {self._nb_samples}'

    
    def _visualazation(self):
        means = self._bootstrap_sampling()
        if self._is_diff_statistic:
            fig, axes = plt.subplots(nrows=1, ncols=3, figsize =(15,5))
            sns.distplot(self._sample1, kde=False, ax = axes[0])
            axes[0].set_title('Distribution of the sample_1 data', fontsize=16)
            axes[0].set_xlabel('X1', fontsize=14)
            sns.distplot(self._sample2, color = 'green', kde=False,ax = axes[1])
            axes[1].set_title('Distribution of the sample_2 data', fontsize=16)
            axes[1].set_xlabel('X2', fontsize=14)
            sns.distplot(means, kde=False,  color = 'red', ax = axes[2])
            axes[2].set_title('Sampling distribution of difference in {}'.format(self._statistic), fontsize=16)
            axes[2].set_xlabel('difference in {}'.format(self._statistic), fontsize=14)
            axes[2].axvline(self._ci_statistics['confidence interval'][0], color='black')
            axes[2].axvline(self._ci_statistics['confidence interval'][1], color='black')
            plt.tight_layout()
            plt.show()

        else:
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize =(12,5))
            sns.distplot(self._sample1, kde=False,ax = axes[0])
            axes[0].set_title('Distribution of the sample data', fontsize=16)
            axes[0].set_xlabel('X', fontsize=14)
            sns.distplot(means, kde=False,  color = 'red', ax = axes[1])
            axes[1].set_title('Sampling distribution of the sample {}'.format(self._statistic), fontsize=16)
            axes[1].set_xlabel(self._statistic, fontsize=14)
            axes[1].axvline(self._ci_statistics['confidence interval'][0], color='black')
            axes[1].axvline(self._ci_statistics['confidence interval'][1], color='black')
            plt.tight_layout()
            plt.show()



    @property
    def result(self):
        ''' This function returns the confidence interval and
            the correspond visualization as property
        '''
        if not self._ci_statistics:
            lw, up = self._compute_ci()
            self._ci_statistics[self._mess] = self._sample_statistic
            self._ci_statistics['confidence interval'] = [lw, up]
            self._ci_statistics['interpretation'] ='A point estimate for the true {} in the population is {}, and we are {}% confident that the true population {} is between {} and {}'.format(self._statistic ,self._sample_statistic,self._CI,self._statistic,lw,up)
        self._visualazation()
        return self._ci_statistics 

