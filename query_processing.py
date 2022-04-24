from positional_index import PositionalIndexing
from preprocess import Preprocess
from preprocess import DATA_NEWS_FILE
import pandas as pd


def query(query_content):
    preprocessor = Preprocess()
    positional_indexing = PositionalIndexing()

    positional_indexing = positional_indexing.load_positional_indexind(WSR=True)
    df = pd.read_json(DATA_NEWS_FILE, orient='index')

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

    # print(query_quoted)
    # print(query_not)
    # print(query_noraml)
    # print(query_quotations)

    answers = {}

    # Words
    for query_token in query_noraml:
        if query_token in positional_indexing:
            freq = positional_indexing[query_token][0]
            doc_n_positions = positional_indexing[query_token][1]

            for doc in doc_n_positions:
                for _ in doc_n_positions[doc]:
                    if doc in answers:
                        if query_token in answers[doc]:
                            answers[doc][query_token] += 1
                        else:
                            answers[doc][query_token] = 1
                    else:
                        answers[doc] = {query_token: 1}

    # Phrase
    for quotation_list in query_quotations:
        query_quote_token = quotation_list[0]
        if query_quote_token in positional_indexing:
            freq_1 = positional_indexing[query_quote_token][0]
            doc_n_positions_1 = positional_indexing[query_quote_token][1]

            if len(quotation_list) == 1:

                if len(answers) > 0:
                    shared_docs = answers.keys() & doc_n_positions_1.keys()
                    answers = {k: answers[k] for k in shared_docs}

                for doc in doc_n_positions_1:
                    if doc in answers:
                        if str(quotation_list) in answers[doc]:
                            answers[doc][str(quotation_list)] += 1
                        else:
                            answers[doc][str(quotation_list)] = 1
                    else:
                        answers[doc] = {str(quotation_list): 1}

            for j in range(1, len(quotation_list)):
                if quotation_list[j] in positional_indexing:
                    freq_2 = positional_indexing[quotation_list[j]][0]
                    doc_n_positions_2 = positional_indexing[quotation_list[j]][1]

                    shared = {}
                    for doc1 in doc_n_positions_1:
                        if doc1 in doc_n_positions_2:
                            positions1 = doc_n_positions_1[doc1]
                            positions2 = doc_n_positions_2[doc1]
                            for p1 in positions1:
                                for p2 in positions2:
                                    if p2 - p1 == j:

                                        shared[doc1] = 1

                                        if j == len(quotation_list) - 1:
                                            if doc1 in answers:
                                                if str(quotation_list) in answers[doc1]:
                                                    answers[doc1][str(quotation_list)] += 1
                                                else:
                                                    answers[doc1][str(quotation_list)] = 1
                                            else:
                                                answers[doc1] = {str(quotation_list): 1}

                    if len(answers) > 0:
                        shared_docs = answers.keys() & shared.keys()
                        answers = {k: answers[k] for k in shared_docs}

                        if len(answers) == 0:
                            break
                else:
                    answers = {}
                    break
        else:
            answers = {}
            break

    # NOT
    for query_token in query_not:
        if query_token in positional_indexing:
            freq = positional_indexing[query_token][0]
            doc_n_positions = positional_indexing[query_token][1]

            for doc in doc_n_positions:
                if doc in answers:
                    del answers[doc]

    answers = dict(sorted(answers.items(), key=lambda item: sum(item[1].values()), reverse=True))
    print('\nTotal Retrieved Documents: {}\n'.format(len(answers)))

    total_retrived_tokens = {}
    for doc, tokens in answers.items():
        for token, score in tokens.items():
            total_retrived_tokens[token] = total_retrived_tokens.get(token, 0) + score

    ranked_docs = {}
    for doc, tokens in answers.items():
        sum_score = sum(total_retrived_tokens.values())
        for token in total_retrived_tokens:
            if token in tokens:
                if doc in ranked_docs:
                    ranked_docs[doc] *= (tokens[token] / total_retrived_tokens[token])
                else:
                    ranked_docs[doc] = (tokens[token] / total_retrived_tokens[token])
            else:
                ranked_docs[doc] = 0

        # if doc in ranked_docs:
        #     ranked_docs[doc] /= sum_score

    ranked_docs = dict(sorted(ranked_docs.items(), key=lambda item: item[1], reverse=True))

    for k, v in ranked_docs.items():
        print('Doc ID: {}'.format(k))
        # print(v)
        # print(answers[k])
        print('Title: {}'.format(df.iloc[int(k)].title))
        print('URL: {}'.format(df.iloc[int(k)].url))
        print()


if __name__ == '__main__':
    q = input()
    query(q)
