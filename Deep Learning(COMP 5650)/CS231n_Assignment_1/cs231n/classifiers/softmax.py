from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train = X.shape[0]
    num_classes = W.shape[1]

    for i in range(num_train):
        scores_vector = X[i].dot(W)
        scores_vector -= np.max(scores_vector)
        exp_scores_vector = np.exp(scores_vector)
        prob_vector = exp_scores_vector / sum(exp_scores_vector)
        prob_true_label = prob_vector[y[i]]
        loss += (-np.log(prob_true_label))

        for j in range(num_classes):
            if j == y[i]:
                dW[:, j] += ((prob_vector[j] - 1) * X[i])
            else:
                dW[:, j] += (prob_vector[j] * X[i])
      
    loss /= num_train
    loss += (reg * np.sum(W * W))

    dW /= num_train
    dW += (2 * reg * W)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train = X.shape[0]
    num_classes = W.shape[1]

    # Compute Loss
    scores_matrix = X.dot(W)
    scores_matrix -= np.max(scores_matrix)
    exp_scores_matrix = np.exp(scores_matrix)
    sum_exp_scores_vector = np.sum(exp_scores_matrix, axis=1).reshape(-1, 1)
    prob_matrix = exp_scores_matrix / sum_exp_scores_vector
    log_prob_matrix = -np.log(prob_matrix)
    loss = sum(log_prob_matrix[np.arange(num_train), y])
    loss /= num_train
    loss += (reg * np.sum(W * W))

    # Compute dW
    one_hot_matrix = np.zeros((num_train, num_classes))
    one_hot_matrix[np.arange(num_train), y] = 1
    prob_minus_target = prob_matrix - one_hot_matrix
    dW = (prob_minus_target.T.dot(X)).T
    dW /= num_train
    dW += (2 * reg * W)
    
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
