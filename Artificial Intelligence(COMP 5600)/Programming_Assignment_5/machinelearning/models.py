from torch import no_grad, stack
from torch.utils.data import DataLoader
from torch.nn import Module


"""
Functions you should use.
Please avoid importing any other functions or modules.
Your code will not pass if the gradescope autograder detects any changed imports
"""
import torch
from torch.nn import Parameter, Linear
from torch import optim, tensor, tensordot, ones, matmul
from torch.nn.functional import cross_entropy, relu, mse_loss, softmax
from torch import movedim
import math


class PerceptronModel(Module):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.

        In order for our autograder to detect your weight, initialize it as a 
        pytorch Parameter object as follows:

        Parameter(weight_vector)

        where weight_vector is a pytorch Tensor of dimension 'dimensions'

        
        Hint: You can use ones(dim) to create a tensor of dimension dim.
        """
        super(PerceptronModel, self).__init__()
        
        "*** YOUR CODE HERE ***"
        # Create a parameter 2D tensor of dimensions (1, dimensions)
        self.w = Parameter(ones(1, dimensions))
        

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)

        The pytorch function `tensordot` may be helpful here.
        """
        "*** YOUR CODE HERE ***"

        # Return the dot product of the input and weights
        return tensordot(x, self.get_weights())
        

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"

        # If the dot product is non-negative return 1 else return -1
        if self.run(x) >= 0:
            return 1
        else:
            return -1


    def train(self, dataset):
        """
        Train the perceptron until convergence.
        You can iterate through DataLoader in order to 
        retrieve all the batches you need to train on.

        Each sample in the dataloader is in the form {'x': features, 'label': label} where label
        is the item we need to predict based off of its features.
        """
        with no_grad():
            dataloader = DataLoader(dataset, batch_size=1, shuffle=True)
            "*** YOUR CODE HERE ***"

            # Loop until there are no mistakes
            while True:

                made_mistake = False

                for sample in dataloader:

                    label = sample["label"]

                    # For each sample in the dataset find the perceptron's prediction
                    prediction = self.get_prediction(sample["x"])

                    # If the prediction is different from the sample's label update the perceptron's weights
                    if prediction != label:
                        made_mistake = True
                        self.w += (label * sample["x"])

                # Stop training if the perceptron has made an entire pass through the training data without making any mistakes
                if not made_mistake:
                    break



