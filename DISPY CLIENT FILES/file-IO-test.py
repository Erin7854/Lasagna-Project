import sklearn.datasets as dataset
numdata = 100
features = 2
data = dataset.make_blobs(n_samples=numdata, n_features=features)
f=open("data.txt","w")
for a in data[0]:
    tempstr = ""
    for x in a:
        tempstr = tempstr + str(x) + " "
    tempstr = tempstr + "\r\n"
    f.write(tempstr)
f.close()
