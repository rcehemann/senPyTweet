#!/usr/bin/env python
# coding: utf8
"""Train a convolutional neural network text classifier on the
IMDB dataset, using the TextCategorizer component. The dataset will be loaded
automatically via Thinc's built-in dataset loader. The model is added to
spacy.pipeline, and predictions are available via `doc.cats`. For more details,
see the documentation:
* Training: https://spacy.io/usage/training
Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function
import plac
from pathlib import Path
import pandas as pd
import sys, os, shutil
import spacy
from spacy.util import minibatch, compounding
from app.sen_py import clean_tweet
spacy.prefer_gpu()

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_texts=("Number of texts to train from", "option", "t", int),
    n_iter=("Number of training iterations", "option", "n", int),
    n_gram_size=("N-gram size in bag of words component", "g", int))
def main(model=None, output_dir=None, n_iter=20, n_texts=250000, seed=None, n_gram_size=2):
    if seed is None:
      from random import randint
      seed = randint(0, 1e6)
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        if output_dir == model:
            if os.path.isdir(model+'_backup'):
                shutil.rmtree(model+'_backup')
            os.rename(model, model+'_backup')
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.load('en_core_web_sm')  # create blank Language class
        print("loaded 'en_core_web_sm' model")

    # add the text classifier to the pipeline if it doesn't exist
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'textcat' not in nlp.pipe_names:
        textcat = nlp.create_pipe(
                      'textcat',
                      config={
                        'architecture':'ensemble',
                        'ngram_size':n_gram_size
                      }
                  )
        nlp.add_pipe(textcat, last=True)
    # otherwise, get it, so we can add labels to it
    else:
        textcat = nlp.get_pipe('textcat')

    # add label to text classifier
    if 'POSITIVE' not in textcat.labels:
        textcat.add_label('POSITIVE')

    # load the IMDB dataset
    print("Loading Sentiment 140 data...")
    (train_texts, train_cats), (dev_texts, dev_cats) = load_data(limit=n_texts)
    print("Using {} examples ({} training, {} evaluation)"
          .format(n_texts, len(train_texts), len(dev_texts)))
    train_data = list(zip(train_texts,
                          [{'cats': cats} for cats in train_cats]))

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
    with nlp.disable_pipes(*other_pipes):  # only train textcat
        optimizer = nlp.begin_training()
        print("Training the model...")
        with open("training_log.dat", 'w') as f:
            print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))
            for i in range(n_iter):
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(train_data, size=compounding(1., 32., 1.1))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(texts, annotations, sgd=optimizer, drop=0.2,
                            losses=losses)
                with textcat.model.use_params(optimizer.averages):
                    # evaluate on the dev data split off in load_data()
                    scores = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
                print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'  # print a simple table
                    .format(losses['textcat'], scores['textcat_p'],
                            scores['textcat_r'], scores['textcat_f']))
                f.write('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'  # print a simple table
                    .format(losses['textcat'], scores['textcat_p'],
                            scores['textcat_r'], scores['textcat_f']))

    # test the trained model
    test_text = "This movie sucked"
    doc = nlp(test_text)
    print(test_text, doc.cats)

    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        doc2 = nlp2(test_text)
        print(test_text, doc2.cats)

def load_data(limit=0, split=0.8):
    """Load data from the IMDB dataset."""
    # Partition off part of the train data for evaluation
    data = pd.read_csv('./app/data/training.1600000.processed.noemoticon.csv',
                       encoding='iso_8859_1')
    train_data = data.sample(frac=1.0)[['tweet', 'sentiment']]
    #train_data['tweet'] = train_data['tweet'].apply(clean_tweet)
    train_data = train_data.values[-limit:]
    texts, labels = zip(*train_data)
    cats = [{'POSITIVE': bool(y)} for y in labels]
    split = int(len(train_data) * split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])


def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    tp = 1e-8  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 1e-8  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        for label, score in doc.cats.items():
            if label not in gold:
                continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f_score = 2 * (precision * recall) / (precision + recall)
    return {'textcat_p': precision, 'textcat_r': recall, 'textcat_f': f_score}

if __name__ == '__main__':
    plac.call(main)
