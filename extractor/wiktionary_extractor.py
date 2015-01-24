__author__ = 'kartik'
from utils.wikipedia_util import WikipediaConnector
import re

# class to perform extraction operations on wiktionary raw article text
class WiktionaryExtractor:

    def __init__(self):
        self.noun_pattern = "===Noun==="
        self.adjective_pattern = "===Adjective==="
        self.synonym_pattern = "===Synonyms==="
        pass

    # method to extract definitions based on word POS tag
    # params: raw text of wiktionary article
    def get_definitions(self, raw):
        if raw.find(self.noun_pattern, 0, len(raw)) != -1:
            return self.noun_processing(raw)

        if raw.find(self.adjective_pattern, 0, len(raw)) != -1:
            return self.adjective_processing(raw)

    # method to check if its noun and extract definitions
    # params: raw text of wiktionary article
    def noun_processing(self, raw):
        return self.extract_definitions(raw,  self.noun_pattern)

    # method to check if its adjective and extract definitions
    # params: raw text of wiktionary article
    def adjective_processing(self, raw):
        return self.extract_definitions(raw, self.adjective_pattern)

    # generic method to extract definitions for noun, adjective word
    # params: raw text of wiktionary article, word type
    def extract_definitions(self, raw, word_type):
        start_index = raw.find(word_type, 0, len(raw)) + len(word_type)
        end_index = raw.find(self.synonym_pattern, 0, len(raw))

        def_raw = raw[start_index:end_index]

        items_list = def_raw.split("\n")
        result_list = []
        for item in items_list:
            if item[0:2] == "# ":
                clean_def = self.cleanup(item[2:]).strip()
                if clean_def != "":
                    result_list.append(clean_def)
            if item[0:3] == "## ":
                clean_def = self.cleanup(item[3:]).strip()
                if clean_def != "":
                    result_list.append(clean_def)
        return result_list

    # method to extract non definitions for article/word with this title
    # params: article title
    def get_non_definitions(self, title):
        if title.strip() == "":
            return

        # we are using wikipedia article with given title to extract non definitions
        # get instancec of wikipedia connector and get raw article text
        _wiki_connector = WikipediaConnector()
        # delegating to wikipedia connector to fetch non definitions for the articles
        result = _wiki_connector.get_non_definitional_sentences_for_article(title)
        return result

    # method to cleanup the definition
    def cleanup(self, definition):
        result = re.sub('{{.*?}}', '', definition)
        result = re.sub('{{.*?}', '', result)
        result = re.sub("''", '', result)
        result = re.sub('\[\[', '', result)
        result = re.sub(']]', '', result)
        result = re.sub('<ref.*?>', '', result)
        result = re.sub('</ref>', '', result)
        result = re.sub('#.+|', '', result)
        return result