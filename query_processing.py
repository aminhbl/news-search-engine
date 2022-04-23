from preprocess import Preprocess
from positional_index import PositionalIndexing


def query(query_content):
    preprocessor = Preprocess()
    positional_indexing = PositionalIndexing()

    positional_indexing = positional_indexing.load_positional_indexind(WSR=True)

    query_preprocessed = preprocessor.query_preprocess(query=query_content)
    query_quoted = {}
    query_not = {}

    quote_positions = []
    not_positions = []
    try:
        quote_positions = query_preprocessed["\""]
        del query_preprocessed["\""]
    except KeyError:
        pass
    try:
        not_positions = query_preprocessed["!"]
        del query_preprocessed["!"]
    except KeyError:
        pass

    for token, positions in query_preprocessed.items():
        for pos in positions:
            for i in range(len(quote_positions)):
                if i % 2 == 0:
                    if quote_positions[i] < pos < quote_positions[i + 1]:
                        query_quoted[token] = query_preprocessed[token]

            for i in range(len(not_positions)):
                if pos == not_positions[i] - 1:
                    query_not[token] = query_preprocessed[token]

    for key in query_quoted:
        del query_preprocessed[key]
    for key in query_not:
        del query_preprocessed[key]
    query_noraml = query_preprocessed

    print(query_quoted)
    print(query_not)
    print(query_noraml)


if __name__ == '__main__':
    q = input()
    query(q)
