from sklearn.ensemble import RandomForestClassifier
from transfer_model import TransferModel
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, accuracy_score, confusion_matrix, recall_score
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

rf = RandomForestClassifier(n_estimators=100,
                        criterion="gini",
                        max_depth=None,
                        min_samples_split=2, 
                        min_samples_leaf=1, 
                        min_weight_fraction_leaf=0., 
                        max_features="auto", 
                        max_leaf_nodes=None, 
                        min_impurity_decrease=0., 
                        min_impurity_split=None, 
                        bootstrap=True, 
                        oob_score=False, 
                        n_jobs=-1, 
                        random_state=None, 
                        verbose=0, 
                        warm_start=False, 
                        class_weight=None)


if __name__ == "__main__":
    train_loc = 'data/Train'
    holdout_loc = 'data/Holdout'
    test_loc = 'data/Test'
    transfer = TransferModel('transfer', (100,100,3), 3, 10)
    transfer.fit(train_loc,test_loc,holdout_loc,1)
    
    train_labels, train_feats = transfer.train_labels, transfer.train_features 
    test_labels, test_feats = transfer.test_labels, transfer.test_features
    holdout_labels, holdout_feats = transfer.holdout_labels, transfer.holdout_features


    rf.fit(train_feats, train_labels)
