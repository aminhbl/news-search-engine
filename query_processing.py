from preprocess import Preprocess
from positional_index import PositionalIndexing


def query(query_content):
    preprocessor = Preprocess()
    positional_indexing = PositionalIndexing()

    positional_indexing = positional_indexing.load_positional_indexind(WSR=True)

    query_preprocessed, query_list = preprocessor.query_preprocess(query=query_content)
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
                if pos == not_positions[i] + 1:
                    query_not[token] = query_preprocessed[token]

    for key in query_quoted:
        del query_preprocessed[key]
    for key in query_not:
        del query_preprocessed[key]
    query_noraml = query_preprocessed

    print(query_quoted)
    print(query_not)
    print(query_noraml)
    print(query_list)

    answers = {}

    for query_token in query_noraml:
        if query_token in positional_indexing:
            freq = positional_indexing[query_token][0]
            doc_n_positions = positional_indexing[query_token][1]

            if len(answers) > 0:
                shared_docs = answers.keys() & doc_n_positions.keys()
                # answers = {k: answers[k] for k in shared_docs}
                for doc in shared_docs:
                    answers[doc] += 1
                # doc_n_positions = {k: doc_n_positions[k] for k in shared_docs}

            else:
                for doc in doc_n_positions:
                    answers[doc] = 1

    for i in range(0, len(query_list)):
        if query_list[i] in query_quoted and query_list[i] in positional_indexing:
            freq_1 = positional_indexing[query_list[i]][0]
            doc_n_positions_1 = positional_indexing[query_list[i]][1]

            for j in range(i + 1, len(query_list)):
                if query_list[j] in query_quoted and query_list[j] in positional_indexing:
                    freq_2 = positional_indexing[query_list[j]][0]
                    doc_n_positions_2 = positional_indexing[query_list[j]][1]

                    if len(answers) > 0:
                        shared_docs = answers.keys() & doc_n_positions_2.keys()
                        answers = {k: answers[k] for k in shared_docs}
                        doc_n_positions_2 = {k: doc_n_positions_2[k] for k in shared_docs}

                    #  possible check for shortest dict
                    for doc1 in doc_n_positions_1:
                        if doc1 in doc_n_positions_2:
                            positions1 = doc_n_positions_1[doc1]
                            positions2 = doc_n_positions_2[doc1]
                            for p1 in positions1:
                                for p2 in positions2:
                                    if p1 > p2:
                                        break
                                    if abs(p1 - p2) == abs(i - j):
                                        if doc1 in answers:
                                            answers[doc1] += 1
                                        else:
                                            answers[doc1] = 1


if __name__ == '__main__':
    q = input()
    query(q)
