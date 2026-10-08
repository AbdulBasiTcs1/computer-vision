import math


class LVQVariant:
    # Choose the prototype with the smallest Euclidean distance.
    def winner(self, weights, sample):
        distances = [math.dist(sample, w) for w in weights]
        return 0 if distances[0] <= distances[1] else 1

    # Move the winner closer to the correct class and away from wrong class.
    def update(self, weights, sample, winner_index, alpha, label):
        direction = 1 if label == winner_index else -1
        for i in range(len(weights[winner_index])):
            diff = sample[i] - weights[winner_index][i]
            weights[winner_index][i] += direction * alpha * diff


def main():
    X = [
        [0, 0, 1, 1], [1, 0, 0, 0],
        [0, 0, 0, 1], [0, 1, 1, 0],
        [1, 1, 0, 0], [1, 1, 1, 0]
    ]
    Y = [0, 1, 0, 1, 1, 1]

    # Use the first two samples as initial prototype vectors.
    weights = [X.pop(0), X.pop(0)]
    training_samples = X
    training_labels = Y[2:]

    model = LVQVariant()
    for _ in range(3):
        for sample, label in zip(training_samples, training_labels):
            winner_index = model.winner(weights, sample)
            model.update(weights, sample, winner_index, 0.1, label)

    test_sample = [0, 0, 1, 0]
    result = model.winner(weights, test_sample)
    print("Sample T belongs to class:", result)
    print("Trained weights:", weights)


if __name__ == "__main__":
    main()
