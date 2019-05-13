# INFERENCE package


## Inferencial_statistics (AB Testing and confidence interval)

There are two main approches of inferential statistics. The first, is the estimation of the parameters (such as mean, median, and standard deviation) of a population based on those calculated for a sample of that population. The estimation of parameters can be done by constructing a range of values in which the true population parameter is likely to fall. The second approch of inferential statistics is hypothesis testing. It is to determine the effectiveness of an experimental treatment. This is done by determining if the treatment yields results that are significantly different from those obtained from a sample given no treatment at all.

There are two method to perform an inferential statistics, traditional method and modern method. The traditional method uses formula, while the modern method uses Bootstrap technique (sampling with replacement). **inference** package allow you to AB test and compute a confidence interval, using modern method: bootstraping.

## Getting Started
in the (How_to_ use_ inference_ pakcage.ipynb) jupyter notebook file there are several examples that show you how to use this tool.

## Files

There are 3 files:

inference/Inference : contains a supper calss **Inference** 

inference/confidenceInterval: is a child of the **Inference** class, by instanciate an object of this class the confidence interval is computed.

inference/abTesting: is a child of the **Inference** class, by instanciate an object of this class an AB test is performed.


