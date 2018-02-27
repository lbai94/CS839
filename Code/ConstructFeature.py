import os
import sys
from sklearn import svm

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
X = [];
#training data, label
Y = [];
num_of_files = 0;
WhiteList_Mr = ['mr', 'ms', 'sir', 'lord', 'mrs', 'chairman', 'leader'];
WhiteList_verb = ['say', 'says', 'said', 'feel', 'feels', 'felt'];
BlackList = ['england', 'lib dems', 'tory', 'tories', 'lim dem', 'monday'\
			'sunday', 'british', 'labour Party', 'manchester', 'association'];
for fid in fids:
	if fid.endswith('.txt'):
		num_of_files += 1;
		X_fid, Y_fid = Construct(Data+'/'+fid);
		X=X+X_fid;
		Y=Y+Y_fid;
print(len(Y));

fid = './Input.txt';
f = open(fid, 'w');
for i in range(len(Y)):
	for j in range(len(X[i])):
		if j==len(X[i])-1:
			f.write(str(X[i][j]) + '\n');
		else:
			f.write(str(X[i][j]) + ',');
	f.write(str(Y[i]) + '\n');
f.close();
