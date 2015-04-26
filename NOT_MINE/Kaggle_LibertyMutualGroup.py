"""
Beating the benchmark for Liberty Mutual Fund @ Kaggle

__author__ : Abhishek Thakur
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, Lasso

data_folder = "C:/coding/Kaggle/Liberty MutualGroup_FirePeril_LossCost/data/"
submissions_folder = "C:/coding/Kaggle/Liberty MutualGroup_FirePeril_LossCost/submissions/"

train = pd.read_csv(data_folder + 'train.csv')
test = pd.read_csv(data_folder + 'test.csv')
sample = pd.read_csv(data_folder + 'sampleSubmission.csv')

tr = train[['var11', 'var12', 'var13', 'var14', 'var15', 'var16', 'var17']]
ts = test[['var11', 'var12', 'var13', 'var14', 'var15', 'var16', 'var17']]

tr = np.nan_to_num(np.array(tr))
ts = np.nan_to_num(np.array(ts))

clf = Ridge()
clf.fit(tr, train['target'].values)
preds = clf.predict(ts)

sample['target'] = preds

sample.to_csv(submssions_folder + 'submission.csv', index = False)