class RegressionModel(Module):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        super().__init__()

        # Initialize hidden layers and output layer
        self.hidden_layer_one = Linear(1, 128)
        self.hidden_layer_two = Linear(128, 128)
        self.hidden_layer_three = Linear(128, 128)
        self.output_layer = Linear(128, 1)
        # Initialize Adam optimizer with a learning rate of 0.01
        self.optimizer = optim.Adam(self.parameters(), lr=0.01)


    def forward(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"

        # Pass our input through all 4 layers to get our predictions
        output_1 = relu(self.hidden_layer_one(x))
        output_2 = relu(self.hidden_layer_two(output_1))
        output_3 = relu(self.hidden_layer_two(output_2))
        output_4 = self.output_layer(output_3)
        return output_4

    
    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a tensor of size 1 containing the loss
        """
        "*** YOUR CODE HERE ***"
        predictions = self.forward(x)
        # Return our loss from our predictions
        return mse_loss(predictions, y)
        

    def train(self, dataset):
        """
        Trains the model.

        In order to create batches, create a DataLoader object and pass in `dataset` as well as your required 
        batch size. You can look at PerceptronModel as a guideline for how you should implement the DataLoader

        Each sample in the dataloader object will be in the form {'x': features, 'label': label} where label
        is the item we need to predict based off of its features.

        Inputs:
            dataset: a PyTorch dataset object containing data to be trained on
            
        """
        "*** YOUR CODE HERE ***"

        # Set a batch size of 64
        dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

        # Train for 300 epochs
        for i in range(300):
            # For each iteration we reset the gradient calculated by the last batch
            for batch in dataloader:
                self.optimizer.zero_grad()
                x = batch["x"]
                y = batch["label"]
                # We calculate the loss from our input and labels
                loss = self.get_loss(x, y)
                # We find the gradients of our weight matrices
                loss.backward()
                # Update the weights using the optimizer
                self.optimizer.step()


class DigitClassificationModel(Module):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        super().__init__()
        input_size = 28 * 28
        output_size = 10
        "*** YOUR CODE HERE ***"

        # Initialize hidden layers and output layer
        self.hidden_layer_one = Linear(input_size, 256)
        self.hidden_layer_two = Linear(256, 256)
        self.hidden_layer_three = Linear(256, 128)
        self.output_layer = Linear(128, output_size)
        # Initialize Adam optimizer with a learning rate of 0.001
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a tensor with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        """ YOUR CODE HERE """
        # Pass our input through all 3 hidden layers and the output layer to get a vector of size 10 for each example
        output_1 = relu(self.hidden_layer_one(x))
        output_2 = relu(self.hidden_layer_two(output_1))
        output_3 = self.hidden_layer_three(output_2)
        result = self.output_layer(output_3)
        return result
 

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a tensor with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss tensor
        """
        """ YOUR CODE HERE """
        predictions = self.run(x)
        # Return our loss from our predictions
        return cross_entropy(predictions, y)


    def train(self, dataset):
        """
        Trains the model.
        """
        """ YOUR CODE HERE """

        # Set a batch size of 128
        dataloader = DataLoader(dataset, batch_size=128, shuffle=True)

        # Train for 5 epochs
        for i in range(5):
            # For each iteration we reset the gradient calculated by the last batch
            for batch in dataloader:
                self.optimizer.zero_grad()
                x = batch["x"]
                y = batch["label"]
                # We calculate the loss from our input and labels
                loss = self.get_loss(x, y)
                # We find the gradients of our weight matrices
                loss.backward()
                # Update the weights using the optimizer
                self.optimizer.step()

            # Stop training if the validation accuracy is 98% or above
            if dataset.get_validation_accuracy() >= .98:
                break


class LanguageIDModel(Module):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]
        super(LanguageIDModel, self).__init__()
        "*** YOUR CODE HERE ***"
        # Initialize the hidden size to 256
        self.hidden_size = 256
        # Initialize your two linear layers, one that transform the input character and one that transforms the hidden state
        self.W_x = Linear(self.num_chars, self.hidden_size)
        self.W_h = Linear(self.hidden_size, self.hidden_size)
        # Initialize your output layer
        self.output_layer = Linear(self.hidden_size, len(self.languages))
        # Initialize Adam optimizer with a learning rate of 0.005
        self.optimizer = optim.Adam(self.parameters(), lr=0.005)


    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        tensor with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a tensor that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single tensor of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a tensor of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"

        # Find the batch size from the input
        batch_size = xs[0].shape[0]

        # Set the initial hidden state to a tensor of 0s with dimensions batch_size, self.hidden_size
        hidden_state = torch.zeros(batch_size, self.hidden_size)

        # Update the hidden state after each input character across the whole batch
        for i in range(len(xs)):
            hidden_state = relu(self.W_x(xs[i]) + self.W_h(hidden_state))

        # Return the result from passing the final hidden state through the output layer which return a tensor of batch_size, number of languages
        return self.output_layer(hidden_state)

    
    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"

        predictions = self.run(xs)
        # Return our loss from our predictions
        return cross_entropy(predictions, y)
        

    def train(self, dataset):
        """
        Trains the model.

        Note that when you iterate through dataloader, each batch will returned as its own vector in the form
        (batch_size x length of word x self.num_chars). However, in order to run multiple samples at the same time,
        get_loss() and run() expect each batch to be in the form (length of word x batch_size x self.num_chars), meaning
        that you need to switch the first two dimensions of every batch. This can be done with the movedim() function 
        as follows:

        movedim(input_vector, initial_dimension_position, final_dimension_position)

        For more information, look at the pytorch documentation of torch.movedim()
        """
        "*** YOUR CODE HERE ***"

        # Set a batch size of 64
        dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

        # Train for 20 epochs
        for i in range(20):
            # For each iteration we reset the gradient calculated by the last batch
            for batch in dataloader:
                self.optimizer.zero_grad()
                x = batch["x"]
                xs = movedim(x, 0, 1)
                y = batch["label"]
                # We calculate the loss from our input and labels
                loss = self.get_loss(xs, y)
                # We find the gradients of our weight matrices
                loss.backward()
                # Update the weights using the optimizer
                self.optimizer.step()

            # Stop training if the validation accuracy is 84% or above
            if dataset.get_validation_accuracy() >= .84:
                break
        

def Convolve(input: tensor, weight: tensor):
    """
    Acts as a convolution layer by applying a 2d convolution with the given inputs and weights.
    DO NOT import any pytorch methods to directly do this, the convolution must be done with only the functions
    already imported.

    There are multiple ways to complete this function. One possible solution would be to use 'tensordot'.
    If you would like to index a tensor, you can do it as such:

    tensor[y:y+height, x:x+width]

    This returns a subtensor who's first element is tensor[y,x] and has height 'height, and width 'width'
    """
    input_tensor_dimensions = input.shape
    weight_dimensions = weight.shape
    Output_Tensor = tensor(())
    "*** YOUR CODE HERE ***"

    # Find the input height and input width
    input_height, input_width = input_tensor_dimensions[0], input_tensor_dimensions[1]
    # Find the weight height and weight width
    weight_height, weight_width = weight_dimensions[0], weight_dimensions[1]
    # Initialize Output Tensor with all zeros
    Output_Tensor = torch.zeros(input_height - weight_height + 1, input_width - weight_width + 1)

    # Iterate through all possible patches in the input that have the dimensions of the weight tensor
    # Assume a stride of 1 and padding of 0
    for y in range(input_height - weight_height + 1):
        for x in range(input_width - weight_width + 1):
            # Create patch from input
            input_patch = input[y:y+weight_height, x:x+weight_width]
            # Find the dot product of the input patch and weight tensor
            # Update the corresponding position in the Output Tensor
            Output_Tensor[y, x] = tensordot(input_patch, weight, dims=2)

    "*** End Code ***"
    return Output_Tensor



