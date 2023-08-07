import pickle
from pathlib import Path

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline


def read_data(dataset_path):
    class_names = ['toxic', 'severe_toxic', 'obscene',
                   'insult', 'identity_hate']
    train = pd.read_csv(dataset_path).fillna(' ')
    train_text = train['comment_text']
    train_targets = train[class_names]
    return train_text, train_targets


def build_pipeline():
    seed = 1234
    word_vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        strip_accents='unicode',
        analyzer='word',
        token_pattern=r'\w{1,}',
        stop_words='english',
        ngram_range=(1, 1),
        max_features=10000,
    )

    logistic = LogisticRegression(C=0.1, solver='sag', random_state=seed)
    classifier = MultiOutputClassifier(logistic)

    pipeline = Pipeline(steps=[
        ('word_tfidf', word_vectorizer),
        ('logistic', classifier)
    ])
    return pipeline


def build_model(dataset_path: Path, model_path: Path) -> None:
    train, targets = read_data(dataset_path)

    pipeline = build_pipeline()
    pipeline.fit(train, targets)

    output_path = model_path / "pipeline.dat"
    with output_path.open("wb") as f:
        pickle.dump(pipeline, f)
