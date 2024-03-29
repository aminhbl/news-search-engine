import pandas as pd
import logging
import parsivar
import hazm

DATA_NEWS_FILE = 'data/IR_data_news_12k.json'
PREPROCESSED_FILE_WSR = 'data/preprocessed_WSR.json'
PREPROCESSED_FILE_WOSR = 'data/preprocessed_WOSR.json'
LOGGING_FILE = 'data/preprocess.log'

logging.basicConfig(filename=LOGGING_FILE,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


class Preprocess:
    def __init__(self):
        self.normalizer = parsivar.Normalizer(pinglish_conversion_needed=True)
        self.tokenizer = parsivar.Tokenizer()
        self.stemmer = parsivar.FindStems()
        self.stop_words = hazm.stopwords_list()
        self.to_remove = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹',
                          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                          '(', ')', '[', ']', '«', '»', '<<', '>>', '{', '}',
                          '?', '،', '.', ':', '-', '_', '/', '=', '؛', '&', "%", "#", "*",
                          'https://', 'http://', 'انتهای پیام', '://']

        self.logger = logging.getLogger()

    def normalize(self, sentence):
        return self.normalizer.normalize(sentence)

    def tokenize(self, sentence):
        sentence = sentence.replace("انتهای پیام", "")
        tokens = self.tokenizer.tokenize_words(sentence)

        # tokens_indexed = {}
        # for pos in range(len(tokens)):
        #     try:
        #         tokens_indexed[tokens[pos]].append(pos)
        #     except KeyError:
        #         tokens_indexed[tokens[pos]] = [pos]

        return tokens

    def stem(self, tokens):
        stem_tokens_indexed = []
        for token in tokens:
            stem_tokens = self.stemmer.convert_to_stem(token)

            # self.logger.info('Stemmer: {} -> {}'.format(token, stem_tokens))

            stem_tokens_indexed.append(stem_tokens)

        return stem_tokens_indexed

    def redact_stops(self, tokens):
        temp = set(self.stop_words)
        to_redact1 = [_ for _ in tokens if _ in temp]

        temp2 = set(self.to_remove)
        to_redact2 = [_ for _ in tokens if _ in temp2]

        to_redact = to_redact1 + to_redact2
        # self.logger.info('Stop Tokens: {} '.format(to_redact))

        tokens = list(filter(lambda k: k not in to_redact, tokens))

        tokens_indexed = {}
        for pos in range(len(tokens)):
            try:
                tokens_indexed[tokens[pos]].append(pos)
            except KeyError:
                tokens_indexed[tokens[pos]] = [pos]

        return tokens_indexed

    def query_preprocess(self, query):
        query_normalized = self.normalize(query)
        query_tokenized = self.tokenize(query_normalized)
        query_stemmed = self.stem(query_tokenized)
        query_stops_redacted = self.redact_stops(query_stemmed)

        # query = self.tokenizer.tokenize_words(query_normalized)
        # map(self.stemmer.convert_to_stem, query)
        query = query_stemmed

        temp = set(self.stop_words)
        to_redact1 = [_ for _ in query if _ in temp]

        temp2 = set(self.to_remove)
        to_redact2 = [_ for _ in query if _ in temp2]

        to_redact = to_redact1 + to_redact2
        # self.logger.info('Stop Tokens: {} '.format(to_redact))

        query = list(filter(lambda k: k not in to_redact, query))

        return query_stops_redacted, query


def run_preprocess(stemmer, stops_redactor):
    preprocess = Preprocess()

    df = pd.read_json(DATA_NEWS_FILE, orient='index')

    df_processed = df

    df_processed['content'] = df['content'].apply(preprocess.normalize)
    # print(df_processed["content"][5239])

    df_processed['tokens'] = df_processed['content'].apply(preprocess.tokenize)
    # print(df_processed["tokens"][5239])
    # print(len(df_processed["tokens"][5239]))

    if stemmer:
        df_processed['tokens'] = df_processed['tokens'].apply(preprocess.stem)
        # print(df_processed["tokens"][5239])
        # print(len(df_processed["tokens"][5239]))

    if stops_redactor:
        df_processed['tokens'] = df_processed['tokens'].apply(preprocess.redact_stops)
        # print(df_processed["tokens"][5239])
        # print(len(df_processed["tokens"][5239]))

    return df_processed


def main():
    df_processed = run_preprocess(True, True)
    df_processed.to_json(PREPROCESSED_FILE_WSR)


if __name__ == '__main__':
    main()
    # sentence = "آیا امشب این تیم می تواند به مرحله بعدی جام حذفی فوتبال انگلیس راه پیدا کند"
    # preprocess = Preprocess()
    # query_normalized = preprocess.normalize(sentence)
    # print(query_normalized)
    # query_tokenized = preprocess.tokenize(query_normalized)
    # print(query_tokenized)
    # query_stemmed = preprocess.stem(query_tokenized)
    # print(query_stemmed)
    # query_stops_redacted = preprocess.redact_stops(query_stemmed)
    # print(query_stops_redacted)
