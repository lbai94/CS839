import os
import sys
from sklearn import svm

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
