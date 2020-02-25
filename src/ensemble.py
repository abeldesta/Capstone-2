from sklearn.ensemble import RandomForestClassifier
from transfer_model import TransferModel
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, accuracy_score, confusion_matrix, recall_score
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from multiscorer import MultiScorer


scorer = MultiScorer({
    'Accuracy'  : (accuracy_score , {}),
    'Precision' : (precision_score, {'pos_label': 3, 'average':'macro'}),
    'Recall'    : (recall_score   , {'pos_label': 3, 'average':'macro'})
})

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
    transfer.fit(train_loc,test_loc,holdout_loc)
    
    train_labels, train_feats = transfer.train_labels.reshape(-1,1), transfer.train_features 
    test_labels, test_feats = transfer.test_labels.reshape(-1,1), transfer.test_features
    holdout_labels, holdout_feats = transfer.holdout_labels, transfer.holdout_features

    train_df = np.vstack([train_feats, test_feats])
    train_labels = np.vstack([train_labels, test_labels]).reshape(-1,)

    rf.fit(train_df, train_labels)
    # scoring = [accuracy_score(), precision_score('macro'), recall_score('macro')]
    rmse = cross_validate(rf, train_df, train_labels, n_jobs=-1, cv = 10, scoring = scorer)
    print('Mean MSE: {0}'.format(rmse))
    print('MSE: {0}'.format(rmse))
    acc = rf.score(holdout_feats, holdout_labels)
    print('Holdout Accuracy: {0}'.format(acc))


