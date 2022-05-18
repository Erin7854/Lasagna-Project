def featureAverage(data):
    numData = len(data)
    s = 0
    for i in range(numdata):
        s = s + data[i]
    mean = s/numData
    return(mean)

def cmap1(centroids, data, k):
    import socket
    features = len(data)
    s = 0
    for i in range(features):
        s = s + (centroids[0,i] - data[i])*(centroids[0,i] - data[i])
    mindist = s
    minid = 0
    # compute pre root euclidean distance from datapoint to each centroid
    # the below method supports any number of features
    # result is not rooted as this has no impact on classification
    for i in range(1,k):
        s = 0
        for j in range(features):
            s = s + (centroids[i,j] - data[j]) * (centroids[i,j] - data[j])
        if (s<mindist):
            mindist = s
            minid = i
    host = socket.gethostname()
    return(host, minid)

def cmap(centroids, data, k):
    import socket
    import numpy as np
    numdata = len(data)
    features = len(data[0])
    results = np.zeros(numdata)
    for d in range(numdata):
        s = 0
        for i in range(features):
            s = s + (centroids[0,i] - data[d,i])*(centroids[0,i] - data[d,i])
        mindist = s
        minid = 0
        # compute pre root euclidean distance from datapoint to each centroid
        # the below method supports any number of features
        # result is not rooted as this has no impact on classification
        for i in range(k):
            s = 0
            for j in range(features):
                s = s + (centroids[i,j] - data[d,j]) * (centroids[i,j] - data[d,j])
            if (s<mindist):
                mindist = s
                minid = i
        results[d] = minid
    host = socket.gethostname()
    return(host, results)

if __name__ == '__main__':
    import dispy, socket
    import numpy as np
    # fetch the IP address of the client
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.0.0.1", 80)) # doesn't matter if 8.8.8.8 can't be reached
    
    f = open("data.txt","r")

    lines = f.readlines()

    f.close()

    numdata = len(lines)
    features = len(lines[0].split())

    data = np.random.rand(numdata,features)

    for x in range(numdata):
        templine = lines[x].split()
        for y in range(features):
            data[x][y] = templine[y]

    k = 7
    centroidID = np.random.permutation(numdata)
    centroids = np.random.rand(k,features)
    for i in range(k):
        centroids[i] = data[centroidID[i]]
    
    # repeat cycle x number of times to train centroids
    numtrials = 2
    
    for trialNum in range(numtrials):
        #  reset cluster for fresh use
        cluster = dispy.JobCluster(cmap1,ip_addr=s.getsockname()[0], nodes='10.0.0.*')
        
        # split each data piece into its own job
        numJobs = numdata
        results = []
        jobs = []

        for i in range(numJobs):
            # schedule execution of 'cmap1' on a node (running 'dispynode')
            # with a parameter (single data piece to be classafied)
            job = cluster.submit(centroids,data[i],k)
            job.id = i # optionally associate an ID to job (if needed later)
            jobs.append(job)
        # cluster.wait() # waits for all scheduled jobs to finish


        for job in jobs:
            host, n = job() # waits for job to finish and returns results
            # for single values
            results.append(n)
            # for iterables
            # results = [*results, *n]
            print('%s executed job %s in %s seconds' % (host, job.id, job.end_time - job.start_time))
            # other fields of 'job' that may be useful:
            # print(job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time)
        cluster.print_status()
        cluster.close()
        
        # group data by clusterID to facilitate recomputing clusters
        clusteredData = []
        for a in range(k):
            clusteredData.append([i for i, x in enumerate(results) if x == a])
            l = len(clusteredData[a])
            for j in range(l):
                clusteredData[a][j] = data[clusteredData[a][j]]
                
        # reset cluster to use different function
        cluster = dispy.JobCluster(featureAverage,ip_addr=s.getsockname()[0], nodes='10.0.0.*')
        
        # setup empty results and jobs
        results = []
        jobs = []
        # cluster averages will be computed feature by feature
        jobId = 0
        
        # for each cluster
        for i in range(k):
            numDiC = len(clusteredData[i])
            # for each feature in the cluster
            for j in range(features):
                featureList = np.zeros(numDiC)
                # append each datas value for the feature
                for m in range(numDiC):
                    featureList[m] = clusteredData[i][m][j]
                # send off to be calculated
                job = cluster.submit(featureList)
                job.id = jobId
                jobId = jobId + 1
                jobs.append(job)

        for job in jobs:
            n = job() # waits for job to finish and returns results
            # for single values
            results.append(n)
            # for iterables
            # results = [*results, *n]
            print('executed job %s in %s seconds' % (job.id, job.end_time - job.start_time))
        cluster.print_status()
        cluster.close() # the MOST important line if the cluster needs to be activated multiple times with different jobs
        
        # reset the centroids
        for i in range(k):
            for j in range(features):
                centroids[i,j] = results[(features*i) + j]
        print(centroids)
cluster.close()