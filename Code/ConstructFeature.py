import os
import sys
from sklearn import svm
import shutil
import numpy as np
def FindAround(line, S, E, k, Type):
	num = k;
	symbol = [',', ':', '<', '>', '^'];
	s = S;
	for s in range(S-1, -1, -1):
		if line[s] == ' ':
			break;
	stringAhead = line[0: s];
	WordList = stringAhead.split();
	L = len(WordList);

	for i in range(L):
		for j in symbol:
			WordList[i] = WordList[i].replace(j, '');

	ListAhead = [WordList[i].replace('^', '').replace('<','').replace('>', '') for i in range(max(0, L-k), L)];

	e = E;
	for e in range(E+1, len(line)):
		if line[e] == ' ':
			break;
	stringAfter = line[e: len(line)];
	WordList = stringAfter.split();
	L = len(WordList);

	for i in range(L):
		for j in symbol:
			WordList[i] = WordList[i].replace(j, '');

	ListAfter = [WordList[i].replace('^', '').replace('<','').replace('>', '') for i in range(0, min(k, len(WordList)))];

	if Type =='Ahead':
		return ListAhead;
	elif Type=='After':
		return ListAfter;
	elif Type=='Both':
		return ListAhead+ListAfter;

def Construct(fid):
	f=open(fid);
	X = []; Y = [];
	for line in f:
		l = len(line);
		s = 0; e = 0;
		state = 0;
		for i in range(l):
			if line[i]=='^' and state==0:
				s = i;
				state += 1;
			elif line[i]=='^' and state==1:
				e = i;
				state += 1;
			elif line[i]=='<':
				s=i;
			elif line[i]=='>':
				e=i;

			# a new example appears
			if line[i]=='>' or state==2:
				x = []; y = [];
				if state==2:
					label = 1;
				else:
					label=-1;
				y.append(label);
				name = line[s:e+1];
				name = name.replace('^', '');
				name = name.replace('<', '');
				name = name.replace('>', '');

				AllLetterCapital = 1;
				for j in range(len(name)):
					if name[j].islower():
						AllLetterCapital = 0;
						break;

				name = name.split();
				FirstLetterCapital = 1;
				for j in range(len(name)):
					if name[j][0].islower():
						FirstLetterCapital = 0;
						break;

				# feature 1
				x.append(FirstLetterCapital);

				if len(name)<=1 and label==-1:
					state=0;
					continue;

				# feature 2
				x.append(len(name));

				k=1;
				Ahead = FindAround(line, s, e, k, 'Ahead');
				ExistMr = 0;
				for j in Ahead:
					if i in WhiteList_Mr:
						ExistMr=1;
						break;
				# feature 3
				x.append(ExistMr);

				k=3;
				Both = FindAround(line, s, e, k, 'Both');

				ExistVerb = 0;
				for j in Both:
					if j.lower() in WhiteList_verb:
						ExistVerb=1;
						break;
				# feature 4
				x.append(ExistVerb);

				AtBeginEnd = 0;
				if s == 0 or e == len(line):
					AtBeginEnd = 1;
					# feature 5
				#x.append(AtBeginEnd);

				# feature 6
				x.append(AllLetterCapital);

				k=3;
				Ahead = FindAround(line, s, e, k, 'Ahead');
				ExistThe = 0;
				for j in Ahead:
					if j.lower() == 'the' or j.lower() == 'a':
						ExistThe=1;
						break;

				# feature 7
				x.append(ExistThe);

				inBlackList = 0;

				for j in name:
					if j.lower() in BlackList:
						inBlackList = 1;
				#feature 8
				x.append(inBlackList);
				X.append(x);
				Y=Y+y;
				state = 0;
	return X, Y;

Data=sys.argv[1];
fids=os.listdir(Data);
#traing data, input
X_train = [];
#training data, label
Y_train = [];

#traing data, input
X_test = [];
#training data, label
Y_test = [];

num_of_files = 0;
WhiteList_Mr = ['mr', 'ms', 'sir', 'lord', 'mrs', 'chairman', 'leader'];
WhiteList_verb = ['say', 'says', 'said', 'feel', 'feels', 'felt'];
BlackList = ['england', 'lib dems', 'tory', 'tories', 'lim dem', 'monday'\
			'sunday', 'british', 'labour Party', 'manchester', 'association'];

n=0;
I=np.random.permutation(320)[0:220];
for fid in fids:
	if fid.endswith('.txt'):
		X_fid, Y_fid = Construct(Data+'/'+fid);
		if n in I:
			X_train=X_train+X_fid;
			Y_train=Y_train+Y_fid;
			shutil.copy('/Users/host/Desktop/YuzheMa/Work/Class/Homework/CS839/CS839_1/Data/'+fid, '/Users/host/Desktop/YuzheMa/Work/Class/Homework/CS839/CS839_1/Data/Train');
		else:
			X_test=X_test+X_fid;
			Y_test=Y_test+Y_fid;
			shutil.copy('/Users/host/Desktop/YuzheMa/Work/Class/Homework/CS839/CS839_1/Data/'+fid, '/Users/host/Desktop/YuzheMa/Work/Class/Homework/CS839/CS839_1/Data/Test')
		n=n+1;

fid = './train.txt';
f = open(fid, 'w');
for i in range(len(Y_train)):
	for j in range(len(X_train[i])):
		if j==len(X_train[i])-1:
			f.write(str(X_train[i][j]) + '\n');
		else:
			f.write(str(X_train[i][j]) + ',');
	f.write(str(Y_train[i]) + '\n');
f.close();

print(len([Y_train[i] for i in range(len(Y_train)) if Y_train[i]==1]));
print(len([Y_train[i] for i in range(len(Y_train)) if Y_train[i]==-1]));

fid = './test.txt';
f = open(fid, 'w');
for i in range(len(Y_test)):
	for j in range(len(X_test[i])):
		if j==len(X_test[i])-1:
			f.write(str(X_test[i][j]) + '\n');
		else:
			f.write(str(X_test[i][j]) + ',');
	f.write(str(Y_test[i]) + '\n');
f.close();
print(len(Y_test))
print(len([Y_test[i] for i in range(len(Y_test)) if Y_test[i]==1]));
print(len([Y_test[i] for i in range(len(Y_test)) if Y_test[i]==-1]));
