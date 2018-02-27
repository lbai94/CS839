import os
import sys
from sklearn import svm

fid = './train.txt';
f = open(fid);
Xtr = []; Ytr = [];
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
	Xtr.append(x);
	Ytr.append(y);
f.close();

fid = './test.txt';
f = open(fid);
Xte = []; Yte = [];
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
	Xte.append(x);
	Yte.append(y);
f.close();