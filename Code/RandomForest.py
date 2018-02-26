import os
import sys
import numpy as np
from sklearn.ensemble import RandomForestClassifier

fid = './Input.txt';
f = open(fid);
X = []; Y = [];
while 1:
	x = f.readline();
	if not x:
		break;
	x = x.rstrip('\n');
	x = x.split(',');
	x = [float(x[i]) for i in range(len(x))];
	y = f.readline();
	y = y.rstrip('\n');
	y = float(y);
	X.append(x);
	Y.append(y);

f.close();
N = len(Y);
I = list(range(N));
Tnum = int(N/5);
TeList = np.random.choice(N, Tnum);
Xte = [X[i] for i in TeList];
Yte = [Y[i] for i in TeList];
Xtr = [X[i] for i in I if i not in TeList];
Ytr = [Y[i] for i in I if i not in TeList];
clf = RandomForestClassifier(n_estimators=50)
clf = clf.fit(X, Y)
Yp = clf.predict(Xte);
Np = 0;
Nr = 0;
TotalPositive = 0;
for i in range(len(Yte)):
	if Yp[i]==Yte[i]:
		Np += 1;
	if Yte[i]==1:
		TotalPositive += 1;
		if Yp[i]==Yte[i]:
			Nr += 1;

print('Precision: %f' %(float(Np)/len(Yte)));
print('Recall: %f' %(float(Nr)/TotalPositive));


