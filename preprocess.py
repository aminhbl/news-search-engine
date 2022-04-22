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
        self.normalizer = parsivar.Normalizer(statistical_space_correction=True,
                                              pinglish_conversion_needed=True)
        self.tokenizer = parsivar.Tokenizer()
        self.stemmer = parsivar.FindStems()
        self.stop_words = hazm.stopwords_list()
        self.to_remove = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹',
                          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                          '(', ')', '[', ']', '«', '»', '<<', '>>', '{', '}',
                          "!", '?', '،', '.', ':', '-', '_', '/', '=', '؛', '&', "%", "#", "*",
                          'https://', 'http://', 'انتهای پیام', '://']

        self.logger = logging.getLogger()

    def normalize(self, sentence):
        return self.normalizer.normalize(sentence)

    def tokenize(self, sentence):
        sentence = sentence.replace("انتهای پیام", "")
        tokens = self.tokenizer.tokenize_words(sentence)

        tokens_indexed = {}
        for pos in range(len(tokens)):
            try:
                tokens_indexed[tokens[pos]].append(pos)
            except KeyError:
                tokens_indexed[tokens[pos]] = [pos]

        return tokens_indexed

    def stem(self, tokens):
        stem_tokens_indexed = {}
        for token, positions in tokens.items():
            stem_tokens = self.stemmer.convert_to_stem(token)

            if "&" in stem_tokens:
                past_form, present_form = stem_tokens.split("&")
                # self.logger.info('Stemmer: {} -> {}, {}'.format(token, past_form, present_form))

                for i in range(len(positions)):
                    try:
                        stem_tokens_indexed[past_form].append(positions[i])
                    except KeyError:
                        stem_tokens_indexed[past_form] = [positions[i]]

                    try:
                        stem_tokens_indexed[present_form].append(positions[i])
                    except KeyError:
                        stem_tokens_indexed[present_form] = [positions[i]]

            else:
                self.logger.info('Stemmer: {} -> {}'.format(token, stem_tokens))

                for i in range(len(positions)):
                    try:
                        stem_tokens_indexed[stem_tokens].append(positions[i])
                    except KeyError:
                        stem_tokens_indexed[stem_tokens] = [positions[i]]

        return stem_tokens_indexed

    def redact_stops(self, tokens):
        temp = set(self.stop_words)
        to_redact1 = [_ for _ in list(tokens) if _ in temp]

        temp2 = set(self.to_remove)
        to_redact2 = [_ for _ in list(tokens) if _ in temp2]

        to_redact = to_redact1 + to_redact2
        self.logger.info('Stop Tokens: {} '.format(to_redact))

        for word in to_redact:
            del tokens[word]

        return tokens


def run_preprocess(stemmer, stops_redactor):
    preprocess = Preprocess()

    df = pd.read_json(DATA_NEWS_FILE, orient='index')

    df_processed = df

    df_processed['content'] = df['content'].apply(preprocess.normalize)
    print(df_processed["content"][214])

    df_processed['tokens'] = df_processed['content'].apply(preprocess.tokenize)
    print(df_processed["tokens"][214])

    if stemmer:
        df_processed['tokens'] = df_processed['tokens'].apply(preprocess.stem)
        print(df_processed["tokens"][214])
        print(len(df_processed["tokens"][214]))

    if stops_redactor:
        df_processed['tokens'] = df_processed['tokens'].apply(preprocess.redact_stops)
        print(df_processed["tokens"][214])
        print(len(df_processed["tokens"][214]))

    df_processed.to_json(PREPROCESSED_FILE_WSR)


def main():
    run_preprocess(True, True)


main()
