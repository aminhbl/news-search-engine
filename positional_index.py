import pandas as pd
import json


class PositionalIndexing:
    def __init__(self):
        # WSR: With Stops Redacted
        # WOSR: Without Stops Redacted
        self.PREPROCESSED_FILE_WSR = 'data/preprocessed_WSR.json'
        self.PREPROCESSED_FILE_WOSR = 'data/preprocessed_WSOR.json'
        self.preprocessed_data = None
        self.POSITIONAL_INDEXED_FILE_WSR = 'data/positional_indexes_WSR.json'
        self.POSITIONAL_INDEXED_FILE_WOSR = 'data/positional_indexes_WOSR.json'
        self.positional_index = dict()

    def create(self):

        for docID, row in self.preprocessed_data.iterrows():
            tokens = row['tokens']
            for token, positions in tokens.items():
                try:
                    self.positional_index[token][0] += len(positions)
                    self.positional_index[token][1][docID] = positions
                except KeyError:
                    self.positional_index[token] = [
                        len(positions),
                        {docID: positions}
                    ]

    def store_positional_indexind(self):

        with open(self.POSITIONAL_INDEXED_FILE_WSR, 'w') as fp:
            json.dump(self.positional_index, fp, sort_keys=True, indent=4)

    def fit_preprocessed_data(self, WSR):

        if WSR:
            self.preprocessed_data = pd.read_json(self.PREPROCESSED_FILE_WSR)
        else:
            self.preprocessed_data = pd.read_json(self.PREPROCESSED_FILE_WOSR)


def main():
    positional_indexing = PositionalIndexing()
    positional_indexing.fit_preprocessed_data(True)
    positional_indexing.create()
    positional_indexing.store_positional_indexind()


main()
