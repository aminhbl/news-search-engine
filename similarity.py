from document_vector import Vector
import pandas as pd
import itertools
from preprocess import DATA_NEWS_FILE

K = 10


def query_processing(query_content):
    vector = Vector()
    vector.load_doc2vec()
    vector.load_chamption_list()
    vector.query2vec(query_content)

    # Index Elimination
    documents = []
    for term in vector.query_vector:
        documents = list(set(documents + list(vector.positional_indexing[term][1].keys())))

    # Chmapion List
    for term in vector.query_vector:
        documents = list(set(documents + list(vector.champion_list[term])))

    docID_score = {}
    for docID in documents:
        a = vector.document_vectors[docID]
        b = vector.query_vector
        common_terms = a.keys() & b.keys()
        cosine_similarity = 0
        for term in common_terms:
            cosine_similarity += a[term] * b[term]

        docID_score[docID] = cosine_similarity

    docID_score = dict(sorted(docID_score.items(), key=lambda item: item[1], reverse=True))
    # print(docID_score)
    top_docs = dict(itertools.islice(docID_score.items(), K))

    print('\nTop 10 documents:')
    df = pd.read_json(DATA_NEWS_FILE, orient='index')
    for doc in top_docs:
        print('Doc ID: {}'.format(doc))
        print('Title: {}'.format(df.iloc[int(doc)].title))
        print('URL: {}'.format(df.iloc[int(doc)].url))
        print()


if __name__ == '__main__':
    q = input()
    query_processing(q)
