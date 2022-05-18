def taylorarctan(indiciesList,X):
    sum = 0
    for n in range(indiciesList[0],indiciesList[1]):
        ##The Taylor Series formula for arctan when -1 <= X <= 1
        middle = ((2*n)+1)
        sum = sum + ((-1)**n)*((X**(middle)) / (middle))
    return sum


if __name__ == '__main__':
    import dispy, socket, time
    import numpy as np
    
    ##fetch the IP address of the client
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.0.0.2", 80)) ##doesn't matter if 8.8.8.8 can't be reached
    
    ##Setup Cluster
    cluster = dispy.JobCluster(taylorarctan,ip_addr=s.getsockname()[0], nodes=['10.0.0.3','10.0.0.4','10.0.0.5','10.0.0.6'])
    
    ##Initialise Variables
    precision = 10000
    indicies = list(range(precision))
    numJobs = 16
    nums = (0.5666666666666,-0.232323232323,0.99999999,0.00001,0.94524837652)
    joblist = np.array_split(indicies,numJobs)

    for x in nums:
        results = 0
        jobs = []

        for job in joblist:
            job = cluster.submit((job[0],job[-1]),x)
            jobs.append(job)
            
        for job in jobs:
            results = results + job()
        
        print("Arctan of %s" % x)
        print("Taylor Approximation at %s precision: %s" % (precision, results))
        realResults = np.arctan(x)
        print("Function Results: %s" % realResults)
        difference = realResults - results
        dPercentage = (1-abs(difference/realResults)) * 100
        print("Similarity: %s %% " % dPercentage)
        print("")
    
    cluster.close()
