__author__ = 'luoshalin'

from corpus_generator import generate_dataset
from vocab_transformer import Vocab
from vocab_transformer import pad_into_matrix
from lstm_model import Model
from theano_lstm import RNN


def main():
    # generate dataset
    lines = generate_dataset(100)

    # create vocab
    vocab = Vocab()
    for line in lines:
        vocab.add_words(line.split(" "))

    # transform into big numerical matrix of sentences:
    numerical_lines = []
    for line in lines:
        numerical_lines.append(vocab(line))
    numerical_lines, numerical_lengths = pad_into_matrix(numerical_lines)

    # construct model & theano functions:
    model = Model(
        input_size=10,
        hidden_size=10,
        vocab_size=len(vocab),
        stack_size=1,  # make this bigger, but makes compilation slow
        celltype=RNN   # use RNN or LSTM
    )
    model.stop_on(vocab.word2index["."])

    # train:
    for i in range(10000):
        error = model.update_fun(numerical_lines, numerical_lengths)
        if i % 100 == 0:
            print("epoch %(epoch)d, error=%(error).2f" % ({"epoch": i, "error": error}))
        if i % 500 == 0:
            print(vocab(model.greedy_fun(vocab.word2index["the"])))


if __name__ == '__main__':
    main()
