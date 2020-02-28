
import pickle
import pandas as pd 
import numpy as np
import skimage.io
import skimage.transform
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, accuracy_score
from sklearn.metrics import confusion_matrix, f1_score, recall_score
from sklearn.model_selection import KFold
from numpy.random import seed
import os
import itertools
from transfer_model import TransferModel


train_loc = 'data/Train'
holdout_loc = 'data/Holdout'
test_loc = 'data/Test'
transfer = TransferModel('transfer', (250,250,3), 3, 10)
transfer.fit(train_loc,test_loc,holdout_loc)

train_labels, train_feats = transfer.train_labels.reshape(-1,1), transfer.train_features 
test_labels, test_feats = transfer.test_labels, transfer.test_features
holdout_labels, holdout_feats = transfer.holdout_labels.reshape(-1,1), transfer.holdout_features
class_names = transfer.class_names

train_df = np.vstack([train_feats, holdout_feats])
train_labels = np.vstack([train_labels, holdout_labels]).reshape(-1,)

rf_model = pickle.load(open('models/randomforest.pkl', 'rb'))
gdbc_model = pickle.load(open('models/gradientboost.pkl', 'rb'))


#Random Forest
y_pred = rf_model.predict(test_feats)
pred_prob = rf_model.predict_proba(test_feats)
acc = accuracy_score(test_labels, y_pred)
p = precision_score(test_labels, y_pred, average='macro')
r = recall_score(test_labels, y_pred, average = 'macro')
f_score = f1_score(test_labels, y_pred, average = 'macro')
print('Holdout Accuracy: {0}'.format(acc))
print('Holdout Precision: {0}'.format(p))
print('Holdout Recall: {0}'.format(r))
print('Holdout F1 Score: {0}'.format(f_score))
cm = confusion_matrix(test_labels, y_pred)
print('Confusion Matrix: \n {}'.format(cm))
predictions = np.array(test_labels == y_pred)
misclass = np.where(predictions == False)[0]


#Gradient Boost
y_pred_gdbc = gdbc_model.predict(test_feats)
pred_prob_gbdc = rf_model.predict_proba(test_feats)
acc = accuracy_score(test_labels, y_pred_gdbc)
p = precision_score(test_labels, y_pred_gdbc, average='macro')
r = recall_score(test_labels, y_pred_gdbc, average = 'macro')
f_score = f1_score(test_labels, y_pred_gdbc, average = 'macro')
print('Holdout Gradient Boosting Accuracy: {0}'.format(acc))
print('Holdout Gradient Boosting Precision: {0}'.format(p))
print('Holdout Gradient Boosting Recall: {0}'.format(r))
print('Holdout Gradient Boosting F1 Score: {0}'.format(f_score))
cm_gdbc = confusion_matrix(test_labels, y_pred_gdbc)
print('Confusion Matrix: \n {}'.format(cm))


predictions = np.array(test_labels == y_pred_gdbc)
misclass_gdbc = np.where(predictions == False)[0]

home = os.getcwd()
imgs = []
for i in class_names:
    os.chdir(os.path.abspath(test_loc + '/' + i))
    files = os.listdir()
    imgs.append(files)
    os.chdir(home)

images = np.array(list(itertools.chain.from_iterable(imgs)))[misclass]
wrong_class = test_labels[misclass]

fig, axs = plt.subplots(8,8, figsize=(12,12))
for i, ax in enumerate(axs.flatten()):
    file = class_names[wrong_class[i]]
    path_img = os.path.join(home, test_loc, file, images[i])
    img = skimage.io.imread(path_img)
    ax.imshow(img)
    ax.set_ylabel(file)
    ax.set_xlabel(images[i])
plt.savefig('img/misclassified.png')
plt.tight_layout()