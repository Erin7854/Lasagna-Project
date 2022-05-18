import numpy as np
a=np.array([8.540661510576545, 4.324649145818755])
b=np.array([[0.2750202243558064, 0.8212089454499039],[7.940391961683975, 4.318108993038565],[0.6860993906578856, 2.635333944999667]])
dists = []
for c in b:
    i = np.linalg.norm(a-c)
    print(i)
    dists.append(i)
Min = min(dists)
j = dists.index(Min)
print(j)
