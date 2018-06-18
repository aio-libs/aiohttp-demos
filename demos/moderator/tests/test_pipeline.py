from moderator.model.pipeline import build_pipeline, read_data


def test_build_pipeline():
    pipeline = build_pipeline()
    steps = pipeline.steps
    assert [s[0] for s in steps] == ['word_tfidf', 'logistic']


def test_train_model():
    dataset_path = "tests/toxic.csv"
    train, targets = read_data(dataset_path)

    pipeline = build_pipeline()
    pipeline.fit(train, targets)
    scores = pipeline.score(train, targets)
    assert scores
