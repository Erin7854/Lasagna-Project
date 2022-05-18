import numpy as np
import math

f = open("data.txt","r")

lines = f.readlines()

f.close()

numData = len(lines)
numFeatures = len(lines[0].split())

data = np.random.rand(numData,numFeatures)

for x in range(numData):
    templine = lines[x].split()
    for y in range(numFeatures):
        data[x][y] = templine[y]


print(numFeatures)
print(numData)
numJobs = 16
numDataForJobs = math.ceil(numData/numJobs)

for i in range(numJobs):
    jobdata = data[numDataForJobs*i:numDataForJobs*(i+1)-1]