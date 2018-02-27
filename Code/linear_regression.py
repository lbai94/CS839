
# coding: utf-8

# In[2]:


#cd E:\18Spring\CS839\Stage1\CS839_1\Code


# In[3]:


import os
import sys
#from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split


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


fid = './test.txt';
f = open(fid);
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
# Split the data into training/testing sets
#X_train = X[:-1130]
#X_test = X[-1130:]

# Split the targets into training/testing sets
#Y = [int(y>0) for y in Y]
#split
#X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Create linear regression object

Y_train = [int(y>0) for y in Y_train]
Y_test = [int(y>0) for y in Y_test]
regr = linear_model.LinearRegression()



# Train the model using the training sets
regr.fit(X_train, Y_train)

Y_predict = regr.predict(X_test)






# In[6]:


from sklearn.model_selection import cross_val_score
from sklearn import metrics
threshold = 0.5
Y_predict = [int(y>threshold) for y in Y_predict]
p = metrics.precision_score(Y_test, Y_predict)
r = metrics.recall_score(Y_test,Y_predict)
print p, r


# In[14]:


#cross validation
from sklearn.utils import shuffle
#X_train, Y_train = shuffle(X_train,Y_train)
train_size = len(X_train)
print train_size
subset_size = train_size/5
print subset_size
p_list = []
r_list = []
f1_list = []
for i in range(0, 5):
    regr = linear_model.LinearRegression()
    cv_train_X = X_train[0:i*subset_size] +  X_train[(i+1)*subset_size:]
    cv_train_Y = Y_train[0:i*subset_size] +  Y_train[(i+1)*subset_size:]
    cv_test_X = X_train[i*subset_size:(i+1)*subset_size]
    cv_test_Y = Y_train[i*subset_size:(i+1)*subset_size]
    #print len(cv_train_X), len(cv_train_Y),len(cv_test_X),len(cv_test_Y)
    regr.fit(cv_train_X, cv_train_Y)
    cv_predict = regr.predict(cv_test_X)
    cv_predict = [int(y>threshold) for y in cv_predict]
    #print cv_test_Y[0:100]
    #print cv_predict[0:100]
    p_list.append(metrics.precision_score(cv_test_Y, cv_predict))
    r_list.append(metrics.recall_score(cv_test_Y, cv_predict))
    f1_list.append(metrics.f1_score(cv_test_Y, cv_predict))
print np.average(p_list)
print np.average(r_list)
print np.average(f1_list)

