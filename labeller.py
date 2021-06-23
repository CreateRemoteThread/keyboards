#!/usr/bin/env python3

import glob
import support
import numpy as np

print("step 1: training")
import sklearn.model_selection as model_selection

test_data = []
test_labels = []
for fn in glob.glob("toothpicks/*.npy"):  
  print("Loading %s" % fn)
  f_data = np.load(fn)
  test_data.append(f_data[0:5000])
  test_labels.append(support.get_label(fn))

print(test_data)
print(test_labels)

from sklearn import svm
clf = svm.SVC(gamma=0.001,C=100.)
clf.fit(test_data,test_labels)

for fn in glob.glob("floss/*.npy"):
  print("Predicting %s" % fn)
  f_data = np.load(fn)
  print(clf.predict([f_data[0:5000]]))

