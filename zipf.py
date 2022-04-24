from positional_index import PositionalIndexing
from preprocess import run_preprocess
import matplotlib.pyplot as plt
import math


def indexing(tokens):
    tokens_indexed = {}
    for pos in range(len(tokens)):
        try:
            tokens_indexed[tokens[pos]].append(pos)
        except KeyError:
            tokens_indexed[tokens[pos]] = [pos]

    return tokens_indexed


def create_positional_indexing(preprocessed_data):
    positional_indexing = PositionalIndexing()
    positional_indexing.preprocessed_data = preprocessed_data
    positional_indexing.create()
    return positional_indexing.positional_index


def zipf():
    preprocess_wo_stops = run_preprocess(True, False)
    preprocess_wo_stops['tokens'] = preprocess_wo_stops['tokens'].apply(indexing)
    positional_indexing_wos = create_positional_indexing(preprocess_wo_stops)
    word_frequency_wos = {}
    for token, posting in positional_indexing_wos.items():
        word_frequency_wos[token] = posting[0]
    word_frequency_wos = dict(sorted(word_frequency_wos.items(), key=lambda item: item[1], reverse=True))
    max_word_wos = list(word_frequency_wos.values())[0]

    preprocess_w_stops = run_preprocess(True, True)
    positional_indexing_ws = create_positional_indexing(preprocess_w_stops)
    word_frequency_ws = {}
    for token, posting in positional_indexing_ws.items():
        word_frequency_ws[token] = posting[0]
    word_frequency_ws = dict(sorted(word_frequency_ws.items(), key=lambda item: item[1], reverse=True))
    max_word_ws = list(word_frequency_ws.values())[0]

    ith_frequent = []
    most_requency = []
    frequency = []

    for token in word_frequency_wos:
        token_ith = list(word_frequency_wos.keys()).index(token)
        ith_frequent.append(math.log(token_ith + 1, 10))
        most_requency.append(math.log(max_word_wos / (token_ith + 1), 10))
        frequency.append(math.log(word_frequency_wos[token], 10))

    plt.plot(ith_frequent, most_requency)
    plt.plot(ith_frequent, frequency)
    plt.legend(['Real', 'Prediction'])
    plt.xlabel("log10 rank")
    plt.ylabel("log10 cf")
    plt.title("With StopWords")
    plt.show()

    ith_frequent_ws = []
    most_requency_ws = []
    frequency_ws = []

    for token in word_frequency_ws:
        token_ith = list(word_frequency_ws.keys()).index(token)
        ith_frequent_ws.append(math.log(token_ith + 1, 10))
        most_requency_ws.append(math.log(max_word_ws / (token_ith + 1), 10))
        frequency_ws.append(math.log(word_frequency_ws[token], 10))

    plt.plot(ith_frequent_ws, most_requency_ws)
    plt.plot(ith_frequent_ws, frequency_ws)
    plt.legend(['Real', 'Prediction'])
    plt.xlabel("log10 rank")
    plt.ylabel("log10 cf")
    plt.title("Without StopWords")
    plt.show()


if __name__ == '__main__':
    zipf()
