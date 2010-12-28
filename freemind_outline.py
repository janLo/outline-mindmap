'''Converts a freemind xml .mm file to an outline file compatable with vim 
outliner.

Make sure that you check that round trip on your file works.

Author: Julian Ryde
'''
import sys
from xml.etree.ElementTree import XMLParser
import textwrap

class Outline:                     # The target object of the parser
    depth = -1
    indent = '\t'
    current_tag = None
    p_count = 0
    def start(self, tag, attrib):  # Called for each opening tag.
        self.depth += 1
        self.current_tag = tag
        # print the indented heading
        if tag == 'node' and self.depth > 1:
            #if 'tab' in attrib['TEXT']:
                #import pdb; pdb.set_trace()
            print (self.depth-2)*self.indent + attrib['TEXT'].encode('utf-8')
    def end(self, tag):            # Called for each closing tag.
        self.depth -= 1
        if self.current_tag != 'p':
            self.p_count=0
        self.current_tag = None
    def data(self, data):
        if self.current_tag == 'p':
            bodyline = data.rstrip('\r\n')
            bodyindent = (self.depth-5)*self.indent + ": "
            textlines = textwrap.wrap(bodyline, width=74 - len(bodyindent), break_on_hyphens=False)
            if self.p_count > 0:
                print bodyindent + ""
            for line in textlines: 
                print bodyindent + line.strip().encode('utf-8')
            self.p_count = self.p_count + 1

    def close(self):    # Called when all data has been parsed.
        pass

outline = Outline()
parser = XMLParser(target=outline)

fname = sys.argv[1]
filelines = open(fname).readlines()
parser.feed(''.join(filelines))
parser.close()
