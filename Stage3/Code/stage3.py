import py_entitymatching as em
import os
import pandas as pd

A = em.read_csv_metadata('../Data/amazon.csv', key='ID');
B = em.read_csv_metadata('../Data/Barnob.csv', key='ID');

G = em.read_csv_metadata('../Data/Label.csv', 
                         key='_id',
                         ltable=A, rtable=B, 
                         fk_ltable='ltable_ID', fk_rtable='rtable_ID')

IJ = em.split_train_test(G, train_proportion=0.6, random_state=0);
I = IJ['train'];
J = IJ['test'];

# Create a set of ML-matchers
dt = em.DTMatcher(name='DecisionTree', random_state=0);
rf = em.RFMatcher(name='Random Forest', random_state=0);
svm = em.SVMMatcher(name='SVM', random_state=0);
nb = em.NBMatcher(name='Naive Bayes');
lg = em.LogRegMatcher(name='Logistic Reg', random_state=0);
ln = em.LinRegMatcher(name='Linear Reg');

F = em.get_features_for_matching(A, B, validate_inferred_attr_types=False);

H = em.extract_feature_vecs(I, 
                            feature_table=F, 
                            attrs_after='gold_labels',
                            show_progress=False)

H = em.impute_table(H, 
                exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold_labels'],
                strategy='mean');

# print(any(pd.notnull(H)));

result = em.select_matcher([dt, rf, svm, nb, lg, ln], table=H, 
        exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold_labels'],
        k=5,
        target_attr='gold_labels', metric_to_select_matcher='f1', random_state=0);

print(result['cv_stats']);

Y = dt;

L = em.extract_feature_vecs(J, 
                            feature_table=F, 
                            attrs_after='gold_labels',
                            show_progress=False);

L = em.impute_table(L, 
                exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold_labels'],
                strategy='mean');

Y.fit(table=H, 
       exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold_labels'], 
       target_attr='gold_labels');

predictions = Y.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'gold_labels'], 
              append=True, target_attr='predicted', inplace=False);

eval_result = em.eval_matches(predictions, 'gold_labels', 'predicted');
em.print_eval_summary(eval_result);