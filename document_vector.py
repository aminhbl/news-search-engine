from positional_index import PositionalIndexing
import pandas as pd
import math

from preprocess import Preprocess

DATA_NEWS_FILE = 'data/IR_data_news_12k.json'
POSITIONAL_INDEXED_FILE_WSR = 'data/positional_indexes_WSR.json'


class Vector:
    def __init__(self):
        self.document_vectors = {}
        self.query_vector = {}
        self.df = pd.read_json(DATA_NEWS_FILE, orient='index')
        self.N = self.df.shape[0]

    def doc2vec(self):
        positional_indexing = PositionalIndexing()
        positional_indexing = positional_indexing.load_positional_indexind(WSR=True)

        for docNum in range(self.N):
            tf = {}
            length = 0
            for term in positional_indexing:
                if docNum in positional_indexing[term][1]:
                    raw_tf = len(positional_indexing[term][1][str(docNum)])
                    tf_value = 1 + math.log10(raw_tf)
                    length += tf_value ** 2
                    tf[term] = tf_value
            length = length ** 0.5
            self.document_vectors[docNum] = {k: v / length for k, v in tf.items()}

    def query2vec(self, query_content):
        positional_indexing = PositionalIndexing()
        positional_indexing = positional_indexing.load_positional_indexind(WSR=True)

        preprocessor = Preprocess()
        query_preprocessed, tokens = preprocessor.query_preprocess(query=query_content)

        tf_idf = {}
        length = 0
        for token, positions in query_preprocessed.items():
            raw_tf = len(positions)
            tf = 1 + math.log10(raw_tf)
            df = len(positional_indexing[token][1])
            idf = math.log10(self.N / df)
            length += (tf * idf) ** 2
            tf_idf[token] = tf * idf
        length = length ** 0.5

        for token, w in tf_idf.items():
            self.query_vector[token] = w / length


if __name__ == '__main__':
    vector = Vector()
    vector.doc2vec()