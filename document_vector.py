from positional_index import PositionalIndexing
from preprocess import Preprocess
import pandas as pd
import math
import json


DATA_NEWS_FILE = 'data/IR_data_news_12k.json'
POSITIONAL_INDEXED_FILE_WSR = 'data/positional_indexes_WSR.json'
CHAMPION_LIST_FILE = 'data/chamption_list.json'
DOC2VEC_FILE = 'data/document_vector.json'


class Vector:
    def __init__(self):
        self.document_vectors = {}
        self.query_vector = {}
        self.champion_list = {}

        self.numner_of_documents = None
        self.positional_indexing = None

    def create_doc2vec(self):
        df = pd.read_json(DATA_NEWS_FILE, orient='index')
        self.numner_of_documents = df.shape[0]

        positional_indexing_class = PositionalIndexing()
        self.positional_indexing = positional_indexing_class.load_positional_indexind(WSR=True)

        for docID in range(self.numner_of_documents):
            tf = {}
            length = 0
            for term in self.positional_indexing:
                if str(docID) in self.positional_indexing[term][1]:
                    raw_tf = len(self.positional_indexing[term][1][str(docID)])
                    tf_value = 1 + math.log10(raw_tf)
                    length += tf_value ** 2
                    tf[term] = tf_value
            length = length ** 0.5
            self.document_vectors[docID] = {k: v / length for k, v in tf.items()}

    def store_doc2vec(self):
        with open(DOC2VEC_FILE, 'w', encoding='utf-8') as fp:
            json.dump(self.document_vectors, fp, sort_keys=True, indent=4, ensure_ascii=False)

    def load_doc2vec(self):
        with open(DOC2VEC_FILE, 'r', encoding='utf-8') as fp:
            self.document_vectors = json.load(fp)

    def query2vec(self, query_content):
        if self.numner_of_documents is None:
            df = pd.read_json(DATA_NEWS_FILE, orient='index')
            self.numner_of_documents = df.shape[0]

        if self.positional_indexing is None:
            positional_indexing_class = PositionalIndexing()
            self.positional_indexing = positional_indexing_class.load_positional_indexind(WSR=True)

        preprocessor = Preprocess()
        query_preprocessed, tokens = preprocessor.query_preprocess(query=query_content)

        tf_idf = {}
        length = 0
        for token, positions in query_preprocessed.items():
            raw_tf = len(positions)
            tf = 1 + math.log10(raw_tf)
            df = len(self.positional_indexing[token][1])
            idf = math.log10(self.numner_of_documents / df)
            length += (tf * idf) ** 2
            tf_idf[token] = tf * idf
        length = length ** 0.5

        for token, w in tf_idf.items():
            self.query_vector[token] = w / length

    def create_champion_list(self):
        if self.positional_indexing is None:
            positional_indexing_class = PositionalIndexing()
            self.positional_indexing = positional_indexing_class.load_positional_indexind(WSR=True)

        for term in self.positional_indexing:
            sorted_documents = dict(
                sorted(self.positional_indexing[term][1].items(), key=lambda item: item[1], reverse=True))

            if len(sorted_documents) <= 4:
                self.champion_list[term] = list(sorted_documents.keys())
            else:
                self.champion_list[term] = list(sorted_documents.keys())[0:math.ceil(len(sorted_documents) * 3 / 4)]

    def store_chamption_list(self):
        with open(CHAMPION_LIST_FILE, 'w', encoding='utf-8') as fp:
            json.dump(self.champion_list, fp, sort_keys=True, indent=4, ensure_ascii=False)

    def load_chamption_list(self):
        with open(CHAMPION_LIST_FILE, 'r', encoding='utf-8') as fp:
            self.champion_list = json.load(fp)


if __name__ == '__main__':
    vector = Vector()

    vector.create_doc2vec()
    vector.store_doc2vec()

    vector.create_champion_list()
    vector.store_chamption_list()
