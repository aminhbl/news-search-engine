from positional_index import PositionalIndexing
from preprocess import run_preprocess
import matplotlib.pyplot as plt
import numpy as np
import math


def count_token_n_vocab(preprocessed_data):
    positional_indexing = PositionalIndexing()
    positional_indexing.preprocessed_data = preprocessed_data
    positional_indexing.create()

    vocab_size = len(positional_indexing.positional_index)
    token_size = 0
    for token, posting in positional_indexing.positional_index.items():
        token_size += posting[0]

    return token_size, vocab_size


def heaps():
    preprocess_w_stem = run_preprocess(True, True)
    preprocess_wo_stem = run_preprocess(False, True)

    w_stem_tokens = []
    w_stem_vocab = []
    wo_stem_tokens = []
    wo_stem_vocab = []

    for index in [500, 1000, 1500, 2000]:
        tokens_ws, vocab_ws = count_token_n_vocab(preprocess_w_stem.head(index))
        w_stem_tokens.append(tokens_ws)
        w_stem_vocab.append(vocab_ws)

        tokens_wos, vocab_wos = count_token_n_vocab(preprocess_wo_stem.head(index))
        wo_stem_tokens.append(tokens_wos)
        wo_stem_vocab.append(vocab_wos)

    all_tokens_ws, all_vocab_ws = count_token_n_vocab(preprocess_w_stem)

    all_tokens_wos, all_vocab_wos = count_token_n_vocab(preprocess_wo_stem)

    x = np.array(w_stem_tokens)
    y = np.array(w_stem_vocab)
    tokens_log = np.log10(x)
    vocab_log = np.log10(y)
    coefficients = np.polyfit(tokens_log, vocab_log, 1)
    b = coefficients[0]
    logk = coefficients[1]
    k = math.pow(10, logk)
    dic_predict = math.pow(10, logk) * math.pow(all_tokens_ws, b)

    plt.plot(tokens_log, vocab_log)
    plt.plot(tokens_log, b * tokens_log + logk)
    plt.title("With Stemming\n b={:.3f}  k={:.3f}".format(b, k))
    plt.xlabel("log10 T")
    plt.ylabel("log10 M")
    plt.legend(['Real', 'Prediction'])
    plt.show()

    print("With Stemming\n b={:.3f}   k={:.3f}".format(b, k))
    print("Real = {}".format(all_vocab_ws))
    print("Prediction = {}".format(dic_predict))

    x = np.array(wo_stem_tokens)
    y = np.array(wo_stem_vocab)
    log_token = np.log10(x)
    log_term = np.log10(y)
    coefficients = np.polyfit(log_token, log_term, 1)
    b = coefficients[0]
    logk = coefficients[1]
    k = math.pow(10, logk)
    dic_predict = math.pow(10, logk) * math.pow(all_tokens_wos, b)

    plt.plot(log_token, log_term)
    plt.plot(log_token, b * log_token + logk)
    plt.title("Without Stemming\n b={:.3f}  k={:.3f}".format(b, k))
    plt.xlabel("log10 T")
    plt.ylabel("log10 M")
    plt.legend(['Real', 'Prediction'])
    plt.show()

    print("Without Stemming\n b={:.3f}   k={:.3f}".format(b, k))
    print("Real = {}".format(all_vocab_wos))
    print("Prediction = {}".format(dic_predict))


if __name__ == '__main__':
    heaps()
