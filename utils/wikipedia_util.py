__author__ = 'kartik'

import wikipedia

# class to call wikipedia API
class WikipediaConnector():
    # method to search for articles with article_name
    # params:
    # article_name: name of the article
    def search(self, article_name):
        lst = None
        while (lst == None):
            try:
                lst = wikipedia.search(article_name)
                return lst
            except:
                pass

    # method to get suggestion for articles with article_name
    # params:
    # article_name: name of the article
    def suggest(self, article_name):
        lst = None
        while (lst == None):
            try:
                lst = wikipedia.suggest(article_name)
                return lst
            except:
                pass

    # method to get article for given article_name(using heuristics of search and suggest)
    # params:
    # article_name: name of the article
    def get_article(self, article_name):
        if article_name.strip() == "":
            return None
        obj = None
        try:
            # find page for this article
            obj = wikipedia.page(article_name)
        except:
            # if no page found, search for related articles
            lst = self.search(article_name)
            new_article_name = ""

            # iterate over related articles
            for name in lst:
                # if target article found in related articles
                if article_name.lower() in name.lower():
                    new_article_name = name

                    try:
                        # find page with this new title
                        obj = wikipedia.page(new_article_name)
                        break
                    except:
                        # if not found, get suggestions for this article title
                        lst = self.suggest(new_article_name)

                        # if no suggestions found, pick up next related title from search result
                        if lst == None:
                            continue

                        if type(lst) == type([]):
                            new_article_name = lst[0]  # list of suggested articles
                        else:
                            new_article_name = lst  # single suggestion

                        try:
                            obj = wikipedia.page(new_article_name)
                            break
                        except:
                            continue  # pick up next related title from search result
        if obj is None:
            return None

        response = None
        while (response == None):
            try:
                response = obj.content.encode('utf-8')
                return response
            except:
                print "\nsocket_error:trying again..."

    # method to extract non definitional sentences from wikipedia article raw text
    # params:
    # raw: article raw text
    # article_name: name of the article
    def extract_non_definitional_sentences_from_article(self, raw, article_name):
        lines = raw.split("\n")
        result = []

        # taking all lines except the first line as first line is definitional
        for line in lines[1:]:
            if not "=" in line:
                sentence_collection = line.split(". ")
                for sentence in sentence_collection:
                    art_name = article_name  #.decode('utf-8')
                    sent = sentence.decode('utf-8')
                    if art_name.lower() in sent.lower():
                        result.append(sentence)
        return result

    # proxy method for extracting non definitional sentences from wikipedia article raw text
    # params:
    # article_name: name of the article
    def get_non_definitional_sentences_for_article(self, article_name):
        raw = self.get_article(article_name)
        if raw is None:
            return None
        return self.extract_non_definitional_sentences_from_article(raw, article_name)

