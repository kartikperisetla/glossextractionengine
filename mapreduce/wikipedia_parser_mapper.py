__author__ = 'kartik'

#!/usr/bin/env python
import sys,re
import cStringIO
import xml.etree.ElementTree as xml

class WikipediaParserMapper:
    def __init__(self):
        self.buff = cStringIO.StringIO()
        self.intext = False
        self.intitle = False

    # method to remove tags and replace newlines with spaces
    def normalize(self, raw):
        result = re.sub(r'<.*>',' ',raw)
        result = re.sub(r'\n',' ',result)
        result = re.sub(r'\t',' ',result)
        return result

    def process(self):
        self.current_article_title = self.normalize(self.current_article_title)
        self.current_article_text = self.normalize(self.current_article_text)
        returnval = self.current_article_title + "\t" + self.current_article_text
        return returnval.strip()


if __name__ == '__main__':
    _instance = WikipediaParserMapper()

    for line in sys.stdin:
        line = line.strip()

        if line.find("<title>") !=-1:
            _instance.intitle = True
            _instance.buff = cStringIO.StringIO()
            _instance.buff.write(line)
            _instance.current_article_title = None
        elif line.find("</title>") != -1:
            _instance.intitle = False
            _instance.buff.write(line)
            val = _instance.buff.getvalue()
            _instance.buff.close()
            _instance.buff = None

            # capturing the currently processed article title
            _instance.current_article_title = val
        elif _instance.intitle:
                _instance.buff.write(line)

        elif line.find("<text>") != -1:
            _instance.intext = True
            _instance.buff = cStringIO.StringIO()
            _instance.buff.write(line)
        elif line.find("</text>") != -1:
            _instance.intext = False
            _instance.buff.write(line)
            val = _instance.buff.getvalue()
            _instance.buff.close()
            _instance.buff = None

            # print _instance.process(val)
            _instance.current_article_text = val
            # parsed title and text, now give it to reducer
            _instance.process()
        else:
            if _instance.intext:
                _instance.buff.write(line)