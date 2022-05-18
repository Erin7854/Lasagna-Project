def addElem(A,B):
    import socket
    import numpy as np
    r = len(A)
    C = np.zeros(r)
    for i in range(r):
        C[i] = A[i] + B[i]
    host = socket.gethostname()
    return (host, C)

if __name__ == '__main__':
    import dispy, socket
    import numpy as np
    # fetch the IP address of the client
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.0.0.1", 80)) # doesn't matter if 8.8.8.8 can't be reached
    cluster = dispy.JobCluster(addElem,ip_addr=s.getsockname()[0], nodes='10.0.0.*')

    numJobs = 16
    arrLen = 64000

    # create random arrays
    a1 = np.random.randint(1,101,arrLen)
    a2 = np.random.randint(1,101,arrLen)
    
    l1 = np.array_split(a1,numJobs)
    l2 = np.array_split(a2,numJobs)

    results = []
    jobs = []

    for i in range(numJobs):
        # schedule execution of 'addElem' on a node (running 'dispynode')
        # with a parameter (random number in this case)
        job = cluster.submit(l1[i],l2[i])
        job.id = i # optionally associate an ID to job (if needed later)
        jobs.append(job)
    # cluster.wait() # waits for all scheduled jobs to finish


    for job in jobs:
        host, n = job() # waits for job to finish and returns results
        results = [*results, *n]
        print('%s executed job %s in %s seconds' % (host, job.id, job.end_time - job.start_time))
        # other fields of 'job' that may be useful:
        # print(job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time)
    cluster.print_status()
    cluster.close()
    

    difference = 0
    for j in range(arrLen):
        res = a1[i] + a2[i]
        difference = difference + res - results[i]

    if difference == 0:
        print('Job Completed Successfully')
    else:
        print('Job Completed with difference of %s', difference)
