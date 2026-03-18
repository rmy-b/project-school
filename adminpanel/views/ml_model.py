from sklearn.linear_model import LogisticRegression
import numpy as np

def train_model(data):
    X = []
    y = []

    for item in data:
        X.append([
            item['unit_avg'],
            item['mid_avg'],
            item['attendance']
        ])
        y.append(item['label'])

    if len(X) == 0:
        return None

    model = LogisticRegression()
    if len(set(y)) < 2:
        return None  # Not enough classes to train
    model.fit(X, y)

    return model


def predict_pass_rate(model, data):
    if model is None or len(data) == 0:
        return 0

    predictions = model.predict(data)

    total = len(predictions)
    passed = sum(predictions)

    pass_rate = (passed / total) * 100

    return round(pass_rate, 2)