class DigitConvolutionalModel(Module):
    """
    A model for handwritten digit classification using the MNIST dataset.

    This class is a convolutational model which has already been trained on MNIST.
    if Convolve() has been correctly implemented, this model should be able to achieve a high accuracy
    on the mnist dataset given the pretrained weights.

    Note that this class looks different from a standard pytorch model since we don't need to train it
    as it will be run on preset weights.
    """
    

    def __init__(self):
        # Initialize your model parameters here
        super().__init__()
        output_size = 10

        self.convolution_weights = Parameter(ones((3, 3)))
        """ YOUR CODE HERE """

        input_size = (28 - 3 + 1) * (28 - 3 + 1)

        # Initialize 2 hidden layers and output layer
        self.hidden_layer_one = Linear(input_size, 256)
        self.hidden_layer_two = Linear(256, 256)
        self.output_layer = Linear(256, output_size)
        # Initialize Adam optimizer with a learning rate of 0.005
        self.optimizer = optim.Adam(self.parameters(), lr=0.005)


    def run(self, x):
        return self(x)
 
    def forward(self, x):
        """
        The convolutional layer is already applied, and the output is flattened for you. You should treat x as
        a regular 1-dimentional datapoint now, similar to the previous questions.
        """
        x = x.reshape(len(x), 28, 28)
        x = stack(list(map(lambda sample: Convolve(sample, self.convolution_weights), x)))
        x = x.flatten(start_dim=1)
        """ YOUR CODE HERE """

        # Pass our input through all 2 hidden layers and the output layer to get a vector of size 10 for each example
        output_1 = relu(self.hidden_layer_one(x))
        output_2 = relu(self.hidden_layer_two(output_1))
        output_3 = self.output_layer(output_2)
        return output_3


    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a tensor with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss tensor
        """
        """ YOUR CODE HERE """

        predictions = self.run(x)
        # Return our loss from our predictions
        return cross_entropy(predictions, y)
        

    def train(self, dataset):
        """
        Trains the model.
        """
        """ YOUR CODE HERE """

        # Set a batch size of 128
        dataloader = DataLoader(dataset, batch_size=128, shuffle=True)

        # Train for 5 epochs
        for i in range(5):
            # For each iteration we reset the gradient calculated by the last batch
            for batch in dataloader:
                self.optimizer.zero_grad()
                x = batch["x"]
                y = batch["label"]
                # We calculate the loss from our input and labels
                loss = self.get_loss(x, y)
                # We find the gradients of our weight matrices
                loss.backward()
                # Update the weights using the optimizer
                self.optimizer.step()

            # Stop training if the validation accuracy is 82% or above
            if dataset.get_validation_accuracy() >= .82:
                break


class Attention(Module):
    def __init__(self, layer_size, block_size):
        super().__init__()
        """
        All the layers you should use are defined here.

        In order to pass the autograder, make sure each linear layer matches up with their corresponding matrix,
        ie: use self.k_layer to generate the K matrix.
        """
        self.k_layer = Linear(layer_size, layer_size)
        self.q_layer = Linear(layer_size, layer_size)
        self.v_layer = Linear(layer_size,layer_size)

        #Masking part of attention layer
        self.register_buffer("mask", torch.tril(torch.ones(block_size, block_size))
                                     .view(1, 1, block_size, block_size))

        self.layer_size = layer_size


    def forward(self, input):
        """
        Applies the attention mechanism to input. All necessary layers have
        been defined in __init__()

        In order to apply the causal mask to a given matrix M, you should update
        it as such:

        M = M.masked_fill(self.mask[:,:,:T,:T] == 0, float('-inf'))[0]

        For the softmax activation, it should be applied to the last dimension of the input,
        Take a look at the "dim" argument of torch.nn.functional.softmax to figure out how to do this.
        """
        B, T, C = input.size()

        """YOUR CODE HERE"""

        # Find the K, Q, and V matrices by using their corresponding linear layers with the input
        K = self.k_layer(input)
        Q = self.q_layer(input)
        V = self.v_layer(input)

        # Switch dimensions for Q matrix from B x T x C to B x C x T
        Q = movedim(Q, 1, 2)

        # Find scaled attention scores, has dimensions B x T x T
        attention_scores = matmul(K, Q) / math.sqrt(self.layer_size)

        # Apply a mask to mask out all the timesteps ahead of Ti
        attention_scores = attention_scores.masked_fill(self.mask[:, :, :T, :T] == 0, float('-inf'))[0]

        # Now apply softmax to the attention scores
        softmax_attention_scores = softmax(attention_scores, dim=2)

        # Return the matrix multiplication of the softmax attention scores and the value matrix
        return matmul(softmax_attention_scores, V)

     