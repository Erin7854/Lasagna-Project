def cmap1(centroids, data, k):
    import socket
    import numpy as np
    features = len(data)
    s = 0
    for i in range(0,features-1):
        s = s + (centroids[0,i] - data[i])*(centroids[0,i] - data[i])
    mindist = s
    minid = 0
    # compute pre root euclidean distance from datapoint to each centroid
    # the below method supports any number of features
    # result is not rooted as this has no impact on classification
    for i in range(1,k):
        s = 0
        for j in range(0,features-1):
            s = s + (centroids[i,j] - data[j]) * (centroids[i,j] - data[j])
        if (s<mindist):
            mindist = s
            minid = i
    host = socket.gethostname()
    return(minid)

def cmap(centroids, data, k):
    import socket
    import numpy as np
    numdata = len(data)
    features = len(data[0])
    results = np.zeros(numdata)
    for d in range(0,numdata-1):
        s = 0
        for i in range(0,features-1):
            s = s + (centroids[0,i] - data[d,i])*(centroids[0,i] - data[d,i])
        mindist = s
        minid = 0
        # compute pre root euclidean distance from datapoint to each centroid
        # the below method supports any number of features
        # result is not rooted as this has no impact on classification
        for i in range(1,k):
            s = 0
            for j in range(0,features-1):
                s = s + (centroids[i,j] - data[d,j]) * (centroids[i,j] - data[d,j])
            if (s<mindist):
                mindist = s
                minid = i
        results[d] = minid
    host = socket.gethostname()
    return(results)

import numpy as np
import socket


k = 5
features = 2
a = np.random.rand(k,features)
data = np.random.rand(2)

result = cmap1(a,data,k)
print("cmap1 results: ", result)

k = 5
features = 3
b = np.random.rand(k,features)
data = np.random.rand(10,features)

result = cmap(b,data,k)
print("cmap results: ", result)
