import os
import sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

fid = './train.txt';
f = open(fid);
X_train = []; Y_train = [];
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
	X_train.append(x);
	Y_train.append(y);
f.close();
       
fid1 = './test.txt';
f = open(fid1);
X_test = []; Y_test = [];
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
	X_test.append(x);
	Y_test.append(y);
f.close();       

clf = LogisticRegression();
scores = cross_val_score(clf, X_train, Y_train, cv=5)
print scores, scores.mean();

clf.fit(X_train, Y_train);
Yp = clf.predict(X_test);
Np = 0;
Nr = 0;
TotalPositive = 0;
for i in range(len(Y_test)):
	if Yp[i]==Y_test[i]:
		Np += 1;
	if Y_test[i]==1:
		TotalPositive += 1;
		if Yp[i]==Y_test[i]:
			Nr += 1;

print('Precision: %f' %(float(Np)/len(Y_test)));
print('Recall: %f' %(float(Nr)/TotalPositive));