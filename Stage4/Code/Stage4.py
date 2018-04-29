
# coding: utf-8

# In[3]:


#cd E:\18Spring\CS839\Stage1\CS839_1\Stage3\Data


# In[4]:


import py_entitymatching as em
import pandas as pd
import os, sys
import time
import datetime


# In[5]:


B = em.read_csv_metadata('Barnob.csv',key = 'ID')
B


# In[6]:


A = em.read_csv_metadata('Amazon.csv', key='ID',encoding = "ISO-8859-1")


# In[7]:


A


# In[9]:


#blocking
ab = em.AttrEquivalenceBlocker()
ob = em.OverlapBlocker()
start = datetime.datetime.now()
C = ab.block_tables(A, B, 'Time', 'Time', l_output_attrs=['ID','Title','Author','Publisher','Time'], r_output_attrs=['ID','Title','Author','Publisher','Time'])
C = ob.block_candset(C, 'Author', 'Author')
end = datetime.datetime.now()
print ((end-start).total_seconds())
em.to_csv_metadata(C, 'block.csv')
C


# In[10]:


#Sampling
S = em.sample_table(C, 350)
S


# In[11]:


#Labeling (In this project, we label the saved csv fie in Excel) 
G = em.label_table(S, label_column_name='gold_labels')


# In[12]:


#save sampled Data to a file
em.to_csv_metadata(G, './noLabel.csv')


# In[13]:


# read the labeled data
G = em.read_csv_metadata('../Data/Label.csv', 
                         key='_id',
                         ltable=A, rtable=B, 
                         fk_ltable='ltable_ID', fk_rtable='rtable_ID')
G


# In[14]:


# split the data into training data I and evaluation data J
IJ = em.split_train_test(G, train_proportion=0.6, random_state=0);
I = IJ['train'];
J = IJ['test'];
em.to_csv_metadata(I, './train.csv')
em.to_csv_metadata(J,'./test.csv')
I


# In[15]:


J


# In[16]:


# Create a set of ML-matchers
dt = em.DTMatcher(name='DecisionTree', random_state=0);
rf = em.RFMatcher(name='Random Forest', random_state=0);
svm = em.SVMMatcher(name='SVM', random_state=0);
nb = em.NBMatcher(name='Naive Bayes');
lg = em.LogRegMatcher(name='Logistic Reg', random_state=0);
ln = em.LinRegMatcher(name='Linear Reg');


# In[17]:


# Creating a feature table F.
F = em.get_features_for_matching(A, B, validate_inferred_attr_types=False);


#Converting I into a set H of feature vectors (using the features in F).
H = em.extract_feature_vecs(I, 
                            feature_table=F, 
                            attrs_after='gold_labels',
                            show_progress=False);

#Filling in the missing values if any in H.
H = em.impute_table(H, 
                exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold_labels'],
                strategy='mean');

#Selecting the best matcher in the first iteration using cross-validation.
start = datetime.datetime.now()
result = em.select_matcher([dt, rf, svm, nb, lg, ln], table=H, 
        exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold_labels'],
        k=5,
        target_attr='gold_labels', metric_to_select_matcher='f1', random_state=0);
end = datetime.datetime.now()
print ((end-start).total_seconds())
#print(result['cv_stats']);


# In[18]:


result['cv_stats']


# In[19]:


#Selecting the best matcher Y again using cross-validation.
Y = dt;


# In[20]:


# Evaluating the best matcher Y using J.
L = em.extract_feature_vecs(J, 
                            feature_table=F, 
                            attrs_after='gold_labels',
                            show_progress=False);

L = em.impute_table(L, 
                exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold_labels'],
                strategy='mean');

# train on I using the best learner Y.
Y.fit(table=H, 
       exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold_labels'], 
       target_attr='gold_labels');

# make predictions on J and show the result
predictions = Y.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold_labels'], 
              append=True, target_attr='predicted', inplace=False);

eval_result = em.eval_matches(predictions, 'gold_labels', 'predicted');
em.print_eval_summary(eval_result);


# In[21]:


predictions


# In[22]:


Feature = em.extract_feature_vecs(C, 
                            feature_table=F, 
                            show_progress=False);


# In[23]:


Feature = em.impute_table(Feature, 
                exclude_attrs=['_id', 'ltable_ID', 'rtable_ID'],
                strategy='mean');


# In[24]:


pred = Y.predict(table=Feature, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID'], 
              append=True, target_attr='predicted', inplace=False);


# In[34]:


Matched = [0]*(len(A) + 1)
drop_unmatch = []
for index, row in pred.iterrows():
    if row['predicted'] == 1:
        Matched[int(row['ltable_ID'])] = 1;
    else:
        drop_unmatch.append(index)
all_match = C.drop(drop_unmatch)
em.to_csv_metadata(all_match, './Matches.csv')


# In[27]:


Result = B
id = 3862
for index, row in A.iterrows():
    if Matched[row['ID']] == 0:
        row['ID'] = id
        id = id + 1
        Result.loc[row['ID']-1]=row
em.to_csv_metadata(Result, './E.csv')


# In[28]:


drop_list=[]
Result_clean=Result
for i, row in Result.iterrows():
    if Result.loc[i].isnull().any():
        drop_list.append(i)


# In[29]:


E_clean = Result_clean.drop(drop_list)
em.to_csv_metadata(E_clean, './E_clean.csv')

