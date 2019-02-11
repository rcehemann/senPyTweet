#!/usr/bin/env python
# coding: utf8
"""Train simple Multinomial Naive-Bayes (nb)
  and L1-logistic regression (lr) models using
  the scikit/learn api
fit with sklearn version 0.20.1
"""
import plac
from pathlib import Path
import pandas as pd
import pickle
from copy import deepcopy


from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

classifiers = {
  'nb':MultinomialNB(),
  'lr':LogisticRegression(penalty='l1'),
}

@plac.annotations(
    model=("Model name, accepts NB or LR", "option", "m", str),
    output_dir=("output filename", "option", "o", Path),
    n_texts=("Number of texts to train from", "option", "t", int),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model=None, output_dir=None, n_iter=20, n_texts=250000):
    if model not in classifiers.keys():
      raise Exception("Only supports nb, lr, and svc models")
    else:
        classifier = deepcopy(classifiers[model])
        model = Pipeline([
          ('vec', TfidfVectorizer()),
          ('clf', classifier)
        ])

    # load the IMDB dataset
    print("Loading Sentiment 140 data...")
    (train_texts, train_cats), (dev_texts, dev_cats) = load_data(limit=n_texts)
    print("Using {} examples ({} training, {} evaluation)"
          .format(n_texts, len(train_texts), len(dev_texts)))
    train_data = list(zip(train_texts,
                          [{'cats': cats} for cats in train_cats]))

    model.fit(train_texts, train_cats)

    print(classification_report(dev_cats, model.predict(dev_texts)))

    # test the trained model
    test_text = "This movie sucked"
    print(test_text, model.predict_proba([test_text]))

    if output_dir is not None:
        with open(output_dir, 'wb') as f:
          pickle.dump(model, f)

def load_data(limit=0, split=0.8):
    """Load data from the IMDB dataset."""
    # Partition off part of the train data for evaluation
    data = pd.read_csv('../../data/training.1600000.processed.noemoticon.csv',
                       encoding='iso_8859_1')
    train_data = data.sample(frac=1.0)[['tweet', 'sentiment']].values
    train_data = train_data[-limit:]
    texts, labels = zip(*train_data)
    split = int(len(train_data) * split)
    return (texts[:split], labels[:split]), (texts[split:], labels[split:])

if __name__ == '__main__':
    plac.call(main)
