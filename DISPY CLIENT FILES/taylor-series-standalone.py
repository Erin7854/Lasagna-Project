def taylorarctan(indicies,x):
    sum = 0
    for n in range(indicies[0],indicies[1]):
        middle = ((2*n)+1)
        sum = sum + ((-1)**n)*((x**(middle)) / (middle))
    return sum

import math
import numpy as np

precision = 4096
indicies = list(range(precision))
numJobs = 16
nums = (0.5666666666666,-0.232323232323,0.99999999,0.00001,0.94524837652)
joblist = np.array_split(indicies,numJobs)

for x in nums:
    results = 0

    for job in joblist:
        results = results + taylorarctan((job[0],job[-1]),x)
    
    print("Arctan of %s" % x)    
    print("Taylor Approximation at %s precision: %s" % (precision, results))
    realResults = np.arctan(x)
    print("Function Results: %s" % realResults)
    difference = realResults - results
    dPercentage = (1-abs(difference/realResults)) * 100
    print("Similarity: %s %% " % dPercentage)
    print("")
