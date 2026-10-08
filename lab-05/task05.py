import math


class LVQ:
    # Find the closest weight vector using Euclidean distance
    def winner(self, weights, sample):
        d0 = 0
        d1 = 0

        for i in range(len(sample)):
            d0 += (sample[i] - weights[0][i]) ** 2
            d1 += (sample[i] - weights[1][i]) ** 2

        # Return the class of the nearer prototype
        return 0 if d0 < d1 else 1

    # Move the winning prototype toward or away from the sample
    def update(self, weights, sample, j, alpha, actual):
        if actual == j:
            for i in range(len(weights[j])):
                weights[j][i] += alpha * (sample[i] - weights[j][i])
        else:
            for i in range(len(weights[j])):
                weights[j][i] -= alpha * (sample[i] - weights[j][i])


# Train and test the LVQ model
def main():
    # Training data: samples and their class labels
    X = [[0, 0, 1, 1], [1, 0, 0, 0],
         [0, 0, 0, 1], [0, 1, 1, 0],
         [1, 1, 0, 0], [1, 1, 1, 0]]
    Y = [0, 1, 0, 1, 1, 1]

    # Select first two samples as initial weight vectors
    weights = [X.pop(0), X.pop(0)]
    m = len(X)
    Y = Y[2:]

    # Train LVQ for a few epochs
    model = LVQ()
    epochs = 3
    alpha = 0.1

    for _ in range(epochs):
        for j in range(m):
            sample = X[j]
            winner_index = model.winner(weights, sample)
            model.update(weights, sample, winner_index, alpha, Y[j])

    # Test with a new sample
    test = [0, 0, 1, 0]
    result = model.winner(weights, test)
    print("Sample T belongs to class:", result)
    print("Trained weights:", weights)


if __name__ == "__main__":
    main()