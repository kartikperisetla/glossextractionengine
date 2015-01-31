__author__ = 'kartik'

from lxml import etree
import sys,re
import bz2
import unicodedata

# class that parses wikipedia XML dump in .bz2 format and converts it into a file with one line per article with its title and article text separated by tab:
# <article_title1>\t<article_text1_with_no_newlines>
# <article_title2>\t<article_text2_with_no_newlines>
# <article_title3>\t<article_text3_with_no_newlines>
# ...and so on.

class Parser:
    def __init__(self):
        self.TAG = set(
            ['{http://www.mediawiki.org/xml/export-0.9/}text', '{http://www.mediawiki.org/xml/export-0.9/}title'])
        self.curr_title = None
        self.curr_text = None


    def fast_iter(self, context, func, *args, **kwargs):
        for event, elem in context:
            if event == 'end' and elem.tag in self.TAG:
                # print "found.. about to call process_element..."
                func(elem, *args, **kwargs)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context


    def process_element(self, elem, fout):
        if elem.tag == '{http://www.mediawiki.org/xml/export-0.9/}title':
            self.curr_title = unicodedata.normalize('NFKD', unicode(elem.text)).encode('ASCII', 'ignore')
            # print "got title:", self.curr_title

        if elem.tag == '{http://www.mediawiki.org/xml/export-0.9/}text':
            self.curr_text = unicodedata.normalize('NFKD', unicode(elem.text)).encode('ASCII', 'ignore')
            self.save()


    def save(self):
        if not self.curr_text is None and not self.curr_title is None:
            self.curr_text = re.sub(r'\n',' ',self.curr_text)
            self.curr_text = re.sub(r'\t',' ',self.curr_text)

            res = self.curr_title + "\t" + self.curr_text.replace('\n', ' ') + '\n'
            fout = open('new_file.txt', 'a')
            fout.write(res)
            fout.close()
        self.curr_title = None
        self.curr_text = None

def getfin():
    return  bz2.BZ2File(sys.argv[1], 'r')

def main():
    fin = getfin()
    fout = open('new_file.txt', 'w')
    fout.close()
    context = etree.iterparse(fin)
    p = Parser()
    p.fast_iter(context, p.process_element, fout)


if __name__ == "__main__":
    main()