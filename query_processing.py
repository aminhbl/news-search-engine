from preprocess import Preprocess
from positional_index import PositionalIndexing


def query(query_content):
    preprocessor = Preprocess()
    positional_indexing = PositionalIndexing()

    positional_indexing = positional_indexing.load_positional_indexind(WSR=True)

    query_preprocessed, tokens = preprocessor.query_preprocess(query=query_content)
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

    query_quotations = [[] for _ in range((query_content.count('\"') // 2))]
    quotations_seen = False
    quote_number = 0
    for t in tokens:
        if t == "\"":
            quotations_seen = not quotations_seen
            if not quotations_seen:
                quote_number += 1
            continue
        if quotations_seen:
            query_quotations[quote_number].append(t)

    print(query_quoted)
    print(query_not)
    print(query_noraml)
    print(query_quotations)

    answers = {}

    for query_token in query_noraml:
        if query_token in positional_indexing:
            freq = positional_indexing[query_token][0]
            doc_n_positions = positional_indexing[query_token][1]

            for doc in doc_n_positions:
                if doc in answers:
                    answers[doc] += 1
                else:
                    answers[doc] = 1

    for quotation_list in query_quotations:
        query_quote_token = quotation_list[0]
        if query_quote_token in positional_indexing:
            freq_1 = positional_indexing[query_quote_token][0]
            doc_n_positions_1 = positional_indexing[query_quote_token][1]

            if len(answers) > 0:
                shared_docs = answers.keys() & doc_n_positions_1.keys()
                answers = {k: answers[k] for k in shared_docs}

                if len(answers) == 0:
                    break

            for doc in doc_n_positions_1:
                if doc in answers:
                    answers[doc] += 1
                else:
                    answers[doc] = 1

            print(len(answers))
            print(answers)

            for j in range(1, len(quotation_list)):
                if quotation_list[j] in positional_indexing:
                    freq_2 = positional_indexing[quotation_list[j]][0]
                    doc_n_positions_2 = positional_indexing[quotation_list[j]][1]

                    #  possible check for shortest dict
                    shared = {}
                    for doc1 in doc_n_positions_1:
                        if doc1 in doc_n_positions_2:
                            positions1 = doc_n_positions_1[doc1]
                            positions2 = doc_n_positions_2[doc1]
                            for p1 in positions1:
                                for p2 in positions2:
                                    if p2 - p1 == j:

                                        shared[doc1] = 1

                                        if doc1 in answers:
                                            answers[doc1] += 1
                                        # else:
                                        #     answers[doc1] = 1

                    if len(answers) > 0:
                        shared_docs = answers.keys() & shared.keys()
                        answers = {k: answers[k] for k in shared_docs}

                        print(len(answers))
                        print(answers)
                        if len(answers) == 0:
                            # todo:break
                            break

    answers = dict(sorted(answers.items(), key=lambda item: item[1], reverse=True))
    print(len(answers))
    print(answers)


if __name__ == '__main__':
    q = input()
    query(q)