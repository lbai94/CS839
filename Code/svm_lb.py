
# coding: utf-8

# In[1]:


#cd E:\18Spring\CS839\Stage1\CS839_1\Code


# In[8]:


import os
import sys
#from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model,svm
from sklearn.model_selection import train_test_split


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

# Split the data into training/testing sets
#X_train = X[:-1130]
#X_test = X[-1130:]

# Split the targets into training/testing sets
Y = [int(y>0) for y in Y]
#split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Create linear regression object
clf = svm.SVC(kernel='rbf', C=100, random_state=0, tol=1e-12)



# Train the model using the training sets
#regr.fit(X_train, Y_train)

#Y_predict = regr.predict(X_test)






# In[9]:


from sklearn.model_selection import cross_validate
from sklearn.metrics import recall_score
scoring = ['precision_macro', 'recall_macro']
scores = cross_validate(clf, X_train, Y_train, scoring=scoring,cv=5, return_train_score=False)
sorted(scores.keys())
print scores['test_precision_macro']  
print scores['test_recall_macro']

