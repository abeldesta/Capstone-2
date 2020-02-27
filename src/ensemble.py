from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from transfer_model import TransferModel
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, accuracy_score
from sklearn.metrics import confusion_matrix, f1_score, recall_score
from sklearn.model_selection import KFold
from numpy.random import seed
from sklearn.model_selection import GridSearchCV
seed(1217)

def evaluate(model, test_features, test_labels):
    predictions = model.predict(test_features)
    errors = abs(predictions - test_labels)
    
    accuracy = model.score(test_features, test_labels)
    print('Model Performance')
    print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
    print('Accuracy = {:0.2f}%.'.format(accuracy))
    
    return accuracy

rf = RandomForestClassifier(n_estimators=300,
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
                        random_state=1217, 
                        verbose=0, 
                        warm_start=False, 
                        class_weight=None)




def cross_val(X_train, y_train, k, model):
    kf = KFold(n_splits=k, shuffle = True, random_state=0)
    accs = []
    prec = []
    recall = []
    f_score = []
    for train, test in kf.split(X_train):
        X_tr, X_test = X_train[train], X_train[test]
        y_tr, y_test = y_train[train], y_train[test]
        model.fit(X_tr, y_tr)
        y_pred = model.predict(X_test)
        accs.append(accuracy_score(y_test, y_pred))
        prec.append(precision_score(y_test, y_pred,average = 'macro'))
        recall.append(recall_score(y_test, y_pred, average = 'macro'))
        f_score.append(f1_score(y_test, y_pred, average = 'macro'))
    return [np.mean(accs), np.mean(prec), np.mean(recall), np.mean(f_score)], model

# Create the parameter grid based on the results of random search 
param_grid = {
    'bootstrap': [True, False],
    'max_depth': [20, 30, 40, 80, 90, 100, 110, None],
    'max_features': [2, 3, 4, 5, 6],
    'min_samples_leaf': [3, 4, 5],
    'min_samples_split': [8, 10, 12],
    'n_estimators': [100, 200, 300, 1000]
}

# grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
                        #   cv = 3, n_jobs = -1, verbose = 2)

if __name__ == "__main__":
    train_loc = 'data/Train'
    holdout_loc = 'data/Holdout'
    test_loc = 'data/Test'
    transfer = TransferModel('transfer', (250,250,3), 3, 10)
    transfer.fit(train_loc,test_loc,holdout_loc)
    
    train_labels, train_feats = transfer.train_labels.reshape(-1,1), transfer.train_features 
    test_labels, test_feats = transfer.test_labels, transfer.test_features
    holdout_labels, holdout_feats = transfer.holdout_labels.reshape(-1,1), transfer.holdout_features

    train_df = np.vstack([train_feats, holdout_feats])
    train_labels = np.vstack([train_labels, holdout_labels]).reshape(-1,)

    # base_model = RandomForestClassifier(n_estimators = 100, random_state = 42)
    # base_model.fit(train_df, train_labels)
    # base_accuracy = evaluate(base_model, holdout_feats, holdout_labels)

    # grid_search.fit(train_df, train_labels)
    # best_grid = grid_search.best_estimator_
    # grid_accuracy = evaluate(best_grid, holdout_feats, holdout_labels)

    gdbc = GradientBoostingClassifier(learning_rate=0.1,
                                  loss='deviance',
                                  n_estimators=300,
                                  random_state=1217)

    abc = AdaBoostClassifier(DecisionTreeClassifier(),
                            learning_rate=0.1,
                            n_estimators=300,
                            random_state=1217)

    

    
    # rf.fit(train_df, train_labels)
    # scoring = [accuracy_score(), precision_score('macro'), recall_score('macro')]
    scores, rf_model = cross_val(train_df, train_labels, 5, rf)
    print('Mean Accuracy: {0}'.format(scores[0]))
    print('Mean Precision: {0}'.format(scores[1]))
    print('Mean Recall: {0}'.format(scores[2]))
    print('Mean F1 Score: {0}'.format(scores[3]))
    y_pred = rf_model.predict(test_feats)
    acc = accuracy_score(test_labels, y_pred)
    p = precision_score(test_labels, y_pred, average='macro')
    r = recall_score(test_labels, y_pred, average = 'macro')
    f_score = f1_score(test_labels, y_pred, average = 'macro')
    print('Holdout Accuracy: {0}'.format(acc))
    print('Holdout Precision: {0}'.format(p))
    print('Holdout Recall: {0}'.format(r))
    print('Holdout F1 Score: {0}'.format(f_score))
    cm = confusion_matrix(test_labels, y_pred)
    print('Confusion Matrix: {}'.format(cm))

    scores_gdbc, gdbc_model = cross_val(train_df, train_labels, 5, gdbc)
    print('Mean Gradient Boosting Accuracy: {0}'.format(scores_gdbc[0]))
    print('Mean Gradient Boosting Precision: {0}'.format(scores_gdbc[1]))
    print('Mean Gradient Boosting Recall: {0}'.format(scores_gdbc[2]))
    print('Mean Gradient Boosting F1 Score: {0}'.format(scores[3]))
    y_pred_gdbc = gdbc_model.predict(test_feats)
    acc = accuracy_score(test_labels, y_pred_gdbc)
    p = precision_score(test_labels, y_pred_gdbc, average='macro')
    r = recall_score(test_labels, y_pred_gdbc, average = 'macro')
    f_score = f1_score(test_labels, y_pred_gdbc, average = 'macro')
    print('Holdout Gradient Boosting Accuracy: {0}'.format(acc))
    print('Holdout Gradient Boosting Precision: {0}'.format(p))
    print('Holdout Gradient Boosting Recall: {0}'.format(r))
    print('Holdout Gradient Boosting F1 Score: {0}'.format(f_score))
    cm = confusion_matrix(test_labels, y_pred_gdbc)
    print('Confusion Matrix: {}'.format(cm))



    scores_abc, abc_model = cross_val(train_df, train_labels, 5, abc)
    print('Mean Adaboosting Accuracy: {0}'.format(scores_abc[0]))
    print('Mean Adaboosting Precision: {0}'.format(scores_abc[1]))
    print('Mean Adaboosting Recall: {0}'.format(scores_abc[2]))
    print('Mean Adaboosting F1 Score: {0}'.format(scores[3]))
    y_pred_abc = abc_model.predict(test_feats)
    acc = accuracy_score(test_labels, y_pred_abc)
    p = precision_score(test_labels, y_pred_abc, average='macro')
    r = recall_score(test_labels, y_pred_abc, average = 'macro')
    f_score = f1_score(test_labels, y_pred_abc, average = 'macro')
    print('Holdout Adaboosting Accuracy: {0}'.format(acc))
    print('Holdout Adaboosting Precision: {0}'.format(p))
    print('Holdout Adaboosting Recall: {0}'.format(r))
    print('Holdout Adaboosting F1 Score: {0}'.format(f_score))
    cm = confusion_matrix(test_labels, y_pred_abc)
    print('Confusion Matrix: {}'.format(cm))